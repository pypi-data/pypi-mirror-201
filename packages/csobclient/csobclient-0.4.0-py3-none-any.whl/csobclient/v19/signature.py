"""Module for dealing with the signature."""
import binascii
from base64 import b64decode, b64encode
from collections import OrderedDict
from urllib.parse import quote_plus, urljoin

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


_RESPONSE_KEYS = (
    "payId",
    "customerId",
    "dttm",
    "resultCode",
    "resultMessage",
    "paymentStatus",
    "authCode",
    "merchantData",
)


class InvalidSignatureError(Exception):
    """Response signature is invalid."""


def str_or_jsbool(val):
    """Return str of val."""
    if isinstance(val, bool):
        return str(val).lower()
    return str(val)


def mk_msg_for_sign(payload):
    """Make message for sign."""
    payload = payload.copy()
    if payload.get("cart"):
        cart_msg = []
        for one in payload["cart"]:
            cart_msg.extend(one.values())
        payload["cart"] = "|".join(map(str_or_jsbool, cart_msg))
    msg = "|".join(map(str_or_jsbool, payload.values()))
    return msg.encode("utf-8")


def mk_url(url: str, payload=None):
    """Make URL."""
    if payload is None:
        return url
    return urljoin(url, "/".join(map(quote_plus, payload.values())))


def mk_payload(key: str, pairs):
    """Make payload."""
    payload = OrderedDict([(k, v) for k, v in pairs if v is not None])
    payload["signature"] = sign(payload, key)
    return payload


def sign(payload, key: str):
    """Sign payload."""
    msg = mk_msg_for_sign(payload)
    key = RSA.importKey(key)  # type: ignore
    hasher = SHA256.new(msg)
    signer = PKCS1_v1_5.new(key)  # type: ignore
    return b64encode(signer.sign(hasher)).decode()


def _verify(payload: dict, signature: str, key: str):
    msg = mk_msg_for_sign(payload)
    key = RSA.importKey(key)  # type: ignore
    hasher = SHA256.new(msg)
    verifier = PKCS1_v1_5.new(key)  # type: ignore

    try:
        sig_as_bytes = b64decode(signature)
    except binascii.Error as exc:
        raise InvalidSignatureError(f"Failed to decode base64: {exc}") from exc

    # pylint:disable=not-callable
    return verifier.verify(hasher, sig_as_bytes)


def verify(json_data: dict, key: str) -> None:
    """Verify data."""
    signature = json_data.pop("signature", None)
    if not signature:
        raise InvalidSignatureError("Empty signature")

    payload = OrderedDict()
    for k in _RESPONSE_KEYS:
        if k in json_data:
            payload[k] = json_data[k]

    if not _verify(payload, signature, key):
        raise InvalidSignatureError("Invalid signature")
