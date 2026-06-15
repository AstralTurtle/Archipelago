from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import TimeAttackIslandsWorld

# A region is a container for locations ("checks"), which connects to other regions via "Entrance" objects.
# Many games will model their Regions after physical in-game places, but you can also have more abstract regions.
# For a location to be in logic, its containing region must be reachable.
# The Entrances connecting regions can have rules - more on that in rules.py.
# This makes regions especially useful for traversal logic ("Can the player reach this part of the map?")

# Every location must be inside a region, and you must have at least one region.
# This is why we create regions first, and then later we create the locations (in locations.py).


def create_and_connect_regions(world: TimeAttackIslandsWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TimeAttackIslandsWorld) -> None:
    # Creating a region is as simple as calling the constructor of the Region class.
    menu = Region("Menu", world.player, world.multiworld)
    volcano = Region("Volcano Island", world.player, world.multiworld)
    mountain = Region("Mountain Island", world.player, world.multiworld)
    desert = Region("Desert Island", world.player, world.multiworld)
    lake = Region("Lake Island", world.player, world.multiworld)
    forest = Region("Forest Island", world.player, world.multiworld)
  

    # Let's put all these regions in a list.
    regions = [menu, volcano, desert, lake, mountain, forest]

    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += regions


def connect_regions(world: TimeAttackIslandsWorld) -> None:
    # We have regions now, but still need to connect them to each other.
    # But wait, we no longer have access to the region variables we created in create_all_regions()!
    # Luckily, once you've submitted your regions to multiworld.regions,
    # you can get them at any time using world.get_region(...).
    menu = world.get_region("Menu")
    volcano = world.get_region("Volcano Island")
    mountain = world.get_region("Mountain Island")
    desert = world.get_region("Desert Island")
    lake = world.get_region("Lake Island")
    forest = world.get_region("Forest Island")

    # An even easier way is to use the region.connect helper
    menu.connect(volcano, "Menu to Volcano")
    menu.connect(mountain, "Menu to Mountain")
    menu.connect(desert, "Menu to Desert")
    menu.connect(lake, "Menu to Lake")
    menu.connect(forest, "Menu to Forest")
