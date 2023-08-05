"""SkyClash."""
from pydantic import BaseModel


class SkyClash(BaseModel):
    """SkyClash games stats.

    Args:
        card_packs (int): Card packs. Defaults to 0.
    """

    card_packs: int = 0
