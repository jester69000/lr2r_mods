#Use this class to define an MC serum trait type. MC Serum types will roughly mimic regular serum traits, but without as many variables, since we don't need to sell these.
#Each MC serum should be linked to an existing regular serum trait for research purposes.
#Each MC serum trait also has at least three different levels of effectives, based on their mastery and the category master level.
#MC Serum Traits can be declared in init python statements because their data is all calculated on the fly, so the list can be changed and fucked with as needed without destroying save games.
from __future__ import annotations
from game.main_character.perks.Perks_ren import perk_system
from game.major_game_classes.serum_related.SerumTrait_ren import SerumTrait, list_of_traits
from game.major_game_classes.character_related.Person_ren import mc, ashley
from game.people.Ashley.ashley_definition_ren import ashley_mc_submission_story_complete
from game.people.Ashley.ashley_role_definition_ren import ashley_get_mc_obedience
import renpy

list_of_mc_traits: list["MC_Serum_Trait"] = []
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""
class MC_Serum_Trait():
    def __init__(self, name, linked_trait, category, perk_list, perk_advance_reqs, upg_label, upg_string = None, on_apply = None, on_remove = None):
        self.name = name
        self.linked_trait = linked_trait
        self.category = category
        self.perk_list = perk_list
        self.perk_advance_reqs = perk_advance_reqs
        self.base_tier = 1
        self.is_selected = False
        self.upg_label = upg_label
        if upg_string is None:
            self.upg_string = "Unknown upgrade requirements."
        else:
            self.upg_string = upg_string
        self.on_apply = on_apply
        self.on_remove = on_remove

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: MC_Serum_Trait) -> bool:
        if not isinstance(other, MC_Serum_Trait):
            return NotImplemented
        return self.name == other.name

    def apply_trait(self):  #Apply this trait to MC
        perk_system.add_ability_perk(self.perk_list[self.trait_tier - 1](), self.name)
        if mc.business.prod_assistant == ashley and not ashley_mc_submission_story_complete():
            ashley.event_triggers_dict["mc_obedience"] = ashley_get_mc_obedience() + 1
        if self.on_apply is not None:
            self.on_apply()

    def remove_trait(self):
        if self.on_remove is not None:
            self.on_remove()
        perk_system.remove_perk(self.name)

    def menu_name(self):
        return self.name.replace('Serum: ', '')

    @property
    def trait_tier(self):   #Calculate the current tier
        calc_tier = self.base_tier
        dict_key = f"mc_serum_{self.category}_tier"    #Determine category tier
        calc_tier += mc.business.event_triggers_dict.get(dict_key, 0)
        return calc_tier

    @property
    def trait_description(self):   #Return text description
        return self.perk_list[self.trait_tier - 1]().description

    def get_side_effect_chance(self):
        base_side_effect_chance = 0
        if found := next((x for x in list_of_traits if x.name == self.linked_trait), None):
            base_side_effect_chance += max(found.mastery_level - 20, 0)
            base_side_effect_chance += get_mc_serum_category_side_effect_chance(self.category)
            base_side_effect_chance += get_mc_serum_duration_side_effect_chance()
        return base_side_effect_chance

    @property
    def is_unlocked(self): #Returns true of the category AND serum trait itself should be unlocked
        dict_key = f"mc_serum_{self.category}_unlocked"
        if mc.business.event_triggers_dict.get(dict_key, False):
            if found := next((x for x in list_of_traits if x.name == self.linked_trait), None):
                return found.researched
        return False

    @property
    def is_active(self):   #Returns true if this trait is currently active on MC.
        return perk_system.has_ability_perk(self.name)

    @property
    def is_available(self):     #Returns true of the serum is able to be used.
        if self.is_unlocked: #Determine if its unlocked first
            active_traits = 0
            for trait in [x for x in list_of_mc_traits if x.is_selected]:
                active_traits += 1
                if trait.category == self.category:   #Check and see if another trait in the same category is available.
                    return False
            if active_traits >= mc_serum_max_quantity():    #Check and see if we have hit the max possible active traits.
                return False
            return True
        return False

    @property
    def can_be_upgraded(self):    #Returns true if this trait is ready to be upgraded
        if self.base_tier > len(self.perk_advance_reqs):    #We are at max tier already
            return False
        if not self.is_unlocked:
            return False
        if self.perk_advance_reqs[self.base_tier - 1]():
            return True
        return False

    @property
    def is_upgraded(self):
        if self.base_tier > 1:
            return True
        return False

    def upgrade_with_string(self, the_person):   #fabricate a string to return if we are upgrading this trait, upgrade string accordingly.
        self.base_tier += 1
        if self.is_active:
            self.is_selected = False
        renpy.call(self.upg_label, the_person)
        return True

    def toggle_selected(self):
        if self.is_selected:
            self.is_selected = False
        elif self.is_available:
            self.is_selected = True

    @property
    def upgrade_info(self):
        if self.base_tier > 1:
            return "Fully Upgraded"
        return self.upg_string

def get_mc_serum_duration():
    return 6

def get_mc_serum_category_side_effect_chance(category):
    return 0

def get_mc_serum_duration_side_effect_chance():
    return 0

def get_production_serum(tier = 0):
    return next((x for x in list_of_traits if x.tier == tier and x.has_tag("Production") and isinstance(x, SerumTrait)), None)

# jes: added list for anatomical serum
def mc_anatomical_serum_unlocked():
    return True
    # return mc.business.event_triggers_dict.get("mc_serum_anatomical_unlocked", False)

def mc_energy_serum_unlocked():
    return mc.business.event_triggers_dict.get("mc_serum_energy_unlocked", False)

def mc_aura_serum_unlocked():
    return mc.business.event_triggers_dict.get("mc_serum_aura_unlocked", False)

def mc_cum_serum_unlocked():
    return mc.business.event_triggers_dict.get("mc_serum_cum_unlocked", False)

def mc_physical_serum_unlocked():
    return mc.business.event_triggers_dict.get("mc_serum_physical_unlocked", False)

# jes: added list for anatomical serum
def mc_serum_get_anatomical_list():
    return [x for x in list_of_mc_traits if x.category == "anatomical"]

def mc_serum_get_energy_list():
    return [x for x in list_of_mc_traits if x.category == "energy"]

def mc_serum_get_aura_list():
    return [x for x in list_of_mc_traits if x.category == "aura"]

def mc_serum_get_cum_list():
    return [x for x in list_of_mc_traits if x.category == "cum"]

def mc_serum_get_physical_list():
    return [x for x in list_of_mc_traits if x.category == "physical"]

def mc_serum_max_quantity():
    return mc.business.event_triggers_dict.get("mc_serum_max_quant", 1)

# jes: added list for anatomical serum
def mc_serum_anatomical_serum_is_active():
    return any(x for x in mc_serum_get_anatomical_list() if x.is_active)

def mc_serum_energy_serum_is_active():
    return any(x for x in mc_serum_get_energy_list() if x.is_active)

def mc_serum_aura_serum_is_active():
    return any(x for x in mc_serum_get_aura_list() if x.is_active)

def mc_serum_cum_serum_is_active():
    return any(x for x in mc_serum_get_cum_list() if x.is_active)

def mc_serum_physical_serum_is_active():
    return any(x for x in mc_serum_get_physical_list() if x.is_active)

def mc_serum_list_of_upgradable_serums():   #Rework this so we can upgrade active traits
    return [x for x in list_of_mc_traits if x.can_be_upgraded]
