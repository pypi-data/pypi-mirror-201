"""Vampirez."""
from pydantic import BaseModel


class VampireZ(BaseModel):
    """VampireZ games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        human_deaths (int): Total deaths as a human. Defaults to 0.
        vampire_deaths (int): Total deaths as a vampire. Defaults to 0.
        zombie_kills (int): Total kills of a zombie. Defaults to 0.
        vampire_kills (int): Total kills of a vampire. Defaults to 0.
        most_vampire_kills_new (int): Most Vampire kills Defaults to 0.
    """

    coins: int = 0
    human_deaths: int = 0
    vampire_deaths: int = 0
    zombie_kills: int = 0
    vampire_kills: int = 0
    most_vampire_kills_new: int = 0
