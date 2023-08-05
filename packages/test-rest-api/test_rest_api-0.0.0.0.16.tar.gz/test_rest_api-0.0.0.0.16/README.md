<img alt="test_rest_api" src="https://raw.githubusercontent.com/troymjose/test_rest_api/version_0.0.0.3/test_rest_api.png"  width="50%" >

# TEST REST API

The __test_rest_api__ framework makes it easy to write __fast asynchronous__ REST Api tests, yet scales to support
complex testing.

## Requirements

[Python](https://www.python.org/) >= 3.8

[aiohttp](https://pypi.org/project/aiohttp/)

[Jinja2](https://pypi.org/project/Jinja2/)

[python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

```
pip install test_rest_api
```

## Example

An example of a simple test:

```python
from test_rest_api import test


@test()
async def my_func_name():
    pass
```

## Test Execution

An example of a simple test execution command:

__Syntax__

```
python -m test_rest_api -t "<Path of test folder or file>" -r "<Path to save test report>"
```

__Example__

```
python -m test_rest_api -t "/Users/user/Documents/TestSuite" -r "/Users/user/Documents/TestResult"
```

## Features

- __Asyncronus__ programming (Powered by [asyncio](https://pypi.org/project/asyncio/))
- One of the __fastest__ python rest api test frameworks available
- Supports both asyncronus & __syncronuous__ tests
- __Auto discovery__ of test modules and functions
- Beautifull rich __html test reporting__ with dashboards
- Detailed info on unexpected errors while creating automaton tests
- Fast to code, increase the speed to develop tests by about 200% to 300%
- Designed to be easy to use and learn
- Supports end-to-end testing with __CI/CD pipelines__
- Supports __parameterization__, __correlation__ and __logging__
- Supports selective test executions using hashtags eg: __#smoke__

## Authors

- [Troy M Jose](https://www.linkedin.com/in/troymjose/)

## License

Copyright Troy M Jose, 2023.

Distributed under the terms of the [MIT](https://choosealicense.com/licenses/mit/) license, pytest is free and open
source software.

