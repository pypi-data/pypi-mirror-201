"""A Python HypixelAPI wrapper."""
#  Copyright (C) 2020 Leon Bowie
# This program is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License a
# long with this program. If not, see <https://www.gnu.org/licenses/>.
import datetime
import uuid
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import aiohttp
from pydantic import parse_obj_as

from .exceptions import ApiNoSuccessError
from .exceptions import InvalidApiKeyError
from .exceptions import RateLimitError
from .models import Auction
from .models import AuctionEnded
from .models import AuctionItem
from .models import Bazaar
from .models import BazaarItem
from .models import Boosters
from .models import Friend
from .models import Game
from .models import GameCounts
from .models import Guild
from .models import Key
from .models import Leaderboards
from .models import News
from .models import Player
from .models import Profile
from .models import Status
from .models import WatchDog
from .utils import calc_player_level

__all__ = ["Hypixel"]

BASE_URL = "https://api.hypixel.net/"

UUID = Union[str, uuid.UUID]


class Hypixel:
    """Client class for hypixel wrapper."""

    def __init__(
        self,
        api_key: Optional[UUID] = None,
    ) -> None:
        """Initialise client object.

        Args:
            api_key (Optional[UUID], optional): hypixel api key. Defaults to None.
        """
        if isinstance(api_key, str) and api_key is not None:
            api_key = uuid.UUID(api_key)
        self.api_key = api_key
        self._session = aiohttp.ClientSession()
        self.requests_remaining: int = -1
        self.total_requests: int = 0
        self._ratelimit_reset: datetime.datetime = datetime.datetime(1998, 1, 1)
        self.retry_after: datetime.datetime = datetime.datetime(1998, 1, 1)
        self._calc_player_level = calc_player_level

    async def __aenter__(self) -> "Hypixel":
        """Enter context manager."""
        return self  # pragma: no cover

    async def __aexit__(self, *args: Any) -> None:
        """Exit context manager."""
        await self.close()  # pragma: no cover

    async def close(self) -> None:
        """Used for safe client cleanup."""
        await self._session.close()  # pragma: no cover

    async def _get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        key_required: bool = True,
    ) -> Dict[str, Any]:
        """Base function to get raw data from hypixel.

        Args:
            path (str):
                path that you wish to request from.
            params (Dict, optional):
                parameters to pass into request defaults to empty dictionary.
            key_required (bool): Whether an api key is needed

        Raises:
            RateLimitError: error if ratelimit has been reached.
            InvalidApiKeyError: error if api key is invalid.
            ApiNoSuccessError: error if api throughs an error.

        Returns:
            dict: returns a dictionary of the json response.
        """
        if (
            self.requests_remaining != -1
            and (
                self.requests_remaining == 0
                and self._ratelimit_reset > datetime.datetime.now()
            )
            or self.retry_after
            and (self.retry_after > datetime.datetime.now())
        ):
            raise RateLimitError(self.retry_after)

        if params is None:
            params = {}
        if key_required:
            if self.api_key is None:
                raise InvalidApiKeyError("No API key provided")
            params["key"] = str(self.api_key)

        response: aiohttp.ClientResponse = await self._session.get(
            f"{BASE_URL}{path}", params=params
        )

        if response.status == 429:
            self.requests_remaining = 0
            self.retry_after = datetime.datetime.now() + datetime.timedelta(
                seconds=int(response.headers["Retry-After"])
            )
            raise RateLimitError(
                datetime.datetime.now()
                + datetime.timedelta(seconds=int(response.headers["Retry-After"]))
            )

        elif response.status == 403:
            raise InvalidApiKeyError()

        elif response.status != 200:
            raise ApiNoSuccessError(path)

        elif key_required and "RateLimit-Limit" in response.headers:
            if self.total_requests == 0:
                self.total_requests = int(response.headers["RateLimit-Limit"])
            self.requests_remaining = int(response.headers["RateLimit-Remaining"])
            self._ratelimit_reset = datetime.datetime.now() + datetime.timedelta(
                seconds=int(response.headers["RateLimit-Reset"])
            )

        data: Dict[str, Any] = await response.json()

        return data

    async def watchdog_stats(self) -> WatchDog:
        """Get current watchdog stats.

        Returns:
            WatchDog: WatchDog stats object.
        """
        data = await self._get("watchdogstats")

        return WatchDog.parse_obj(data)

    async def key_data(self, key: Optional[str] = None) -> Key:
        """Get information about an api key.

        Args:
            key (str, optional): api key. Defaults token provided in class.

        Raises:
            InvalidApiKeyError: No api key available.

        Returns:
            Key: Key object.
        """
        if not key:
            key = str(self.api_key)

        if key == "None":
            raise InvalidApiKeyError()

        params = {"key": key}

        data = (await self._get("key", params=params, key_required=False))["record"]

        return Key.parse_obj(data)

    async def boosters(self) -> Boosters:
        """Get the current online boosters.

        Returns:
            Boosters: object containing boosters.
        """
        data = await self._get("boosters")
        data["decrementing"] = data["boosterState"]["decrementing"]
        return Boosters.parse_obj(data)

    async def player_count(self) -> int:
        """Get the current amount of players online.

        Returns:
            int: number of online players.
        """
        data = await self._get("playerCount")

        return int(data["playerCount"])

    async def news(self) -> List[News]:
        """Get current skyblock news.

        Returns:
            List[News]: List of news objects.
        """
        data = await self._get("skyblock/news")

        return parse_obj_as(List[News], data["items"])

    async def player_status(self, uuid: UUID) -> Optional[Status]:
        """Get current online status about a player.

        Args:
            uuid (UUID): uuid of player.

        Returns:
            Status: Status object of player.
        """
        data = await self._get("status", params={"uuid": str(uuid)})
        if data["session"] is None:
            return None
        return Status.parse_obj(data["session"])

    async def player_friends(self, uuid: UUID) -> Optional[List[Friend]]:
        """Get a list of a players friends.

        Args:
            uuid (UUID): the uuid of the player you wish to get friends from.

        Returns:
            List[Friend]: returns a list of friend elements.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("friends", params=params)
        if data["records"] is None:
            return None

        return parse_obj_as(List[Friend], data["records"])

    async def bazaar(self) -> Bazaar:
        """Get info of the items in the bazaar.

        Returns:
            Bazaar: object for bazzar.
        """
        data = await self._get("skyblock/bazaar", key_required=False)

        bazaar_items = []

        for name in data["products"]:
            elements = data["products"][name]
            elements["name"] = name
            bazaar_items.append(BazaarItem.parse_obj(elements))

        return Bazaar(
            last_updated=data["lastUpdated"],
            bazaar_items=bazaar_items,
        )

    async def auctions(self, page: int = 0, retry: int = 3) -> Auction:
        """Get the auctions available.

        Args:
            page (int): Page of auction list you want. Defaults to 0.
            retry (int): Amount of retries to get the data from the api Defaults to 3.

        Returns:
            Auction: Auction object.
        """
        params = {"page": page}
        for _ in range(retry):  # pragma: no cover
            try:
                data = await self._get(
                    "skyblock/auctions", params=params, key_required=False
                )
                break
            except aiohttp.ServerTimeoutError:
                pass
        return Auction.parse_obj(data)

    async def auctions_ended(self, retry: int = 3) -> AuctionEnded:
        """Get the ended auctions.

        Args:
            retry (int): Amount of retries to get the data from the api Defaults to 3.

        Returns:
            AuctionEnded: Auctions ended object.
        """
        for _ in range(retry):  # pragma: no cover
            try:
                data = await self._get("skyblock/auctions_ended", key_required=False)
                break
            except aiohttp.ServerTimeoutError:
                pass
        return AuctionEnded.parse_obj(data)

    async def recent_games(self, uuid: UUID) -> Optional[List[Game]]:
        """Get recent games of a player.

        Args:
            uuid (UUID): uuid of player.

        Returns:
            List[Game]: list of recent games.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("recentGames", params=params)
        if data["games"] is None:
            return None

        return parse_obj_as(List[Game], data["games"])

    async def player(self, uuid: UUID) -> Optional[Player]:
        """Get information about a player from their uuid.

        Args:
            uuid (UUID): uuid of player.

        Returns:
            Player: player object.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("player", params=params)
        if data["player"] is None:
            return None
        return Player.parse_obj(data["player"])

    async def guild_by_name(self, guild_name: str) -> Optional[Guild]:
        """Get guild by name.

        Args:
            guild_name (str): name of guild.

        Returns:
            Guild: guild object.
        """
        params = {"name": guild_name}
        data = await self._get("guild", params=params)
        if data["guild"] is None:
            return None
        return Guild.parse_obj(data["guild"])

    async def guild_by_id(self, guild_id: str) -> Optional[Guild]:
        """Get guild by id.

        Args:
            guild_id (str): id of guild.

        Returns:
            Guild: guild object.
        """
        params = {"id": guild_id}
        data = await self._get("guild", params=params)
        if data["guild"] is None:
            return None
        return Guild.parse_obj(data["guild"])

    async def guild_by_player(self, player_uuid: UUID) -> Optional[Guild]:
        """Get guild by player.

        Args:
            player_uuid (UUID): uuid of a player in the guild.

        Returns:
            Guild: guild object.
        """
        params = {"player": str(player_uuid)}
        data = await self._get("guild", params=params)
        if data["guild"] is None:
            return None
        return Guild.parse_obj(data["guild"])

    async def auction_from_uuid(self, uuid: UUID) -> Optional[List[AuctionItem]]:
        """Get auction from uuid.

        Args:
            uuid (UUID): minecraft uuid.

        Returns:
            List[AuctionItem]: list of auctions.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("skyblock/auction", params=params)
        if data["auctions"] is None:
            return None
        return parse_obj_as(List[AuctionItem], data["auctions"])

    async def auction_from_player(self, player: str) -> Optional[List[AuctionItem]]:
        """Get auction data from player.

        Args:
            player (str): player.

        Returns:
            List[AuctionItem]: list of auction items.
        """
        params = {"player": player}
        data = await self._get("skyblock/auction", params=params)
        if data["auctions"] is None:
            return None
        return parse_obj_as(List[AuctionItem], data["auctions"])

    async def auction_from_profile(
        self, profile_id: str
    ) -> Optional[List[AuctionItem]]:
        """Get auction data from profile.

        Args:
            profile_id (str): profile id.

        Returns:
            List[AuctionItem]: list of auction items.
        """
        params = {"profile": profile_id}
        data = await self._get("skyblock/auction", params=params)
        if data["auctions"] is None:
            return None
        return parse_obj_as(List[AuctionItem], data["auctions"])

    async def game_count(self) -> GameCounts:
        """Gets number of players per game.

        Returns:
            GameCounts: game counts.
        """
        data = await self._get("gameCounts")
        return GameCounts.parse_obj(data)

    async def leaderboards(self) -> Dict[str, List[Leaderboards]]:
        """Get the current leaderboards.

        Returns:
            Dict[str, Leaderboards]: raw json response.
        """
        data = await self._get("leaderboards")
        leaderboard = {}
        leaderboards = data["leaderboards"]
        for key in leaderboards.keys():
            leaderboards_list = []
            for element in leaderboards[key]:
                location: Tuple[int, int, int] = (
                    int(element["location"].split(",")[0]),
                    int(element["location"].split(",")[1]),
                    int(element["location"].split(",")[2]),
                )
                leaderboards_list.append(
                    Leaderboards(
                        path=element["path"],
                        prefix=element["prefix"],
                        title=element["title"],
                        location=location,
                        count=element["count"],
                        leaders=element["leaders"],
                    )
                )
            leaderboard[key] = leaderboards_list

        return leaderboard

    async def resources_achievements(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/achievements", key_required=False)
        return data

    async def resources_challenges(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/challenges", key_required=False)
        return data

    async def resources_quests(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/quests", key_required=False)
        return data

    async def resources_guilds_achievements(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/guilds/achievements", key_required=False)
        return data

    async def resources_guilds_permissions(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/guilds/permissions", key_required=False)
        return data

    async def resources_skyblock_collections(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/skyblock/collections", key_required=False)
        return data

    async def resources_skyblock_skills(self) -> Dict[str, Any]:
        """Get the current resources. Does not require api key.

        Returns:
            Dict[str, Any]: raw json response.
        """
        data = await self._get("resources/skyblock/skills", key_required=False)
        return data

    async def profile(self, profile: str) -> Optional[Profile]:
        """Get profile info of a skyblock player.

        Args:
            profile (str): profile id of player can be gotten from
                            running profiles.

        Returns:
            Union[Profile, None]: Profile if it exists
        """
        params = {"profile": profile}
        data = await self._get("skyblock/profile", params=params)
        if data["profile"] is None:
            return None
        return Profile.parse_obj(data["profile"])

    async def profiles(self, uuid: UUID) -> Optional[Dict[str, Profile]]:
        """Get info on a profile.

        Args:
            uuid (UUID): uuid of player.

        Returns:
            Dict[str, Profile]: json response.
        """
        params = {"uuid": str(uuid)}
        data = await self._get("skyblock/profiles", params=params)
        if data["profiles"] is None:
            return None
        profiles = data["profiles"]
        profile_dict = {}
        for profile in profiles:
            _id = profile["profile_id"]
            profile_dict[_id] = Profile.parse_obj(profile)
        return profile_dict

    async def uuid_from_name(self, username: str) -> Optional[uuid.UUID]:
        """Helper method to get uuid from username.

        Args:
            username (str): username of player

        Returns:
            UUID4: uuid of player
        """
        async with self._session.get(
            "https://api.mojang.com/users/profiles/minecraft/" f"{username}"
        ) as response:
            if response.status != 200:
                return None
            else:
                return uuid.UUID((await response.json())["id"])
