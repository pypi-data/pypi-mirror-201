"""Duels."""
from pydantic import BaseModel


class Duels(BaseModel):
    """Duels games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        deaths (int): Totaldeaths. Defaults to 0.
        losses (int): Games lost. Defaults to 0.
        losses (int): Games won. Defaults to 0.
        damage_dealt (int): Damge dealt in total. Defaults to 0.
        rounds_played (int): Number of rounds played. Defaults to 0.
    """

    coins: int = 0
    deaths: int = 0
    losses: int = 0
    wins: int = 0
    damage_dealt: int = 0
    rounds_played: int = 0
