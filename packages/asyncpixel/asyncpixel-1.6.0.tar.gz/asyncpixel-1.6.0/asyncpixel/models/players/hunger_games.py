"""Hunger Games."""
from pydantic import BaseModel


class HungerGames(BaseModel):
    """Hunger Games games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
        damge (int): Total damage dealt. Defaults to 0.
        wins (int): Total wins. Defaults to 0.
        games_played (int): Total games player. Defaults to 0.
    """

    coins: int = 0
    deaths: int = 0
    damge: int = 0
    wins: int = 0
    games_played: int = 0
