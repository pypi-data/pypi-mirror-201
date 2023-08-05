"""Watchdog objects."""
from pydantic import BaseModel
from pydantic import Field

from .utils import to_camel


class WatchDog(BaseModel):
    """Base class for watchdog.

    Args:
        watchdog_last_minute (int): Watchdog bans in last minute.
        staff_rolling_daily (int): Staff bans in the day.
        watchdog_total (int): Watchdog total bans.
        watchdog_rolling_daily (int): Watchdog bans in the day.
        staff_total (int): Staff total bans.
    """

    watchdog_last_minute: int = Field(alias="watchdog_lastMinute")
    staff_rolling_daily: int = Field(alias="staff_rollingDaily")
    watchdog_total: int = Field(alias="watchdog_total")
    watchdog_rolling_daily: int = Field(alias="watchdog_rollingDaily")
    staff_total: int = Field(alias="staff_total")

    class Config:
        """Config."""

        alias_generator = to_camel
