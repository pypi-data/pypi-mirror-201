"""Profile objects."""
import datetime
import math
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from asyncpixel.models.pet import ProfilePet
from pydantic import BaseModel


class Quests(BaseModel):
    """Armor.

    Args:
        status (str): Status of quest.
        activated_at (datetime.datetime): Time activated.
        activated_at_sb (datetime.datetime): Time activated.
        completed_at (datetime.datetime): Time Completed.
        completed_at_sb (datetime.datetime): Time Completed.
    """

    status: str
    activated_at: datetime.datetime
    activated_at_sb: datetime.datetime
    completed_at: datetime.datetime
    completed_at_sb: datetime.datetime


class Objective(BaseModel):
    """Armor.

    Args:
        status (str): Status of objective.
        progress (int): Progress through objective.
        completed_at (Optional[datetime.datetime]): Time compelted at. Defaults to None.
    """

    status: str
    progress: int
    completed_at: Optional[datetime.datetime] = None


class InvArmor(BaseModel):
    """Armor.

    Args:
        type (int): Type of armor.
        data (str): Data of armor.
    """

    type: int
    data: str


class Members(BaseModel):
    """Member.

    Args:
        last_save (datetime.datetime):Time last saved.
        inv_armor (InvArmor): Armor.
        first_join (datetime.datetime): Time first joined.
        first_join_hub (Optional[datetime.datetime]): first joined hub.
        stats (Dict[str, int]): Member stats.
        objectives (Dict[str, Objective]): Objectives.
        tutorial (List[str]): Tutorial.
        quests (Dict[str, Quests]): Quests done.
        coin_purse (Optional[int]): Amount of coins in purse.
        last_death (datetime.datetime): Time last died.
        crafted_generators (List[str]): Crafted generators.
        visited_zones (Optional[List[str]]): Visited zones.
        fairy_souls_collected (int): Souls collected.
        fairy_souls (Optional[int]): Fairy souls.
        death_count (Optional[int]): death count.
        slayer_bosses (Dict[str, Dict[str, Any]]): Slayer bosses.
        pets (List[ProfilePet]): Pets.
    """

    last_save: Optional[datetime.datetime]
    first_join: Optional[datetime.datetime]
    coin_purse: float = 0
    fairy_souls_collected: int = 0
    fairy_souls: int = 0
    fairy_exchanges: int = 0
    pets: List[ProfilePet] = []
    collection: Dict[str, Any] = {}
    collections_unlocked: int = 0

    inv_armor: Optional[InvArmor]
    first_join_hub: Optional[int]
    stats: Optional[Dict[str, float]]
    tutorial: List[str] = []
    last_death: Optional[int]
    crafted_generators: List[str] = []
    visited_zones: List[str] = []
    death_count: int = 0

    @property
    def fairy_bonus(self) -> Dict[str, int]:
        """Bonus from fairy.

        Returns:
            Dict[str, int]: Fairy bonus.
        """
        bonus = {"speed": 0, "strength": 0, "defense": 0, "health": 0}
        bonus["speed"] = math.floor(self.fairy_exchanges / 10)

        for i in range(self.fairy_exchanges):
            bonus["strength"] += 2 if (i + 1) % 5 == 0 else 1
            bonus["defense"] += 2 if (i + 1) % 5 == 0 else 1
            bonus["health"] += 3 + math.floor(i / 2)
        return bonus


class Profile(BaseModel):
    """Profile.

    Args:
        profile_id (str): Id of profile
        cute_name (Optional[str]): Cute name of profile
        members (Dict[str, Members]): Dict of all members in profile.
    """

    profile_id: uuid.UUID
    cute_name: Optional[str]
    members: Dict[str, Members]
    banking: Optional[Dict[str, Any]]
    community_upgrades: Optional[Dict[str, Any]]
