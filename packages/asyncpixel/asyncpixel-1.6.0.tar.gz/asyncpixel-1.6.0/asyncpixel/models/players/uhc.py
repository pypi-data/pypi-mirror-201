"""UHC."""
from pydantic import BaseModel


class UHC(BaseModel):
    """UHC games stats.

    Args:
        coins (int): Number of coins gathered in this Game Mode. Defaults to 0.
    """

    coins: int = 0
