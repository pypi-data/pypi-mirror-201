"""TNT Games."""
from pydantic import BaseModel
from pydantic import Field


class TNTGames(BaseModel):
    """TNT games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
        wins (int): Total wins. Defaults to 0.
        record (int): Record. Defaults to 0.
        winstreak (int): Current winstreak. Defaults to 0.
    """

    coins: int = 0
    deaths: int = Field(0, alias="deaths_tntrun")
    wins: int = 0
    record: int = Field(0, alias="record_tntrun")
    winstreak: int = 0
