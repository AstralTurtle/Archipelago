from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import TimeAttackIslandsWorld

# Every location must have a unique integer ID associated with it.
# We will have a lookup from location name to ID here that, in world.py, we will import and bind to the world class.
# Even if a location doesn't exist on specific options, it must be present in this lookup.
LOCATION_NAME_TO_ID = {
    "Volcano Island - Bronze Medal": 1,
    "Volcano Island - Silver Medal": 2,
    "Volcano Island - Gold Medal": 3,
    "Volcano Island - Platinum Medal": 4,
    "Volcano Island - Diamond Medal": 5,
    "Mountain Island - Bronze Medal": 6,
    "Mountain Island - Silver Medal": 7,
    "Mountain Island - Gold Medal": 8,
    "Mountain Island - Platinum Medal": 9,
    "Mountain Island - Diamond Medal": 10,
    "Desert Island - Bronze Medal": 11,
    "Desert Island - Silver Medal": 12,
    "Desert Island - Gold Medal": 13,
    "Desert Island - Platinum Medal": 14,
    "Desert Island - Diamond Medal": 15,
    "Lake Island - Bronze Medal": 16,
    "Lake Island - Silver Medal": 17,
    "Lake Island - Gold Medal": 18,
    "Lake Island - Platinum Medal": 19,
    "Lake Island - Diamond Medal": 20,
    "Forest Island - Bronze Medal": 21,
    "Forest Island - Silver Medal": 22,
    "Forest Island - Gold Medal": 23,
    "Forest Island - Platinum Medal": 24,
    "Forest Island - Diamond Medal": 25,
}


# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class TimeAttackIslandsLocation(Location):
    game = "Time Attack Islands"


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: TimeAttackIslandsWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: TimeAttackIslandsWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    menu = world.get_region("Menu")
    volcano = world.get_region("Volcano Island")
    mountain = world.get_region("Mountain Island")
    desert = world.get_region("Desert Island")
    lake = world.get_region("Lake Island")
    forest = world.get_region("Forest Island")

    # A simpler way to do this is by using the region.add_locations helper.
    # For this, you need to have a dict of location names to their IDs (i.e. a subset of location_name_to_id)
    # Aha! So that's why we made that "get_location_names_with_ids" helper method earlier.
    # You also need to pass your overridden Location class.

    volcano_locations = get_location_names_with_ids(["Volcano Island - Bronze Medal", "Volcano Island - Silver Medal", "Volcano Island - Gold Medal", "Volcano Island - Platinum Medal", "Volcano Island - Diamond Medal"])
    mountain_locations = get_location_names_with_ids(["Mountain Island - Bronze Medal", "Mountain Island - Silver Medal", "Mountain Island - Gold Medal", "Mountain Island - Platinum Medal", "Mountain Island - Diamond Medal"])
    lake_locations = get_location_names_with_ids(["Lake Island - Bronze Medal", "Lake Island - Silver Medal", "Lake Island - Gold Medal", "Lake Island - Platinum Medal", "Lake Island - Diamond Medal"])
    forest_locations = get_location_names_with_ids(["Forest Island - Bronze Medal", "Forest Island - Silver Medal", "Forest Island - Gold Medal", "Forest Island - Platinum Medal", "Forest Island - Diamond Medal"])
    desert_locations = get_location_names_with_ids(["Desert Island - Bronze Medal", "Desert Island - Silver Medal", "Desert Island - Gold Medal", "Desert Island - Platinum Medal", "Desert Island - Diamond Medal"])

    volcano.add_locations(volcano_locations, TimeAttackIslandsLocation)
    mountain.add_locations(mountain_locations, TimeAttackIslandsLocation)
    lake.add_locations(lake_locations, TimeAttackIslandsLocation)
    forest.add_locations(forest_locations, TimeAttackIslandsLocation)
    desert.add_locations(desert_locations, TimeAttackIslandsLocation)



    # Locations may be in different regions depending on the player's options.
    # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     top_middle_room.add_locations(top_middle_room_locations, TimeAttackIslandsLocation)
    # else:
    #     menu.add_locations(top_middle_room_locations, TimeAttackIslandsLocation)

    # Locations may exist only if the player enables certain options.
    # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
        # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
        # exist, it must still always be present in the world's location_name_to_id.
        # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
        # bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
        # menu.add_locations(bottom_left_extra_chest, TimeAttackIslandsLocation)


def create_events(world: TimeAttackIslandsWorld) -> None:
    tiers = ["Bronze", "Silver", "Gold", "Diamond", "Platinum"]
    islands = ["Volcano", "Mountain", "Desert", "Lake", "Forest"]

    for island in islands:
        region = world.get_region(f"{island} Island")
        region.add_event(f"{island} Island Completed", "Island Completed", location_type=TimeAttackIslandsLocation)
