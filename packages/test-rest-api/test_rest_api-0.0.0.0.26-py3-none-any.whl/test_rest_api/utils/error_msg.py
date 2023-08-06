from dataclasses import dataclass
from test_rest_api.utils.colors import colors


@dataclass(frozen=True)
class Docs:
    commands: str = f"""
--------
Commands
--------
-> Run Test Suite
Syntax : {colors.LIGHT_BLUE}python -m test_rest_api -t "{colors.LIGHT_CYAN}<Path to test suite folder/file>{colors.LIGHT_BLUE}" -r "{colors.LIGHT_CYAN}<Path to test result folder>{colors.LIGHT_BLUE}" -h "{colors.LIGHT_CYAN}<#smoke>{colors.LIGHT_BLUE}"{colors.RESET}
Example: python -m test_rest_api -t "/Users/user/Documents/TestSuite" -r "/Users/user/Documents/TestResult" -h #smoke#sanity
"""


@dataclass(frozen=True)
class ErrorMsg:
    INVALID_TEST_SUITE_PATH: str = f"""
ERROR! Please provide a valid path for the test suite
{Docs.commands}
"""
    INVALID_ENV_PATH: str = f"""
ERROR! Please provide a valid path for .env file
{Docs.commands}
"""
    INVALID_TEST_RESULT_PATH: str = f"""
ERROR! Please provide a valid path for the test result
{Docs.commands}
"""
    INVALID_TEST_TAG: str = f"""
ERROR! Please provide a valid tag list
{Docs.commands}
"""
    INVALID_COMMAND: str = f"""
ERROR! Please provide a valid command
{Docs.commands}
"""
    EMPTY_TESTS: str = f"""
No Tests Found!
"""
    INVALID_REST_API: str = """
Invalid Rest Api
Please create proper rest api functions
Tip: Refer the example below !

Example Code:
from test_rest_api import rest_api
@rest_api
def login_api(username: str, password: str) -> dict:
    return {
            'url': 'https://my_domain.com/login',
            'parameters': {'param1': 'value1', 'param2': 'value2'},
            'headers': {'content-type': 'application/json'},
            'body': {'name':username,'password':password}
            }
"""
    INVALID_REST_API_CONFIG: str = f"""
Invalid Rest Api
Please return a valid dictionary/json from @rest_api decorated api functions
"""
    INVALID_METHOD: str = f"""
Invalid Request Method
Supported methods: 'get', 'post', 'put', 'patch', 'delete', 'head', 'options'
"""
    UNKNOWN_EXCEPTION: str = f"""
Sorry Something went wrong
"""
