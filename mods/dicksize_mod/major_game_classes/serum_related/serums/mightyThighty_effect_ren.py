from __future__ import annotations
import renpy
from game.bugfix_additions.SerumTraitMod_ren import SerumTraitMod
from game.major_game_classes.character_related.Person_ren import Person
from game.major_game_classes.serum_related.SerumDesign_ren import SerumDesign, SerumTrait

"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -1 python:
"""

def tighten_vagina_on_day(person: Person, serum: SerumDesign, add_to_log: bool):
    person.change_happiness(-5, add_to_log=add_to_log)
    if person.vagina_tightness > 1:
        person.vagina_tightness -= 1
        person.change_max_energy(-5, add_to_log = False)

SerumTraitMod(name = "Migthy Tighty Effect",
    desc = "Restores vagina tightness but drains energy",
    positive_slug = "Increases vagina tightness",
    negative_slug = "Permanently reduces energy",
    research_added = 500,
    production_added = 25,
    base_side_effect_chance = 100,
    on_day = tighten_vagina_on_day,
    tier = 2,
    start_researched = False,
    research_needed = 1200,
    clarity_cost = 1000,
    hidden_tag = "Physical",
    mental_aspect = 0, physical_aspect = 3, sexual_aspect = 3, medical_aspect = 1, flaws_aspect = 0, attention = 3,
    start_enabled = True)

