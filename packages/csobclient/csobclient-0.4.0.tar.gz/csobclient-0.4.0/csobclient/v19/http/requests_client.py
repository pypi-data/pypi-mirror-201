"""HTTP client which uses `requests` under the hood."""
from typing import Optional
import requests

from .client import (
    HTTPClient,
    HTTPConnectionError,
    HTTPRequestError,
    HTTPTimeoutError,
    HTTPResponse,
)

_DEFAULT_TIMEOUT = 10


class RequestsHTTPClient(HTTPClient):
    # pylint:disable=too-few-public-methods
    """`requests` HTTP client."""

    def __init__(self) -> None:
        self._session = requests.Session()

    def request(
        self, url: str, method: str = "post", json: Optional[dict] = None
    ) -> HTTPResponse:
        try:
            response = getattr(self._session, method.lower())(
                url, json=json, timeout=_DEFAULT_TIMEOUT
            )
            return HTTPResponse(response.ok, response.json())
        except ConnectionError as exc:
            raise HTTPConnectionError(exc) from exc
        except requests.Timeout as exc:
            raise HTTPTimeoutError(exc) from exc
        except requests.RequestException as exc:
            raise HTTPRequestError(exc) from exc
