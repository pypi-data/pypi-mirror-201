"""Pet objects."""
import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic.types import UUID4

from .utils import to_camel
from .utils import to_upper


class PetStat(BaseModel):
    """Pet State.

    Parameters
    ----------
    timestamp : datetime.datetime
        Timestamp of the stat
    value : int
        Value of the stat
    """

    timestamp: datetime.datetime
    value: int


class Pet(BaseModel):
    """Pet.

    Parameters
    ----------
    thirst : Optional[PetStat]
        Thirst stat
    exercise : Optional[PetStat]
        Exercise stat
    hunger : Optional[PetStat]
        Hunger stat
    experience : Optional[int]
        Experience of the pet
    name : Optional[str]
        Name of the pet
    """

    thirst: Optional[PetStat]
    exercise: Optional[PetStat]
    hunger: Optional[PetStat]
    experience: Optional[int] = Field(alias="experience")
    name: Optional[str] = Field(alias="name")

    class Config:
        """Config."""

        alias_generator = to_upper


class ProfilePet(BaseModel):
    """Profile Pet.

    Parameters
    ----------
    uuid : Optional[UUID4]
        UUID of the pet
    type : str
        Type of the pet
    exp : float
        Experience of the pet
    active : bool
        Wether the pet is active
    tier : str
        Tier of the pet
    held_item : Optional[str]
        Item held by the pet
    candy_used : int
        Amount of candy used on the pet
    skin : Optional[str]
        Skin of the pet
    """

    uuid: Optional[UUID4]
    type: str
    exp: float
    active: bool
    tier: str
    held_item: Optional[str]
    candy_used: int
    skin: Optional[str]

    class Config:
        """Config."""

        alias_generator = to_camel
