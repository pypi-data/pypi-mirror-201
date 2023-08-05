"""Bedwars."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from asyncpixel.models.utils import safe_divide
from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator

# Amount of levels to prestige
LEVELS_PER_PRESTIGE = 100

# The exp required to level up once
LEVEL_COST = 5000

# The exp required to level up to the first few levels after a prestige
EASY_LEVEL_COSTS = {1: 500, 2: 1000, 3: 2000, 4: 3500}

# The exp required to level up past the easy levels
EASY_EXP = sum(EASY_LEVEL_COSTS.values())

# The amount of easy levels
EASY_LEVELS = len(EASY_LEVEL_COSTS)

# The exp required to prestige
PRESTIGE_EXP = EASY_EXP + (100 - EASY_LEVELS) * LEVEL_COST


def bedwars_level_from_exp(exp: int) -> float:
    """Bedwars level/star.

    Args:
        exp (int): the player's bedwars experience

    Returns:
        float: bedwars level + progress towards next level
    """
    levels = (exp // PRESTIGE_EXP) * LEVELS_PER_PRESTIGE
    exp %= PRESTIGE_EXP

    # The first few levels have different costs
    for i in range(1, EASY_LEVELS + 1):
        cost = EASY_LEVEL_COSTS[i]
        if exp >= cost:
            levels += 1
            exp -= cost
        else:
            # We can't afford the next level, so we have found the level we are at
            break

    levels += exp // LEVEL_COST
    exp %= LEVEL_COST

    next_level = (levels + 1) % LEVELS_PER_PRESTIGE

    # The cost of the next level
    if next_level in EASY_LEVEL_COSTS:
        next_level_cost = EASY_LEVEL_COSTS[next_level]
    else:
        next_level_cost = LEVEL_COST

    return levels + exp / next_level_cost


class BedwarsGame(BaseModel):
    """Bedwars GameMode stats.

    Args:
        items_purchased (int): Total Items purchased. Defaults to 0.
        diamond_resources_collected (int): Total diamonds collected. Defaults to 0.
        games_played (int): Number of games played. Defaults to 0.
        losses (int): Games lost for this Game Mode. Defaults to 0.
        gold_resources_collected (int): Total gold collected. Defaults to 0.
        void_deaths (int): Deaths to the void Defaults to 0.
        deaths (int): Total deaths. Defaults to 0.
        winstreak (int): Current winstreak. Defaults to 0.
        beds_lost (int): Total beds lost. Defaults to 0.
        final_deaths (int): Total final deaths. Defaults to 0.
        entity_attack_deaths (int): Number of deaths to an entity. Defaults to 0.
        beds_broken (int): Beds broken. Defaults to 0.
        entity_attack_final_deaths (int): Number of deaths to an entity. Defaults to 0.
        fall_deaths (int): Total deaths from fall damage. Defaults to 0.
        magic_deaths (int): Total deaths to magic. Defaults to 0.
        permanent_items_purchased (int): Number of items that are not lost
            in the game purchased. Defaults to 0.
        void_kills (int): Kills using the void. Defaults to 0.
        kills (int): Total Total kills. Defaults to 0.
        wins (int): Total games won. Defaults to 0.
        void_final_deaths (int): Total final deaths to the void. Defaults to 0.
        final_kills (int): Total final kills. Defaults to 0.
    """

    items_purchased: int = Field(0, alias="items_purchased_bedwars")
    diamond_resources_collected: int = Field(
        0, alias="diamond_resources_collected_bedwars"
    )
    games_played: int = Field(0, alias="games_played_bedwars")
    losses: int = Field(0, alias="losses_bedwars")
    iron_resources_collected: int = Field(0, alias="iron_resources_collected_bedwars")
    resources_collected: int = Field(0, alias="resources_collected_bedwars")
    gold_resources_collected: int = Field(0, alias="gold_resources_collected_bedwars")
    void_deaths: int = Field(0, alias="void_deaths_bedwars")
    deaths: int = Field(0, alias="deaths_bedwars")
    winstreak: int = Field(0, alias="winstreak")
    beds_lost: int = Field(0, alias="beds_lost_bedwars")
    final_deaths: int = Field(0, alias="final_deaths_bedwars")
    entity_attack_deaths: int = Field(0, alias="entity_attack_deaths_bedwars")
    beds_broken: int = Field(0, alias="beds_broken_bedwars")
    entity_attack_final_deaths: int = Field(
        0, alias="entity_attack_final_deaths_bedwars"
    )
    fall_deaths: int = Field(0, alias="fall_deaths_bedwars")
    magic_deaths: int = Field(0, alias="magic_deaths_bedwars")
    permanent_items_purchased: int = Field(
        0, alias="permanent _items_purchased_bedwars"
    )
    void_kills: int = Field(0, alias="void_kills_bedwars")
    kills: int = Field(0, alias="kills_bedwars")
    wins: int = Field(0, alias="wins_bedwars")
    void_final_deaths: int = Field(0, alias="void_final_deaths_bedwars")
    final_kills: int = Field(0, alias="final_kills_bedwars")

    @property
    def win_per_lose(self) -> float:
        """Wins per losses.

        Returns:
            float: ratio between game wins and game losses.
        """
        return safe_divide(self.wins, self.losses)

    @property
    def beds_broken_per_lost(self) -> float:
        """Beds broken per Beds lost.

        Returns:
            float: ratio between beds broken and lost.
        """
        return safe_divide(self.beds_broken, self.beds_lost)

    @property
    def final_kills_per_final_death(self) -> float:
        """Final kills per final death.

        Returns:
            float: ratio between final kills and final deaths.
        """
        return safe_divide(self.final_kills, self.final_deaths)


class Bedwars(BaseModel):
    """Bedwars Stats.

    Args:
        kills (int): Total kills across all Bedwars gamemodes. Defaults to 0.
        wins (int): Total wins across all Bedwars gamemodes. Defaults to 0.
        coins (int): Total coins collected. Defaults to 0.
        games_played (int): Number of bedwars games played. Defaults to 0.
        final_deaths (int): Number of final deaths across all Bedwars gamemodes.
            Defaults to 0.
        deaths (int): Number of deaths across all Bedwars gamemodes. Defaults to 0.
        final_kills (int): Number of final kills across all Bedwars gamemodes.
            Defaults to 0.
        losses (int): Total bedwars games lost. Defaults to 0.
        beds_lost (int): Number of beds lost across all Bedwars gamemodes.
            Defaults to 0.
        beds_broken (int): Number of beds broken across all Bedwars gamemodes.
            Defaults to 0.
        winstreak (int): Current winstreak. Defaults to 0.
        experience (int): Total bedwars experience. Defaults to 0.
        singles (Optional[BedwarsGame]): Stats for the singles Gamemode.
        doubles (Optional[BedwarsGame]): Stats for the doubles Gamemode.
        triples (Optional[BedwarsGame]): Stats for the triples Gamemode.
        quads (Optional[BedwarsGame]): Stats for the quads Gamemode.
        four_v_four (Optional[BedwarsGame]): Stats for the four vs four Gamemode.
        quads_ultimate (Optional[BedwarsGame]): Stats for the quads ultimate Gamemode.
        doubles_ultimate (Optional[BedwarsGame]): Stats for the doubles
            ultimate Gamemode.
        castle (Optional[BedwarsGame]): Stats for the castle Gamemode.
        entity_attack_deaths (int): Deaths to an entity. Defaults to 0.
        entity_attack_final_deaths (int): Final deaths to an entity. Defaults to 0.
        fall_deaths (int): Overall fall deaths. Defaults to 0.
        fall_final_deaths (int): Overall final fall deaths Defaults to 0.
        projectile_deaths (int): Projectile deaths. Defaults to 0.
        suffocation_deaths (int): Overall suffocation deaths. Defaults to 0.
        magic_deaths (int): Overall magic deaths. Defaults to 0.
        entity_explosion_deaths (int): Overall explosion deaths. Defaults to 0.
        magic_final_deaths (int): Overall magic final deaths. Defaults to 0.
        void_deaths (int): Overall void deaths. Defaults to 0.
        void_final_death (int): Overall void final deaths. Defaults to 0.
        fire_tick_final_death (int): Overall fire final deaths. Defaults to 0.
        void_kills (int): Overall void kills. Defaults to 0.
        entity_attack_kills (int): Overall entity attack kills. Defaults to 0.
        entity_attack_final_kills (int): Overall entity attack final kills.
            Defaults to 0.
        projectile_final_kills (int): Overall projectile final kills. Defaults to 0.
        entity_explosion_kills (int): Overall entity explosion kills. Defaults to 0.
        projectile_kills (int): Overall projectile kills. Defaults to 0.
        fall_final_kills (int): Overall final fall kills. Defaults to 0.
        fall_kills (int): Overall fall kills. Defaults to 0.
        resources_collected (int): Overall resources collected. Defaults to 0.
        iron_resources_collected (int): Overall iron resources collected. Defaults to 0.
        diamond_resources_collected (int): Overall diamond resources collected.
            Defaults to 0.
        emerald_resources_collected (int): Overall emerald resources collected.
            Defaults to 0.
        items_purchased (int): Overall items purchased. Defaults to 0.
        permanent_items_purchased (int): Overall permanent items purchased.
            Defaults to 0.
        bedwars_box_rares (int): Bedwars boxes that are rare. Defaults to 0.
        bedwars_box (int): Total Bedwars boxes. Defaults to 0.
        chest_history_new (List[str]): Chest history.  Defaults to [].
        bedwars_box_commons (int): Total common Bedwars boxes. Defaults to 0.
        spray_glyph_field (str): Current spray glyph.  Defaults to "".
        active_island_topper (str): Current island topper.  Defaults to "".
        active_projectile_trail (str): Current projectile trail.  Defaults to "".
        bedwars_easter_boxes (int): Bedwars easters boxes. Defaults to 0.
        Bedwars_opened_chests (int): Total chests opened in Bedwars. Defaults to 0.
        Bedwars_opened_rares (int): Total rare chests opened in Bedwars.
            Defaults to 0.
        Bedwars_opened_commons (int): Total common chests opened in Bedwars.
            Defaults to 0.
        active_npc_skin (str): Current active NPC skin.  Defaults to "".
        favourites_2 (str): Favourites.  Defaults to "".
        Bedwars_opened_epics (int): Total epic chests opened in Bedwars.
            Defaults to 0.
        active_death_cry (str): Equiped active death cry.  Defaults to "".
        active_kill_effect (str): Equiped kill effect.  Defaults to "".
        active_sprays (str): Equiped spray.  Defaults to "".
        active_glyph (str): Active glyph.  Defaults to "".
        selected_ultimate (str): Selected Ultimate.  Defaults to "".
    """

    kills: int = Field(0, alias="kills_bedwars")
    wins: int = Field(0, alias="wins_bedwars")
    coins: int = Field(0, alias="coins")
    games_played: int = Field(0, alias="games_played_bedwars")
    final_deaths: int = Field(0, alias="final_deaths_bedwars")
    deaths: int = Field(0, alias="deaths_bedwars")
    final_kills: int = Field(0, alias="final_kills_bedwars")
    losses: int = Field(0, alias="losses_bedwars")
    beds_lost: int = Field(0, alias="beds_lost_bedwars")
    beds_broken: int = Field(0, alias="beds_broken_bedwars")
    winstreak: int = Field(0, alias="winstreak")
    experience: int = Field(0, alias="Experience")

    singles: Optional[BedwarsGame]
    doubles: Optional[BedwarsGame]
    triples: Optional[BedwarsGame]
    quads: Optional[BedwarsGame]
    four_v_four: Optional[BedwarsGame]
    quads_ultimate: Optional[BedwarsGame]
    doubles_ultimate: Optional[BedwarsGame]
    castle: Optional[BedwarsGame]

    # Deaths
    entity_attack_deaths: int = Field(0, alias="entity_attack_deaths_bedwars")
    entity_attack_final_deaths: int = Field(
        0, alias="entity_attack_final_deaths_bedwars"
    )
    fall_deaths: int = Field(0, alias="fall_deaths_bedwars")
    fall_final_deaths: int = Field(0, alias="fall_final_deaths_bedwars")
    projectile_deaths: int = Field(0, alias="projectile_deaths_bedwars")
    suffocation_deaths: int = Field(0, alias="suffocation_deaths_bedwars")
    magic_deaths: int = Field(0, alias="magic_deaths_bedwars")
    entity_explosion_deaths: int = Field(0, alias="entity_explosion_deaths_bedwars")
    magic_final_deaths: int = Field(0, alias="magic_final_deaths_bedwars")
    void_deaths: int = Field(0, alias="void_deaths_bedwars")
    void_final_death: int = Field(0, alias="void_final_deaths_bedwars")
    fire_tick_final_death: int = Field(0, alias="fire_tick_final_deaths_bedwars")

    # Kills
    void_kills: int = Field(0, alias="void_kills_bedwars")
    entity_attack_kills: int = Field(0, alias="entity_attack_kills_bedwars")
    entity_attack_final_kills: int = Field(0, alias="entity_attack_final_kills_bedwars")
    projectile_final_kills: int = Field(0, alias="projectile_final_kills_bedwars")
    entity_explosion_kills: int = Field(0, alias="entity_explosion_kills_bedwars")
    projectile_kills: int = Field(0, alias="projectile_kills_bedwars")
    fall_final_kills: int = Field(0, alias="fall_final_kills_bedwars")
    fall_kills: int = Field(0, alias="fall_kills_bedwars")

    # Resources
    resources_collected: int = Field(0, alias="resources_collected_bedwars")
    iron_resources_collected: int = Field(0, alias="iron_resources_collected_bedwars")
    diamond_resources_collected: int = Field(
        0, alias="diamond_resources_collected_bedwars"
    )
    emerald_resources_collected: int = Field(
        0, alias="emerald_resources_collected_bedwars"
    )

    # Purchases
    items_purchased: int = Field(0, alias="_items_purchased_bedwars")
    permanent_items_purchased: int = Field(0, alias="permanent_items_purchased_bedwars")

    # Other
    bedwars_box_rares: int = Field(0, alias="bedwars_box_rares")
    bedwars_box: int = Field(0, alias="bedwars_box")
    chest_history_new: List[str] = Field([], alias="chest_history_new")
    bedwars_box_commons: int = Field(0, alias="bedwars_box_commons")
    spray_glyph_field: str = Field("", alias="spray_glyph_field")
    active_island_topper: str = Field("", alias="activeIslandTopper")
    active_projectile_trail: str = Field("", alias="activeProjectileTrail")
    bedwars_easter_boxes: int = Field(0, alias="beds_lost_bedwars")
    Bedwars_opened_chests: int = Field(0, alias="Bedwars_openedChests")
    Bedwars_opened_rares: int = Field(0, alias="Bedwars_openedRares")
    Bedwars_opened_commons: int = Field(0, alias="Bedwars_openedCommons")
    active_npc_skin: str = Field("", alias="activeNPCSkin")
    favourites_2: str = Field("", alias="favourites_2")
    Bedwars_opened_epics: int = Field(0, alias="Bedwars_openedEpics")
    active_death_cry: str = Field("", alias="activeDeathCry")
    active_kill_effect: str = Field("", alias="activeKillEffect")
    active_sprays: str = Field("", alias="activeSprays")
    active_glyph: str = Field("", alias="activeGlyph")
    selected_ultimate: str = Field("", alias="selected_ultimate")

    @property
    def final_kills_per_final_death(self) -> float:
        """Final kills per final death.

        Returns:
            float: ratio between final kills and final deaths.
        """
        return safe_divide(self.final_kills, self.final_deaths)

    @property
    def beds_broken_per_lost(self) -> float:
        """Beds broken per Beds lost.

        Returns:
            float: ratio between beds broken and beds lost.
        """
        return safe_divide(self.beds_broken, self.beds_lost)

    @property
    def win_lose(self) -> float:
        """Wins per losses.

        Returns:
            float: ratio between game wins and game losses.
        """
        return safe_divide(self.wins, self.losses)

    @property
    def level(self) -> float:
        """Bedwars level/star.

        Returns:
            float: bedwars level + progress towards next level
        """
        return bedwars_level_from_exp(self.experience)

    @root_validator(pre=True)
    @classmethod
    def traverse_sources(cls, values: Dict[str, Any]) -> Dict[str, Any]:  # noqa: C901
        """Traverse all sources."""
        out = values.copy()
        for name, field in values.items():
            if name.startswith("eight_one_"):
                if "singles" not in out:
                    out["singles"] = {}

                out["singles"][name[10:]] = field
            elif name.startswith("eight_two_"):
                if "doubles" not in out:
                    out["doubles"] = {}

                out["doubles"][name[10:]] = field
            elif name.startswith("four_three_"):
                if "triples" not in out:
                    out["triples"] = {}

                out["triples"][name[11:]] = field
            elif name.startswith("four_four_"):
                if "quads" not in out:
                    out["quads"] = {}

                out["quads"][name[10:]] = field
            elif name.startswith("two_four_"):
                if "four_v_four" not in out:
                    out["four_v_four"] = {}

                out["four_v_four"][name[9:]] = field
            elif name.startswith("quads_ultimate_"):  # pragma: no cover
                if "quads_ultimate" not in out:
                    out["quads_ultimate"] = {}

                out["quads_ultimate"][name[15:]] = field
            elif name.startswith("ultimate_"):  # pragma: no cover
                if "doubles_ultimate" not in out:
                    out["doubles_ultimate"] = {}

                out["doubles_ultimate"][name[9:]] = field
            elif name.startswith("castle_"):
                if "castle" not in out:
                    out["castle"] = {}

                out["castle"][name[7:]] = field

        return out
