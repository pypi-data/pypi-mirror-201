from abc import ABC, abstractmethod
import logging
import os
from typing import Dict

import yaml

from blazetest.core.config import BUILD_FOLDER_PATH
from blazetest.core.utils.command_executor import CommandExecutor

logger = logging.getLogger(__name__)


class InfraSetupTool(ABC):
    def __init__(self, aws_region: str, stack_name: str):
        self.aws_region = aws_region
        self.stack_name = stack_name

    @abstractmethod
    def deploy(self) -> None:
        pass


# TODO: Pulumi, is it possible to use it without subprocess and directly?
class PulumiInfraSetup(InfraSetupTool):
    """
    Pulumi infrastructure setup tool. Uses Pulumi (https://www.pulumi.com/docs/) to build and
    deploy artifacts to the cloud.
    """

    EXECUTABLE = "pulumi"
    LOGIN_COMMAND = "login"
    STACK_INIT_COMMAND = "stack"
    UP_COMMAND = "up"

    def __init__(self, aws_region: str, stack_name: str):
        super().__init__(aws_region=aws_region, stack_name=stack_name)

    def deploy(self) -> None:
        self.login()
        self.create_config_files()
        self.create_stack()

        logger.info(
            "Deploying..",
        )
        self.up()
        logger.info(
            "Deploying has finished.",
        )
        return None

    def up(self):
        return self.__execute(
            command=self.UP_COMMAND,
            arguments={
                "--cwd": ".blazetest/",
                "--stack": self.stack_name,
                "--non-interactive": None,
                "--yes": None,
                "--skip-preview": None,
            },
        )

    def create_stack(self):
        return self.__execute(
            command=self.STACK_INIT_COMMAND,
            arguments={
                "init": self.stack_name,
                "--non-interactive": None,
            },
            allowed_return_codes=[0, 255],
        )

    def login(self):
        return self.__execute(
            command=self.LOGIN_COMMAND,
            arguments={
                "--local": None,
            },
        )

    def __execute(
        self, command: str, arguments: Dict, allowed_return_codes=None
    ) -> int:
        if allowed_return_codes is None:
            allowed_return_codes = [0]

        command_executor = CommandExecutor(
            executable=self.EXECUTABLE,
            command=command,
            arguments=arguments,
        )
        command_result = command_executor.execute_command(
            allowed_return_codes=allowed_return_codes
        )
        return command_result

    # TODO: optimize the function, consider moving it somewhere else
    def create_config_files(self):
        pulumi_yaml = {
            "name": "blazetest-aws",
            "runtime": {
                "name": "python",
                "options": {
                    "virtualenv": os.environ.get("VIRTUAL_ENV"),
                },
            },
        }
        pulumi_dev_yaml = {
            "config": {
                "aws:region": self.aws_region,
            }
        }
        with open(os.path.join(BUILD_FOLDER_PATH, "Pulumi.yaml"), "w") as f:
            yaml.dump(pulumi_yaml, f, default_flow_style=False)

        with open(
            os.path.join(BUILD_FOLDER_PATH, f"Pulumi.{self.stack_name}.yaml"), "w"
        ) as f:
            yaml.dump(pulumi_dev_yaml, f, default_flow_style=False)
