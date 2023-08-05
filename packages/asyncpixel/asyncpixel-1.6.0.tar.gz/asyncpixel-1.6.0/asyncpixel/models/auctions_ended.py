"""Ended auction related objects."""
import datetime
from typing import Dict
from typing import List
from typing import Union

from pydantic import BaseModel
from pydantic.types import UUID4

from .utils import to_camel


class AuctionEndedItem(BaseModel):
    """Ended auction model.

    Args:
        auction_id (UUID4): Id of auction.
        seller (UUID4): Id of seller.
        seller_profile (UUID4): Profile_id of seller.
        buyer (str): Id of buyer.
        timestamp (datetime.datetime): Time when the auction was bought.
        bin (bool): Whether the auction is BIN (Buy It Now).
        item_bytes (Union[str, Dict[str, Union[int, str]]]): NBT-encoded item data.
        price (int): Final sell price of the auction.
    """

    auction_id: UUID4
    seller: UUID4
    seller_profile: UUID4
    buyer: UUID4
    timestamp: datetime.datetime
    bin: bool = False
    item_bytes: Union[str, Dict[str, Union[int, str]]]
    price: int


class AuctionEnded(BaseModel):
    """Main auction ended object.

    Args:
        last_updated (datetime.datetime): Time last updated.
        auctions (List[AuctionItem]): List of auctions.
    """

    last_updated: datetime.datetime
    auctions: List[AuctionEndedItem]

    class Config:
        """Config."""

        alias_generator = to_camel
