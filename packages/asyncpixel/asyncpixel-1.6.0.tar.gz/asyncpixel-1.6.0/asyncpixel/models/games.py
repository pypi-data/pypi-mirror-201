"""Game related objects."""
import datetime
from typing import Optional

from asyncpixel.constants import get_game_types
from pydantic import BaseModel
from pydantic import validator

from .game_type import GameType
from .utils import to_camel


class Game(BaseModel):
    """Game class.

    Args:
        date (datetime.datetime): Time game started.
        game_type (GameType): Game Type.
        mode (Optional[str]): Game mode.
        map (Optional[str]): Map the game is on.
        ended (Optional[datetime.datetime]): Time game ended. Defaults to None.
    """

    date: datetime.datetime
    game_type: GameType
    mode: Optional[str]
    map: Optional[str]
    ended: Optional[datetime.datetime] = None

    @validator("game_type", pre=True)
    @classmethod
    def validate_game_type(cls, v: str) -> GameType:
        """Turn game type to correct format."""
        game_type = [game for game in get_game_types() if game.type_name == v][0]
        return game_type

    class Config:
        """Config."""

        alias_generator = to_camel
