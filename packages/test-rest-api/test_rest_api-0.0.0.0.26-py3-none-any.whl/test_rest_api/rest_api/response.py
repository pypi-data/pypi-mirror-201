from dataclasses import dataclass
from aiohttp import ClientResponse


@dataclass(frozen=True)
class RestApiResponse:
    """
    test_rest_api Response object
    Users can use this instead of aiohttp ClientResponse object
    """
    status_code: int
    content_type: str
    body: dict
    headers: dict
    obj: ClientResponse
