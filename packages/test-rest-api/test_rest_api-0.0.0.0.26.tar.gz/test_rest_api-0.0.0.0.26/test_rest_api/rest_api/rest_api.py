from dataclasses import asdict
from aiohttp.client_exceptions import ClientConnectorError, InvalidURL, ContentTypeError
from .method import RestApiMethod
from ..utils.error_msg import ErrorMsg
from ..utils.aiohttp_session import AioHttpSession
from .response import RestApiResponse, ClientResponse
from .exception import RestApiSendException, RestApiCreationException


class RestApiMeta(type):
    """
    Meta class for raising RestApiCreationException
    """

    # Calls for each instance creation
    def __call__(cls, *args, **kwargs):
        try:
            cls._instance = super().__call__(*args, **kwargs)
        except Exception as e:
            # Catch python class instance creation exceptions
            raise RestApiCreationException(msg=str(e).replace('RestApi.__init__()', '').strip().capitalize())
        # Validate _instance url, parameters, headers and body
        cls._validate()
        # Return the instance
        return cls._instance

    def _validate(self):
        """
        Validate url, parameters, headers and body
        """
        self._validate_url()
        self._validate_parameters_and_headers()
        self._validate_body()

    def _validate_url(self):
        """
        Checks
        ------
        1. Valid string
        """
        if not isinstance(self._instance.url, str):
            raise RestApiCreationException(msg='Invalid data type for url. Please provide a valid string')

    def _validate_parameters_and_headers(self):
        """
        Checks
        ------
        1. Valid dictionary
        2. Valid dictionary schema
        """
        error = 'Please provide a valid dictionary, with both dictionary key and dictionary value as string type'
        for item in ('parameters', 'headers'):
            if not isinstance(getattr(self._instance, item), dict):
                raise RestApiCreationException(msg=f'Invalid data type for {item}. {error}')
            if not all([isinstance(key, str) and isinstance(key, str) for key, value in
                        getattr(self._instance, item).items()]):
                raise RestApiCreationException(msg=f'Invalid dictionary for {item}. {error}')

    def _validate_body(self):
        """
        Checks
        ------
        1. Valid dictionary
        """
        if not isinstance(self._instance.body, dict):
            raise RestApiCreationException(msg='Invalid data type for body. Please provide a valid dictionary')


class RestApi(metaclass=RestApiMeta):
    """
    Class for creating rest api instances
    """
    # Create a frozen instance of RestApiMethod, so that it can be used as a constant in code
    METHODS = RestApiMethod()

    def __init__(self, url: str, parameters: dict = {}, headers: dict = {}, body: dict = {}):
        # Rest api variables
        self.url = url
        self.parameters = parameters
        self.headers = headers
        self.body = body
        # Aiohttp variables
        self._session = AioHttpSession()

    def __str__(self):
        return f"""
Url:        {self.url}
Headers:    {self.headers}
Parameters: {self.parameters}
Body:       {self.body}
"""

    async def send(self, method: str):
        """
        Send the rest api by providing the request method
        """
        try:
            # Check if method is of type string
            if not isinstance(method, str):
                raise Exception('Invalid data type for method. Please provide a valid string')
            # Convert to lowercase
            method = method.lower()
            # Check if the method is valid
            if method not in asdict(self.METHODS).values():
                raise Exception(ErrorMsg.INVALID_METHOD)
            # Send the request
            async with getattr(self._session, method)(url=self.url,
                                                      params=self.parameters,
                                                      headers=self.headers,
                                                      json=self.body) as response:
                return await self._create_response(response=response)
        except ClientConnectorError as exc:
            raise RestApiSendException(msg=str(exc))
        except InvalidURL as exc:
            raise RestApiSendException(msg='Invalid ULR')
        except ContentTypeError as exc:
            raise RestApiSendException(msg=str(exc))
        except Exception as exc:
            raise RestApiSendException(msg=str(exc))

    async def _create_response(self, response: ClientResponse) -> RestApiResponse:
        """
        Create response instance object from aiohttp async response
        """
        # Retrieve the response body in JSON
        body = await response.json()
        # Get the other response parameters
        status_code, headers, content_type = response.status, dict(response.headers), response.content_type
        # Create and return the RestApiResponse instance object
        return RestApiResponse(status_code=status_code,
                               content_type=content_type,
                               body=body,
                               headers=headers,
                               obj=response)

    async def get(self):
        """
        Send HTTP GET Request
        """
        return await self.send(method=self.METHODS.GET)

    async def post(self):
        """
        Send HTTP POST Request
        """
        return await self.send(method=self.METHODS.POST)

    async def put(self):
        """
        Send HTTP PUT Request
        """
        return await self.send(method=self.METHODS.PUT)

    async def patch(self):
        """
        Send HTTP PATCH Request
        """
        return await self.send(method=self.METHODS.PATCH)

    async def delete(self):
        """
        Send HTTP DELETE Request
        """
        return await self.send(method=self.METHODS.DELETE)

    async def head(self):
        """
        Send HTTP HEAD Request
        """
        return await self.send(method=self.METHODS.HEAD)

    async def options(self):
        """
        Send HTTP OPTIONS Request
        """
        return await self.send(method=self.METHODS.OPTIONS)
