import logging
import os
import platform
import shutil
import uuid
from pathlib import Path
from typing import List

from blazetest.core.config import (
    BUILD_FOLDER_PATH,
    PWD,
    EXECUTABLE_FILES,
    CWD,
    SUPPORTED_PYTHON_VERSIONS,
)
from blazetest.core.utils.exceptions import PythonVersionNotSupported

logger = logging.getLogger(__name__)


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_python_version() -> str:
    """
    Gets current Python version

    Returns:
        string in the format of:
            '3.8'
            '3.7'
    Raises:
        If the version is not supported, raises PythonVersionNotSupported
    """
    python_version = ".".join(list(platform.python_version_tuple()[:2]))

    if python_version not in SUPPORTED_PYTHON_VERSIONS:
        raise PythonVersionNotSupported(
            f"Supported versions are: {', '.join(SUPPORTED_PYTHON_VERSIONS)}, "
            f"installed version: {python_version}"
        )

    return python_version


def remove_junit_report_path(pytest_args: List[str]) -> List[str]:
    """Remove the `--junitxml` argument from a list of pytest arguments.

    Args:
        pytest_args: List of pytest arguments.

    Returns:
        List of pytest arguments with the `--junitxml` argument removed.
    """
    return [arg for arg in pytest_args if not arg.startswith("--junitxml")]


def set_environment_variables(
    aws_access_key_id: str = None,
    aws_secret_access_key: str = None,
    aws_region: str = None,
    s3_bucket: str = None,
    ecr_repository_name: str = None,
    tags: str = None,
):
    """Set AWS credentials as environment variables.

    Args:
        aws_access_key_id: AWS access key ID.
        aws_secret_access_key: AWS secret access key.
        aws_region: AWS region.
        s3_bucket: S3 bucket name.
        ecr_repository_name: ECR repository name.
        tags: AWS Lambda tags.
    """
    if aws_access_key_id:
        os.environ["AWS_ACCESS_KEY_ID"] = aws_access_key_id

    if aws_secret_access_key:
        os.environ["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key

    if aws_region:
        os.environ["AWS_DEFAULT_REGION"] = aws_region

    if s3_bucket:
        os.environ["S3_BUCKET"] = s3_bucket

    if ecr_repository_name:
        os.environ["ECR_REPOSITORY_NAME"] = ecr_repository_name

    if tags:
        os.environ["LAMBDA_TAGS"] = tags

    os.environ["PROJECT_CWD"] = CWD
    os.environ["PULUMI_CONFIG_PASSPHRASE"] = "pass"


def insert_python_version(dockerfile_path, python_version):
    """
    Inserts an indicated Python version to the Dockerfile variable PYTHON_VERSION

    :param dockerfile_path: Path to the Dockerfile
    :param python_version: Python version in the format '3.8'
    """
    with open(dockerfile_path, "r") as f:
        lines = f.read()

    lines = lines.replace("PYTHON_VERSION", python_version)
    with open(dockerfile_path, "w") as f:
        f.write(lines)


def get_s3_bucket_path(s3_bucket: str, timestamp: str) -> str:
    return f"s3://{s3_bucket}/{timestamp}/target/junitxml/"


# TODO: optimize function to be more readable and more efficient
def create_build_folder() -> None:
    """Create a build folder and copy necessary files to it.

    The `__main__.py` file in the `deployment/aws` directory will also be copied
    to the build folder.
    """
    # Create build folder and necessary subdirectories
    Path(BUILD_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(BUILD_FOLDER_PATH, "scripts")).mkdir(
        parents=True,
        exist_ok=True,
    )
    # Path(os.path.join(BUILD_FOLDER_PATH, "scripts")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(BUILD_FOLDER_PATH, "tests_runner_handler")).mkdir(
        parents=True,
        exist_ok=True,
    )

    # Create list of source-destination file pairs for the files in EXECUTABLE_FILES
    src_dst_pairs = [
        (os.path.join(PWD, file), os.path.join(BUILD_FOLDER_PATH, file))
        for file in EXECUTABLE_FILES
    ]

    # Copy the files
    for src, dst in src_dst_pairs:
        shutil.copyfile(src=src, dst=dst)

    deployment_files = ["__main__.py", ".envignore", "requirements.txt"]
    for deployment_file in deployment_files:
        shutil.copyfile(
            src=os.path.join(PWD, f"deployment/aws/{deployment_file}"),
            dst=os.path.join(BUILD_FOLDER_PATH, deployment_file),
        )

    # Insert current Python version to the Dockerfile
    insert_python_version(
        dockerfile_path=os.path.join(BUILD_FOLDER_PATH, "Dockerfile"),
        python_version=get_python_version(),
    )

    logger.info(
        "Successfully created build folder",
    )
