"""Player objects."""
import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from asyncpixel import utils
from asyncpixel.constants import get_game_types
from asyncpixel.models.pet import Pet
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from pydantic.class_validators import root_validator
from pydantic.types import UUID4

from .game_type import GameType
from .players import Arcade
from .players import Arena
from .players import Battleground
from .players import Bedwars
from .players import BuildBattle
from .players import Duels
from .players import GingerBread
from .players import Housing
from .players import HungerGames
from .players import Legacy
from .players import MCGO
from .players import Paintball
from .players import Pit
from .players import Quake
from .players import SkyClash
from .players import Skywars
from .players import TNTGames
from .players import UHC
from .players import VampireZ
from .players import Walls
from .players import Walls3
from .utils import to_camel


class Stats(BaseModel):
    """Game Stats.

    Args:
        bedwars (Optional[Bedwars]): bedwars stats.
        arcade (Optional[Arcade]): Arcade stats.
        build_battle (Optional[BuildBattle]): Build Battle stats.
        duels (Optional[Duels]): Duels stats.
        battleground (Optional[Battleground]): Battleground stats.
        hunger_games (Optional[HungerGames]): Hunger Games stats.
        ginger_bread (Optional[GingerBread]): Ginger Bread stats.
        paintball (Optional[Paintball]): Paintball stats.
        quake (Optional[Quake]): Quake stats.
        vampirez (Optional[VampireZ]): VampireZ stats.
        tnt_games (Optional[TNTGames]): TNT Games stats.
        uhc (Optional[UHC]): UHC stats.
        mcgo (Optional[MCGO]): MCGO stats.
        walls3 (Optional[Walls3]): Walls3 stats.
        walls (Optional[Walls]): Walls stats.
        arena (Optional[Arena]): Arena stats.
        sky_clash (Optional[SkyClash]): SkyClash stats.
        pit (Optional[Pit]): Pit stats.
        housing (Optional[Housing]): Housing stats.
        legacy (Optional[Legacy]): Legacy stats.
    """

    bedwars: Optional[Bedwars] = Field(alias="Bedwars")
    arcade: Optional[Arcade] = Field(alias="Arcade")
    build_battle: Optional[BuildBattle] = Field(alias="BuildBattle")
    duels: Optional[Duels] = Field(alias="Duels")
    battleground: Optional[Battleground] = Field(alias="Battleground")
    hunger_games: Optional[HungerGames] = Field(alias="HungerGames")
    ginger_bread: Optional[GingerBread] = Field(alias="GingerBread")
    paintball: Optional[Paintball] = Field(alias="Paintball")
    quake: Optional[Quake] = Field(alias="Quake")
    vampirez: Optional[VampireZ] = Field(alias="VampireZ")
    tnt_games: Optional[TNTGames] = Field(alias="TNTGames")
    uhc: Optional[UHC] = Field(alias="UHC")
    mcgo: Optional[MCGO] = Field(alias="MCGO")
    walls3: Optional[Walls3] = Field(alias="Walls3")
    walls: Optional[Walls] = Field(alias="Walls")
    arena: Optional[Arena] = Field(alias="Arena")
    sky_clash: Optional[SkyClash] = Field(alias="SkyClash")
    pit: Optional[Pit] = Field(alias="Pit")
    housing: Optional[Housing] = Field(alias="Housing")
    legacy: Optional[Legacy] = Field(alias="Legacy")
    skywars: Optional[Skywars] = Field(alias="SkyWars")

    # true_combat: Optional[TrueCombat] = Field(alias="TrueCombat")
    # speed_uhc: Optional[SpeedUHC]= Field(alias="SpeedUHC")
    # sky_block: Optional[SkyBlock]= Field(alias="SkyBlock")
    # super_smash: Optional[SuperSmash] = Field(alias="SuperSmash")


class Social(BaseModel):
    """Social accounts.

    Args:
        twitter (Optional[str]): Twitter.
        youtube (Optional[str]): YouTube.
        instagram (Optional[str]): Instagram.
        twitch (Optional[str]): Twitch.
        discord (Optional[str]): Discord.
        hypixel_forums (Optional[str]): Hypixel Forums.
    """

    twitter: Optional[str]
    youtube: Optional[str]
    instagram: Optional[str]
    twitch: Optional[str]
    discord: Optional[str]
    hypixel_forums: Optional[str]

    @root_validator(pre=True)
    @classmethod
    def get_social_media(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Get social media in correct format."""
        out = values.copy()
        for k, v in out["links"].items():
            out[k.lower()] = v
        return out


class Player(BaseModel):
    """Player.

    Args:
        uuid (UUID4): uuid of user.
        displayname (Optional[str]): Display name of user.
        rank (Optional[str]): Rank of user
        first_login (datetime.datetime): First login date.
        last_login (Optional[datetime.datetime]): Most recent login date.
        last_logout (Optional[datetime.datetime]): Last logout.
        stats (Stats): Stats for various game types.
        social_media (Optional[Social]): Social media accounts.
        id (Optional[str]): id of user.
        playername (Optional[str]): Playername.
        known_aliases (Optional[List[str]]): known aliases.
        known_aliases_lower (Optional[List[str]]): known aliases in lowercase.
        achievements_one_time (Optional[List[str]]): Achievements.
        mc_version_rp (Optional[str]): Minecraft version.
        network_exp (Optional[float]): Network experience.
        karma (Optional[int]): Player karma.
        last_adsense_generate_time (Optional[datetime.datetime]): Last generate
            time for adsense.
        last_claimed_reward (Optional[int]): Last claimed reward.
        total_rewards (Optional[int]): Total rewards.
        total_daily_rewards (Optional[int]): Total daily awards.
        reward_streak (Optional[int]): Current reward streak.
        reward_score (Optional[int]): Reward score.
        reward_high_score (Optional[int]): High score for rewards.
        friend_requests_uuid (Optional[List[UUID4]]): UUID of friend requests.
        achievement_tracking (Optional[List[str]]): Achievement tracking.
        achievement_points (Optional[int]): achievement points.
        current_gadget (Optional[str]): Current equipped gadget.
        channel (Optional[str]): Channel.
        most_recent_game_type (Optional[GameType]): Most recent Game Type that
            has been played.
        level (Optional[float]): Level of user.
        pet_stats (Optional[Pet]): Pet stats.
        raw (Dict[str, Any]): raw data
    """

    uuid: UUID4
    displayname: Optional[str]
    rank: Optional[str]

    @root_validator(pre=True)
    @classmethod
    def create_rank(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Get the rank."""
        out = values.copy()
        rank = utils.get_rank(
            values.get("rank"),
            values.get("prefix"),
            values.get("monthlyPackageRank"),
            values.get("newPackageRank"),
            values.get("packageRank"),
        )
        out["rank"] = rank
        return out

    first_login: datetime.datetime
    last_login: Optional[datetime.datetime]
    last_logout: Optional[datetime.datetime]
    stats: Stats
    social_media: Optional[Social]

    id: Optional[str] = Field(alias="_id")
    playername: Optional[str]
    known_aliases: Optional[List[str]]
    known_aliases_lower: Optional[List[str]]
    achievements_one_time: Optional[List[str]]
    mc_version_rp: Optional[str]
    network_exp: Optional[float]
    karma: Optional[int]
    last_adsense_generate_time: Optional[datetime.datetime]
    last_claimed_reward: Optional[int]
    total_rewards: Optional[int]
    total_daily_rewards: Optional[int]
    reward_streak: Optional[int]
    reward_score: Optional[int]
    reward_high_score: Optional[int]
    friend_requests_uuid: Optional[List[UUID4]]
    achievement_tracking: Optional[List[str]]
    achievement_points: Optional[int]
    current_gadget: Optional[str]
    channel: Optional[str]
    most_recent_game_type: Optional[GameType]
    pet_stats: Optional[Dict[str, Pet]]

    @validator("most_recent_game_type", pre=True)
    @classmethod
    def validate_game_type(cls, v: Union[str, int]) -> GameType:
        """Validate game type."""
        try:
            game_type = [game for game in get_game_types() if game.id == v][0]
        except Exception:
            game_type = [game for game in get_game_types() if game.type_name == v][0]
        return game_type

    level: float

    @root_validator(pre=True)
    @classmethod
    def create_level(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Create level."""
        out = values.copy()
        exp = float(out.get("networkExp", 0.0))
        out["level"] = utils.calc_player_level(exp)
        return out

    raw: Dict[str, Any]

    @root_validator(pre=True)
    @classmethod
    def create_raw(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Create a copy of the values to directly access."""
        out = values.copy()
        out["raw"] = values
        return out

    class Config:
        """Config."""

        alias_generator = to_camel
