from test_rest_api.utils.decorator_hints import decorated_func_param_hints


class TestRestApiException(Exception):
    """
    Base Exception class
    """

    def format(self, exc, error_msg):
        """
        Format of reporting
        """
        _no_data_to_display = 'No data to display'
        return f"""
EXCEPTION
---------
{exc.strip() if exc.strip() else _no_data_to_display}

ERROR MESSAGE
-------------
{error_msg.strip() if error_msg.strip() else _no_data_to_display}
"""


@decorated_func_param_hints
def catch_exc(test_rest_api_exception: TestRestApiException):
    """
    Decorator used for catching python code exceptions for functions
    Example: Function calls with empty params, invalid params etc

    Developers can raise python Exceptions inside function body which will be auto converted to TestRestApiExceptions
    """

    def catch_exc_dec(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                raise test_rest_api_exception(msg=str(exc))

        return inner

    return catch_exc_dec
