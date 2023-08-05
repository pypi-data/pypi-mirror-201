from datetime import datetime
from .exception import LoggerException
from ..utils.exception import catch_exc


class Logger:
    """
    Class for creating logger objects
    """

    @catch_exc(test_rest_api_exception=LoggerException)
    def __init__(self):
        self._logs = ''

    @catch_exc(test_rest_api_exception=LoggerException)
    def log(self, message):
        """
        Add log messages to your logger instance
        """
        # Validate the message type
        if not isinstance(message, str):
            raise Exception('Invalid data type for message. Please provide a valid string')
        # Update the message tp Logger._logs instance variable with current time stamp
        self._logs += f'{datetime.now().strftime("%H:%M:%S") : <8}: {message}\n'

    def __str__(self):
        return f'LOGS\n----\n{self._logs}\n'
