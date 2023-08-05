"""Data object for player friends."""
import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic.types import UUID4

from .utils import to_camel


class Friend(BaseModel):
    """Friend object.

    Args:
        id (bool): Id of friend.
        uuid_sender (UUID4): UUID of player sending friend request.
        uuid_receiver (UUID4): UUID of player receiving friend request.
        started (datetime.datetime): Time players started being friends.
    """

    id: str = Field(alias="_id")
    uuid_sender: UUID4
    uuid_receiver: UUID4
    started: datetime.datetime

    class Config:
        """Config."""

        alias_generator = to_camel
