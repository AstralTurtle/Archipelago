from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
# class HardMode(Toggle):
#     """
#     In hard mode, the basic enemy and the final boss will have more health.
#     The Health Upgrades become progression, as they are now required to beat the final boss.
#     """

#     # The docstring of an option is used as the description on the website and in the template yaml.

#     # You'll also want to set a display name, which will determine what the option is called on the website.
#     display_name = "Hard Mode"

class DeathLink(Toggle):
    """When you die, everyone who enabled death link dies. Of course, the reverse is true too."""
    display_name = "Death Link"
    rich_text_doc = True

# A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
class IslandsToGoal(Range):
    """
    How many islands are required to beat the game.
    """

    display_name = "Islands to Goal"

    range_start = 0
    range_end = 5

    # Range options must define an explicit default value.
    default = 3


# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
class MedalTierRequired(Choice):
    """
    The tier of medals required to complete an island.
    """

    display_name = "Medal Tier Required"

    option_bronze = 0
    option_silver = 1
    option_gold= 2
    option_diamond = 3
    option_platinum = 4

    # Choice options must define an explicit default value.
    default = option_gold

    # For choices, you can also define aliases.
    # For example, we could make it so "player_sprite: kitty" resolves to "player_sprite: cat" like this:
    


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class IslandRacerOptions(PerGameCommonOptions):
    medal_tier_required: MedalTierRequired
    islands_to_goal: IslandsToGoal
    death_link: DeathLink


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Goal Options", [MedalTierRequired, IslandsToGoal]
    ),
    OptionGroup(
        "Death Link" ,[DeathLink]
    )
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "Easy": {
        "medal_tier_required": 2,
        "islands_to_goal": 3,
    },
    "Hard": {
        "medal_tier_required": 4,
        "islands_to_goal": 5,
    },
}
