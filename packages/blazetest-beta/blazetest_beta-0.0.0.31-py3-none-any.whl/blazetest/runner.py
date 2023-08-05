import logging
import time
from typing import Optional

import click

from blazetest import __version__
from blazetest.core.infra.infra_setup import InfraSetup
from blazetest.core.license.manager import LicenseManager
from blazetest.core.project_config.project_config import ProjectConfiguration
from blazetest.core.run_test.runner_facade import TestRunner
from blazetest.core.run_test.result_model import TestSessionResult
from blazetest.core.utils.logging_config import setup_logging
from blazetest.core.utils.utils import (
    create_build_folder,
    generate_uuid,
    set_environment_variables,
)

logger = logging.getLogger(__name__)


@click.option(
    "--config-path",
    help="Configuration path to the TOML file for the CLI. "
    "If not specified -> searches the project's root folder for the file blazetest.toml. "
    "If not found -> raises an error.",
)
@click.option(
    "--aws-access-key-id",
    help="AWS Access Key ID which is used to deploy artifacts.",
)
@click.option(
    "--aws-secret-access-key",
    help="AWS Secret Access Key which is used to deploy artifacts.",
)
@click.option(
    "--license-key",
    help="License key for Blazetest CLI. Either --license-key or --license-file should be specified."
    "License key has a higher priority if both are specified.",
)
@click.option(
    "--license-file",
    help="License file for Blazetest CLI. Either --license-key or --license-file should be specified."
    "License file has a lower priority if both are specified.",
)
@click.option(
    "--tags",
    help="Tags specified for the AWS Lambda function. The tags will be attached to created Lambda function instance.",
)
@click.option(
    "--logs",
    default="enabled",
    type=click.Choice(["enabled", "disabled"]),
    help="Default is enabled. When logs are enabled, they are shown in the console stdout. "
    "When they are set to disabled, the logs are not shown during CLI execution, but saved to blazetest.log, "
    "which will be located in the project's root.",
)
@click.option(
    "--loki",
    help="Loki API Key. If provided, logs are sent to the Loki",
)
@click.option(
    "--invoke-only",
    is_flag=True,
    help="If specified, it searches for the Lambda with the specified stack name and invokes it. "
    "If not found, raises an exception.",
)
@click.option("--debug", is_flag=True, help="Enables debugging output.")
@click.option("--info", is_flag=True, help="Prints Blazetest CLI version.")
@click.pass_context
def run_tests(
    config_path: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    license_key: str,
    license_file: str,
    tags: str,
    logs: str,
    loki: str,
    invoke_only: bool,
    debug: bool,
    info: bool,
):
    """
    Runs tests using the pytest library and parallel Lambda functions.
    It deploys the necessary AWS resources (ECR, Lambda, and S3 bucket) using Pulumi.
    It also accepts any additional arguments passed to the command, which will be passed to pytest as arguments.

    Args:
        config_path (str): Path to the TOML configuration file.
        aws_access_key_id (str): AWS access key id.
        aws_secret_access_key (str): AWS secret access key.
        license_key (str): License key.
        license_file (str): Path to the license file.
        tags (str): Tags in the format key1=value,key2=value. Will be attached to created Lambda function instance.
        logs (str): Defaults to enabled, possible values: enabled, disabled.
        loki (str): Loki API Key. If provided, logs are sent to the Loki
        invoke_only (bool): If true, invokes the function with provided stack name without deploying
        debug (bool): flag that enables debugging output if true
        info (bool): prints Blazetest CLI version
    """
    s = time.time()
    session_uuid = generate_uuid()
    setup_logging(
        debug=debug,
        stdout_enabled=logs != "disabled",
        loki_api_key=loki,
        session_uuid=session_uuid,
    )

    logger.info(f"Blazetest version: {__version__}")

    # TODO: is there a better way to print only the package version
    if info:
        return

    # Get project configuration from Blazetest TOML
    config = ProjectConfiguration.from_toml(config_path)

    licence_manager = LicenseManager(
        license_key=license_key,
        license_file=license_file,
        config_license_key=config.license_key,
        config_license_file=config.license_file,
    )

    expiration_date = licence_manager.check_license()
    logger.info(f"License expiration date: {expiration_date}")
    logger.info(f"Config initialized: {config}")

    if licence_manager.flaky_test_retry_enabled():
        logger.info("Flaky test retry feature is on")
    else:
        if config.failed_test_retry > 0:
            logger.warning(
                "Flaky test retry feature is not available within this license"
            )

    set_environment_variables(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_region=config.aws_region,
        s3_bucket=config.deploy.s3_bucket,
        ecr_repository_name=config.build.ecr_repository_name,
        tags=tags if tags else None,
    )

    logger.info(f"Blazetest initialization took {time.time() - s}")

    s = time.time()
    if not invoke_only:
        # Creating build folder for blazetest files
        create_build_folder()

        # Using Pulumi to do the deployment, create ECR, Lambda and S3 bucket
        infra_setup = InfraSetup(
            aws_region=config.aws_region,
            stack_name=config.deploy.stack_name,
            setup_tool="pulumi",
        )

        infra_setup.deploy()

    logger.info(f"Deployment took {time.time() - s}")

    logger.info("Waiting 10s before invoking tests...")
    time.sleep(10)

    s = time.time()
    # Running tests on the Lambda
    test_runner = TestRunner(config=config)

    flaky_test_retry_enabled = (
        config.failed_test_retry > 0 and licence_manager.flaky_test_retry_enabled()
    )

    test_session_result: Optional[TestSessionResult] = test_runner.run_tests(
        flaky_test_retry_enabled=flaky_test_retry_enabled,
    )

    if test_session_result is not None:
        test_session_result.log_results(
            failed_test_retry_enabled=flaky_test_retry_enabled
        )

    logger.info(f"Running tests and giving results took {time.time() - s}")
