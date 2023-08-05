"""Paintball."""
from pydantic import BaseModel


class Paintball(BaseModel):
    """Paintball games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
        wins (int): Total wins. Defaults to 0.
        shots_fired (int): Total shots fired. Defaults to 0.
    """

    coins: int = 0
    deaths: int = 0
    wins: int = 0
    shots_fired: int = 0
