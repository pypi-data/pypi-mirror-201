from ..utils.exception import TestRestApiException


class LoggerException(TestRestApiException):
    """
    Exception raised while creating logger object using Logger class
    """

    def __init__(self, *, msg: str):
        self.exc = msg
        self.error_msg = """
Logger creation failed

Example Code
------------
(Example 1)

from test_rest_api import Logger

my_logger = Logger()

my_logger.log("log message 001")
my_logger.log("log message 002")
my_logger.log("log message n")

my_logger_messages = str(my_logger)

(Example 2)

from test_rest_api import Logger

my_logger = Logger()

my_logger.log(message = "log message 001")
my_logger.log(message = "log message 002")
my_logger.log(message = "log message n")

my_logger_messages = str(my_logger)

Note: Both the above 2 examples does the same functionality but with different syntax

It is recommended to return logger object for all you testcase functions, for rich html test reports

(Example 3)

from test_rest_api import test, Logger

@test()
def my_test():
    my_logger = Logger()
    my_logger.log(message = "log message 001")
    return my_logger
"""
        self.message = self.format(exc=self.exc, error_msg=self.error_msg)
        super().__init__(self.message)
