from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import logging
import time
from typing import List, Optional

from blazetest.core.config import MAX_LAMBDA_WORKERS
from blazetest.core.project_config.project_config import BlazetestConfig
from blazetest.core.lambda_.invocation import Invocation
from blazetest.core.run_test.pytest_collect import collect_tests
from blazetest.core.run_test.result_model import TestSessionResult
from blazetest.core.utils.utils import remove_junit_report_path

logger = logging.getLogger(__name__)


class TestRunner:
    """
    Class for running tests using Lambda functions.
    This class is responsible for collecting the test items,
    creating the report paths, and invoking the Lambda functions.

    Attributes:
        config (BlazetestConfig): Configuration for running the tests on AWS Lambda.
        lambda_function (Lambda):  Object responsible for interacting with AWS Lambda.

    Methods:
        run_tests(): Collects the test items, creates the report paths,
            and invokes the Lambda functions.
    """

    FOLDER_NAME_TIMESTAMP = "%Y-%m-%d_%H-%M-%S"
    TMP_REPORT_FOLDER = "/tmp/junitxml/{}.xml"
    REPLACE_SYMBOLS = ["::", ".", "/"]
    REPLACE_TO = "-"

    # Lambda function name, which will be invoked to run tests
    function_name: str = None

    # S3 bucket name, where the reports should be saved
    s3_bucket: str = None

    def __init__(self, config: BlazetestConfig):
        """
        Initializes the class with the given config and creates a new Lambda Invocation object.

        :param config: Configuration for running the tests on AWS Lambda.
        """
        self.config = config

        logger.info(
            f"Pytest collection args initialised: {config.pytest.collection_args}"
        )
        logger.info(f"Pytest execution args initiated: {config.pytest.execution_args}")

        self.lambda_function = Invocation(
            region=self.config.aws_region,
            stack_name=config.deploy.stack_name,
        )
        self.timestamp = self.__get_timestamp_now()

    def run_tests(
        self, flaky_test_retry_enabled: bool = True
    ) -> Optional[TestSessionResult]:
        """
        Collects the test items, creates the report paths,
        and invokes the Lambda functions in parallel.
        """
        node_ids = collect_tests(pytest_args=self.config.pytest.collection_args)

        logger.info(f"Collected tests: {len(node_ids)}")

        if len(node_ids) == 0:
            logger.error("Exiting as there are no tests to run")
            return None

        function_details = self.lambda_function.get_created_lambda_function_details()
        self.function_name = function_details["function_name"]
        self.s3_bucket = function_details["s3_bucket"]
        logger.info(
            f"Lambda function: {self.function_name}, " f"S3 bucket: {self.s3_bucket}",
        )

        logger.info("Invoking tests and running in parallel.. It might take some time")
        tests_results = self.__run_in_parallel(node_ids=node_ids)

        failed_tests = tests_results["failed"]
        failed_tests_on_retry = 0

        if flaky_test_retry_enabled and failed_tests:
            logger.info(
                f"Retrying running {len(failed_tests)} failed tests {self.config.failed_test_retry} times"
            )
            retry_test_results = self.__run_in_parallel(
                node_ids=failed_tests * self.config.failed_test_retry
            )
            failed_tests_on_retry = len(retry_test_results["failed"])

        return TestSessionResult(
            lambda_function_name=self.function_name,
            tests_count=len(node_ids),
            tests_passed=tests_results["passed"],
            duration=tests_results["duration"],
            s3_bucket=self.s3_bucket,
            timestamp=self.timestamp,
            failed_tests_count=len(failed_tests),
            failed_tests_after_retry=failed_tests_on_retry,
        )

    def invoke_lambda(self, node_id: str):
        logger.debug(f"Invoking Lambda with node_id: {node_id}")

        report_path = self.__get_pytest_xml_report_path(node_id=node_id)
        pytest_args = remove_junit_report_path(self.config.pytest.execution_args)

        invocation_result = self.lambda_function.invoke(
            function_name=self.function_name,
            node_id=node_id,
            pytest_args=pytest_args,
            report_path=report_path,
            timestamp=self.timestamp,
        )
        return node_id, invocation_result

    def __run_in_parallel(self, node_ids: List[str]):
        start_time = time.time()

        # TODO: is 1000 appropriate value for workers for threads?
        with ThreadPoolExecutor(max_workers=MAX_LAMBDA_WORKERS) as executor:
            results = list(executor.map(self.invoke_lambda, node_ids))
            tests_passed = sum(result[1] for result in results)
            failed_tests = [result[0] for result in results if result[1] is False]

        return {
            "passed": tests_passed,
            "failed": list(set(failed_tests)),
            "duration": time.time() - start_time,
        }

    def __get_timestamp_now(self):
        return datetime.now().strftime(self.FOLDER_NAME_TIMESTAMP)

    def __get_pytest_xml_report_path(self, node_id: str) -> str:
        for symbol in self.REPLACE_SYMBOLS:
            node_id = node_id.replace(symbol, self.REPLACE_TO)

        return self.TMP_REPORT_FOLDER.format(node_id)

    # TODO: separate arguments of pytest to: collection and execution
    def __process_pytest_arguments(self):
        pass
