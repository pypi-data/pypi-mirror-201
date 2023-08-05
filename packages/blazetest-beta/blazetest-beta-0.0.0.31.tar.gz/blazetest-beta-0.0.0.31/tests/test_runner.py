from unittest.mock import patch, Mock

from click.testing import CliRunner

from blazetest.core.project_config.project_config import ProjectConfiguration
from blazetest.runner import run_tests


@patch("blazetest.runner.TestRunner")
@patch("blazetest.runner.LicenseManager")
@patch("blazetest.runner.InfraSetup")
@patch("blazetest.runner.set_environment_variables")
@patch("blazetest.runner.setup_logging")
@patch("blazetest.runner.create_build_folder")
@patch("uuid.uuid4")
def test_tests_runner(
    uuid_mock,
    build_folder_mock,
    logging_mock,
    set_env_vars_mock,
    deploy_mock,
    check_license_mock,
    tests_runner_facade,
):
    uuid_mock.return_value = "UNIQUE UUID"
    build_folder_mock.return_value = None
    logging_mock.return_value = None
    deploy_mock.deploy = Mock(return_value=None)
    check_license_mock.check_license = Mock(return_value="21 Jun 2028")
    check_license_mock.flaky_test_retry_enabled = Mock(side_effect=[False, True, True])
    tests_runner_facade.run_tests = Mock(return_value=None)
    set_env_vars_mock.return_value = None

    runner = CliRunner()

    result = runner.invoke(
        run_tests,
        [
            "-v",
            "--config-path=tests/core/test_config/config1.yaml",
            "--license-key",
            "test-key",
        ],
    )

    config = ProjectConfiguration.from_yaml("tests/core/test_config/config1.yaml")
    assert result.exit_code == 0
    print(result.output)

    logging_mock.assert_called_with(
        debug=False,
        stdout_enabled=True,
        loki_api_key=None,
        session_uuid="UNIQUE UUID",
    )

    tests_runner_facade.assert_called_with(
        pytest_args=["-v"],
        config=config,
    )

    set_env_vars_mock.assert_called_with(
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_region="test-region",
        s3_bucket="test-bucket",
        ecr_repository_name="test-repository",
        tags=None,
    )

    tests_runner_facade.run_tests.assert_called_with(
        flaky_test_retry_enabled=False,
    )

    result = runner.invoke(
        run_tests,
        [
            "-v",
            "--config-path=tests/core/test_config/config2.yaml",
            "--license-key=test-key",
            "--tags",
            "service=blazetest,region=test-region",
        ],
    )

    assert result.exit_code == 0
    config = ProjectConfiguration.from_yaml("tests/core/test_config/config2.yaml")

    tests_runner_facade.assert_called_with(
        pytest_args=["-v"],
        config=config,
    )

    set_env_vars_mock.assert_called_with(
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_region="test-region",
        s3_bucket="test-bucket",
        ecr_repository_name="test-repository",
        tags="service=blazetest,region=test-region",
    )

    deploy_mock.deploy.assert_called_once()

    tests_runner_facade.run_tests.assert_called_with(
        flaky_test_retry_enabled=False,
    )
