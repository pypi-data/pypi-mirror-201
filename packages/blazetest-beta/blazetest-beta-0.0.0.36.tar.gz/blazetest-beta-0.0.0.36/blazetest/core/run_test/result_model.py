import logging
from dataclasses import dataclass

from blazetest.core.utils.utils import get_s3_bucket_path

logger = logging.getLogger(__name__)


@dataclass
class TestSessionResult:
    lambda_function_name: str
    s3_bucket: str

    tests_count: int
    tests_passed: int

    failed_tests_count: int
    failed_tests_after_retry: int

    duration: float
    timestamp: str

    def log_results(self, failed_test_retry_enabled: bool = False):
        s3_bucket_path = get_s3_bucket_path(
            s3_bucket=self.s3_bucket, timestamp=self.timestamp
        )
        logger.info(f"Reports have been saved to {s3_bucket_path}")
        logger.info(f"Time taken to execute {self.tests_count} tests: {self.duration}")
        logger.info(f"Passed tests: {self.tests_passed} out of {self.tests_count}")

        # If the configuration was set to retry the tests that have failed and license has this feature
        # failed_test_retry is by default 0
        if failed_test_retry_enabled:
            logger.info(
                f"{self.failed_tests_count} tests have been retried, "
                f"{self.failed_tests_after_retry} have failed after retrial"
            )
            logger.info(
                f"Summary: {self.tests_count - self.failed_tests_after_retry} have passed."
            )
