"""Game type."""
from typing import Optional

from pydantic import BaseModel


class GameType(BaseModel):
    """Main game class.

    Args:
        id (str): ID
        purchaser_uuid (uuid.UUID): UUID of booster.
        amount (int): Amount of boosters.
        original_length (int): Original length of booster.
        length (int): Length of booster.
        game_type (int): Game type.
        date_activated (datetime.datetime): Date boost activated.
        stacked (Union[List[uuid.UUID], bool]): Wether boosters stacked.
    """

    id: int
    type_name: str
    database_name: str
    lobby_name: Optional[str]
    clean_name: str
    standard_name: str
    legacy: bool = False
