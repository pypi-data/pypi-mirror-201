"""Walls3."""
from pydantic import BaseModel


class Walls3(BaseModel):
    """Walls3 games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        losses (int): Games lost. Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
    """

    coins: int = 0
    losses: int = 0
    deaths: int = 0
