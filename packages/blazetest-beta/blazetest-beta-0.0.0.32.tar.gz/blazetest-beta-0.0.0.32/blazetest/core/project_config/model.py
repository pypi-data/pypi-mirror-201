from dataclasses import dataclass, field
from typing import List


@dataclass
class PytestConfig:
    collection_args: List[str] = field(default_factory=lambda: [])
    execution_args: List[str] = field(default_factory=lambda: [])


@dataclass
class BuildConfig:
    ecr_repository_name: str


@dataclass
class DeployConfig:
    stack_name: str
    s3_bucket: str


@dataclass
class BlazetestConfig:
    aws_region: str
    build: BuildConfig
    deploy: DeployConfig
    pytest: PytestConfig
    license_key: str = field(default_factory=lambda: None)
    license_file: str = field(default_factory=lambda: None)
    failed_test_retry: int = field(default_factory=lambda: 0)
