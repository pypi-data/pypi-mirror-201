"""Merchant models."""
from base64 import b64encode, b64decode
from typing import Optional


class _MerchantData:
    """Merchant data."""

    def __init__(self, data: Optional[bytes]) -> None:
        self.data = data

    @property
    def base64(self) -> Optional[str]:
        """Return merchant data as string."""
        if self.data is None:
            return None

        data = b64encode(self.data).decode("UTF-8")
        if len(data) > 255:
            raise ValueError(
                "Merchant data length encoded to BASE64 is over 255 chars"
            )

        return data

    @classmethod
    def from_base64(cls, b64: Optional[str]) -> "_MerchantData":
        """Parse merchant data from base64 encoded string."""
        if b64 is None:
            return cls(None)

        return cls(b64decode(b64))
