"""Status data class."""
from typing import Optional

from asyncpixel.constants import get_game_types
from pydantic import BaseModel
from pydantic import validator

from .game_type import GameType
from .utils import to_camel


class Status(BaseModel):
    """Status data object.

    Args:
        online (bool): Wether player is online.
        game_type (Optional[GameType]): Current game player is playing.
            Defaults to None.
        mode (Optional[str]): Mode of current game. Defaults to None.
    """

    online: bool = False
    game_type: Optional[GameType] = None
    mode: Optional[str] = None

    @validator("game_type", pre=True)
    @classmethod
    def validate_game_type(cls, v: str) -> GameType:
        """Validate game type."""
        game_type = [game for game in get_game_types() if game.type_name == v][0]
        return game_type

    class Config:
        """Config."""

        alias_generator = to_camel
