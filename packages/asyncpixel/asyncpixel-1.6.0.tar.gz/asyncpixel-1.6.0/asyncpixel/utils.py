"""Utils."""
import re
from typing import Optional
from typing import Union

ranks = {
    "NONE": None,
    "VIP": "VIP",
    "VIP_PLUS": "VIP+",
    "MVP": "MVP",
    "MVP_PLUS": "MVP+",
    "SUPERSTAR": "MVP++",
    "YOUTUBER": "YOUTUBE",
    "PIG+++": "PIG+++",
    "BUILD TEAM": "BUILD TEAM",
    "HELPER": "HELPER",
    "MODERATOR": "MOD",
    "ADMIN": "ADMIN",
    "SLOTH": "SLOTH",
    "OWNER": "OWNER",
}


def get_rank(
    package_rank: Optional[str] = None,
    rank: Optional[str] = None,
    prefix_raw: Optional[str] = None,
    monthly_package_rank: Optional[str] = None,
    new_package_rank: Optional[str] = None,
) -> Optional[str]:
    """Get rank of Hypixel player.

    Args:
        rank (Optional[str]): rank
        prefix_raw (Optional[str]): raw prefix
        monthly_package_rank (Optional[str]): monthly package for mvp++
        new_package_rank (Optional[str]): new rank format
        package_rank (Optional[str]): old rank format

    Returns:
        Optional[str]: rank
    """
    real_rank = None
    if prefix_raw and prefix_raw != "NONE":
        prefix = re.sub(r"§.", "", prefix_raw)[1:-1]
        # prefixes all start and end with brackets, and have Minecraft color codes,
        # this is to remove color codes and
        # brackets
        real_rank = ranks.get(prefix, prefix)
    elif rank and rank != "NORMAL":
        real_rank = ranks.get(re.sub(r"§.", "", rank)[1:-1], rank)
    elif (monthly_package_rank and monthly_package_rank != "NONE") and not real_rank:
        real_rank = ranks.get(monthly_package_rank, monthly_package_rank)
    elif new_package_rank and not real_rank:
        real_rank = ranks.get(new_package_rank, new_package_rank)
    elif package_rank and not real_rank:
        real_rank = ranks.get(package_rank, package_rank)
    return real_rank


def calc_player_level(xp: Union[float, int]) -> float:
    """Calculate player level from xp.

    Args:
        xp (int): amount of xp a player has.

    Returns:
        float: current level of player.
    """
    return float(1 + (-8750.0 + (8750**2 + 5000 * xp) ** 0.5) / 2500)
