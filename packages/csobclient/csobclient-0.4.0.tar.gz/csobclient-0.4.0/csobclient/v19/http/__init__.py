"""Module responsible for HTTP requests."""
from .client import (
    HTTPClient,
    HTTPRequestError,
    HTTPConnectionError,
    HTTPTimeoutError,
    HTTPResponse,
)
from .requests_client import RequestsHTTPClient
