import json
import os
from typing import List, Dict

import pytest

import logging

# TODO: consider moving all initialization logic outside of the functions -> optimize Lambda INVOKE, move to INIT
PWD = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        format="%(process)d-%(levelname)s-%(message)s", level=logging.INFO
    )


class S3Upload:
    def __init__(self, region):
        import boto3

        self.client = boto3.client(
            "s3",
            region_name=region,
        )

    def upload_file_to_s3_bucket(
        self,
        filepath: str,
        timestamp: str,
        s3_bucket: str,
    ) -> str:
        filename = os.path.basename(filepath)
        dst_folder = os.path.join(timestamp, "target/junitxml")
        dst_filepath = os.path.join(dst_folder, filename)

        with open(filepath, "rb") as f:
            self.client.put_object(
                Body=f,
                Bucket=s3_bucket,
                Key=dst_filepath,
            )

        return dst_filepath


def execute_tests(args: List[str]):
    return pytest.main(args)


def run_tests(event, context=None) -> Dict:  # noqa
    setup_logging()

    pytest_args: List[str] = event["pytest_args"]
    node_id: str = event["node_id"]
    report_path: str = event["report_path"]
    region: str = event["region"]
    timestamp: str = event["timestamp"]

    s3_bucket = os.environ.get("S3_BUCKET")

    args = [node_id, f"--junitxml={report_path}"] + pytest_args

    exit_code = execute_tests(args=args)
    test_result = True if exit_code == 0 else False

    s3 = S3Upload(region=region)
    s3.upload_file_to_s3_bucket(
        filepath=report_path,
        s3_bucket=s3_bucket,
        timestamp=timestamp,
    )

    test_result = {
        "test_result": test_result,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(test_result),
    }
    logger.info(f"Response: {response}")
    return response
