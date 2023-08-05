"""Pit."""
from pydantic import BaseModel


class Pit(BaseModel):
    """Pit games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        total_kills (int): Total kills. Defaults to 0.
        total_wins (int): Total wins. Defaults to 0.
        shots_fired (int): Total shots fired. Defaults to 0.
    """

    coins: int = 0
    total_kills: int = 0
    total_wins: int = 0
