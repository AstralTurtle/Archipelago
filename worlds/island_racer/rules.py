from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import IslandRacerWorld

from rule_builder.rules import Rule

class MedalTierReached(Rule["IslandRacerWorld"], game="Island Racer"):
    island: str

    def _instantiate(self, world):
        tier = world.MEDAL_TIERS[world.options.medal_tier_required.value]
        return self.Resolved(
            island=self.island,
            tier=tier,
            player=world.player,
        )

    class Resolved(Rule.Resolved):
        island: str
        tier: str

        def _evaluate(self, state) -> bool:
            return state.has_loc(f"{self.island} Island - {self.tier} Medal", self.player)

def set_all_rules(world: IslandRacerWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world)
    # set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: IslandRacerWorld) -> None:
    # First, we need to actually grab our entrances. Luckily, there is a helper method for this.


    # volcano_entrance =  world.get_entrance("Menu to Volcano")
    mountain_entrance = world.get_entrance("Menu to Mountain")
    desert_entrance = world.get_entrance("Menu to Desert")
    lake_entrance = world.get_entrance("Menu to Lake")
    forest_entrance = world.get_entrance("Menu to Forest")


    # Now, let's make some rules!
    # First, let's handle the transition from the overworld to the bottom right room,
    # which requires slashing a bush with the Sword.
    # For this, we need a rule that says "player has a Sword".
    # We can use a "Has"-type rule from the rule_builder module for this.
    can_access_mountain = Has("Mountain Pass")
    can_access_desert = Has("Desert Pass")
    can_access_lake = Has("Lake Pass")
    can_access_forest = Has("Forest Pass")


    # Now we can set our "can_destroy_bush" rule to the entrance which requires slashing a bush to clear the path.
    # The easiest way to do this is by calling world.set_rule, which works for both Locations and Entrances.
    world.set_rule(mountain_entrance, can_access_mountain)
    world.set_rule(desert_entrance, can_access_desert)
    world.set_rule(lake_entrance, can_access_lake)
    world.set_rule(forest_entrance, can_access_forest)



    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.
    # TODO: probably need something like this for random start
    # if world.options.hammer:
    #     overworld_to_top_middle_room = world.get_entrance("Overworld to Top Middle Room")
    #     can_smash_brick = Has("Hammer")
    #     world.set_rule(overworld_to_top_middle_room, can_smash_brick)

    # So far, we've been using "Has" from the Rule Builder to make our rules.
    # There is another way to make rules that you will see in a lot of older worlds.
    # A rule can just be a function that takes a "state" argument and returns a bool.
    # As a demonstration of what that looks like, let's do it with our final Entrance rule:
    # world.set_rule(overworld_to_top_left_room, lambda state: state.has("Key", world.player))
    # This style is not really recommended anymore, though.
    # Notice how you have to explicitly capture world.player here so that the rule applies to the correct player?
    # Well, Rule Builder does this part for you, inside of world.set_rule.
    # This doesn't just result in shorter code, it also means you can define rules statically (at the module level).
    # APQuest opts to create its Rule objects locally, but just to show what this would look like,
    # we'll re-set the "Overworld to Top Left Room" rule to a constant defined at the top of this file:
    # world.set_rule(overworld_to_top_left_room, HAS_KEY)

    # Beyond these structural advantages,
    # Rule Builder also allows the core AP code to do a lot of under-the-hood optimizations.
    # Rule Builder is quite comprehensive, and even if you have really esoteric rules,
    # you can make custom rules by subclassing CustomRule.

def set_all_location_rules(world: IslandRacerWorld) -> None:
    
    for island in IslandRacerWorld.ISLANDS:
        gold_loc = world.get_location(f"{island} Island - Gold Medal")
        world.set_rule(gold_loc, Has("Progressive Stats"), 2)

        platinum_loc = world.get_location(f"{island} Island - Platinum Medal")
        diamond_loc = world.get_location(f"{island} Island - Diamond Medal")

        world.set_rule(platinum_loc, Has("Progressive Stats"), 3)
        world.set_rule(diamond_loc, Has("Progressive Stats"), 3)
    

    tier_threshold = world.options.medal_tier_required.value
    qualifying_tiers = world.MEDAL_TIERS[tier_threshold:]

    for island in world.ISLANDS:
        world.set_rule(
            world.get_location(f"{island} Island Completed"),
            MedalTierReached(island)
        )
 


def set_completion_condition(world: IslandRacerWorld) -> None:
    # Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
    # For this, we can use world.set_completion_rule.


    # In our case, we went for the Victory event design pattern (see create_events() in locations.py).
    # So lets undo what we just did, and instead set the completion condition to:
    world.set_completion_rule(
    Has("Island Completed", count=world.options.islands_to_goal.value) )


# One final comment about rules:
# If your world exclusively uses Rule Builder rules (like APQuest), it's worth trying CachedRuleBuilderWorld.
# CachedRuleBuilderWorld is a subclass of World that has a bunch of caching magic to make rules faster.
# Just have your world class subclass CachedRuleBuilderWorld instead of World:
#   class APQuestWorld(CachedRuleBuilderWorld): ...
# This may speed up your world, or it may make it slower.
# The exact factors are complex and not well understood, but there is no harm in trying it.
# Generate a few seeds and see if there is a noticeable difference!
# If you're wondering, author has checked: APQuest is too simple to see any benefits, so we'll stick with "World".
