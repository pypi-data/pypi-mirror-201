"""MCGO."""
from pydantic import BaseModel
from pydantic import Field


class MCGO(BaseModel):
    """MCGO games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
        shots_fired (int): Total shots fired. Defaults to 0.
        round_wins (int): Total round wins. Defaults to 0.
        bombs_planted (int): Total bombs planted. Defaults to 0.
        game_wins_deathmatch (int): Total games won of deathmatch. Defaults to 0.
        wins (int): Total wins. Defaults to 0.
        kills (int): Total kills. Defaults to 0.
    """

    coins: int = 0
    deaths: int = 0
    shots_fired: int = 0
    round_wins = 0
    bombs_planted: int = 0
    game_wins_deathmatch: int = 0
    wins: int = Field(0, alias="game_wins")
    kills: int = 0
