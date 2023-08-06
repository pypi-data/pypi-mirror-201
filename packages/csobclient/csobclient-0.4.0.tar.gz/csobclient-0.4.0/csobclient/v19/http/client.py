"""HTTP base client."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


class HTTPRequestError(Exception):
    """Base HTTP request error."""


class HTTPConnectionError(HTTPRequestError):
    """Any error related to connection."""


class HTTPTimeoutError(HTTPRequestError):
    """HTTP request timed out."""


@dataclass
class HTTPResponse:
    """HTTP response wrapper."""

    http_success: bool
    data: dict


class HTTPClient(ABC):
    # pylint:disable=too-few-public-methods
    """Base HTTP client."""

    @abstractmethod
    def request(
        self, url: str, method: str = "post", json: Optional[dict] = None
    ) -> HTTPResponse:
        """Perform HTTP request.

        :param url: API method URL
        :param method: HTTP method to use
        :param json: JSON data to post

        :raises HTTPConnectionError: if connection fails
        :raises HTTPTimeoutError: if request timeouts
        :raises HTTPRequestError: for any other exception
        """
