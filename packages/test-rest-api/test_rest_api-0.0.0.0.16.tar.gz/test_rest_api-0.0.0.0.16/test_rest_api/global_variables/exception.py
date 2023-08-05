from ..utils.exception import TestRestApiException


class GlobalVariablesException(TestRestApiException):
    """
    Exception raised for error in using GlobalVariables class
    """

    def __init__(self, *, msg: str):
        self.exc = msg
        self.error_msg = """
Global Variables Error

Example Code
------------
(Example 1)

from test_rest_api import GlobalVariables

GlobalVariables.set("variable_name", variable_value)

variable = GlobalVariables.get("variable_name")

(Example 2)

from test_rest_api import GlobalVariables

GlobalVariables.set(name= "variable_name", value= "variable_value", is_constant= False)

variable: str = GlobalVariables.get(name= "variable_name")

Note: Both the above 2 examples does the same functionality but with different syntax

Set is_constant = True, for constant values
is_constant is an optional attribute
Default is_constant: False

We can store value of any datatypes in global variables including dict, list, set, tuple, str, int etc
GlobalVariables.set(name= "my_list", value= [1, 2, 3])
"""
        self.message = self.format(exc=self.exc, error_msg=self.error_msg)
        super().__init__(self.message)
