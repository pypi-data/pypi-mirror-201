"""Guild objects."""
import datetime
import uuid
from typing import Dict
from typing import List
from typing import Optional

from asyncpixel.models.utils import to_camel
from pydantic import BaseModel
from pydantic.fields import Field


class Pattern(BaseModel):
    """Pattern.

    Args:
        color (int): colour.
        pattern (str): pattern.
    """

    color: int
    pattern: str


class GuildMembers(BaseModel):
    """Members in a guild.

    Args:
        uuid (uuid.UUID): UUID of player.
        rank (str): Rank of player.
        joined (datetime.datetime): Time player joined guild.
        exp_history (Dict[str, int]): Exp history of player.
        quest_participation (int): How many quests the player has participated in.
        muted_till (Optional[datetime.datetime]): Time player unmuted. Defaults to None.
    """

    uuid: uuid.UUID
    rank: str
    joined: datetime.datetime
    exp_history: Optional[Dict[str, int]]
    quest_participation: Optional[int] = None
    muted_till: Optional[datetime.datetime] = None

    class Config:
        """Config."""

        alias_generator = to_camel


class Rank(BaseModel):
    """Rank.

    Args:
        name (str): Name of rank.
        default (bool): wether its the default.
        created (int): Created.
        priority (int): Priority of role.
        tag (str): Tag of role.
    """

    name: str
    default: bool
    created: int
    priority: int
    tag: Optional[str] = None


class Guild(BaseModel):
    """Guild object.

    Args:
        id (str): Guild ID.
        created (datetime.datetime): Timestamp this guild was created at.
        name (str): Name of guild.
        name_lower (str: Priority of role.
        description (str): Description of this guild that appears in the
            guild list and /g info.
        tag (str): Tag of guild.
        exp (int): Exp or guild.
        members (List[GuildMembers]): Array of guild members.
        achievements (Dict[str, int]): Guild achievements earned and
            the current progress.
        ranks (List[Rank]): Array of guild ranks.
        joinable (bool): Whether this guild can be joined using /g join.
        legacy_ranking (int): Ranking in the number of guild coins owned in
            the legacy guild system (0-indexed).
        publicly_listed (bool): Whether this guild is listed in the Guild Finder.
        preferred_games (List[str]): This guild's set preferred games.
        chat_mute (datetime.datetime): Timestamp guild chat will be unmuted at,
            or 0 if guild chat is not muted.
        guild_exp_by_game_type (Dict[str, str]): Amount of EXP earned for this guild
            by which game it was earned in.
        tag_color (Optional[str]): Color of this guild's tag, if set. Defaults to None.
    """

    id: str = Field(alias="_id")
    created: datetime.datetime
    name: str
    name_lower: str = Field(alias="name_lower")
    description: Optional[str]
    tag: Optional[str]
    exp: int
    members: List[GuildMembers]
    achievements: Dict[str, int]
    ranks: Optional[List[Rank]]
    joinable: bool = False
    legacy_ranking: Optional[int] = None
    publicly_listed: Optional[bool]
    preferred_games: Optional[List[str]]
    chat_mute: Optional[datetime.datetime] = None
    guild_exp_by_game_type: Optional[Dict[str, int]]
    tag_color: Optional[str]

    class Config:
        """Config."""

        alias_generator = to_camel
