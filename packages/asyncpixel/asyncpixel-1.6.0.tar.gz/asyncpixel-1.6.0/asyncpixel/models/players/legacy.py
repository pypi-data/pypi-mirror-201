"""Legacy."""
from pydantic import BaseModel


class Legacy(BaseModel):
    """Legacy games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
        total_kills (int): Total kills. Defaults to 0.
        total_wins (int): Total wins. Defaults to 0.
    """

    coins: int = 0
    total_kills: int = 0
    total_wins: int = 0
