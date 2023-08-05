"""Skywars."""
from asyncpixel.models.utils import safe_divide
from pydantic import BaseModel
from pydantic import Field


class Skywars(BaseModel):
    """Skywars games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        games_played (int): Total games played. Defaults to 0.
        tokens (int): Number of tokens. Defaults to 0.
        souls (int): Souls. Defaults to 0.
        winstreak (int): Current winstreak. Defaults to 0.
        kills (int): Total kills. Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
        wins (int): Total wins Defaults to 0.
        losses (int): Total losses. Defaults to 0.
    """

    coins: int = 0
    games_played: int = Field(0, alias="games_played_skywars")
    tokens: int = Field(0, alias="cosmetic_tokens")
    souls: int = 0
    winstreak: int = Field(0, alias="win_streak")
    kills: int = 0
    deaths: int = 0
    wins: int = 0
    losses: int = 0

    @property
    def kills_per_death(self) -> float:
        """Kills per deaths.

        Returns:
            float: ratio between kills and deaths.
        """
        return safe_divide(self.kills, self.deaths)

    @property
    def wins_per_lose(self) -> float:
        """Wins per losses..

        Returns:
            float: ratio between wins and losses.
        """
        return safe_divide(self.wins, self.losses)
