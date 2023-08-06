import os
from typing import List
from datetime import datetime
from jinja2 import Environment
from dataclasses import dataclass, asdict
from .html import html_str
from ..testing.bug import BugPriority


@dataclass
class TestStatus:
    PASS: str = 'pass'
    FAIL: str = 'fail'
    ERROR: str = 'error'
    DISABLE: str = 'disable'
    SKIP: str = 'skip'


@dataclass
class ErrorType:
    REST_API: str = 'rest_api'
    GLOBAL_VARIABLES: str = 'global_variables'
    BUG: str = 'bug'
    LOGGER: str = 'logger'
    UNEXPECTED: str = 'unexpected'


@dataclass
class ReportTestResult:
    name: str
    desc: str
    is_async: bool
    testsuite: str
    status: str
    details: str
    tags: tuple
    start: str
    end: str
    duration: str
    bug_priority: str
    error_type: str


@dataclass
class ReportTestSummaryTest:
    start: str = ''
    end: str = ''
    duration: str = ''
    tags: tuple = ()
    status: bool = True
    total: int = 0


@dataclass
class ReportTestSummaryTests:
    total: int = 0
    sync_tests: int = 0
    async_tests: int = 0
    success: int = 0
    fail: int = 0
    error: int = 0
    disable: int = 0
    skip: int = 0


@dataclass
class ReportTestSummaryBugs:
    total: int = 0
    low: int = 0
    minor: int = 0
    major: int = 0
    critical: int = 0
    blocker: int = 0


@dataclass
class ReportTestSummaryErrors:
    total: int = 0
    rest_api: int = 0
    global_variables: int = 0
    bug: int = 0
    logger: int = 0
    unexpected: int = 0


@dataclass
class ReportTestSummary:
    test: ReportTestSummaryTest = ReportTestSummaryTest()
    tests: ReportTestSummaryTests = ReportTestSummaryTests()
    bugs: ReportTestSummaryBugs = ReportTestSummaryBugs()
    errors: ReportTestSummaryErrors = ReportTestSummaryErrors()


class Report:
    def __init__(self):
        self.sync_tests: List[ReportTestResult] = []
        self.async_tests: List[ReportTestResult] = []
        self.summary: ReportTestSummary = ReportTestSummary()
        self.template = self.create_jija2_template()

    def add_test_result(self, test_result: ReportTestResult):
        """
        Add test result details for a single test
        """
        # Add the test result to tests instance variable only if it's not disabled or skipped
        if test_result.status != TestStatus.DISABLE and test_result.status != TestStatus.SKIP:
            # Update the total run count
            self.summary.test.total += 1
            if test_result.is_async:
                self.async_tests.append(test_result)
            else:
                self.sync_tests.append(test_result)
        # Update the total tests count
        self.summary.tests.total += 1
        # Update the sync and async tests count
        if test_result.is_async:
            self.summary.tests.async_tests += 1
        else:
            self.summary.tests.sync_tests += 1
        # Update the overall test summary status if failed (It was initialized as True)
        if test_result.status == TestStatus.FAIL or test_result.status == TestStatus.ERROR:
            self.summary.test.status = False
        # Update the total test status count
        if test_result.status in asdict(TestStatus()).values():
            # pass is converted to success, because 'pass' is a python keyword & hence we can't create dataclass
            # This change is done for handling ReportTestSummaryTests dataclass which uses "success" instead of "pass"
            report_test_summary_tests_status = 'success' if test_result.status == TestStatus.PASS else test_result.status
            setattr(self.summary.tests, report_test_summary_tests_status,
                    getattr(self.summary.tests, report_test_summary_tests_status) + 1)
        # Update the total bug and bug priority count
        if test_result.status == TestStatus.FAIL and test_result.bug_priority in asdict(BugPriority()).values():
            self.summary.bugs.total += 1
            setattr(self.summary.bugs, test_result.bug_priority,
                    getattr(self.summary.bugs, test_result.bug_priority) + 1)
        # Update the total error and error type count
        if test_result.status == TestStatus.ERROR and test_result.error_type in asdict(ErrorType()).values():
            self.summary.errors.total += 1
            setattr(self.summary.errors, test_result.error_type,
                    getattr(self.summary.errors, test_result.error_type) + 1)

    def save(self, *, path):
        """
        Save the test report to the disk
        """
        # Render the jinja report template html file
        rendered_html = self.template.render(summary=self.summary,
                                             sync_tests=self.sync_tests,
                                             async_tests=self.async_tests)
        # Create html report file name using current datetime details
        file_name = f"Result {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.html"
        # Save to html file
        with open(os.path.join(path, file_name), 'w') as f:
            f.write(rendered_html)

    @staticmethod
    def create_jija2_template():
        """
        Jinja2 initialisation
        """
        # Create Jinja environment
        environment = Environment()
        # Create Jinja template
        template = environment.from_string(html_str)
        # Return the template object
        return template


report = Report()
