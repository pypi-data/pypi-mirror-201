import re
import traceback
import functools
from itertools import count
from datetime import datetime
from time import perf_counter_ns
from inspect import iscoroutinefunction
from .bug import BugException
from ..utils.colors import colors
from .exception import BugCreationException
from ..logger.exception import LoggerException
from ..utils.logger import test_rest_api_logger
from ..global_variables.exception import GlobalVariablesException
from ..reporting.report import report, ReportTestResult, TestStatus, ErrorType
from ..rest_api.exception import RestApiCreationException, RestApiSendException

# Iter for creating id for testcase name
iter_test_name = count(start=1)


def test(*, name="", desc="", enabled=True, tags=[], is_async=True, execution_order='zzzzz'):
    def testcase_decorator(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            # Get the test file path
            testsuite: str = func.__module__ if func.__module__ else 'root file'
            # Create the test name
            testcase_name: str = f'{name} ({testsuite})' if name else f'{func.__name__} ({testsuite})'
            # Add unique id to the name (Users can provide same name for multiple testcases)
            testcase_name += f" [{next(iter_test_name)}]"
            # Start the stopwatch / counter
            timer_start = perf_counter_ns()
            # Get the start date time of the test
            start = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            # Initialise test status and test details
            test_status, test_details = TestStatus.SKIP, 'Testcase is skipped'
            # Initialise bug priority and error type which will be used for reporting
            bug_priority, error_type = '', ''
            # Initialise skip as false
            skip = False
            # Get the runner test tags
            from test_rest_api import runner
            # If we have any runner test tags
            if runner.test_tags:
                # Check if the tag is #ALL (This will run for all tag cases, eg: login api)
                if 'ALL' not in tags:
                    # Check if any of the runner test tag is present in the current test else skip the test
                    if not any(test_tag in tags for test_tag in runner.test_tags):
                        skip = True
            if not skip:
                # Initialise test status and test details
                test_status, test_details = TestStatus.DISABLE, 'Testcase is disabled'
                # Only execute enabled testcases
                if enabled:
                    try:
                        # Call the async test function
                        result = await func(*args, **kwargs)
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.LIGHT_GREEN}{'PASS' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the test status and details
                        test_status, test_details = TestStatus.PASS, f'Success !\n\n{str(result) if result else ""}'
                    except RestApiCreationException as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.REST_API
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        end_res = re.search(r'raise RestApiCreationException', traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:end_res.end()]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        if re.search(r'test_rest_api/rest_api/rest_api.py", line (.*?), in __call__', traceback_data):
                            traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                            traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
                    except RestApiSendException as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.REST_API
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        end_res = re.search(r'raise RestApiSendException', traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:end_res.end()]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
                    except BugCreationException as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.BUG
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        end_res = re.search(r'raise BugCreationException', traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:end_res.end()]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        if re.search(r'test_rest_api/testing/bug.py", line (.*?), in __call__', traceback_data):
                            traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                            traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
                    except GlobalVariablesException as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.GLOBAL_VARIABLES
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        end_res = re.search(r'raise test_rest_api_exception', traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:end_res.end()]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
                    except LoggerException as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.LOGGER
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        end_res = re.search(r'raise test_rest_api_exception', traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:end_res.end()]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
                    except BugException as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.LIGHT_RED}{'FAIL' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the bug priority for reporting
                        bug_priority = exc.priority
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        end_res = re.search(r'raise BugException', traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:end_res.end()]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        traceback_data = traceback_data[:traceback_data.rfind('File "') - 3]
                        # Update the test status and details
                        test_status, test_details = TestStatus.FAIL, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
                    except AttributeError as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.UNEXPECTED
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}\n\n{"Tip: This may be due to not using await keyword in function calls"}'
                    except Exception as exc:
                        # Log the result
                        test_rest_api_logger.info(
                            f"{colors.YELLOW}{'ERROR' : <8}{colors.LIGHT_CYAN}{testcase_name}{colors.LIGHT_BLUE}")
                        # Update the error type for reporting
                        error_type = ErrorType.UNEXPECTED
                        # Get the code traceback details
                        traceback_data = traceback.format_exc()
                        # Format the traceback (Remove unwanted info)
                        start_res = re.search(r'test_rest_api/testing/decorator.py", line (.*?), in inner',
                                              traceback_data)
                        traceback_data = traceback_data[start_res.start() + 98:]
                        # Update the test status and details
                        test_status, test_details = TestStatus.ERROR, f'\nTRACEBACKS\n----------\n{traceback_data}\n{exc}'
            # Set the end time of the test
            end = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            # Stop the stopwatch / counter
            timer_stop = perf_counter_ns()
            # Calculate the time duration of the test in seconds (note: duration is in nanoseconds)
            duration = f'{(timer_stop - timer_start) / 1000000000} seconds'
            # Create Report test result object instance
            test_result = ReportTestResult(name=testcase_name,
                                           desc=desc,
                                           is_async=is_async,
                                           testsuite=testsuite,
                                           status=test_status,
                                           details=test_details,
                                           tags=tags,
                                           start=start,
                                           end=end,
                                           duration=duration,
                                           bug_priority=bug_priority,
                                           error_type=error_type)
            # Add the test result to the report
            report.add_test_result(test_result)

        # Only async functions can be decorated with @test
        inner.is_testcase = True if iscoroutinefunction(func) else False
        inner.is_async_testcase = is_async
        # For ordering sequential testcases
        inner.execution_order = execution_order
        return inner

    return testcase_decorator
