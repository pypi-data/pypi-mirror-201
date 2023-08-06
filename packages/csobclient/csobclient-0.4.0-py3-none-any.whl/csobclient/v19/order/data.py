"""Order data."""
from enum import Enum
from typing import Optional

from ..currency import Currency
from .delivery import DeliveryData
from .address import AddressData

from ..fields import _IntField


class OrderType(Enum):
    """Order type."""

    PURCHASE = "purchase"
    BALANCE = "balance"
    PREPAID = "prepaid"
    CASH = "cash"
    CHECK = "check"


class OrderAvailability(Enum):
    """Order availability."""

    NOW = "now"
    PREORDER = "preorder"


class GiftCardsData:
    # pylint:disable=too-few-public-methods
    """Gift cards data."""

    quantity = _IntField(min_value=1, max_value=99)

    def __init__(
        self,
        total_amount: Optional[int] = None,
        currency: Optional[Currency] = None,
        quantity: Optional[int] = None,
    ) -> None:
        self.total_amount = total_amount
        self.currency = currency
        self.quantity = quantity


class OrderData:
    # pylint:disable=too-few-public-methods, too-many-instance-attributes
    """Order data."""

    def __init__(
        self,
        order_type: Optional[OrderType] = None,
        availability: Optional[
            OrderAvailability
        ] = None,  # TODO: or ISO8061 format, eg "YYYY-MM-DD".
        delivery: Optional[DeliveryData] = None,
        name_match: Optional[bool] = None,
        address_match: Optional[bool] = None,
        billing: Optional[AddressData] = None,
        shipping: Optional[AddressData] = None,
        shipping_added_at: Optional[str] = None,  # TODO: ISO8061
        reorder: Optional[bool] = None,
        gift_cards: Optional[GiftCardsData] = None,
    ) -> None:
        # pylint:disable=too-many-arguments
        self.order_type = order_type
        self.availability = availability
        self.delivery = delivery
        self.name_match = name_match
        self.address_match = address_match
        self.billing = billing
        self.shipping = shipping
        self.shipping_added_at = shipping_added_at
        self.reorder = reorder
        self.gift_cards = gift_cards
