"""Customer login."""
from enum import Enum
from typing import Optional


class AuthMethod(Enum):
    """Auth method."""

    GUEST = "guest"
    ACCOUNT = "account"
    FEDERATED = "federated"
    ISSUER = "issuer"
    THIRD_PARTY = "thirdparty"
    FIDO = "fido"
    FIDO_SIGNED = "fido_signed"
    API = "api"


class LoginData:
    # pylint:disable=too-few-public-methods
    """Customer login data."""

    def __init__(
        self,
        auth: Optional[AuthMethod] = None,
        auth_at: Optional[str] = None,  # TODO: ISO8061
        auth_data: Optional[str] = None,
    ):
        self.auth = auth
        self.auth_at = auth_at
        self.auth_data = auth_data
