import logging
from typing import Dict

import toml
import yaml
from dacite import from_dict, MissingValueError

from blazetest.core.config import PROJECT_CONFIG_TOML, PROJECT_CONFIG_YAML
from blazetest.core.project_config.model import BlazetestConfig
from blazetest.core.utils.exceptions import (
    LambdaConfigurationFileNotFound,
    LambdaConfigurationMissingValue,
)

logger = logging.getLogger(__name__)


class ProjectConfiguration:
    def validate(self):
        # TODO: validations of the config parameters from TOML file
        pass

    @classmethod
    def from_yaml(cls, yaml_file_path: str = None) -> BlazetestConfig:
        """
        DEPRECATED: It has been decided to use TOML file

        Load configuration data from a YAML file and create a `LambdaConfig` object.
        Args:
            yaml_file_path: Path to the YAML file. If not specified, the default
                location specified by `LAMBDA_CONFIG_YAML` will be used.
        Returns:
            A `LambdaConfig` object created from the data in the YAML file.
        Raises:
            LambdaConfigurationFileNotFound: If the specified YAML file does not exist.
            LambdaConfigurationMissingValue: If required values are missing from the YAML file.
        """
        if not yaml_file_path:
            logger.info(
                f"Config file location not specified. Using default location: {PROJECT_CONFIG_YAML}",
            )
            yaml_file_path = PROJECT_CONFIG_YAML

        try:
            with open(yaml_file_path) as f:
                data = yaml.safe_load(f)
                return cls._get_dataclass_from_dict(data=data)
        except FileNotFoundError as err:
            raise LambdaConfigurationFileNotFound(
                f"Configuration file does not exist: {err}"
            )

    @classmethod
    def from_toml(cls, toml_file_path: str = None) -> BlazetestConfig:
        """Load configuration data from a TOML file and create a `LambdaConfig` object.

        Args:
            toml_file_path: Path to the TOML file. If not specified, the default
                location specified by `LAMBDA_CONFIG_TOML` will be used.

        Returns:
            A `LambdaConfig` object created from the data in the TOML file.

        Raises:
            LambdaConfigurationFileNotFound: If the specified TOML file does not exist.
            LambdaConfigurationMissingValue: If required values are missing from the TOML file.
        """
        if not toml_file_path:
            logger.info(
                f"Config file location not specified. Using default location: {PROJECT_CONFIG_TOML}",
            )
            toml_file_path = PROJECT_CONFIG_TOML

        try:
            with open(toml_file_path) as f:
                data = toml.loads(f.read())
                return cls._get_dataclass_from_dict(data=data)
        except FileNotFoundError as err:
            raise LambdaConfigurationFileNotFound(
                f"Configuration file does not exist: {err}"
            )

    @staticmethod
    def _get_dataclass_from_dict(data: Dict):
        """Create a `LambdaConfig` object from a dictionary.

        Args:
            data: Dictionary containing configuration data.

        Returns:
            A `LambdaConfig` object created from the data in the dictionary.

        Raises:
            LambdaConfigurationMissingValue: If required values are missing from the dictionary.
        """
        try:
            return from_dict(data_class=BlazetestConfig, data=data)
        except MissingValueError as err:
            raise LambdaConfigurationMissingValue(f"Lambda configuration: {err}")
