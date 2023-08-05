"""Build Battle."""
from pydantic import BaseModel


class BuildBattle(BaseModel):
    """Build Battle games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        games_played (int): Total games played. Defaults to 0.
        score (int): Score. Defaults to 0.
    """

    coins: int = 0
    games_played: int = 0
    score: int = 0
