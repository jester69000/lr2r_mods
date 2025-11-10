from __future__ import annotations
import builtins
import copy
import inspect
from itertools import chain
import renpy
from typing import Callable, Iterable
from renpy import persistent
from renpy.character import Character
from renpy.color import Color
from renpy.display import im
from renpy.display.im import AlphaMask, Composite
from renpy.display.layout import Flatten
from renpy.text.text import Text
from game.game_loops.sexmechanic_code_ren import _character_position_filter
from game.random_lists_ren import build_generic_weighted_list, get_random_copy_from_named_list, get_random_from_weighted_list, index_in_weighted_list, is_in_weighted_list
from game.bugfix_additions.debug_info_ren import validate_texture_memory, write_log
from game.bugfix_additions.mapped_list_ren import generate_identifier
from game.helper_functions.character_display_functions_ren import clear_scene
from game.helper_functions.convert_to_string_ren import SO_relationship_to_title, capitalize_first_word, girl_relationship_to_title, opinion_score_to_string, remove_punctuation
from game.helper_functions.list_functions_ren import flatten_list, get_random_from_list
from game.helper_functions.misc_helpers_ren import darken_colour, lighten_colour
from game.helper_functions.play_sounds_ren import play_female_orgasm, play_spank_sound
from game.helper_functions.random_generation_functions_ren import make_person
from game.helper_functions.webcolors_usage_ren import closest_eye_color, closest_hair_colour
from game.general_actions.interaction_actions.chat_actions_definition_ren import sort_display_list
from game._image_definitions_ren import portrait_mask_image
from game.clothing_lists_ren import position_size_dict, hair_styles, pube_styles, braided_bun, messy_short_hair, shaved_side_hair, short_hair, windswept_hair, messy_ponytail, twintail, ponytail, long_hair, messy_hair, shaved_pubes, landing_strip_pubes, default_pubes, bald_hair, no_tan, white_skin, tan_skin, black_skin, bath_robe, apron
from game.main_character.perks.Perks_ren import perk_system
from game.main_character.mc_serums._mc_serum_definitions_ren import mc_serum_aura_obedience, mc_serum_aura_fertility
from game.main_character.MainCharacter_ren import mc
from game.map.map_code_ren import list_of_hubs
from game.map.MapHub_ren import MapHub, home_hub, office_hub, strip_club_hub, harem_hub, aunt_home_hub, university_hub, gym_hub
from game.map.HomeHub_ren import HomeHub, residential_home_hub, industrial_home_hub, downtown_home_hub, university_home_hub
from game.game_roles._role_definitions_ren import Role, mother_role, sister_role, girlfriend_role, harem_role, affair_role, generic_student_role, instapic_role, dikdok_role, onlyfans_role, trance_role, heavy_trance_role, very_heavy_trance_role, slave_role, caged_role, anal_fetish_role, cum_fetish_role, breeding_fetish_role, exhibition_fetish_role, jealous_sister_role, jealous_act_get_score, drunk_role
from game.game_roles.role_pregnant_definition_ren import become_pregnant, pregnant_role
from game.game_roles.stripclub._stripclub_role_definitions_ren import strip_club_is_closed
from game.game_roles.business_roles._business_role_definitions_ren import employee_role, college_intern_role, clone_role, employee_freeuse_role
from game.game_roles.business_roles._duty_definitions_ren import work_for_tips_duty
from game.sex_positions._position_definitions_ren import kissing, spanking
from game.business_policies.clothing_policies_ren import strict_uniform_policy, casual_friday_uniform_policy, dress_code_policy, creative_colored_uniform_policy
from game.business_policies.organisation_policies_ren import office_punishment
from game.business_policies.special_policies_ren import genetic_manipulation_policy
from game.personality_types._personality_definitions_ren import relaxed_personality, alpha_personality
from game.major_game_classes.clothing_related.Expression_ren import Expression
from game.major_game_classes.clothing_related.zip_manager_ren import emotion_images_dict
from game.major_game_classes.business_related.Infraction_ren import Infraction
from game.major_game_classes.serum_related.SerumDesign_ren import SerumDesign
from game.major_game_classes.serum_related.serums._serum_traits_T1_ren import antidote_trait
from game.major_game_classes.serum_related.serums.fetish_serums_ren import start_anal_fetish_quest, start_cum_fetish_quest, start_breeding_fetish_quest
from game.major_game_classes.game_logic.Action_ren import Action, Limited_Time_Action
from game.major_game_classes.game_logic.ActionList_ren import ActionList
from game.major_game_classes.game_logic.Duty_ren import Duty
from game.major_game_classes.game_logic.Position_ren import Position
from game.major_game_classes.game_logic.Room_ren import Room, list_of_places, lily_bedroom, mom_bedroom, aunt_bedroom, cousin_bedroom, strip_club, bdsm_room, prostitute_bedroom, generic_bedroom_1, generic_bedroom_2, generic_bedroom_3, generic_bedroom_4, gym, gym_shower, her_hallway, purgatory, dungeon, clone_facility, downtown_bar, standard_indoor_lighting, mom_office_lobby, mom_offices
from game.major_game_classes.game_logic.RoomObject_factories_ren import make_wall, make_floor, make_couch, make_window
from game.major_game_classes.character_related.scene_manager_ren import Scene
from game.major_game_classes.character_related.configuration.opinion_lists_ren import init_list_of_opinions, init_list_of_sexy_opinions
from game.major_game_classes.character_related.configuration.other_character_configs_ren import init_list_of_eyes, init_list_of_faces, init_list_of_hairs
from game.major_game_classes.character_related.Opinion_ren import Opinion
from game.major_game_classes.character_related.Progression_ren import Progression
from game.major_game_classes.character_related.Personality_ren import Personality, list_of_personalities
from game.major_game_classes.character_related.Schedule_ren import Schedule
from game.major_game_classes.character_related.configuration.character_name_lists_ren import init_list_of_last_names, init_list_of_male_names, init_list_of_names
from game.major_game_classes.character_related._job_definitions_ren import JobDefinition, university_professor_job, student_job, doctor_job, waitress_job, unemployed_job, stripper_job, stripclub_stripper_job, stripclub_bdsm_performer_job, stripclub_mistress_job, stripclub_waitress_job, stripclub_manager_job, prostitute_job, secretary_job, office_worker_job, lawyer_job, architect_job, interior_decorator_job, fashion_designer_job
from game.major_game_classes.character_related.ActiveJob_ren import ActiveJob
from game.major_game_classes.character_related.Story_ren import Story_Tracker
from game.major_game_classes.clothing_related.Clothing_ren import Clothing
from game.major_game_classes.character_related.Relationship_ren import RelationshipArray
from game.major_game_classes.clothing_related.outfit_selector_ren import outfit_queue
from game.major_game_classes.clothing_related.Outfit_ren import Outfit
from game.major_game_classes.clothing_related.Wardrobe_ren import Wardrobe, lingerie_wardrobe
from game.major_game_classes.clothing_related.wardrobe_builder_ren import WardrobeBuilder, panties_list, real_bra_list, thong, tiny_g_string, strappy_panties, string_panties, crotchless_panties, lace_bra, thin_bra, strappy_bra, quarter_cup_bustier
from game.major_game_classes.clothing_related.wardrobe_preferences_ren import WardrobePreference
from game.major_game_classes.clothing_related.LimitedWardrobeCollection_ren import limited_wardrobes
from game.people.Sarah.sarah_definition_ren import sarah_threesomes_unlocked
from game.people.Nora.nora_definition_ren import nora_professor_job
from game.people.Lily.lily_definition_ren import sister_student_job

GAME_SPEED = 1
TIER_1_TIME_DELAY = 5
TIER_2_TIME_DELAY = 12
TIER_3_TIME_DELAY = 20

global report_log
report_log: dict[str, int]
list_of_people: list[Person] = []
list_of_patreon_characters: list[Person] = []
list_of_instantiation_functions: list[Callable[[], None]]
tan_images_dict: dict[str, Clothing] = {}
body_images_dict: dict[str, Clothing] = {}

cousin: Person
lily: Person
aunt: Person
mom: Person
stephanie: Person
emily: Person
christina: Person
nora: Person
erica: Person
police_chief: Person
sarah: Person
naomi: Person
alexia: Person
ashley: Person
candace: Person
salon_manager: Person
starbuck: Person
camila: Person
kaya: Person
sakari: Person
ellie: Person
myra: Person
city_rep: Person
iris: Person

day = 0
time_of_day = 0
town_relationships = RelationshipArray()

character_right = None
clothing_fade = None
fast_clothing_fade = None

# proxy methods for type system

def make_character_unique(person: Person, home_hub: HomeHub) -> bool:
    return True
def scale_person(x):
    return x
def basic_bounce(x):
    return x

"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""
import time
from collections import defaultdict
from functools import cached_property
from pylru import LRUCache # type: ignore

###################################
# Person object caching functions #
###################################

# cache the last 15 generated displayables
character_cache = LRUCache(15)
portrait_cache = LRUCache(20)

class Person(): #Everything that needs to be known about a person.
    #Define "private" range limits, use static/class methods to retrieve from the Person class
    _final_stat_floor = 0
    _initial_stat_floor = 1
    _initial_stat_ceiling = 5

    _final_skill_floor = 0
    _initial_skill_floor = 1
    _initial_skill_ceiling = 5

    _final_sex_skill_floor = 0
    _initial_sex_skill_floor = 1
    _initial_sex_skill_ceiling = 5

    _final_happiness_floor = 0
    _initial_happiness_floor = 90
    _initial_happiness_ceiling = 110

    _initial_suggestibility_floor = 0
    _initial_suggestibility_ceiling = 15

    _initial_sluttiness_floor = 0
    _initial_sluttiness_ceiling = 10

    _final_love_floor = -100
    _initial_love_floor = 0
    _initial_love_ceiling = 0
    _final_love_ceiling = 100

    _final_obedience_floor = 0
    _initial_obedience_floor = 90
    _initial_obedience_ceiling = 110

    _final_work_experience_floor = 1
    _initial_work_experience_floor = 1
    _initial_work_experience_ceiling = 2
    _final_work_experience_ceiling = 5

    _initial_age_floor = 18
    _initial_age_ceiling = 50
    _final_age_floor = 18
    _final_age_ceiling = 60
    _teen_age_ceiling = 19
    _old_age_floor = 40

    _height_step = 0.015 #1 inch
    _initial_height_floor =   ((5 * 12) +  0) * _height_step #5'  0" # noqa: E222
    _initial_height_ceiling = ((5 * 12) + 10) * _height_step #5' 10" # noqa: E222
    _final_height_floor =     ((4 * 12) +  0) * _height_step #4'  0" # noqa: E222
    _final_height_ceiling =   ((7 * 12) +  0) * _height_step #7'  0" # noqa: E222
    _short_height_ceiling =   ((5 * 12) +  3) * _height_step #5'  3" # noqa: E222
    _tall_height_floor =      ((5 * 12) +  9) * _height_step #5'  9" # noqa: E222

    _base_list_of_relationships = [
        ["Single", 120],
        ["Girlfriend", 50],
        ["Fiancée", 20],
        ["Married", 10]
    ]

    _large_tit_minimum = "D"
    _huge_tit_minimum = "E"
    _small_tit_maximum = "C"
    _tiny_tit_maximum = "AA"

    ###jes:Add vagina_tightness limits
    _tightness_floor = 0
    _tightness_ceiling = 7

    _list_of_names = init_list_of_names()
    _list_of_last_names = init_list_of_last_names()
    _list_of_male_names = init_list_of_male_names()

    _coffee_list = [
        "just black",
        "just a little sugar",
        "one sugar",
        "two sugar",
        "lots of sugar",
        "just a splash of cream",
        "just some cream",
        "lots of cream",
        "cream and sugar"
    ]

    #These are "ideal" hair colours. Individuals will have minor variations applied to them so that different "blonds" have slightly different hair.
    _list_of_hairs = init_list_of_hairs()

    _list_of_skins: list[tuple[str, int]] = [
        ("white", 5),
        ("black", 1),
        ("tan", 2)
    ]

    _list_of_faces = init_list_of_faces() # Only character critical faces are included in all versions.

    _list_of_eyes = init_list_of_eyes()

    _list_of_tits: list[tuple[str, int]] = [
        ("AA", 5),
        ("A", 15),
        ("B", 30),
        ("C", 30),
        ("D", 15),
        ("DD", 10),
        ("DDD", 5),
        ("E", 2),
        ("F", 1),
        ("FF", 1),
    ]

    _list_of_clothing_colours: list[tuple[float, float, float, float]] = [
        (0.15, 0.15, 0.15, 0.95),   #Black
        (1.0, 1.0, 1.0, 0.95),      #White
        (0.7, 0.4, 0.4, 0.95),      #Light Pink
        (0.4, 0.7, 0.4, 0.95),      #Light blue
        (0.4, 0.4, 0.7, 0.95),      #Light green
        (0.31, 0.23, 0.33, 0.95),   #Purple
        (0.9, 0.5, 0.1, 0.95)       #Orange
    ]

    _list_of_body_types: list[str] = ["thin_body", "standard_body", "curvy_body"]

    _record_skill_map = {
        "Handjobs": "Foreplay",
        "Kissing": "Foreplay",
        "Fingered": "Foreplay",
        "Tit Fucks": "Foreplay",
        "Blowjobs": "Oral",
        "Cunnilingus": "Oral",
        "Vaginal Sex": "Vaginal",
        "Anal Sex": "Anal",
        "Spankings": "Foreplay",
        "Insertions": "Foreplay",
    }

    _record_opinion_map = {
        "Handjobs": ["giving handjobs", "sex standing up"],
        "Kissing": ["kissing"],
        "Fingered": ["masturbating", "being fingered", "sex standing up"],
        "Tit Fucks": ["giving tit fucks", "showing her tits"],
        "Blowjobs": ["giving blowjobs"],
        "Cunnilingus": ["getting head"],
        "Vaginal Sex": ["vaginal sex", "missionary style sex", "lingerie"],
        "Anal Sex": ["anal sex", "doggy style sex", "bareback sex"],
        "Cum Facials": ["cum facials"],
        "Cum in Mouth": ["drinking cum"],
        "Cum Covered": ["being covered in cum"],
        "Vaginal Creampies": ["creampies"],
        "Anal Creampies": ["anal creampies"],
        "Threesomes": ["not wearing anything", "skimpy outfits", "skimpy uniforms"],
        "Spankings": ["not wearing underwear", "showing her ass"],
        "Insertions": ["big dicks", "public sex", "sex standing up"],
    }

    # A master list of things a character might like or dislike.
    # Should always be named so it fits the framework "Likes X" or "Dislikes X".
    # Personalities have a unique list that they always draw from as well
    _opinions_list = init_list_of_opinions()

    #Another list of opinions, but these ones are sex/kink related and
    # probably shouldn't be brought up in polite conversation.
    _sexy_opinions_list = init_list_of_sexy_opinions()

    @classmethod
    def get_random_tit(cls, start: int | None = None, end: int | None = None) -> str:
        if not start:
            start = 0
        else:
            start = cls.get_tit_index(start)
        if not end:
            end = len(cls._list_of_tits)
        else:
            end = cls.get_tit_index(end) + 1
        return get_random_from_weighted_list(build_generic_weighted_list("Cup Size", start, end))

    @classmethod
    def get_tit_weighted_list(cls, start=None, end=None):
        if not start:
            start = 0
        else:
            start = cls.get_tit_index(start)
        if not end:
            end = len(cls._list_of_tits)
        else:
            end = cls.get_tit_index(end) + 1
        return cls._list_of_tits[start:end]

    @classmethod
    def get_maximum_tit(cls):
        return get_random_from_weighted_list(cls._list_of_tits[-1:])

    @classmethod
    def get_tit_index(cls, current_tits) -> int:
        return index_in_weighted_list(current_tits, cls._list_of_tits)

    @classmethod
    def rank_tits(cls, the_tits) -> int: #Useful if you need to know exactly who has larger tits and want to compare ints. Also see Person.has_large_tits, for a flat definition of large tits as D or larger
        #Mostly an alias for get_tit_index but defaults to 0 (which is undesirable for a function that may be as like setting a maximum as a minimum)
        try:
            return cls.get_tit_index(the_tits)
        except UnboundLocalError:
            return 0

    @classmethod
    def get_smaller_tit(cls, current_tit) -> str:
        current_index = cls.get_tit_index(current_tit)
        return cls._list_of_tits[builtins.max(0, current_index - 1)][0]

    @classmethod
    def get_larger_tit(cls, current_tit) -> str:
        current_index = cls.get_tit_index(current_tit)
        return cls._list_of_tits[builtins.min(current_index + 1, len(cls._list_of_tits) - 1)][0]

    @classmethod
    def get_random_tiny_tit(cls) -> str:
        return cls.get_random_tit(end = cls.get_tit_index(cls._tiny_tit_maximum))

    @classmethod
    def get_random_small_tit(cls) -> str:
        return cls.get_random_tit(end = cls.get_tit_index(cls._small_tit_maximum))

    @classmethod
    def get_random_large_tit(cls) -> str:
        return cls.get_random_tit(start = cls.get_tit_index(cls._large_tit_minimum))

    @classmethod
    def get_random_huge_tit(cls) -> str:
        return cls.get_random_tit(start = cls.get_tit_index(cls._huge_tit_minimum))

    @classmethod
    def get_maximum_tiny_tit(cls) -> str:
        return cls._tiny_tit_maximum

    @classmethod
    def get_maximum_small_tit(cls) -> str:
        return cls._small_tit_maximum

    @classmethod
    def get_minimum_large_tit(cls) -> str:
        return cls._large_tit_minimum

    @classmethod
    def get_minimum_huge_tit(cls) -> str:
        return cls._huge_tit_minimum

    @classmethod
    def get_tiny_tits_weighted_list(cls):
        return cls.get_tit_weighted_list(end=cls._tiny_tit_maximum)

    @classmethod
    def get_small_tits_weighted_list(cls):
        return cls.get_tit_weighted_list(end=cls._small_tit_maximum)

    @classmethod
    def get_large_tits_weighted_list(cls):
        return cls.get_tit_weighted_list(start=cls._large_tit_minimum)

    @classmethod
    def get_huge_tits_weighted_list(cls):
        return cls.get_tit_weighted_list(start=cls._huge_tit_minimum)

    @staticmethod
    def tit_is_in_weighted_tits_list(tit, weighted_tit_list):
        return is_in_weighted_list(tit, weighted_tit_list)

    @classmethod
    def tit_is_tiny(cls, tit) -> bool:
        return cls.tit_is_in_weighted_tits_list(tit, cls.get_tiny_tits_weighted_list())

    @classmethod
    def tit_is_small(cls, tit) -> bool:
        return cls.tit_is_in_weighted_tits_list(tit, cls.get_small_tits_weighted_list())

    @classmethod
    def tit_is_large(cls, tit) -> bool:
        return cls.tit_is_in_weighted_tits_list(tit, cls.get_large_tits_weighted_list())

    @classmethod
    def tit_is_huge(cls, tit) -> bool:
        return cls.tit_is_in_weighted_tits_list(tit, cls.get_huge_tits_weighted_list())

    @classmethod
    def get_random_skin(cls) -> str:
        return get_random_from_weighted_list(build_generic_weighted_list("Skin Colour"))

    @classmethod
    def get_random_hair_colour(cls):
        return get_random_from_list(cls._list_of_hairs)

    @staticmethod
    def get_darkened_colour(the_colour, variation_constant = 0.07):
        return_list = the_colour[:]
        for component_index in builtins.range(3): #In case there's an alpha component, we don't want to change that.
            return_list[component_index] = return_list[component_index] * (1 - variation_constant)

        return return_list

    @classmethod
    def generate_hair_colour(cls, base_colour: str = None, create_variation = True) -> tuple[str, list[float]]:
        return_hair = None

        if base_colour:
            hair = next((x for x in cls.get_list_of_hairs() if x[0] == base_colour), None)
            if hair:
                return_hair = copy.deepcopy(hair)

        if not return_hair:
            return_hair = copy.deepcopy(cls.get_random_hair_colour()) #Deep copy the hair colours because lists are passed by reference and it is two lists deep.

        if return_hair and create_variation:
            #The colour is modified slightly to give different characters slightly different hair colours.
            if (sum(return_hair[1][:3]) / 3) > 0.6:
                return (return_hair[0], list(darken_colour(return_hair[1], renpy.random.random() * .05).rgba))
            else:
                return (return_hair[0], list(lighten_colour(return_hair[1], renpy.random.random() * .05).rgba))

        # add light opacity to better blend with character
        return_hair[1][3] = .95
        return return_hair

    @classmethod
    def get_random_eye(cls) -> tuple[str, list[float]]:
        return get_random_from_list(cls._list_of_eyes)

    @classmethod
    def generate_eye_colour(cls, base_colour: str = None, create_variation = True) -> tuple[str, list[float]]:
        return_eyes = None
        if base_colour:
            for eyes in cls.get_list_of_eyes():
                if eyes[0] == base_colour: #If we ask for a specific base...
                    return_eyes = copy.deepcopy(eyes)

        if not return_eyes: #Otherwise just get a random one
            return_eyes = copy.deepcopy(cls.get_random_eye()) #Deep copy the hair colours because lists are passed by reference and it is two lists deep.

        if return_eyes and create_variation:
            #The colour is modified slightly to give different characters slightly different eye colours.
            if (sum(return_eyes[1][:3]) / 3) > 0.6:
                return (return_eyes[0], list(darken_colour(return_eyes[1], renpy.random.random() * .02).rgba))
            else:
                return (return_eyes[0], list(lighten_colour(return_eyes[1], renpy.random.random() * .02).rgba))

        return return_eyes  # return random selection

    @classmethod
    def get_random_hair_style(cls) -> Clothing:
        return get_random_copy_from_named_list(build_generic_weighted_list("Hair Style"), hair_styles)

    @classmethod
    def get_random_pubes_style(cls) -> Clothing:
        return get_random_copy_from_named_list(build_generic_weighted_list("Pubes Style"), pube_styles)

    @classmethod
    def get_random_face(cls) -> str:
        return get_random_from_list(cls._list_of_faces)

    @classmethod
    def get_random_name(cls) -> str:
        names = [person.name for person in list_of_people]
        return renpy.random.choice(list(set(cls._list_of_names) - set(names)))

    @classmethod
    def get_random_last_name(cls) -> str:
        names = [person.last_name for person in list_of_people]
        return renpy.random.choice(list(set(cls._list_of_last_names) - set(names)))

    @classmethod
    def get_random_male_name(cls) -> str:
        return get_random_from_list(cls._list_of_male_names)

    @classmethod
    def get_random_glasses_frame_colour(cls) -> tuple[float, float, float, float]:
        # Picks one of several mostly-neutral colours that should go well with most items
        return get_random_from_list(cls._list_of_clothing_colours)

    @classmethod
    def get_random_body_type(cls) -> str:
        return get_random_from_weighted_list(build_generic_weighted_list("Body Type"))

    @classmethod
    def get_normal_opinions_list(cls) -> list[str]:
        return cls._opinions_list[:]

    @classmethod
    def get_sexy_opinions_list(cls) -> list[str]:
        return cls._sexy_opinions_list[:]

    @classmethod
    def get_random_normal_opinion(cls) -> str:
        return get_random_from_list(cls._opinions_list)

    @classmethod
    def get_random_sexy_opinion(cls) -> str:
        return get_random_from_list(cls._sexy_opinions_list)

    @classmethod
    def get_random_coffee_style(cls) -> str:
        return get_random_from_list(cls._coffee_list)

    @classmethod
    def get_list_of_hairs(cls) -> list[tuple[str, list[float]]]:
        return copy.deepcopy(cls._list_of_hairs) #Return a deepcopy so that original list and it's content is immutable

    @classmethod
    def get_list_of_eyes(cls) -> list[tuple[str, list[float]]]:
        return copy.deepcopy(cls._list_of_eyes) #Return a deepcopy so that original list and it's content is immutable

    @classmethod
    def get_stat_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_stat_floor
        return cls._final_stat_floor

    @classmethod
    def get_skill_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_skill_floor
        return cls._final_skill_floor

    @classmethod
    def get_sex_skill_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_sex_skill_floor
        return cls._final_sex_skill_floor

    @classmethod
    def get_stat_ceiling(cls) -> int:
        return cls._initial_stat_ceiling

    @classmethod
    def get_skill_ceiling(cls) -> int:
        return cls._initial_skill_ceiling

    @classmethod
    def get_sex_skill_ceiling(cls) -> int:
        return cls._initial_sex_skill_ceiling

    @classmethod
    def get_happiness_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_happiness_floor
        return cls._final_happiness_floor

    @classmethod
    def get_happiness_ceiling(cls) -> int:
        return cls._initial_happiness_ceiling

    @classmethod
    def get_suggestibility_floor(cls) -> int:
        return cls._initial_suggestibility_floor

    @classmethod
    def get_suggestibility_ceiling(cls) -> int:
        return cls._initial_suggestibility_ceiling

    @classmethod
    def get_sluttiness_floor(cls) -> int:
        return cls._initial_sluttiness_floor

    @classmethod
    def get_sluttiness_ceiling(cls) -> int:
        return cls._initial_sluttiness_ceiling

    @classmethod
    def get_love_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_love_floor
        return cls._final_love_floor

    @classmethod
    def get_love_ceiling(cls, initial=True) -> int:
        if initial:
            return cls._initial_love_ceiling
        return cls._final_love_ceiling

    @classmethod
    def get_obedience_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_obedience_floor
        return cls._final_obedience_floor

    @classmethod
    def get_obedience_ceiling(cls) -> int:
        return cls._initial_obedience_ceiling

    @classmethod
    def get_work_experience_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_work_experience_floor
        return cls._final_work_experience_floor

    @classmethod
    def get_work_experience_ceiling(cls, initial=True) -> int:
        if initial:
            return cls._initial_work_experience_ceiling
        return cls._final_work_experience_ceiling

    @classmethod
    def get_age_floor(cls, initial=True) -> int:
        if initial:
            return cls._initial_age_floor
        return cls._final_age_floor

    @classmethod
    def get_age_ceiling(cls, initial=True) -> int:
        if initial:
            return cls._initial_age_ceiling
        return cls._final_age_ceiling

    @classmethod
    def get_height_floor(cls, initial=True) -> float:
        if initial:
            return cls._initial_height_floor
        return cls._final_height_floor

    @classmethod
    def get_height_ceiling(cls, initial=True) -> float:
        if initial:
            return cls._initial_height_ceiling
        return cls._final_height_ceiling

    @classmethod
    def get_old_age_floor(cls) -> int:
        return cls._old_age_floor

    @classmethod
    def get_teen_age_ceiling(cls) -> int:
        return cls._teen_age_ceiling

    @classmethod
    def get_tall_height_floor(cls) -> float:
        return cls._tall_height_floor

    @classmethod
    def get_short_height_ceiling(cls) -> float:
        return cls._short_height_ceiling

    @classmethod
    def get_height_step(cls) -> float:
        return cls._height_step

    @staticmethod
    def get_person_by_identifier(identifier: int) -> Person:
        return next((x for x in list_of_people if x.identifier == identifier), None)

    @staticmethod
    def get_initial_kids_range(age_range, relationships_array) -> list[int]:
        kids_range = [-1, 4]
        if age_range[0] < 20:
            kids_range[1] -= 2 #Reduce chance of teen pregnancy

        if age_range[0] > 22:
            kids_range[0] += 1 #Young people have less time to have kids in general, so modify their number down a bit.
            kids_range[1] += 1

        if age_range[1] < 28:
            kids_range[1] -= 1 #Young characters don't have as many kids

        if age_range[1] < 38:
            kids_range[1] -= 1 #As you get older you're more likely to have one

        if not (is_in_weighted_list("Fiancée", relationships_array) or is_in_weighted_list("Married", relationships_array)):
            kids_range[1] -= 1 #People who are in a stable relationship have more kids

        if not is_in_weighted_list("Married", relationships_array):
            kids_range[1] -= 2 #And married people have more kids still

        return kids_range

    @classmethod
    def get_potential_relationships_list(cls):
        return copy.deepcopy(cls._base_list_of_relationships)

    #Tighten kid range now that true age is known ?
    @classmethod
    def finalize_kids_range(cls, kids_range, age_range, relationships_list, age, relationship) -> list[int]:
        if (age_range is None or age_range[0] <= 22) and age > 22:
            kids_range[0] += 1 #Young people have less time to have kids in general, so modify their number down a bit.
            kids_range[1] += 1
        if (age_range is None or age_range[1] >= 28) and age < 28:
            kids_range[1] -= 1 #Young characters don't have as many kids
        if (age_range is None or age_range[1] >= 38) and age < 38:
            kids_range[1] -= 1 #Young characters don't have as many kids
        if relationships_list is None or (is_in_weighted_list("Fiancée", relationships_list) or is_in_weighted_list("Married", relationships_list)):
            if relationship not in ("Fiancée", "Married"):
                kids_range[1] -= 1 #People who are in a stable relationship have kids more often than single people
        if relationships_list is None or (is_in_weighted_list("Fiancée", relationships_list) or is_in_weighted_list("Married", relationships_list)):
            if relationship not in ("Married",):
                kids_range[1] -= 2 #People who married have kids more often than single people
        kids_range[0] = max(kids_range[0], 0)
        kids_range[1] = max(kids_range[1], 0)
        if kids_range[0] > kids_range[1]:
            return [kids_range[1], kids_range[0]]
        return kids_range

    @classmethod
    def finalize_relationships_weight(cls, relationships_list, age):
        for relationship in relationships_list:
            if relationship[0] == "Single":
                relationship[1] -= age
            if relationship[0] == "Girlfriend":
                relationship[1] += age
            if relationship[0] == "Fiancée":
                relationship[1] += 2 * age
            if relationship[0] == "Married":
                relationship[1] += 3 * age
        return relationships_list

    def __init__(self, name: str, last_name: str, age: int, body_type: str, tits: str, height: float,
            hair_colour: str | tuple[str, list[float]], hair_style: Clothing, pubes_style: Clothing, skin: str, eyes,
            job: JobDefinition, wardrobe: Wardrobe | None, personality: Personality,
            stat_list: list[int], skill_list: list[int],
            sluttiness: int = 0, obedience: int = 100, suggest: int = 0, sex_skill_list: list[int] | None = None,
            vagina_tightness: int = None, ###jes:Added vagina_tightness
            love: int = 0, happiness: int = 100, home: Room | None = None,
            font = "fonts/Avara.tff", name_color = "#ffffff", dialogue_color = "#ffffff",
            face_style = "Face_1", tan_style: str = None, serum_tolerance = 2,
            special_role: list[Role] | Role | None = None,
            title: str | None = None, possessive_title: str | None = None, mc_title: str | None = None,
            relationship: str | None = None, SO_name: str | None = None, kids: int | None = None, base_outfit: Outfit | None = None,
            generate_insta = False, generate_dikdok = False, generate_onlyfans = False, coffee_style: str | None = None,
            work_experience = 1, type = "random"):

        self.type = type
        self.func_name = name.lower() # used for calling dynamic functions

        #Using char instead of a string lets us customize the font and colour we are using for the character.
        self.char = Character("???", #The name to be displayed above the dialogue.
            what_font = font, #The font to be used for the character.
            who_font = font,
            color = name_color, #The colour of the character's NAME section
            what_color = dialogue_color, #The colour of the character's dialogue.
            what_style = "general_dialogue_style") #Used to describe everything that isn't character specific.

        ## Personality stuff, name, etc. Non-physical stuff.
        self.name = name
        self.last_name = last_name
        ## Physical things.
        self.age = age
        self.body_type = body_type
        self.tits = tits
        self.height = height
        self.face_style = face_style
        self.what_font = font
        self.who_font = font
        self.what_color = dialogue_color

        self.event_triggers_dict = {} #A dict used to store extra parameters used by events, like how many days has it been since a performance review.

        self.identifier: int = generate_identifier((name, last_name, age))
        self.available = True

        self._location: int = None
        self._home: int = None

        self._follow_mc = False
        self._baby_desire = 0   #Set to 0, but with negative modifiers on realistic settings. Mostly used only on realistic setting
        self._birth_control = True

        self.set_title("???")
        if title is not None:
            self.set_title(title)

        self.set_possessive_title("the unknown woman")  #The way the girl is referred to in relation to you. For example "your sister", "your head researcher", or just their title again.
        if possessive_title is not None:
            self.set_possessive_title(possessive_title)

        self.set_mc_title("Stranger")
        if mc_title is not None:
            self.set_mc_title(mc_title)     #What they call the main character, i.e. "first name", "Mr.last name", "master", "sir".

        self.schedule = Schedule()
        self.override_schedule = Schedule() #The mandatory place a person will go EVEN if they have work (useful for giving days off or requiring weekend work)

        if home:
            self._set_home(home)
            self.set_schedule(self.home, time_slots = [0, 4])

        # Relationship and family stuff
        if relationship:
            self.relationship = relationship
        else:
            self.relationship = "Single" #Should be Single, Girlfriend, Fiancée, or Married.

        if SO_name:
            self.SO_name = SO_name
        else:
            self.SO_name = None #If not single, name of their SO (for guilt purposes or future events).

        if kids:
            self.kids = kids
        else:
            self.kids = 0

        self.personality = personality

        # Loves, likes, dislikes, and hates determine some reactions in conversations, options, etc. Some are just fluff.
        self.opinions: dict[str, list[int, bool]] = {} #Key is the name of the opinion (see random list), value is a list holding [value, known]. Value ranges from -2 to 2 going from hate to love (things not on the list are assumed 0). Known is a bool saying if the player knows about their opinion.
        self.sexy_opinions: dict[str, list[int, bool]] = {}

        self.text_modifiers: list[Callable[[Person, str], str]] = [] #A list of functions, each of which take Person, String and return a modified String. Used to modify text to dynamically highlight words, or reflect a speech difference.

        self.pubes_colour = None

        self.hair_style = hair_style
        if pubes_style is None:
            self.pubes_style = self.get_random_pubes_style() #An empty image place holder so we can always call on them to draw.
        else:
            self.pubes_style = pubes_style.get_copy()

        self.hair_colour: tuple[str, list[float]] = None
        self.set_hair_colour(Color(rgb=(hair_colour[1][0], hair_colour[1][1], hair_colour[1][2]), alpha = hair_colour[1][3]))

        self.skin = skin
        self.tan = tan_style
        if self.tan is None:
            self.tan = "No Tan"

        self.eyes: tuple[str, list[float]] = None
        self.set_eye_colour(Color(rgb=(eyes[1][0], eyes[1][1], eyes[1][2]), alpha = eyes[1][3]))

        self._serum_tolerance = serum_tolerance      #How many active serums this person can tolerate before they start to suffer negative effects.
        self.serum_effects: list[SerumDesign] = []  #A list of all of the serums we are under the effect of.
        self.total_serum_count = 0                  #Track how many serums have been give to this person

        self.base_role = Role(self.func_name, hidden = True)
        self.special_role: list[Role] = [self.base_role]
        if isinstance(special_role, Role):
            self.special_role.append(special_role) #Support handing a non-list special role, in case we forget to wrap it in a list one day.
        elif isinstance(special_role, list):
            self.special_role.extend(special_role) #Otherwise we've handed it a list

        self.on_room_enter_event_list = ActionList() #Checked when you enter a room with this character. If an event is in this list and enabled it is run (and no other event is until the room is re-entered)
        self.on_talk_event_list = ActionList() #Checked when you start to interact with a character. If an event is in this list and enabled it is run (and no other event is until you talk to the character again.)\

        ##Mental stats##
        #Mental stats are generally fixed and cannot be changed permanently. Ranges from 1 to 5 at start, can go up or down (min 0)
        self.charisma = stat_list[0] #How likeable the person is. Mainly influences marketing, also determines how well interactions with other characters go. Main stat for HR and sales
        self.int = stat_list[1] #How smart the person is. Mainly influences research, small bonuses to most tasks. #Main stat for research and production.
        self.focus = stat_list[2] #How on task the person stays. Influences most tasks slightly. #Main stat for supplies

        self.charisma_debt = 0 #Tracks how far into the negative a characters stats are, for the purposes of serum effects. Effective stats are never lower than 0.
        self.int_debt = 0
        self.focus_debt = 0

        ##Work Skills##
        #Skills can be trained up over time, but are limited by your raw stats. Ranges from 1 to 5 at start, can go up or down (min 0)
        self.hr_skill = skill_list[0]
        self.market_skill = skill_list[1]
        self.research_skill = skill_list[2]
        self.production_skill = skill_list[3]
        self.supply_skill = skill_list[4]

        self.max_energy = 100
        self.energy = self.max_energy

        self.salary_modifier = 1.0 # Set by events for what this character considers "fair" for their skill, and/or reflects what they were promised.
        self.productivity_adjustment = 1.0 # Set by events for what this character is actually able to produce. Generally a "hidden" stat that you can't change.

        self.work_experience = work_experience # How experienced with work in general this girl is. The higher it is the more money a girl will want, but the more duties she can handle.
        self.primary_job: ActiveJob = None
        self.side_job: ActiveJob = None         # special job that overrides primary job schedule (like kaya working in cafe or erica training in gym)
        self.secondary_job: ActiveJob = None    # special job that fills gaps in primary and side-job schedules (moonlighting -> like stripping during off-hours or intern at office)

        self._idle_pose: str = get_random_from_list(["stand2", "stand3", "stand4", "stand5"]) #Get a random idle pose that you will use while people are talking to you.

        ##Personality Stats##
        #Things like suggestibility, that change over the course of the game when the player interacts with the girl
        self.suggestibility = 0 + suggest #How likely a girl is to enter or deepen a trance when orgasming
        self.suggest_bag = [] #This will store a list of integers which are the different suggestion values fighting for control. Only the highest is used, maintained when serums are added and removed.
        self.event_triggers_dict["mod_suggest_amt"] = suggest   # store her base suggest as modded amount since it can't go over 30%

        self.happiness = happiness #Higher happiness makes a girl less likely to quit and more willing to put up with you pushing her using obedience.
        self.love = love
        self._sluttiness = 0 + sluttiness #How slutty the girl is by default. Higher will have her doing more things just because she wants to or you asked.
        self._obedience = obedience #How likely the girl is to listen to commands. Default is 100 (normal person), lower actively resists commands, higher follows them.

        if coffee_style is None:
            self.coffee_style = self.get_random_coffee_style()
        else:
            self.coffee_style = coffee_style

        #Situational modifiers are handled by events. These dicts and related functions provide a convenient way to avoid double contributions. Remember to clear your situational modifiers when you're done with them!!
        self.situational_sluttiness = {} #A dict that stores a "situation" string and the corresponding amount it is contributing to the girls sluttiness.
        self.situational_obedience = {} #A dict that stores a "situation" string and a corresponding amount that it has affected their obedience by.

        ##Sex Stats##
        #These are physical stats about the girl that impact how she behaves in a sex scene. Future values might include things like breast sensitivity, pussy tightness, etc.
        self.arousal = 0 #How actively horny a girl is, and how close she is to orgasm.
        self.max_arousal = 100 #Her maximum arousal. TODO: Keep this hidden until you make her cum the first time?

        self.novelty = 100 #How novel this girl making you cum is. Breaking taboos and time increases it, the girl making you cum decreases it.

        ####
        self.vagina_tightness = vagina_tightness

        if sex_skill_list is None:
            sex_skill_list = [0, 0, 0, 0]

        ##Sex Skills##
        #These represent how skilled a girl is at different kinds of intimacy, ranging from kissing to anal. The higher the skill the closer she'll be able to bring you to orgasm (whether you like it or not!)
        self.sex_skills = {}
        self.sex_skills["Foreplay"] = sex_skill_list[0] #A catch all for everything that goes on before blowjobs, sex, etc. Includes things like kissing and strip teases.
        self.sex_skills["Oral"] = sex_skill_list[1] #The girls skill at giving head.
        self.sex_skills["Vaginal"] = sex_skill_list[2] #The girls skill at different positions that involve vaginal sex.
        self.sex_skills["Anal"] = sex_skill_list[3] #The girls skill at different positions that involve anal sex.

        self.sex_record: dict[str, int] = {}
        self.broken_taboos: list[str] = [] #Taboos apply a penalty to the _first_ time you are trying to push some boundary (first time touching her pussy, first time seeing her tits, etc.), and trigger special dialogue when broken.

        bc_chance = 100 - self.age + (self.opinion.bareback_sex * 15)
        if persistent.pregnancy_pref == 2 and renpy.random.randint(0, 100) > bc_chance:
            self.on_birth_control = False #If this character is on birth control or not. Note that this may be overridden by a game wide setting preventing pregnancy. (and on other settings may not be 100% effective)
        elif persistent.pregnancy_pref == 3 and renpy.random.randint(0, 100) > 70:    #Studies show roughly 65-70% of women using some form of birth control. Simplify this to BC pill only for the game
            self.on_birth_control = False
        else:
            self.on_birth_control = True
        self.bc_penalty = 0 #Lowers the chance of birth control preventing a pregnancy. (Default is 100% if predictable or 90% if realistic).
        self.fertility_percent = 20.0 - ((self.age - Person.get_age_floor()) / 3.0) #The chance, per creampie, that a girl gets pregnant.
        self.ideal_fertile_day = renpy.random.randint(0, 29) #Influences a girls fertility chance. It is double on the exact day of the month, dropping down to half 15 days before/after. Only applies on sem-realistic setting.

        self.lactation_sources = 0 #How many things are causing this girl to lactate. Mainly serum traits, side effects, or pregnancy.
        self.breast_milk = 0.0  # available breast milk


        ## Clothing things.
        self.wardrobe: Wardrobe | None = None
        if wardrobe is not None:
            self.wardrobe = copy.copy(wardrobe) #Note: we overwrote default copy behaviour for wardrobes so they do not have any interference issues with each other.

        if base_outfit is None:
            self.base_outfit = Outfit(name + "'s Base Outfit")
        elif isinstance(base_outfit, Outfit):
            self.base_outfit = base_outfit

        self.infractions: list[Infraction] = [] #List of infractions this character has committed.

        self.outfit: Outfit = None  # what outfit is she currently wearing
        self.planned_outfit: Outfit = None #planned_outfit is the outfit the girl plans to wear today while not at work. She will change back into it after work or if she gets stripped. Cop0y it in case the outfit is changed during the day.
        self.next_day_outfit: Outfit = None

        ## Conversation things##
        self.sexed_count = 0
        self.is_favourite = False
        self.stay_wet = False
        self.slave_collar = False
        self.drink_level = 0
        self.gtk_list = None    #Action list for unique characters to have backstory during small talk

        self.training_log = defaultdict(int) #Contains a list of Trainable.training_tag's that this person has had trained already, which is used to increase the cost of future training in similar things.

        ## Internet things ##
        if generate_insta: #NOTE: By default all of these are not visible to the player.
            self.add_role(instapic_role)
        if generate_dikdok:
            self.add_role(dikdok_role)
        if generate_onlyfans:
            self.add_role(onlyfans_role)
        if job is None: # make sure she has at least unemployed as job
            job = unemployed_job

        self._add_job(job, 0, False)
        self.story_tracker = Story_Tracker(self)

    def __call__(self, what, *args, **kwargs): #Required to play nicely with statement equivalent say() when passing only Person object.
        new_what = self.personalise_text(what) #keep the old what as a reference in case we need it.

        global portrait_say
        portrait_say = self.build_person_portrait()
        global talking_person
        talking_person = self
        if not persistent.text_effects:
            self.char(new_what, *args, **kwargs)
            portrait_say = None
            talking_person = None
            return

        new_colour = Color(self.what_color) #Multiple sections may modify the colour of the entire string, so we apply it once at the end.

        #Tags that are applied are generally applied to the inner most parts up here, more general as we go down.
        if self.has_role(trance_role): #Desaturate her dialogue as she falls deeper into a trance.
            if self.has_exact_role(trance_role):
                new_colour = new_colour.multiply_hsv_saturation(0.7)
            elif self.has_exact_role(heavy_trance_role):
                new_colour = new_colour.multiply_hsv_saturation(0.4)
            elif self.has_exact_role(very_heavy_trance_role):
                new_colour = new_colour.multiply_hsv_saturation(0.1)

        def __wrap_text_with_tag(self: Person, text: str, words: str, colour: Color, start_tag: str, end_tag: str):
            start_index = text.lower().find(words)
            if start_index == -1:
                return text
            wrapped_string = text[start_index:start_index + len(words)]
            replacement = f"{start_tag}{self.wrap_string(wrapped_string, the_colour = colour)}{end_tag}"
            return text.replace(wrapped_string, replacement)

        if self.has_breeding_fetish or self.arousal_perc > 40 - (10 * self.opinion.bareback_sex + self.opinion.creampies):
            for words in ("knocked_up", "knock me up", "preg me", "oh god", "oh my god"):
                new_what = __wrap_text_with_tag(self, new_what, words, new_colour, "{sc=1}", "{/sc}")

        temp_what = ""
        for word in new_what.split(): #Per word modifications
            flattened_word = remove_punctuation(word).lower() #Stripped and lower case for easy comparison, we use the full raw word (including punctuation) for replacement.
            modified_word = False
            effect_strength = int(6 * (self.arousal_perc / 100)) + 2 #If an effect triggers this scales the effect with arousal.
            if word[0] == "{" and word[-1] == "}":
                pass #Don't do anything to tags.

            elif flattened_word in ("cum", "cumming"): #Strip punctuation, avoids us catching phrases like "cumming" and only shaking the front.
                if self.arousal_perc > (40 - 10 * (self.opinion.drinking_cum + self.opinion.being_covered_in_cum + self.opinion.cum_facials + self.opinion.creampies)):
                    modified_word = True
                    cum_color = Color("#e5e5d6")

                    word_replace = self.wrap_string(word, the_colour = cum_color, the_font = "fonts/plasdrip.ttf")
                    word_replace = f"{{atl=0.3,drop_text~#~ 2.0, bounce_text~{effect_strength}}}{word_replace}{{/atl}}"
                    temp_what += word_replace + " "

            elif flattened_word in ("cock", "dick"):
                if self.arousal_perc > (40 - 10 * (self.opinion.big_dicks)):
                    modified_word = True
                    word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                    word_replace = f"{{sc=1}}{{bt={effect_strength}}}{word_replace}{{/bt}}{{/sc}}"
                    temp_what += word_replace + " "

            elif flattened_word in ("pussy", "vagina", "cunt"):
                if self.arousal_perc > (50):
                    modified_word = True
                    word_replace = self.wrap_string(word, the_colour = new_colour)
                    word_replace = f"{{bt={effect_strength}}}{word_replace}{{/bt}}"
                    temp_what += word_replace + " "

            elif flattened_word in ("tit", "tits", "boob", "boobs", "breast", "breasts", "mommy milkers"):
                if self.arousal_perc > 40 - 10 * self.opinion.showing_her_tits:
                    modified_word = True
                    tit_effect_strength = int(6 * (self.arousal_perc / 100)) + Person.rank_tits(self.tits)
                    word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                    word_replace = f"{{bt={tit_effect_strength}}}{word_replace}{{/bt}}"
                    temp_what += word_replace + " "

            elif flattened_word == "fuck":
                if self.arousal_perc > 60:
                    modified_word = True
                    word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                    temp_what += word_replace + " "

            elif flattened_word in ("pregnant", "bred", "breed"):
                if self.arousal_perc > 40 - (10 * self.opinion.bareback_sex + self.opinion.creampies) or self.has_breeding_fetish:
                    modified_word = True
                    word_replace = self.wrap_string(word, the_colour = new_colour, size_mod = effect_strength)
                    word_replace = f"{{sc=3}}{word_replace}{{/sc}}"
                    temp_what += word_replace + " "

            if not modified_word:
                temp_what += word + " "

        new_what = temp_what #[:-1] #STrip the last character, which is an unused space.
        new_what = self.wrap_string(new_what, the_colour = new_colour)

        self.char(new_what, *args, **kwargs)
        portrait_say = None
        talking_person = None

    def __hash__(self) -> int:
        return self.identifier

    def __eq__(self, other: Person) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.identifier == other.identifier

    def __getstate__(self): # excludes decorators from serialization
        state = self.__dict__.copy()
        for x in chain(("bedroom", "opinion", "known_opinion", "progress") + Person._location_clear_keys):
            state.pop(x, None)
        return state

    def wrap_string(self, string: str, the_colour: Color | None = None, the_font: str | None = None, size_mod: int | None = None): #Useful for wrapping a piece of advanced tag dialogue with the proper font, colour, style.
        return_string = string
        if the_colour is None:
            the_colour = self.what_color
        else:
            the_colour = the_colour.hexcode

        if the_font is None:
            the_font = self.who_font
        return_string = "{color=" + the_colour + "}" + return_string + "{/color}"
        return_string = "{font=" + the_font + "}" + return_string + "{/font}" #Then set the font
        if size_mod is not None:
            size_string = str(size_mod)
            if size_mod > 0:
                size_string = "+" + size_string
            return_string = "{size=" + size_string + "}" + return_string + "{/size}"
        #return_string = "{=general_dialogue_style}" + return_string + "{/=general_dialogue_style}"
        return return_string

    @property
    def idle_pose(self):
        if "downtown_bar" not in globals(): # skip this when running tutorial
            return self._idle_pose

        if renpy.call_stack_depth() < 2:
            if self.is_at_job(waitress_job):
                return renpy.random.choice(("stand3", "stand4", "walking_away", "back_peek"))
            # we are in the main menu (alternative idle_pose)
            if (self.is_employee and self.is_at_work) or (self.is_intern and self.is_at_office) or self.is_at(downtown_bar):
                return "sitting"
            if self.is_at(gym):
                pose = self.event_triggers_dict.get("gym_pose", None)
                if not pose: # store preferred position in bdsm room (prevent switching on hover)
                    pose = renpy.random.choice(["missionary", "stand2", "back_peek", "stand4", "sitting"])
                    self.event_triggers_dict["gym_pose"] = pose
                return pose

        if self.has_role(caged_role):
            pose = self.event_triggers_dict.get("bdsm_room_pose", None)
            if not pose: # store preferred position in bdsm room (prevent switching on hover)
                pose = renpy.random.choice(["cowgirl", "kneeling1", "blowjob"])
                self.event_triggers_dict["bdsm_room_pose"] = pose
            return pose
        return self._idle_pose

    @idle_pose.setter
    def idle_pose(self, value):
        self._idle_pose = value

    @cached_property
    def location(self) -> Room:
        return next((x for x in list_of_places if x.identifier == self._location), self.home or purgatory)

    def _set_location(self, value: Room):
        if not isinstance(value, Room):
            write_log("location.setter(): Error new location parameter is not a room.")
            return NotImplemented
        self._location = value.identifier
        self._clear_location_cache()

    _location_clear_keys = ("location", "current_location_hub", "current_job", "is_at_work", "is_at_office", "is_at_stripclub", "is_at_mc_house")

    def _clear_location_cache(self):
        for x in Person._location_clear_keys:
            self.__dict__.pop(x, None)

    @cached_property
    def current_location_hub(self) -> MapHub:
        return next((x for x in list_of_hubs if self.location in x), MapHub("Unknown", "Unknown"))

    @cached_property
    def home(self) -> Room:
        found = next((x for x in list_of_places if x.identifier == self._home), None)
        if found:
            return found
        # something got fucked up -> create new home
        return self.generate_home()

    def _set_home(self, value: Room):
        if not isinstance(value, Room):
            write_log("home.setter(): Error new home parameter is not a room.")
            return NotImplemented
        # print(f"Set new home {self.name} to '{value.name}'")
        self._home = value.identifier
        self.__dict__.pop("home", None)
        self.__dict__.pop("home_hub", None)

    @cached_property
    def home_hub(self) -> HomeHub:
        if self.home in harem_hub.locations:
            return harem_hub
        if self in (lily, mom):
            return home_hub
        if self in (aunt, cousin):
            return aunt_home_hub
        return next((x for x in (residential_home_hub, industrial_home_hub, downtown_home_hub, university_home_hub) if self.home in x), HomeHub("Unknown", "Unknown"))

    def learn_home(self) -> bool: # Adds the_person.home to mc.known_home_locations allowing it to be visited without having to go through date label
        if not self.mc_knows_address:
            mc.known_home_locations.append(self.home)
            return True # Returns true if it succeeds
        return False # Returns false otherwise, so it can be used for checks.

    def change_home_location(self, new_home):
        if not isinstance(new_home, Room):
            write_log("change_home_location(): Error new home parameter is not a room.")
            return NotImplemented

        # remove current location, if house will be empty
        if not any(x for x in list_of_people if x != self and x.home == self.home) \
                and self.mc_knows_address:
            #print(f"Remove known home location '{self.home.name}'")
            mc.known_home_locations.remove(self.home)

        # if at old home location, move to new home
        if self.is_at(self.home):
            #print(f"Move {self.name} to new home '{new_home.name}'")
            self.change_location(new_home)

        # special case: unique character changes home location (moves in with someone or harem mansion)
        for hub in (residential_home_hub, industrial_home_hub, downtown_home_hub, university_home_hub):
            if self in hub.people:
                #print(f"Remove unique character {self.name} from {hub.name}")
                hub.people.remove(self)

        # special case: when home owner and other people live there, one of them becomes the new home owner
        if f"{self.name} {self.last_name}" in self.home.name:
            next_owner = next((x for x in list_of_people if x != self and x.home == self.home), None)
            if next_owner:
                #print(f"Change home owner of '{self.home.name}' to '{next_owner.name} {next_owner.last_name}'")
                new_name = f"{next_owner.name} {next_owner.last_name}"
                self.home.name = new_name
                self.home.formal_name = new_name

        # set home and default schedule to new home location
        self.set_schedule(new_home, time_slots = [0, 4])
        self._set_home(new_home)

    def toggle_favourite(self):
        self.is_favourite = not self.is_favourite

    @property
    def is_home(self) -> bool:
        return self.is_at(self.home)

    def is_at(self, location: Iterable[Room | MapHub | HomeHub] | Room | MapHub | HomeHub) -> bool:
        '''
        Return True when person is in passed Room, MapHub or HomeHub
        '''
        if isinstance(location, Room):
            return self.location == location
        if isinstance(location, (HomeHub, MapHub)):
            return self.current_location_hub == location
        if isinstance(location, Iterable) or inspect.isgenerator(location):
            return any(x for x in location if self.is_at(x))
        return NotImplemented

    @property
    def living_with(self) -> list[Person]:
        '''
        Returns a list of people living with this person.
        '''
        # special cases
        if self.home in harem_hub.locations: # harem
            return [x for x in list_of_people if x != self and x.home in harem_hub.locations]
        if self.is_family: # family
            if aunt.has_event_day("arrival") and not aunt.has_event_day("moved_out"):
                return [x for x in list_of_people if x != self and x.home in chain(home_hub.locations, aunt_home_hub.locations)]
            if self in (mom, lily):
                return [x for x in list_of_people if x != self and x.home in home_hub.locations]
            if self in (aunt, cousin):
                return [x for x in list_of_people if x != self and x.home in aunt_home_hub.locations]

        return [x for x in list_of_people if x != self and x.home == self.home]

    @property
    def lives_alone(self):
        return len(self.living_with) == 0

    @property
    def mc_knows_address(self) -> bool:
        return self.is_family or self.home in mc.known_home_locations

    @property
    def is_job_known(self) -> bool:
        '''
        Do we know the current / primary job of the person?
        '''
        if not self.is_at_work:
            return self.primary_job.job_known
        return self.current_job.job_known

    def learn_job(self, job: str | JobDefinition = None):
        '''
        Learns the current / primary job or passed job of the person.
        '''
        if job:
            found = self.get_job(job)
            if found:
                found.job_known = True
            return

        if not self.is_at_work:
            self.primary_job.job_known = True
        self.current_job.job_known = True

    @cached_property
    def current_job(self) -> ActiveJob | None:
        # returns job she should be working at now
        scheduled_job = next((x for x in self.jobs if x.is_work_day() and x.is_work_shift()), None)
        # special case 'unemployed' is always at work
        if not scheduled_job and self.has_job(unemployed_job):
            return self.primary_job
        return scheduled_job

    @cached_property
    def is_at_work(self) -> bool:
        '''
        Returns True when the person is at currently scheduled job
        '''
        if self.current_job and self.current_job.scheduled_location:
            # list of special conditions for is at work
            if ((self.is_employee or self.is_intern) and self.is_at_office):
                return True # for employees the whole office is valid
            if (self.has_job(stripper_job) or self.is_strip_club_employee) and self.is_at_stripclub:
                return not strip_club_is_closed() # only if stripclub not closed
            if self.has_job("City Administrator") and self.is_at_office:
                return True # when she's at your office

            return self.is_at(self.current_job.scheduled_location)

        return False

    @cached_property
    def is_at_office(self) -> bool:
        '''
        Returns True when the person is at the MC's business.
        '''
        return self.is_at(office_hub)

    @cached_property
    def is_at_stripclub(self) -> bool:
        '''
        Returns True when the person is at the strip club.
        '''
        return self.is_at(strip_club_hub)

    @cached_property
    def is_at_mc_house(self) -> bool:
        '''
        Returns True when the person is at the MC's home.
        '''
        return self.is_at(home_hub)

    @cached_property
    def bedroom(self) -> Room:
        if not hasattr(self, "_bedroom"):
            if self == lily:
                self._bedroom = lily_bedroom.identifier
            elif self == mom:
                self._bedroom = mom_bedroom.identifier
            elif self == cousin:
                self._bedroom = cousin_bedroom.identifier
            elif self == aunt:
                self._bedroom = aunt_bedroom.identifier
            elif self.has_job(prostitute_job):
                self._bedroom = prostitute_bedroom.identifier
            else:
                self._bedroom = renpy.random.choice([generic_bedroom_1, generic_bedroom_2, generic_bedroom_3, generic_bedroom_4]).identifier
        return next((x for x in list_of_places if x.identifier == self._bedroom), self.home) # fallback location is her home

    def change_location(self, destination: Room) -> bool:
        '''
        Returns True when Person changes location
        '''
        if self.is_at(destination):
            return False

        self._set_location(destination)

        # only change outfit when not following mc
        if self.follow_mc:
            # when moving to a non-private location, make sure she is dressed properly
            if self._follow_mc_outfit and not destination.is_private:
                self.apply_outfit(self._follow_mc_outfit)
            return True

        self.apply_planned_outfit(show_dress_sequence = False)
        return True

    def change_to_bedroom(self):
        mc.change_location(self.bedroom)

    def change_to_hallway(self):
        mc.change_location(her_hallway) # use generic hallway

    @property
    def can_clone(self) -> bool:
        if not genetic_manipulation_policy.is_owned:
            return False
        if self.is_clone:
            return False
        if self.is_unique:
            return False
        return True

    @property
    def follow_mc(self) -> bool:
        self._follow_mc_outfit = self.current_planned_outfit
        return self._follow_mc

    @follow_mc.setter
    def follow_mc(self, value):
        self._follow_mc_outfit = None
        self._follow_mc = value

    @property
    def body_images(self) -> Clothing:
        global body_images_dict
        return body_images_dict[self.skin]

    @property
    def tan_images(self) -> Clothing:
        global tan_images_dict
        return tan_images_dict[self.tan]

    @property
    def expression_images(self) -> Expression:
        global emotion_images_dict
        return emotion_images_dict[self.skin][self.face_style]

    @property
    def fname(self) -> str:
        global talking_person
        if self.is_stranger:
            return self.create_formatted_title("???")
        if talking_person is None:
            if self.is_family or self.has_job(prostitute_job): # always use their title when MC is talking
                return self.title

        name = self.create_formatted_title(self.name)
        if isinstance(talking_person, Person) and town_relationships.is_family(self, talking_person):
            relation = town_relationships.get_relationship_type(talking_person, self)
            if relation == "Mother":
                return self.create_formatted_title("Mom")
            elif relation == "Aunt":
                return f"aunt {name}"
            elif relation == "Cousin":
                return f"cousin {name}"
            elif relation == "Daughter":
                return f"{name}"
            elif relation == "Sister":
                return self.create_formatted_title("Sis")
            elif relation == "Niece":
                return f"niece {name}"
            elif relation == "Grandmother":
                return f"grandma {name}"
            elif relation == "Granddaughter":
                return self.create_formatted_title("Pumpkin")
        return name

    @property
    def display_name(self) -> str:
        # this will now return fname (future refactor, replace all Person.display_name calls with Person.fname)
        return self.fname

    @property
    def arousal_perc(self) -> float:
        return ((self.arousal * 1.0) / max(self.max_arousal, 1)) * 100

    @property
    def is_unique(self) -> bool:
        return self.type == "story"

    @property
    def is_family(self) -> bool:
        return self in (mom, lily, aunt, cousin)

    @property
    def is_employee(self) -> bool:
        return self.has_role(employee_role)

    @property
    def is_strip_club_employee(self) -> bool:
        return self.has_job((stripper_job, stripclub_stripper_job, stripclub_bdsm_performer_job, stripclub_waitress_job, stripclub_manager_job, stripclub_mistress_job))

    @property
    def is_clone(self) -> bool:
        return self.has_role(clone_role)

    @property
    def suggest_tier(self) -> int:
        return next((i for i, threshold in enumerate([15, 35, 55, 75]) if self.suggestibility < threshold), 4)

    @property
    def obedience_tier(self) -> int:
        return next((i for i, threshold in enumerate([100, 120, 140, 160, 180]) if self.obedience < threshold), 5)

    @property
    def sluttiness_tier(self) -> int:
        return max(0, min(5, (self.sluttiness - 5) // 20))

    @property
    def is_available(self) -> bool:
        return self.available and not self.is_at(purgatory)

    @property
    def is_bald(self) -> bool:
        return bald_hair.is_similar(self.hair_style)

    @property
    def is_dominant(self) -> bool:
        if self.personality == alpha_personality and self.obedience < (240 - ((2 + self.opinion.being_submissive) * 10)):
            return True
        return (self.opinion.taking_control > 1
                or self.opinion.taking_control > self.opinion.being_submissive
                or self.obedience < (160 - ((2 + self.opinion.being_submissive) * 10)))

    @property
    def is_submissive(self) -> bool:
        if self.is_slave:
            return True
        if self.personality == alpha_personality and self.obedience < (200 - ((2 + self.opinion.being_submissive) * 10)):
            return False
        return (self.opinion.being_submissive > 1
                or self.opinion.taking_control < self.opinion.being_submissive
                or self.obedience > (200 - ((2 + self.opinion.being_submissive) * 10)))

    @property
    def is_slave(self) -> bool:
        return self.has_role(slave_role)

    @property
    def is_stranger(self) -> bool:
        return self.title is None or "???" in self.title or self.mc_title == "Stranger"

    @property
    def has_significant_other(self) -> bool:
        return self.relationship != "Single" if self.relationship is not None else False

    @property
    def is_single(self) -> bool:
        return not self.has_significant_other and not self.is_girlfriend

    @property
    def in_harem(self) -> bool:
        return self.has_role(harem_role)

    @property
    def is_girlfriend(self) -> bool:
        return self.has_role(girlfriend_role) or self.in_harem

    @property
    def is_affair(self) -> bool:
        return self.has_role(affair_role)

    @property
    def has_relation_with_mc(self) -> bool:
        return self.is_girlfriend or self.is_affair

    @property
    def formal_address(self) -> str:
        if self.has_job((nora_professor_job, university_professor_job)):
            return "Professor"
        if self.has_job(doctor_job):
            return "Doctor"
        if self.relationship == "Married":
            return "Mrs."
        if self.age > 30:
            return "Ms."
        return "Miss"

    def change_height(self, amount: float, chance: int) -> bool:
        lower_limit = Person.get_height_floor(initial=False)
        upper_limit = Person.get_height_ceiling(initial=False)

        if amount == 0 or (self.height <= lower_limit and amount < 0) or (self.height >= upper_limit and amount > 0):
            return False

        if renpy.random.randint(0, 100) > chance:
            return False

        self.height += amount
        self.height = min(self.height, upper_limit)
        self.height = max(self.height, lower_limit)
        return True

    @property
    def weight(self) -> float:
        if not hasattr(self, "_weight"):
            check_type = self.event_triggers_dict.get("pre_preg_body", self.body_type)
            if check_type == "thin_body":
                self._weight = 60 * self.height
            elif check_type == "standard_body":
                self._weight = 75 * self.height
            else:
                self._weight = 90 * self.height

        extra_modifier = 0
        if self.is_pregnant:
            extra_modifier = max(self.days_since_event("preg_start_date") - 25, 0) * .17
        return self._weight + extra_modifier

    @weight.setter
    def weight(self, value: float):
        self._weight = value

    def change_weight(self, amount: float, chance: int = 100) -> bool:
        if amount == 0:
            return False

        _ = self.weight        # make sure internal _weight is set

        if renpy.random.randint(0, 100) <= chance:
            self._weight += amount

        # maximum and minimum weight are dependent on height
        max_weight = (self.height) * 100
        min_weight = (self.height) * 50
        switch_point_low = (self.height) * 68
        switch_point_high = (self.height) * 83

        if amount > 0:
            if self.weight > switch_point_low + 3 and self.body_type == "thin_body":
                self.body_type = "standard_body"
                return True
            if self.weight > switch_point_high + 3 and self.body_type == "standard_body":
                self.body_type = "curvy_body"
                return True
            if self.weight > max_weight: #Maximum weight
                self._weight = max_weight
            return False

        if amount < 0:
            if self.weight < min_weight:  #Minimum weight
                self._weight = min_weight
                return False
            if self.weight < switch_point_low - 3 and self.body_type == "standard_body":
                self.body_type = "thin_body"
                return True
            if self.weight < switch_point_high - 3 and self.body_type == "curvy_body":
                self.body_type = "standard_body"
                return True
            return False

    #jes: Add method to change vagina tightness
    def change_tightness(self, amount: int, chance: int = 100) -> bool:
        lower_limit = self._tightness_floor
        upper_limit = self._tightness_ceiling

        if amount == 0 or (self.vagina_tightness <= lower_limit and amount < 0) or (self.vagina_tightness >= upper_limit and amount > 0):
            return False

        if renpy.random.randint(0, 100) > chance:
            return False

        self.vagina_tightness += amount
        self.vagina_tightness = min(self.vagina_tightness, upper_limit)
        self.vagina_tightness = max(self.vagina_tightness, lower_limit)
        return True

    @property
    def hair_description(self) -> str:
        if self.is_bald:
            return "bald head"
        if self.hair_style == braided_bun:
            return "braided hair"
        if self.hair_style in (messy_short_hair, shaved_side_hair, short_hair, windswept_hair):
            return "short hair"
        if self.hair_style in (messy_ponytail, twintail, ponytail):
            return "pony tail"
        if self.hair_style in (long_hair, messy_hair):
            return "long hair"
        return "hair"

    @property
    def pubes_description(self) -> str:
        if self.pubes_style.is_similar(shaved_pubes):
            return "bald"
        if self.pubes_style.is_similar(landing_strip_pubes):
            return "brazilian waxed"
        if self.pubes_style.is_similar(default_pubes):
            return "hairy"
        return "neatly trimmed"

    @property
    def tits_description(self) -> str:
        rank = self.rank_tits(self.tits)
        adjective = "perky"
        descriptor = "tits"

        if rank == 0:
            adjective = renpy.random.choice(("flat", "minute", "tiny"))
            descriptor = renpy.random.choice(("titties", "tits", "nipples"))
        elif rank in (1, 2, 3):
            adjective = renpy.random.choice(("firm", "perky", "small"))
            descriptor = renpy.random.choice(("breasts", "tits", "boobs"))
        elif rank in (4, 5, 6):
            adjective = renpy.random.choice(("shapely", "large", "big", "generous"))
            descriptor = renpy.random.choice(("breasts", "tits", "bosoms"))
        elif rank in (7, 8, 9):
            adjective = renpy.random.choice(("large", "voluptuous", "colossal", "huge"))
            descriptor = renpy.random.choice(("breasts", "tits", "jugs", "melons"))

        return f"{adjective} {descriptor}"

    def reset_event_parameters(self):
        base_value = 0 if "GAME_SPEED" not in globals() else GAME_SPEED
        self.event_triggers_dict["chatted"] = 4 - base_value
        self.event_triggers_dict["flirted"] = 4 - base_value
        self.event_triggers_dict["complimented"] = 4 - base_value

    def init_person_variables(self):
        #Set personality based opinions.
        for _ in builtins.range(2, 5):
            the_opinion_key, opinion_list = self.personality.generate_default_opinion()
            if the_opinion_key:
                self.opinions[the_opinion_key] = opinion_list

        for _ in builtins.range(2, 4):
            the_opinion_key, opinion_list = self.personality.generate_default_sexy_opinion()
            if the_opinion_key:
                self.sexy_opinions[the_opinion_key] = opinion_list

        self.sex_record = {k: 0 for k in
            ("Handjobs", "Blowjobs", "Cunnilingus", "Tit Fucks", "Vaginal Sex", "Anal Sex",
             "Cum Facials", "Cum in Mouth", "Cum Covered", "Vaginal Creampies", "Anal Creampies",
             "Fingered", "Kissing")}

    def generate_home(self, set_home_time = True, force_new_home = False) -> Room: #Creates a home location for this person and adds it to the master list of locations so their turns are processed.
        # generate new home location if we don't have one
        # don't use self.home since it now calls this function
        # when we cannot find self._home in list of places
        start_home = next((x for x in list_of_places if x.identifier == self._home), None)
        if force_new_home or not start_home:
            start_home = Room(f"{self.name} {self.last_name}", f"{self.name} {self.last_name}", "Home_Background", [make_wall(), make_floor(), make_couch(), make_window()], [], False, [0.5, 0.5], visible = False, hide_in_known_house_map = False, lighting_conditions = standard_indoor_lighting)

        # add home location to list of places, before assignment
        if start_home not in list_of_places:
            list_of_places.append(start_home)

        self._set_home(start_home)

        if set_home_time:
            self.set_schedule(self.home, time_slots = [0, 4])
        return self.home

    def generate_daughter(self, force_live_at_home = False, age: int = None, job: JobDefinition = None) -> Person: #Generates a random person who shares a number of similarities to the mother
        if self.is_unique:
            write_log(f"{self.name} {self.last_name} is a unique character and cannot have a random daughter generated.")
            return get_random_from_list(town_relationships.get_existing_children(self))

        if not age:
            age = renpy.random.randint(Person.get_age_floor(), self.age - 16)

        if renpy.random.randint(0, 100) < 60:
            if self.is_pregnant:
                body_type = self.event_triggers_dict.get("pre_preg_body", None)
            else:
                body_type = self.body_type
        else:
            body_type = None

        if renpy.random.randint(0, 100) < 40: #Slightly lower for facial similarities to keep characters looking distinct
            face_style = self.face_style
        else:
            face_style = None

        if renpy.random.randint(0, 100) < 30: #30% of the time they share hair colour (girls dye their hair a lot)
            hair_colour = self.hair_colour[0]
        else:
            hair_colour = None

        if renpy.random.randint(0, 100) < 60: # 60% they share the same breast size
            if self.is_pregnant:
                tits = self.event_triggers_dict.get("pre_preg_tits", None)
            else:
                tits = self.tits
        else:
            tits = None

        if renpy.random.randint(0, 100) < 60: #Share the same eye colour
            eyes = self.eyes[0]
        else:
            eyes = None

        if renpy.random.randint(0, 100) < 80: #Have heights that roughly match (mostly)
            height = self.height * (renpy.random.randint(95, 105) / 100.0)
            if height > 1.0:
                height = 1.0
            elif height < 0.8:
                height = 0.8
        else:
            height = None

        if force_live_at_home or renpy.random.randint(0, 100) < 85 - age: #It is less likely she lives at home the older she is.
            start_home = self.home
            kids = 0
            relationship = "Single"
        else:
            start_home = None
            kids = None
            relationship = None

        the_daughter = make_person(last_name = self.last_name, age = age, body_type = body_type, face_style = face_style, tits = tits, height = height,
            hair_colour = hair_colour, skin = self.skin, eyes = eyes, start_home = start_home, job = job, kids = kids, relationship = relationship)

        if start_home is None:
            the_daughter.generate_home()

        the_daughter.home.add_person(the_daughter)

        for sister in town_relationships.get_existing_children(self): #First find all of the other kids this person has
            town_relationships.update_relationship(the_daughter, sister, "Sister") #Set them as sisters

        town_relationships.update_relationship(self, the_daughter, "Daughter", "Mother") #Now set the mother/daughter relationship (not before, otherwise she's a sister to herself!)

        self.kids += 1  # increment children

        return the_daughter

    def generate_mother(self, lives_with_daughter = False, age: int = None, job: JobDefinition = None) -> Person: #Generates a random person who shares a number of similarities to the mother
        '''
        Generates a mother for this person.
        When a mother already exists, returns existing mother.
        '''
        if self.is_unique:
            write_log(f"{self.name} {self.last_name} is a unique character and cannot have a random mother generated.")
            return town_relationships.get_existing_mother(self)

        mother = town_relationships.get_existing_mother(self)
        if mother:
            return mother

        if age is None:
            age = renpy.random.randint(self.age + 16, max(self.age + 16, 55))

        if renpy.random.randint(0, 100) < 60:
            if self.is_pregnant:
                body_type = self.event_triggers_dict.get("pre_preg_body", None)
            else:
                body_type = self.body_type
        else:
            body_type = None

        if renpy.random.randint(0, 100) < 40: #Slightly lower for facial similarities to keep characters looking distinct
            face_style = self.face_style
        else:
            face_style = None

        if renpy.random.randint(0, 100) < 30: #30% of the time they share hair colour (girls dye their hair a lot)
            hair_colour = self.hair_colour[0]
        else:
            hair_colour = None

        if renpy.random.randint(0, 100) < 60: # 60% they share the same breast size
            if self.is_pregnant:
                tits = self.event_triggers_dict.get("pre_preg_tits", None)
            else:
                tits = self.tits
        else:
            tits = None

        if renpy.random.randint(0, 100) < 60: #Share the same eye colour
            eyes = self.eyes[0]
        else:
            eyes = None

        if renpy.random.randint(0, 100) < 80: #Have heights that roughly match (mostly)
            height = self.height * (renpy.random.randint(95, 105) / 100.0)
            if height > 1.0:
                height = 1.0
            elif height < 0.8:
                height = 0.8
        else:
            height = None

        if lives_with_daughter:
            start_home = self.home
        else:
            start_home = None

        # set kids fixed to 1, to prevent circular relative creations (like create mom, has 3 children, so we can start hiring her other daughters)
        the_mother = make_person(last_name = self.last_name, age = age, body_type = body_type, face_style = face_style, tits = tits, height = height,
            kids = 1, hair_colour = hair_colour, skin = self.skin, eyes = eyes, start_home = start_home, job = job)

        if start_home is None:
            the_mother.generate_home()

        the_mother.home.add_person(the_mother)

        for sister in town_relationships.get_existing_sisters(self): #First find all of the sisters this person has
            town_relationships.update_relationship(the_mother, sister, "Daughter", "Mother") #Set the mother/daughter relationship for the sisters
            the_mother.kids += 1 # increase child count per sister

        town_relationships.update_relationship(self, the_mother, "Mother", "Daughter") #Now set the mother/daughter relationship with person
        return the_mother

    def _remove_expired_serums(self):
        # use reverse traversal to remove correct serum from effects list
        # when 2 serums have same base design the __eq__ operator for list.remove()
        # does not find the correct serum to remove
        for i in range(self.active_serum_count - 1, -1, -1):
            if self.serum_effects[i].is_expired:
                serum = self.serum_effects.pop(i)
                serum.run_on_remove(self)

    def _remove_expired_infractions(self):
        for infraction in self.infractions[:]:
            infraction.days_existed += 1
            if infraction.days_existed > infraction.days_valid:
                self.remove_infraction(infraction)

    def _remove_expired_limited_time_actions(self):
        # expire limited time actions
        for lta_store in (self.on_room_enter_event_list, self.on_talk_event_list):
            for an_action in (x for x in lta_store if isinstance(x, Limited_Time_Action)):
                an_action.turns_valid -= 1
                if an_action.turns_valid <= 0:
                    lta_store.remove(an_action)

    def _auto_develop_fetishes(self):
        # auto-develop fetishes without serum
        if (not self.has_anal_fetish and self.anal_sex_skill >= 5
                and self.opinion.anal_sex >= 2 and self.opinion.anal_creampies >= 2
                and (self.anal_sex_count > 19 or self.anal_creampie_count > 19)):
            if start_anal_fetish_quest(self):
                self.event_triggers_dict["anal_fetish_start"] = True

        if (not self.has_cum_fetish and self.oral_sex_skill >= 5
                and self.opinion.giving_blowjobs >= 2 and (self.opinion.drinking_cum >= 2 or self.opinion.cum_facials >= 2)
                and self.cum_exposure_count > 19):
            if start_cum_fetish_quest(self):
                self.event_triggers_dict["cum_fetish_start"] = True

        if (not self.has_breeding_fetish and self.vaginal_sex_skill >= 5
                and self.opinion.vaginal_sex >= 2 and self.opinion.creampies >= 2
                and self.vaginal_creampie_count > 19):
            if start_breeding_fetish_quest(self):
                self.event_triggers_dict["breeding_fetish_start"] = True

    def _update_daily_stat_changes(self):
        #Now we will normalize happiness towards 100 over time. Every 5 points of happiness above or below 100 results in a -+1 per turn, rounded towards 0.
        self.change_happiness(-builtins.int((self.happiness - 100) / 5.0), add_to_log = False) #Apply the change

        # dominant person slowly bleeds obedience on run_day (lowest point offset by love)
        if self.is_dominant and self.obedience - self.love > 100 - (self.opinion.taking_control * 10):
            self.change_obedience(-1, add_to_log = False)

        # girls not in harem bleed love when over 80 and not having sex regularly
        if not self.in_harem and self.love > 80 and day > self.sex_record.get("Last Sex Day", 0) + 5:
            self.change_love(-1, add_to_log = False)

        # girls not trained as slave bleed obedience when over 200
        if not self.is_slave and self.obedience > 200:
            self.change_obedience(-1, add_to_log = False)

        if day % 7 == 0: #If the new day is Monday
            self.change_happiness(self.opinion("Mondays") * 5, add_to_log = False)

        elif day % 7 == 4: #If the new day is Friday
            self.change_happiness(self.opinion("Fridays") * 5, add_to_log = False)

        elif day % 7 == 5 or day % 7 == 6: #If the new day is a weekend day
            self.change_happiness(self.opinion("the weekend") * 3, add_to_log = False)

    @property
    def serum_tolerance(self):
        value = self._serum_tolerance
        if any(x for x in self.serum_effects if x.has_trait(antidote_trait)):
            value += 1
        return value

    @property
    def active_serum_count(self):
        return len(self.serum_effects)

    def is_affected_by_serum(self, serum: SerumDesign):
        return any(x for x in self.serum_effects if x.is_same_design(serum))

    def active_serum_with_tag(self, the_tag: list[str] | str) -> bool:
        return any(x for x in self.serum_effects if x.has_tag(the_tag))

    def active_serum_with_hidden_tag(self, the_tag: list[str] | str) -> bool:
        return any(x for x in self.serum_effects if x.has_hidden_tag(the_tag))

    def _check_serum_tolerance(self):
        over_tolerance_count = self.active_serum_count - self.serum_tolerance
        if over_tolerance_count <= 0:
            self.clear_situational_slut("over serum tolerance")
            self.clear_situational_obedience("over serum tolerance")
            return

        self.change_happiness(over_tolerance_count * -5, add_to_log = False)
        self.add_situational_slut("over serum tolerance", over_tolerance_count * -5, "My body feels strange...")
        self.add_situational_obedience("over serum tolerance", over_tolerance_count * -5, "My body feels strange...")

        # side effect of going over tolerance is shorter duration of all serum
        for serum in (x for x in self.serum_effects if x.expires):
            serum.duration_counter += over_tolerance_count

        self._remove_expired_serums()

    def _update_breast_milk(self):
        if self.lactation_sources <= 0 or not hasattr(self, "breast_milk"): # quick reset
            self.breast_milk = 0
            return
        if self.breast_milk >= self.maximum_milk_in_breasts:    # quick exit
            self.breast_milk = self.maximum_milk_in_breasts
            return

        milk_increase = Person.rank_tits(self.tits) * self.lactation_sources * 0.2
        if self.breast_milk + milk_increase > self.maximum_milk_in_breasts:
            milk_increase = self.maximum_milk_in_breasts - self.breast_milk
        self.breast_milk += milk_increase

    def run_turn(self):
        self.change_energy(20, add_to_log = False)

        if self.is_at_work:
            self.current_job.shifts += 1    # track worked shifts

        # when at gym for turn increase max energy by 1
        if self.max_energy < 160 and self.is_at(gym_hub):
            self.change_max_energy(1, add_to_log = False)

        # realistic pregnancy
        # for the next days she can get pregnant from a previous cum in vagina
        if (persistent.pregnancy_pref == 3
                and self.has_event_day("last_insemination")
                and self.days_since_event("last_insemination") < 4):
            self.did_she_become_pregnant()

        # apply serum effects
        for serum in self.serum_effects:
            serum.run_on_turn(self)

        self._remove_expired_serums()

        # Check for serum overdoses after expired effects have been removed.
        self._check_serum_tolerance()

        if persistent.pregnancy_pref != 0:    # only when pregnancy enabled
            self._update_breast_milk()

        for duty in self.active_duties:
            duty.on_turn(self)

        for role in self.special_role:
            role.run_turn(self)

    #########################################################
    # helper method for outfit_thread to load daily outfits #
    #########################################################
    def update_daily_outfit(self):
        if self.next_day_outfit:
            self.planned_outfit = self.next_day_outfit
            self.next_day_outfit = None
        else:
            self.planned_outfit = self.decide_on_outfit()

    def run_move(self):
        # reset talk actions
        self.reset_event_parameters()

        # reset sleep event data
        if time_of_day == 2 and "event_sleepwear" in self.event_triggers_dict:
            self.event_triggers_dict.pop("event_sleepwear", None)   # won't throw exception when key doesn't exist

        self.sexed_count = 0 #Reset the counter for how many times you've been seduced, you might be seduced multiple times in one day!

        if time_of_day == 0:
            # wait for outfit_thread to complete setting planned outfits for the day
            while outfit_queue.qsize() != 0:
                time.sleep(.1)
            self.apply_daily_outfit_bonus(self.planned_outfit)

        destination = self.get_destination()
        if not destination: #None destination means they have free time so pick a random
            destination = self.get_random_destination()

        if not self.is_at(destination): # only call move_person when location changed
            # changing outfits is handled by change_location
            self.change_location(destination)
        else:
            # when not changing location, she might need to change to her uniform
            self.apply_planned_outfit(show_dress_sequence = False)

        # apply after she moved to her scheduled location (job)
        self.apply_turn_based_outfit_bonus()

        self._remove_expired_limited_time_actions()

        for duty in self.active_duties:
            duty.on_move(self)

        for role in self.special_role:
            role.run_move(self)

    def run_day(self):
        if self.max_energy > 180:
            self.change_max_energy(-1, add_to_log = False)  # daily max energy bleed

        self.change_energy(.6 * self.max_energy, add_to_log = False)
        self.change_novelty(1, add_to_log = False)

        # healing of ass after spanking
        self.spank_level = max(self.spank_level - 2, 0)

        if self.arousal > (self.max_arousal / 2.0): # her arousal is high she masturbates at night, generating a small amount of sluttiness
            self.arousal = 0
            if self.opinion.masturbating > 0: # Masturbating turns her on, so just getting off turns her back on!
                self.arousal = 15 * self.opinion.masturbating
            self.change_happiness(5 + 5 * self.opinion.masturbating, add_to_log = False)
            self.run_orgasm(show_dialogue = False, trance_chance_modifier = self.opinion.masturbating, add_to_log = False, fire_event = False)

        for serum in self.serum_effects:
            serum.run_on_turn(self) #If a run_on_turn is called and the serum has expired no effects are calculated, so we can safely call this as many times as we want.
            serum.run_on_turn(self) #Night is 3 turn chunks, but one is already called when time progresses. Run serums twice more, and if we've gotten here we also run the on day function.
            serum.run_on_day(self) #Serums that effect people at night must effect two of the three turns.

        if self.love > self.baby_desire + 20:
            self.change_baby_desire(1)
        if self.love < self.baby_desire - 20:
            self.change_baby_desire(-1)

        self._remove_expired_serums()

        self._remove_expired_infractions()

        self.situational_sluttiness.clear()
        self.situational_obedience.clear()

        self._update_daily_stat_changes()

        for duty in self.daily_duties:
            duty.on_day(self)

        for role in self.special_role:
            role.run_day(self)

        for job in self.jobs:
            # daily effect on happiness when she isn't happy in her job (only for MC controlled jobs)
            if job.is_paid and job.shifts > 0:
                happiness_drop = int(job.job_happiness_score / 10.0) # basically first negative 5 points have no effect
                if happiness_drop < 0:
                    self.change_happiness(happiness_drop, add_to_log = False)
            job.reset()

        self._auto_develop_fetishes()

    def apply_turn_based_outfit_bonus(self):
        if self.should_wear_uniform: #She's wearing a uniform
            if creative_colored_uniform_policy.is_active:
                self.change_happiness(max(-1, self.opinion.work_uniforms), add_to_log = False)
            else:
                self.change_happiness(self.opinion.work_uniforms, add_to_log = False)
            if self.opinion.skimpy_uniforms > -2 and self.current_job.planned_uniform and self.current_job.planned_uniform.outfit_slut_score > self.sluttiness * 0.8:
                self.change_slut(1, ((self.opinion.skimpy_uniforms + 1) * 10), add_to_log = False)
        else:
            #A skimpy outfit is defined as the top 20% of a girls natural sluttiness.
            if self.opinion.skimpy_outfits > -2 and self.planned_outfit and self.planned_outfit.outfit_slut_score > self.sluttiness * 0.80:
                self.change_slut(1, ((self.opinion.skimpy_outfits + 1) * 10), add_to_log = False)

    def apply_daily_outfit_bonus(self, outfit: Outfit):
        if not outfit:
            return

        #A conservative outfit is defined as the bottom 20% of a girls natural sluttiness.
        if self.sluttiness < 30 and outfit.outfit_slut_score < self.sluttiness * 0.20:
            # happiness won't go below 80 or over 120 by this trait and only affects in low sluttiness range, after that she won't care
            if self.happiness > 80 and self.happiness < 120:
                self.change_happiness(self.opinion.conservative_outfits, add_to_log = False)

        # lingerie only impacts to sluttiness level 30
        if (outfit.wearing_bra or outfit.wearing_panties or outfit.has_thigh_high_socks):
            lingerie_bonus = 0
            if outfit.has_thigh_high_socks:
                lingerie_bonus += self.opinion.lingerie
            if outfit.bra_is_lingerie: #We consider underwear with an innate sluttiness of 2 or higher "lingerie" rather than just underwear.
                lingerie_bonus += self.opinion.lingerie
            if outfit.panties_is_lingerie:
                lingerie_bonus += self.opinion.lingerie
            lingerie_bonus = builtins.int(lingerie_bonus / 3.0)
            self.change_slut(lingerie_bonus, 30, add_to_log = False)

        # not wearing underwear only impacts sluttiness to level 40
        if not outfit.is_wearing_underwear: #We need to determine how much underwear they are not wearing. Each piece counts as half, so a +2 "love" is +1 slut per chunk.
            underwear_bonus = 0
            if not outfit.wearing_bra:
                underwear_bonus += self.opinion.not_wearing_underwear
            if not outfit.wearing_panties:
                underwear_bonus += self.opinion.not_wearing_underwear
            underwear_bonus = builtins.int(underwear_bonus / 2.0) #I believe this rounds towards 0. No big deal if it doesn't, very minor detail.
            self.change_slut(underwear_bonus, 40, add_to_log = False)

        # showing the goods only impacts sluttiness to level 50
        if outfit.tits_visible:
            self.change_slut(self.opinion.showing_her_tits, 50, add_to_log = False)
        if outfit.vagina_visible:
            self.change_slut(self.opinion.showing_her_ass, 50, add_to_log = False)

        # showing everything only impacts sluttiness to level 60
        if outfit.has_full_access:
            self.change_slut(self.opinion.not_wearing_anything, 60, add_to_log = False)

    def get_display_colour_code(self, saturation = 1.0, given_alpha = 1.0) -> str:
        the_colour = Color(self.char.what_args["color"])
        the_colour = the_colour.multiply_hsv_saturation(saturation)
        the_colour = the_colour.multiply_value(saturation)
        the_colour = the_colour.replace_opacity(given_alpha)

        return the_colour.hexcode

    def build_person_portrait(self, special_modifier = None):
        position = "stand5"
        emotion = "happy"
        special_modifier = None
        lighting = [.98, .98, .98]

        disp_key = "P:{}_C:{}_BO:{}".format(self.identifier,
            hash((self.face_style, self.hair_style.name, self.skin, special_modifier)
                + tuple(self.hair_style.colour)
                + tuple(self.eyes[1])),
            hash(tuple(x.identifier for x in self.base_outfit)))

        global portrait_cache

        if disp_key in portrait_cache:
            return portrait_cache[disp_key]

        displayable_list = []
        displayable_list.append(self.expression_images.generate_emotion_displayable(position, emotion, special_modifier = special_modifier, eye_colour = self.eyes[1], lighting = lighting)) #Get the face displayable
        displayable_list.extend(self.base_outfit.generate_draw_list(self, position, emotion, special_modifier, lighting))
        displayable_list.append(self.hair_style.generate_item_displayable("standard_body", self.tits, position, lighting = lighting)) #Get hair

        composite_list = [position_size_dict.get(position)]

        for display in displayable_list:
            if isinstance(display, builtins.tuple):
                composite_list.extend(display)
            else:
                composite_list.append((0, 0))
                composite_list.append(display)

        portrait_cache[disp_key] = AlphaMask(Flatten(Composite(*composite_list)), portrait_mask_image)
        return portrait_cache[disp_key]

    def build_person_displayable(self, position: str = "default", emotion: str | None = None, special_modifier: str | None = None, lighting = None, hide_list = None, outfit: Outfit | None = None, cache_item = True): #Encapsulates what is done when drawing a person and produces a single displayable.
        if hide_list is None:
            hide_list = []
        if position == "default" or position is None:
            position = self.idle_pose
        if emotion is None:
            emotion = self.get_emotion()
        if outfit is None:
            outfit = self.outfit

        forced_special_modifier = self.outfit.get_forced_modifier()
        if forced_special_modifier is not None:
            special_modifier = forced_special_modifier

        disp_key = "ID:{}_C:{}_O:{}".format(self.identifier,
            hash(
                (position, emotion, special_modifier) +
                (self.skin, self.face_style, self.tits, self.body_type, self.tan) +
                tuple(flatten_list(lighting))
            ),
            outfit.identifier)
        if disp_key in character_cache:
            return character_cache[disp_key]

        displayable_list = []
        displayable_list.append(self.body_images.generate_item_displayable(self.body_type, self.tits, position, lighting)) #Add the body displayable
        displayable_list.append(self.expression_images.generate_emotion_displayable(position, emotion, special_modifier = special_modifier, eye_colour = self.eyes[1], lighting = lighting)) #Get the face displayable
        if self.tan != "No Tan":
            displayable_list.append(self.tan_images.generate_item_displayable(self.body_type, self.tits, position, lighting = lighting)) # Add the tan
            if self.tan_images.has_extension:
                displayable_list.append(self.tan_images.has_extension.generate_item_displayable(self.body_type, self.tits, position, lighting = lighting)) # Add the tan
        displayable_list.append(self.pubes_style.generate_item_displayable(self.body_type, self.tits, position, lighting = lighting)) #Add in her pubes

        displayable_list.extend(outfit.generate_draw_list(self, position, emotion, special_modifier, lighting = lighting, hide_layers = hide_list))
        displayable_list.append(self.hair_style.generate_item_displayable("standard_body", self.tits, position, lighting = lighting)) #Get hair

        composite_list = [position_size_dict.get(position)]
        for display in displayable_list:
            if isinstance(display, builtins.tuple):
                composite_list.extend(display)
            else:
                composite_list.append((0, 0))
                composite_list.append(display)

        character_composite = Composite(*composite_list)

        if persistent.vren_display_pref in ("Float", "Frame"):
            character_raw_body = im.Composite(position_size_dict.get(position),
                (0, 0), self.body_images.generate_raw_image(self.body_type, self.tits, position),
                #(0, 0), self.expression_images.generate_raw_image(position, emotion, special_modifier = special_modifier),
                self.hair_style.crop_offset_dict.get(position, (0, 0)), self.hair_style.generate_raw_image("standard_body", self.tits, position))

            blurred_image = im.Blur(character_raw_body, 6)
            aura_colour = self.get_display_colour_code()
            recoloured_blur = im.MatrixColor(blurred_image, im.matrix.colorize(aura_colour, aura_colour))

            final_composite = Composite(position_size_dict.get(position), (0, 0), recoloured_blur, (0, 0), character_composite)
        else:
            final_composite = character_composite

        # Create a composite image using all of the display-ables
        if cache_item:
            character_cache[disp_key] = Flatten(final_composite)
            return character_cache[disp_key]
        return Flatten(final_composite)

    # NOTE: Instead of directly drawing a character, use Scene() and Actor() class for drawing.
    def draw_person(self, position: str = "default", emotion: str | None = None, special_modifier: str | None = None, show_person_info = True, lighting = None,
            draw_layer = "solo", display_transform = None, display_zorder: int = 0, wipe_scene = True): #Draw the person, standing as default if they aren't standing in any other position
        validate_texture_memory()
        if position == "default" or position is None:
            position = self.idle_pose

        if emotion is None:
            emotion = self.get_emotion()

        if display_transform is None:
            display_transform = character_right

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        at_arguments = [display_transform, scale_person(self.height)]

        self.hide_person(draw_layer = draw_layer)
        if wipe_scene:
            clear_scene() #Make sure no other characters are drawn either.
            if show_person_info:
                renpy.show_screen("person_info_ui", self)

        renpy.show(str(self.identifier), at_list=at_arguments, layer = draw_layer, what = self.build_person_displayable(position, emotion, special_modifier, lighting), zorder = display_zorder, tag = str(self.identifier))

    def hide_person(self, draw_layer = "solo"): #Hides the person. Makes sure to hide all possible known tags for the character.
        # We keep track of tags used to display a character so that they can always be unique, but still tied to them so they can be hidden
        renpy.hide(str(self.identifier), draw_layer)
        renpy.hide(str(self.identifier) + "_old", draw_layer)

    def draw_animated_removal(self, clothing: Clothing, position: str = "default", emotion: str | None = None, show_person_info = True, special_modifier: str | None = None, lighting: list[float] | None = None, half_off_instead = False,
            draw_layer = "solo", display_transform = None, display_zorder: int = 0, wipe_scene = True, scene_manager: Scene | None = None):
        if clothing is None:  #we need something to take off
            renpy.say("WARNING", "Draw animated removal called without passing a clothing item.")
            return

        if self.outfit is None:
            renpy.say("WARNING", self.name + " is not wearing any outfit to remove an item from, aborting draw animated removal.")
            return

        if position == "default" or position is None:
            position = self.idle_pose

        if emotion is None:
            emotion = self.get_emotion()

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        if display_transform is None: # make sure we don't need to pass the position with each draw
            display_transform = character_right

        at_arguments = [display_transform, scale_person(self.height)]

        if wipe_scene:
            clear_scene()

        if scene_manager is None:
            if show_person_info:
                renpy.show_screen("person_info_ui", self)
        else:   # when we are called from the scene manager we have to draw the other characters
            scene_manager.draw_scene(exclude_list = [self])

        bottom_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False) # needs to be flattened for fade to work correctly
        if clothing.can_be_half_off and half_off_instead:
            self.outfit.half_off_clothing(clothing) #Half-off the clothing
        else:
            self.outfit.remove_clothing(clothing) #Remove the clothing
        top_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False)

        self.hide_person()

        renpy.show(str(self.identifier), at_list=at_arguments, layer = draw_layer, what = top_displayable, zorder = display_zorder, tag = str(self.identifier))
        renpy.show(str(self.identifier) + "_old", at_list= at_arguments + [clothing_fade], layer = draw_layer, what = bottom_displayable, zorder = display_zorder + 1, tag = str(self.identifier) + "_old") #Overlay old and blend out

        renpy.pause(1.2) # slight pause between animations

    def draw_quick_removal(self, clothing: Clothing, position: str = "default", emotion: str | None = None, special_modifier: str | None = None, lighting: list[float] | None = None, show_person_info = True,
            half_off_instead = False, draw_layer = "solo", display_transform = None, display_zorder: int = 0, wipe_scene = True, scene_manager: Scene | None = None):

        if clothing is None:  #we need something to take off
            renpy.say("WARNING", "Draw animated removal called without passing a clothing item.")
            return

        if self.outfit is None:
            renpy.say("WARNING", self.name + " is not wearing any outfit to remove an item from, aborting draw animated removal.")
            return

        if position == "default" or position is None:
            position = self.idle_pose

        if emotion is None:
            emotion = self.get_emotion()

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        if display_transform is None: # make sure we don't need to pass the position with each draw
            display_transform = character_right

        at_arguments = [display_transform, scale_person(self.height)]

        if wipe_scene:
            clear_scene()

        if scene_manager is None:
            if show_person_info:
                renpy.show_screen("person_info_ui", self)
        else:
            scene_manager.draw_scene(exclude_list = [self])

        bottom_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False) # needs to be flattened for fade to work correctly
        if clothing.can_be_half_off and half_off_instead:
            self.outfit.half_off_clothing(clothing) #Half-off the clothing
        else:
            self.outfit.remove_clothing(clothing) #Remove the clothing
        top_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False)

        self.hide_person()

        renpy.show(str(self.identifier), at_list=at_arguments, layer = draw_layer, what = top_displayable, zorder = display_zorder, tag = str(self.identifier))
        renpy.show(str(self.identifier) + "_old", at_list= at_arguments + [fast_clothing_fade], layer = draw_layer, what = bottom_displayable, zorder = display_zorder + 1, tag = str(self.identifier) + "_old") #Overlay old and blend out

        renpy.pause(0.7) # slight pause between animations

    def draw_quick_addition(self, clothing: Clothing, position: str = "default", emotion: str | None = None, special_modifier: str | None = None, lighting: list[float] | None = None,
            draw_layer = "solo", display_transform = None, display_zorder: int = 0, add_function = None):

        if add_function is None:
            renpy.say("WARNING", "Draw animation requires and add_function, to add item to correct body part.")
            return

        if clothing is None:  #we need something to take off
            renpy.say("WARNING", "Draw animated removal called without passing a clothing item.")
            return

        if self.outfit is None:
            renpy.say("WARNING", self.name + " is not wearing any outfit to remove an item from, aborting draw animated removal.")
            return

        if position == "default" or position is None:
            position = self.idle_pose

        if emotion is None:
            emotion = self.get_emotion()

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        if display_transform is None: # make sure we don't need to pass the position with each draw
            display_transform = character_right

        at_arguments = [display_transform, scale_person(self.height)]

        if not isinstance(clothing, list):  # convert clothing to list, if not already
            clothing = [clothing]

        bottom_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False)
        for cloth in clothing:
            add_function(cloth)
        top_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False) # needs to be flattened for fade to work correctly

        self.hide_person()

        renpy.show(str(self.identifier), at_list=at_arguments, layer = draw_layer, what = top_displayable, zorder = display_zorder, tag = str(self.identifier))
        renpy.show(str(self.identifier) + "_old", at_list= at_arguments + [fast_clothing_fade], layer = draw_layer, what = bottom_displayable, zorder = display_zorder + 1, tag = str(self.identifier) + "_old") #Overlay old and blend out

        renpy.pause(0.7)

    def quick_draw_slide_back(self, clothing: Clothing, position: str = "default", emotion: str | None = None, special_modifier: str | None = None, lighting: list[float] | None = None,
            draw_layer = "solo", display_transform = None, display_zorder: int = 0):

        if clothing is None:  #we need something to take off
            renpy.say("WARNING", "Draw animated removal called without passing a clothing item.")
            return

        if self.outfit is None:
            renpy.say("WARNING", self.name + " is not wearing any outfit to remove an item from, aborting draw animated removal.")
            return

        if position == "default" or position is None:
            position = self.idle_pose

        if emotion is None:
            emotion = self.get_emotion()

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        if display_transform is None: # make sure we don't need to pass the position with each draw
            display_transform = character_right

        at_arguments = [display_transform, scale_person(self.height)]

        if not isinstance(clothing, list):  # convert clothing to list, if not already
            clothing: list[Clothing] = [clothing]

        bottom_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False)
        for cloth in clothing:
            cloth.half_off = False
        top_displayable = self.build_person_displayable(position, emotion, special_modifier, lighting, cache_item = False) # needs to be flattened for fade to work correctly

        self.hide_person()

        renpy.show(str(self.identifier), at_list=at_arguments, layer = draw_layer, what = top_displayable, zorder = display_zorder, tag = str(self.identifier))
        renpy.show(str(self.identifier) + "_old", at_list= at_arguments + [fast_clothing_fade], layer = draw_layer, what = bottom_displayable, zorder = display_zorder + 1, tag = str(self.identifier) + "_old") #Overlay old and blend out

        renpy.pause(0.7)

    def get_emotion(self): # Get the emotion state of a character, used when the persons sprite is drawn and no fixed emotion is required.
        if self.arousal >= self.max_arousal:
            return "orgasm"
        if self.happiness > 120:
            return "happy"
        if self.happiness < 80:
            if self.love > 0:
                return "sad"
            return "angry"

        return "default"

    def call_dialogue(self, label_name: str, *args, **kwargs): #Passes the parameter along to the persons personality and gets the correct dialogue for the event if it exists in the dict.
        if label_name == "sex_review" and kwargs.get("the_report", {}).get("is_angry", False):
            renpy.say(self, "Now leave me alone, I'm done.")
        else:
            # when not wearing condom, call the appropriate taboo break dialog
            if not mc.condom:
                if label_name == "cum_vagina" and self.has_taboo("creampie"):
                    label_name = "creampie_taboo_break"
                if label_name == "cum_anal" and self.has_taboo("anal creampie"):
                    label_name = "anal_creampie_taboo_break"

            self.personality.get_dialogue(self, label_name, *args, **kwargs)

    def get_known_opinion_score(self, topic) -> int:
        the_topic = self.get_opinion_topic(topic)
        if the_topic is None:
            return 0
        if the_topic[1]:
            return the_topic[0]
        return 0

    def get_known_opinion_list(self, include_sexy = False, include_normal = True, only_positive = False, only_negative = False): #Gets the topic string of a random opinion this character holds. Includes options to include known opinions and sexy opinions. Returns None if no valid opinion can be found.
        the_dict = {} #Start our list of valid opinions to be listed as empty

        if include_normal: #if we include normal opinions build a dict out of the two
            the_dict = dict(the_dict, **self.opinions)

        if include_sexy: #If we want sexy opinions add them in too.
            the_dict = dict(the_dict, **self.sexy_opinions)

        known = [topic for topic, opinion in the_dict.items() if opinion[1]]
        if only_positive:
            return [x for x in known if self.opinion(x) > 0]

        if only_negative:
            return [x for x in known if self.opinion(x) < 0]

        return known

    @property
    def has_unknown_opinions(self) -> bool:
        return self.has_unknown_normal_opinions or self.has_unknown_sexy_opinions

    @property
    def has_unknown_normal_opinions(self) -> bool:
        return any(x for x, opinion in self.opinions.items() if opinion[0] != 0 and not opinion[1])

    @property
    def has_unknown_sexy_opinions(self) -> bool:
        return any(x for x, opinion in self.sexy_opinions.items() if opinion[0] != 0 and not opinion[1])

    def get_opinion_score(self, topic: str | Iterable[str]) -> int: #Like get_opinion_topic, but only returns the score and not a tuple. Use this when determining a persons reaction to a relevant event.
        '''
        Returns score of topic range[-2, 2]
        When topic is an iterable, sums scores of all topics in the iterable
        '''
        if isinstance(topic, str):
            if topic in self.opinions:
                return self.opinions[topic][0]
            if topic in self.sexy_opinions:
                return self.sexy_opinions[topic][0]

        if isinstance(topic, (list, tuple, set)):
            return sum(self.get_opinion_score(a_topic) for a_topic in topic)
        return 0

    def get_opinion_topics_list(self, include_unknown = True, include_normal = True, include_sexy = True, include_hate = True, include_dislike = True, include_like = True, include_love = True):
        opinion_return_list = []
        if include_normal:
            for topic, opinion in self.opinions.items():
                if opinion[1] or include_unknown:
                    if opinion[0] == -2 and include_hate:
                        opinion_return_list.append(topic)
                    elif opinion[0] == -1 and include_dislike:
                        opinion_return_list.append(topic)
                    elif opinion[0] == 1 and include_like:
                        opinion_return_list.append(topic)
                    elif opinion[0] == 2 and include_love:
                        opinion_return_list.append(topic)
        if include_sexy:
            for topic, opinion in self.sexy_opinions.items():
                if opinion[1] or include_unknown:
                    if opinion[0] == -2 and include_hate:
                        opinion_return_list.append(topic)
                    elif opinion[0] == -1 and include_dislike:
                        opinion_return_list.append(topic)
                    elif opinion[0] == 1 and include_like:
                        opinion_return_list.append(topic)
                    elif opinion[0] == 2 and include_love:
                        opinion_return_list.append(topic)
        return opinion_return_list

    def get_opinion_topic(self, topic: str) -> list[int, bool] | None:
        '''
        Returns: opinion structure [score, known]
        If passed topic does not exist, returns None
        '''
        if topic in self.opinions:
            return self.opinions[topic]

        if topic in self.sexy_opinions:
            return self.sexy_opinions[topic]

        return None

    def get_random_opinion(self, include_known = True, include_sexy = False, include_normal = True, only_positive = False, only_negative = False): #Gets the topic string of a random opinion this character holds. Includes options to include known opinions and sexy opinions. Returns None if no valid opinion can be found.
        the_dict = {} #Start our list of valid opinions to be listed as empty

        if include_normal: #if we include normal opinions build a dict out of the two
            the_dict = dict(the_dict, **self.opinions)

        if include_sexy: #If we want sexy opinions add them in too.
            the_dict = dict(the_dict, **self.sexy_opinions)

        if not include_known: #If we do not want to talk about known values
            known_keys = [topic for topic, opinion in the_dict.items() if opinion[1]]
            for del_key in known_keys:
                del the_dict[del_key]

        if only_positive or only_negative: # Lets us filter opinions so they only include positive or negative ones.
            remove_keys = []
            if only_positive:
                remove_keys.extend(topic for topic in the_dict if self.opinion(topic) < 0)

            if only_negative:
                remove_keys.extend(topic for topic in the_dict if self.opinion(topic) > 0)

            for del_key in remove_keys:
                del the_dict[del_key]

        if the_dict:
            return get_random_from_list(list(the_dict.keys())) #If we have something in the list we can return the topic string we used as a key for it. This can then be used with get_opinion_score to get the actual opinion
        return None #If we have nothing return None, make sure to deal with this when we use this function.

    def favourite_opinion(self, topics: tuple[str]) -> str:
        '''
        Returns the opinion with the highest score from the list of topics.
        If multiple opinions have the same score, one is chosen at random.
        '''
        for score in range(2, -3, -1):
            values = [x for x in topics if self.get_opinion_score(x) == score]
            if values:
                return get_random_from_list(values)
        return get_random_from_list(topics)

    def discover_opinion(self, topic: str, add_to_log = True): #topic is a string matching the topics given in our random list (ie. "the colour blue"). If the opinion is in either of our opinion dicts we will set it to known, otherwise we do nothing. Returns True if the opinion was updated, false if nothing was changed.
        updated = False
        if topic in self.opinions:
            if not self.opinions[topic][1]:
                updated = True
                if add_to_log:
                    mc.stats.change_tracked_stat("Girl", "Opinion Discovered", 1)
            self.opinions[topic][1] = True

        if topic in self.sexy_opinions:
            if not self.sexy_opinions[topic][1]:
                updated = True
                if add_to_log:
                    mc.stats.change_tracked_stat("Girl", "Sexy Opinion Discovered", 1)
            self.sexy_opinions[topic][1] = True

        if updated and add_to_log and self.title is not None:
            mc.log_event(f"Discovered: {self.display_name} {opinion_score_to_string(self.opinion(topic))} {topic}", "float_text_grey")

        return updated

    def discover_random_opinion(self, include_normal = True, include_sexy = False):
        topic = self.get_random_opinion(include_known = False, include_normal = include_normal, include_sexy = include_sexy)
        if topic:
            self.discover_opinion(topic)

    def set_opinion(self, topic: str, score: int, known = False): #override function to set an opinion to a known value, mainly used to set up characters before they are introduced
        if topic in self.get_sexy_opinions_list():
            self.sexy_opinions[topic] = [score, known]
        else:
            self.opinions[topic] = [score, known]

    def remove_opinion(self, topic: str):
        if topic in self.sexy_opinions:
            self.sexy_opinions.pop(topic, None)
        elif topic in self.opinions:
            self.opinions.pop(topic, None)

    def update_opinion_with_score(self, topic: str, score: int, add_to_log = True):
        if topic in Person._sexy_opinions_list:
            if topic in self.sexy_opinions:
                self.sexy_opinions[topic][0] = score
            else:
                self.sexy_opinions[topic] = [score, add_to_log]

        if topic in Person._opinions_list:
            if topic in self.opinions:
                self.opinions[topic][0] = score
            else:
                self.opinions[topic] = [score, add_to_log]

        if add_to_log:
            self.discover_opinion(topic, False)
            mc.log_event(f"{self.display_name} {opinion_score_to_string(score)} {topic}", "float_text_blue")

    def strengthen_opinion(self, topic: str, add_to_log = True):
        old_opinion = self.get_opinion_topic(topic)
        if old_opinion is None or old_opinion[0] == 0: #You cannot strengthen an opinion of 0, for that make a new one entirely.
            return False

        updated = False
        if old_opinion[0] == 1 or old_opinion[0] == -1:
            updated = True
            new_opinion_value = 2 * old_opinion[0]
            if topic in self.opinions:
                self.opinions[topic] = [new_opinion_value, old_opinion[1]]
            else:
                self.sexy_opinions[topic] = [new_opinion_value, old_opinion[1]]

        if add_to_log and updated:
            mc.log_event(f"{self.display_name} {opinion_score_to_string(self.opinion(topic))} {topic}", "float_text_blue")
        return updated

    def increase_opinion_score(self, topic: str, max_value = 2, add_to_log = True, weighted = False):
        score = self.opinion(topic)

        if score >= 2 or score >= max_value:
            return

        if not weighted or renpy.random.randint(0, 100) < self.suggestibility:
            self.update_opinion_with_score(topic, score + 1, add_to_log)

    def weaken_opinion(self, topic: str, add_to_log = True):
        old_opinion = self.get_opinion_topic(topic)
        if old_opinion is None or old_opinion[0] == 0: #You cannot weaken an opinion of 0, for that make a new one entirely.
            return False

        updated = False
        if old_opinion[0] == 2 or old_opinion[0] == -2:
            updated = True
            new_opinion_value = old_opinion[0] // 2
            if topic in self.opinions:
                self.opinions[topic] = [new_opinion_value, old_opinion[1]]
            else:
                self.sexy_opinions[topic] = [new_opinion_value, old_opinion[1]]

        else: #ie it was -1 or 1, because 0 already returned
            updated = True
            if topic in self.opinions:
                self.opinions[topic] = [0, old_opinion[1]]
            elif topic in self.sexy_opinions:
                self.sexy_opinions[topic] = [0, old_opinion[1]]

        if add_to_log and updated:
            mc.log_event(f"{self.display_name} {opinion_score_to_string(self.opinion(topic))} {topic}", "float_text_blue")

        return updated

    def decrease_opinion_score(self, topic: str, add_to_log = True):
        score = self.opinion(topic)

        if score > -2:
            self.update_opinion_with_score(topic, score - 1, add_to_log)

    def max_opinion_score(self, topic: str, add_to_log = True):
        score = self.opinion(topic)
        if score != 2:
            self.update_opinion_with_score(topic, 2, add_to_log)

    def create_opinion(self, topic: str, start_positive = True, start_known = True, add_to_log = True):
        start_value = 1
        if not start_positive:
            start_value = -1 #Determines if the opinion starts as like or dislike.
        if self.opinion(topic) != 0: #She already has an opinion
            return False

        opinion_tuple = [start_value, start_known]
        if topic in self.get_sexy_opinions_list():
            self.sexy_opinions[topic] = opinion_tuple
        else:
            self.opinions[topic] = opinion_tuple

        if add_to_log:
            mc.log_event(f"{self.display_name} {opinion_score_to_string(self.opinion(topic))} {topic}", "float_text_blue")
        return True

    def add_opinion(self, topic: str, score: int, known = None, sexy_opinion = None, add_to_global = False, add_to_log = True):
        if known is None and topic in self.opinions:
            sexy_opinion = False # override passed value
            known = self.opinions[topic][1]

        if known is None and topic in self.sexy_opinions:
            sexy_opinion = True # override passed value
            known = self.sexy_opinions[topic][1]

        if known is None:
            known = False

        if sexy_opinion is None: # check global list
            sexy_opinion = False
            if topic in Person._sexy_opinions_list:
                sexy_opinion = True

        if sexy_opinion:
            self.sexy_opinions[topic] = [score, known]

            if add_to_global and topic not in Person._sexy_opinions_list:
                Person._sexy_opinions_list.append(topic)
        else:
            self.opinions[topic] = [score, known]
            if add_to_global and topic not in Person._opinions_list:
                Person._opinions_list.append(topic)

        if add_to_log:
            mc.log_event(f"{self.display_name} {opinion_score_to_string(score)} {topic}", "float_text_blue")

    def has_opinion(self, topic: str) -> bool:
        return topic in self.opinions or topic in self.sexy_opinions

    def reset_opinions(self):
        self.opinions.clear()

    def reset_sexy_opinions(self):
        self.sexy_opinions.clear()

    @property
    def hated_color_opinions(self) -> list[str]:
        return [x for x in WardrobeBuilder.color_prefs if self.opinion(x) == -2]

    @property
    def loved_color_opinions(self) -> list[str]:
        return [x for x in WardrobeBuilder.color_prefs if self.opinion(x) == 2]

    @property
    def hated_outfit_opinions(self) -> list[str]:
        return [x for x in WardrobeBuilder.preferences if self.opinion(x) == -2]

    @property
    def loved_outfit_opinions(self) -> list[str]:
        return [x for x in WardrobeBuilder.preferences if self.opinion(x) == 2]

    def has_taboo(self, taboos) -> bool:
        if taboos is None:
            return False

        if isinstance(taboos, str):
            taboos = [taboos]

        return any(x for x in taboos if x not in self.broken_taboos)

    def has_broken_taboo(self, taboos) -> bool:
        if taboos is None:
            return False

        if isinstance(taboos, str):
            taboos = [taboos]

        return any(x for x in taboos if x in self.broken_taboos)

    def break_taboo(self, the_taboo: str, add_to_log = True, fire_event = True):
        if the_taboo == "kissing":
            mc.listener_system.fire_event("sex_event", the_person = self, the_position = kissing, the_object = make_floor())

        if the_taboo in self.broken_taboos:
            return False

        mc.stats.change_tracked_stat("Corruption", "Taboo Breaks", 1)

        self.broken_taboos.append(the_taboo)
        self.change_novelty(5, add_to_log = add_to_log)

        if add_to_log:
            mc.log_event(f"{the_taboo.replace('_', ' ').title()} taboo broken with {self.display_name}!", "float_text_red")

        if fire_event:
            mc.listener_system.fire_event("girl_taboo_break", the_taboo = the_taboo)
        return True

    def restore_taboo(self, the_taboo: str, add_to_log = True) -> bool:
        if the_taboo not in self.broken_taboos:
            return False

        while the_taboo in self.broken_taboos:
            self.broken_taboos.remove(the_taboo)

        if add_to_log:
            mc.log_event(f"{the_taboo.replace('_', ' ').title()} taboo reasserted with {self.display_name}!", "float_text_red")
        return True

    def pick_position_comment(self, the_report): #Takes a report and has the person pick the most notable thing out of it. Generally used to then have them comment on it.
        highest_slut_position = None
        highest_slut_opinion = 0
        for position in the_report.get("positions_used", []):
            slut_opinion = position.slut_requirement
            slut_opinion += (5 * self.opinion(position.opinion_tags))
            if highest_slut_position is None or slut_opinion > highest_slut_opinion:
                highest_slut_position = position
                highest_slut_opinion = slut_opinion

        return highest_slut_position

    def update_person_sex_record(self, report_log: dict):
        types_seen = []
        position_type: Position
        for position_type in report_log.get("positions_used", []):
            if position_type.record_class and position_type.record_class not in types_seen:
                if position_type.record_class not in self.sex_record: # add missing sex_record key
                    self.sex_record[position_type.record_class] = 0
                self.sex_record[position_type.record_class] += 1
                types_seen.append(position_type.record_class)

        tier = self.suggest_tier
        gained_skill = False    # only one skill per session
        gained_opinion = False  # only one opinion per session
        renpy.random.shuffle(types_seen) # shuffle record classes so we don't know what skills and opinions are checked for increment first
        for record_class in types_seen:
            if not gained_skill and record_class in Person._record_skill_map and renpy.random.randint(0, 100) < 5 + (tier * 5):
                self.increase_sex_skill(Person._record_skill_map[record_class], 2 + tier)
                gained_skill = True
            if not gained_opinion and record_class in Person._record_opinion_map and renpy.random.randint(0, 100) < 15 + (tier * 5):
                self.increase_opinion_score(get_random_from_list(Person._record_opinion_map[record_class]), tier - 1)
                gained_opinion = True

        # Record the total number of orgasms for the girl
        self.sex_record["Orgasms"] = self.sex_record.get("Orgasms", 0) + report_log.get("girl orgasms", 0)
        # Record number of times public sex
        if report_log.get("was_public", False):
            self.sex_record["Public Sex"] = self.sex_record.get("Public Sex", 0) + 1
            self.set_event_day("LastExhibitionFetish")

        # record the last time we had sex
        self.sex_record["Last Sex Day"] = day

    @property
    def current_planned_outfit(self):
        if self.is_at_work and self.current_job.planned_uniform:
            return self.current_job.planned_uniform

        if limited_wardrobes.should_use_limited_wardrobe(self):
            return limited_wardrobes.decide_on_outfit(self, allow_personal_wardrobe = False)

        return self.planned_outfit

    @current_planned_outfit.setter
    def current_planned_outfit(self, outfit: Outfit):
        '''
        Sets current planned outfit, when at work changes her planned uniform,
        always creates a copy of the passed outfit to prevent changes to original passed outfit
        '''
        if isinstance(outfit, Outfit):
            if self.is_at_work and self.current_job.planned_uniform:
                self.current_job.planned_uniform = outfit.get_copy()
            elif limited_wardrobes.should_use_limited_wardrobe(self):
                limited_wardrobes.update_outfit(self, outfit.get_copy())
            else:
                self.planned_outfit = outfit.get_copy()

    def add_outfit(self, outfit: Outfit, outfit_type = "full"):
        if outfit_type == "under":
            self.wardrobe.add_underwear_set(outfit)
        elif outfit_type == "over":
            self.wardrobe.add_overwear_set(outfit)
        else: #outfit_type = full
            self.wardrobe.add_outfit(outfit)

    def decide_on_outfit(self, sluttiness_modifier = 0.0) -> Outfit:
        return self.wardrobe.decide_on_outfit(self, sluttiness_modifier)

    def get_random_appropriate_outfit(self, sluttiness_limit: int = None, sluttiness_min = 0, guarantee_output = False) -> Outfit | None:
        outfit = self.wardrobe.get_random_appropriate_outfit(sluttiness_limit = sluttiness_limit or self.effective_sluttiness(), sluttiness_min = sluttiness_min, guarantee_output = guarantee_output, preferences = WardrobePreference(self))
        if guarantee_output and (not outfit or outfit.name == "Nothing"): # when no outfit and we need one, generate one
            outfit = Wardrobe.generate_random_appropriate_outfit(self, sluttiness_limit = sluttiness_limit or self.effective_sluttiness())
        return outfit

    def get_random_appropriate_underwear(self, sluttiness_limit: int = None, sluttiness_min = 0, guarantee_output = False) -> Outfit | None:
        outfit = self.wardrobe.get_random_appropriate_underwear(sluttiness_limit = sluttiness_limit or self.effective_sluttiness(), sluttiness_min = sluttiness_min, guarantee_output = guarantee_output, preferences = WardrobePreference(self))
        if guarantee_output and (not outfit or outfit.name == "Nothing"): # when no outfit and we need one, generate one
            outfit = Wardrobe.generate_random_appropriate_outfit(self, outfit_type = "under", sluttiness_limit = sluttiness_limit or self.effective_sluttiness())
        return outfit

    def get_random_appropriate_overwear(self, sluttiness_limit: int = None, sluttiness_min = 0, guarantee_output = False) -> Outfit | None:
        outfit = self.wardrobe.get_random_appropriate_overwear(sluttiness_limit = sluttiness_limit or self.effective_sluttiness(), sluttiness_min = sluttiness_min, guarantee_output = guarantee_output, preferences = WardrobePreference(self))
        if guarantee_output and (not outfit or outfit.name == "Nothing"): # when no outfit and we need one, generate one
            outfit = Wardrobe.generate_random_appropriate_outfit(self, outfit_type = "over", sluttiness_limit = sluttiness_limit or self.effective_sluttiness())
        return outfit

    def personalize_outfit(self, outfit, opinion_color = None, coloured_underwear = True, main_colour = None, swap_bottoms = False, allow_skimpy = True) -> Outfit:
        return WardrobeBuilder(self).personalize_outfit(outfit, opinion_color = opinion_color, coloured_underwear = coloured_underwear, main_colour = main_colour, swap_bottoms = swap_bottoms, allow_skimpy = allow_skimpy)

    def apply_outfit_bottom_preference(self, outfit: Outfit, force_swap: bool = False):
        '''
        if the bottom clothing (pants/skirt) of the passed outfit does not match her preference
        the bottom clothing is swapped to match her preference
        When Force Swap is True the bottom clothing item will be swapped regardless of preference
        The swapped items will have a comparable sluttiness value
        '''
        if (force_swap
                or (outfit.has_pants and self.opinion.skirts > self.opinion.pants)
                or (outfit.has_skirt and self.opinion.pants > self.opinion.skirts)):
            outfit.swap_outfit_bottoms()

    def set_sexier_panties(self, outfit: Outfit, the_color: list[float] = None, min_slut = None, max_slut = None) -> bool:
        '''
        Updates passed outfit with sexier panties applying a new colour if the_color is not None
        When no slut values are passed the min/max values for her current sluttiness are used
        '''
        if not (min_slut and max_slut):
            (min_slut, max_slut) = WardrobeBuilder.get_clothing_min_max_slut_value(self.sluttiness)

        panties = outfit.get_panties()
        if panties and (panties.is_extension or panties.slut_value >= min_slut):
            return False

        new_panties: Clothing = get_random_from_list([x for x in panties_list if x.slut_value >= min_slut and x.slut_value <= max_slut])
        if not new_panties:
            new_panties = get_random_from_list([thong, tiny_g_string, strappy_panties, string_panties, crotchless_panties])

        if new_panties:
            if panties and the_color is None:
                new_panties.colour = panties.colour
            else:
                bra = outfit.get_bra()
                if bra and the_color is None:
                    the_color = bra.colour

                new_panties.colour = the_color or WardrobeBuilder.get_color_from_opinion_color(self.favourite_colour)
                if panties:
                    new_panties.transparency = panties.transparency   # preserve original alpha

            if panties:
                outfit.remove_clothing(panties)
            outfit.add_lower(new_panties)
            return True
        return False

    def set_sexier_bra(self, outfit: Outfit, the_color: list[float] = None, allow_remove_bra = True, min_slut = None, max_slut = None) -> bool:
        '''
        Updates passed outfit with sexier bra applying a new colour if the_color is not None
        When no slut values are passed the min/max values for her current sluttiness are used
        '''
        bra = outfit.get_bra()
        if bra and bra.has_extension: # one-piece
            return False

        if not (min_slut and max_slut):
            (min_slut, max_slut) = WardrobeBuilder.get_clothing_min_max_slut_value(self.sluttiness)

        if bra and bra.slut_value >= min_slut:
            return False

        if allow_remove_bra and not outfit.get_panties():   # also remove bra if not wearing panties
            outfit.remove_clothing(bra)
            return True

        new_bra = get_random_from_list([x for x in real_bra_list if x.slut_value >= min_slut and x.slut_value <= max_slut])
        if not new_bra:
            new_bra = get_random_from_list([lace_bra, thin_bra, strappy_bra, quarter_cup_bustier])

        if new_bra:
            if the_color is None and bra:
                new_bra.colour = bra.colour
            else:
                panties = outfit.get_panties()
                if the_color is None and panties:
                    the_color = panties.colour

                new_bra.colour = the_color or WardrobeBuilder.get_color_from_opinion_color(self.favourite_colour)
                if bra:
                    new_bra.colour[3] = bra.colour[3]   # preserve alpha

            if bra:
                outfit.remove_clothing(bra)
            outfit.add_upper(new_bra)
            return True
        return False

    @property
    def is_wearing_uniform(self) -> bool:
        if not self.is_at_work:
            return False #If no uniform is set you aren't wearing one at all.

        if self.is_wearing_forced_uniform:
            return True

        return (self.should_wear_uniform and self.current_job.planned_uniform
                and self.outfit == self.current_job.planned_uniform
                and self.planned_outfit != self.current_job.planned_uniform)

    @property
    def is_wearing_forced_uniform(self):
        if not self.is_at_work:
            return False

        return self.current_job.forced_uniform and self.current_job.forced_uniform == self.outfit

    @property
    def should_wear_uniform(self) -> bool:
        if not self.is_at_work:  # quick exit
            return False

        if self.current_job.forced_uniform:
            return True

        if self.is_at_job(waitress_job):    # jobs with mandatory clothing but no specific uniform
            return True

        wardrobe = self.current_job.wardrobe
        if not wardrobe or not wardrobe.has_outfits:
            return False

        if self.is_at_job((stripper_job, stripclub_stripper_job, stripclub_waitress_job, stripclub_bdsm_performer_job, stripclub_manager_job, stripclub_mistress_job)):
            return not strip_club_is_closed()

        if (self.is_employee or self.is_intern) and self.is_at_office:
            # only when uniform policy is active
            if not strict_uniform_policy.is_active:
                return False
            # Casual Fridays for employees only
            if day % 7 == 4 and casual_friday_uniform_policy.is_active:
                return False

        return True

    @property
    def is_wearing_dress_code(self) -> bool:
        if not self.is_at_work:
            return False
        return self.outfit == self.current_job.dress_code_outfit and self.current_job.dress_code_outfit != self.planned_outfit

    @property
    def should_wear_dress_code(self) -> bool:
        if not self.is_at_work or self.should_wear_uniform:  # quick exit
            return False

        if (self.is_employee or self.is_intern) and self.is_at_office:
            # Casual Fridays for employees only
            if not (day % 7 == 4 and casual_friday_uniform_policy.is_active):
                # Check for dress code and whether planned outfit applies
                return dress_code_policy.is_active
        return False

    @property
    def is_wearing_planned_outfit(self) -> bool:
        return not self.outfit.has_half_off_clothing and self.outfit.matches(self.current_planned_outfit)

    def wear_apron(self, main_colour: list[float] = None, pattern: str = None, pattern_colour: list[float] = None, position: str = "default", show_dress_sequence = True, scene_manager: Scene = None):
        '''
        Will remove any overcoat and replace it with an apron
        When no pattern or pattern_colour is set, it will ben a uni-color apron (Plaid)
        main_colour: When none use person favourite colour
        Valid patterns: 'Plaid' | 'Pattern_1'
        position: only used when show_dress_sequence = True and no scene_manager passed
        scene_manager: pass active scene_manager when show_dress_sequence = True
        '''
        self.outfit.remove_overcoat()
        if not main_colour or len(main_colour) < 4:
            main_colour = WardrobeBuilder.get_color_from_opinion_color(self.favourite_colour)
            main_colour[3] = .9 # slightly transparent

        new_outfit = self.outfit.get_copy()
        if pattern and len(pattern_colour) == 4:
            new_outfit.add_upper(apron.get_copy(), main_colour, pattern, pattern_colour)
        else:
            new_outfit.add_upper(apron.get_copy(), main_colour)

        self.apply_outfit(new_outfit, position = position, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)

    def wear_bathrobe(self, main_colour: list[float] = None, pattern_colour: list[float] = None, position: str = "default", show_dress_sequence = True, scene_manager: Scene = None) -> bool:
        '''
        Will add a bath robe to her current outfit when she is not wearing overwear, else will restore her current outfit
        main_colour: When none use person favourite colour
        colour_pattern: When none choose random contrast colour
        position: only used when show_dress_sequence = True and no scene_manager passed
        scene_manager: pass active scene_manager when show_dress_sequence = True
        Returns True when she put on a bathrobe else False
        '''
        if self.outfit.has_overwear:
            self.apply_planned_outfit(position = position, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)
            return False    # she won't wear a bathrobe when she is wearing clothing

        if not main_colour or len(main_colour) < 4:
            main_colour = WardrobeBuilder.get_color_from_opinion_color(self.favourite_colour)
            main_colour[3] = .9 # slightly transparent
        if not pattern_colour or len(pattern_colour) < 4:
            pattern_colour = renpy.random.choice([[.15, .15, .15, .95], [.95, .95, .95, .9]])
        new_outfit = self.outfit.get_copy()
        new_outfit.add_upper(bath_robe.get_copy(), main_colour, "Pattern_1", pattern_colour)
        self.apply_outfit(new_outfit, position = position, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)
        return True

    def wear_uniform(self, position: str = "default", show_dress_sequence: bool = False, scene_manager: Scene | None = None): #Puts the girl into her uniform, if it exists.
        '''
        When at work, will try to find uniform for current job and wear it
        position: only used when show_dress_sequence = True and no scene_manager passed
        Pass current scene_manager when show_dress_sequence = True
        '''
        if self.is_at_work:
            self.apply_outfit(self.current_job.planned_uniform, position = position, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)

    def apply_outfit(self, outfit: Outfit = None, ignore_base: bool = False, update_taboo: bool = False, show_dress_sequence: bool = False, position: str = "default", scene_manager: Scene | None = None): #Hand over an outfit, we'll take a copy and apply it to the person, along with their base accessories unless told otherwise.
        '''
        Switches to passed outfit
        position: only used when show_dress_sequence = True and no scene_manager passed
        '''
        if outfit is None:
            # put on uniform if required
            if self.should_wear_uniform:
                self.wear_uniform(position = position, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)
                return

            outfit = self.planned_outfit
            if outfit is None:
                return #We don't have a planned outfit, so trying to return to it makes no sense.

        if ignore_base:
            final_outfit = outfit.get_copy()
        else:
            final_outfit = outfit.get_copy().merge_outfit(self.base_outfit)

        final_outfit.restore_all_clothing() # make sure we are not half-off on any item

        if show_dress_sequence:
            if scene_manager:
                scene_manager.show_dress_sequence(self, final_outfit)
            else:
                self.show_dress_sequence(final_outfit, position = position)
        else:
            self.outfit = final_outfit

        if update_taboo: #If True, we assume this outfit is being put on or shown to the MC. It can break taboos about showing underwear, tits, pussy.
            self.update_outfit_taboos()

    def show_dress_sequence(self, outfit: Outfit, position: str = "default", emotion: str = None, special_modifier: str = None, lighting: list[float] = None,
            draw_layer = "solo", display_transform = None, display_zorder: int = 0, scene_manager: Scene | None = None):

        def _dress_sort_key(cloth: Clothing) -> float:
            key = cloth.layer
            if cloth.is_socks:
                key += 1.5  # after underwear
            if cloth.is_shoes:
                key += 3    # after clothes
            return key

        if scene_manager is None:
            clear_scene()
            renpy.show_screen("person_info_ui", self)
        else:
            scene_manager.draw_scene(exclude_list = [self])

        # remove items not in new outfit
        for item in sorted([x for x in self.outfit.upper_body + self.outfit.lower_body + self.outfit.feet if not x.is_extension and not outfit.has_clothing(x)], key = lambda x: x.layer, reverse = True):
            self.draw_quick_removal(item, position = position, emotion = emotion, special_modifier = special_modifier, lighting = lighting, draw_layer = draw_layer, display_transform = display_transform, display_zorder = display_zorder, wipe_scene = False, scene_manager = scene_manager)

        # restore half-off items
        for item in sorted(self.outfit.half_off_clothing_list, key = lambda x: x.layer):
            self.quick_draw_slide_back(item, position = position, emotion = emotion, special_modifier = special_modifier,
                lighting = lighting, draw_layer = draw_layer, display_transform = display_transform, display_zorder = display_zorder)

        outfit_mapping: dict[Clothing, Callable] = {}

        # determine items to add and method for adding it to outfit
        for item in (x for x in outfit.upper_body if not self.outfit.has_clothing(x)):
            outfit_mapping[item] = self.outfit.add_upper
        for item in (x for x in outfit.lower_body if not x.is_extension and not self.outfit.has_clothing(x)):
            outfit_mapping[item] = self.outfit.add_lower
        for item in (x for x in outfit.feet if not self.outfit.has_clothing(x)):
            outfit_mapping[item] = self.outfit.add_feet

        # add items based on redressing order
        for item in sorted(outfit_mapping.keys(), key = lambda x: _dress_sort_key(x)):
            self.draw_quick_addition(item, position = position, emotion = emotion, special_modifier = special_modifier,
                lighting = lighting, draw_layer = draw_layer, display_transform = display_transform, display_zorder = display_zorder,
                add_function = outfit_mapping[item])

        renpy.pause(.2)

        self.outfit = outfit
        # draw final outfit, including correct accessories
        if scene_manager is None:
            self.draw_person(position = position, emotion = emotion, special_modifier = special_modifier, lighting = lighting, draw_layer = draw_layer, display_transform = display_transform, display_zorder = display_zorder)
        else:
            scene_manager.update_actor(self)

    def apply_planned_outfit(self, ignore_base = False, update_taboo = False, position: str = "default", show_dress_sequence: bool = False, scene_manager: Scene | None = None):
        '''
        Switches to location / situation specific outfit
        position: only used when show_dress_sequence = True and no scene_manager passed
        '''
        if self.should_wear_uniform or self.should_wear_dress_code:
            # print(f"{self.name} switches to uniform at location {self.location.name} [{self.current_job.job_title}]")
            self.wear_uniform(position = position, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)
            return

        if limited_wardrobes.should_use_limited_wardrobe(self):
            self.apply_outfit(self.current_planned_outfit, ignore_base = ignore_base, update_taboo = update_taboo, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)
            return

        if not self.planned_outfit: # extra validation to make sure we have a planned outfit
            self.planned_outfit = self.decide_on_outfit()

        # print(f"{self.name} switches to planned outfit at location {self.location.name}")
        self.apply_outfit(self.planned_outfit, ignore_base = ignore_base, update_taboo = update_taboo, show_dress_sequence = show_dress_sequence, scene_manager = scene_manager)

    def approves_outfit_color(self, outfit: Outfit) -> bool:
        return not any(color in self.hated_color_opinions for color in (WardrobeBuilder.get_color_opinion(x.colour) for x in outfit.feet + outfit.lower_body + outfit.upper_body))

    def review_outfit(self, dialogue = True):
        if not self.has_cum_fetish:
            self.outfit.remove_all_cum(from_clothing = False)

        if (not self.is_wearing_planned_outfit
            and (self.location.person_count > 1
                or (self.should_wear_uniform and not self.is_wearing_uniform)
                or (self.should_wear_dress_code and not self.is_wearing_dress_code)
                or not self.judge_outfit(self.outfit))):
            if dialogue:
                self.call_dialogue("clothing_review") # must be last call in function
            else:
                self.apply_planned_outfit()

    def judge_outfit(self, outfit: Outfit, temp_sluttiness_boost: int = 0, use_taboos = True, as_underwear = False, as_overwear = False) -> bool: #Judge an outfit and determine if it's too slutty or not. Can be used to judge other people's outfits to determine if she thinks they look like a slut.
        # temp_sluttiness can be used in situations (mainly crises) where an outfit is allowed to be temporarily more slutty than a girl is comfortable wearing all the time.
        #Returns true if the outfit is wearable, false otherwise
        if not outfit:
            return False

        if as_underwear or as_overwear:
            use_taboos = False

        taboo_modifier = []
        if use_taboos and not (outfit.bra_covered or outfit.panties_covered) and self.has_taboo("underwear_nudity"):
            taboo_modifier.append("underwear_nudity")
        elif use_taboos and outfit.tits_visible and self.has_taboo("bare_tits"):
            taboo_modifier.append("bare_tits")
        elif use_taboos and outfit.vagina_visible and self.has_taboo("bare_pussy"):
            taboo_modifier.append("bare_pussy")

        slut_required = outfit.outfit_slut_score
        if as_underwear:
            slut_required = outfit.underwear_slut_score

        elif as_overwear:
            slut_required = outfit.overwear_slut_score

        if (outfit.get_bra() or outfit.get_panties()) and not as_overwear: #Girls who like lingerie judge outfits with lingerie as less slutty than normal
            lingerie_bonus = 0
            if outfit.bra_is_lingerie: #We consider underwear with an innate sluttiness of 3 or higher "lingerie" rather than just underwear.
                lingerie_bonus += self.opinion.lingerie
            if outfit.panties_is_lingerie:
                lingerie_bonus += self.opinion.lingerie
            lingerie_bonus = builtins.int(lingerie_bonus * 2) # Up to an 8 point swing in either direction
            slut_required += -lingerie_bonus #Treated as less slutty if she likes it, more slutty if she dislikes lingerie

        # Considers the outfit less slutty if she likes showing her tits and ass and that's what it would do.
        if outfit.vagina_visible or outfit.are_panties_visible:
            slut_required += -2 * self.opinion.showing_her_ass

        if outfit.tits_visible or outfit.is_bra_visible:
            slut_required += -2 * self.opinion.showing_her_tits

        if slut_required > (self.effective_sluttiness(taboo_modifier) + temp_sluttiness_boost): #Arousal is important for judging potential changes to her outfit while being stripped down during sex.
            return False
        return True

    def update_outfit_taboos(self) -> bool:
        return_value = False
        if self.tits_visible and self.break_taboo("bare_tits"):
            return_value = True
        if self.vagina_visible and self.break_taboo("bare_pussy"):
            return_value = True
        if (self.outfit.are_panties_visible or self.outfit.is_bra_visible) and self.break_taboo("underwear_nudity"):
            return_value = True
        return return_value

    def give_serum(self, serum: SerumDesign, add_to_log = True):
        if serum is None:
            return #We might have handed over no serum because we aren't producing any and a crisis was looking for one, or something similar.

        mc.stats.change_tracked_stat("Corruption", "Serums Given", 1)
        self.total_serum_count += 1

        # every 20 serums increase tolerance
        if self.total_serum_count % 20 == 0 and self.serum_tolerance < 4:
            self._serum_tolerance += 1
            mc.log_event(f"{self.display_name} serum tolerance increased", "float_text_yellow")

        serum = copy.copy(serum) #Take a copy so we aren't touching the reference we are handed.
        self.serum_effects.append(serum)
        serum.run_on_apply(self, add_to_log)
        mc.listener_system.fire_event("give_random_serum", the_person = self)

    def apply_serum_study(self, add_to_log = True): #Called when the person is studied by the MC. Raises mastery level of all traits used in active serums by 0.2
        updated_traits = [trait.add_mastery(.2) for serum in self.serum_effects for trait in serum.traits]
        if any(updated_traits) and add_to_log:
            mc.log_event(f"Observed {self.display_name}", "float_text_blue")

    def change_suggest(self, amount: int, add_to_log = True): #This changes the base, usually permanent suggest. Use add_suggest_effect to add temporary, only-highest-is-used, suggestion values
        self.suggestibility += amount
        if add_to_log and amount != 0 and self.title:
            mc.log_event(f"{self.display_name}: Suggestibility increased permanently by {amount:+.0f}%", "float_text_blue")

    # monitor that mc serum suggest change amount does not exceed max_amt
    def change_modded_suggestibility(self, amount, max_amt = 30, add_to_log = True):
        if self.event_triggers_dict.get("mod_suggest_amt", 0) >= max_amt:
            return
        change_amount = amount
        if self.event_triggers_dict.get("mod_suggest_amt", 0) + amount > max_amt:
            change_amount = max_amt - self.event_triggers_dict.get("mod_suggest_amt", 0)
        self.change_suggest(change_amount, add_to_log = add_to_log)
        self.event_triggers_dict["mod_suggest_amt"] = self.event_triggers_dict.get("mod_suggest_amt", 0) + change_amount
        return

    def add_suggest_effect(self, amount: int, add_to_log = True):
        if amount > builtins.max(self.suggest_bag or [0]):
            self.change_suggest(-builtins.max(self.suggest_bag or [0]), add_to_log = False) #Subtract the old max and...
            self.change_suggest(amount, add_to_log = False) #add our new suggest.
            if add_to_log and amount != 0 and self.title:
                mc.log_event(f"{self.display_name}: Suggestibility increased, by {amount:.0f}", "float_text_blue")
        # else:
        #     if add_to_log and amount != 0 and self.title:
        #         mc.log_event(f"{self.display_name}: Suggestibility {amount:.0f} lower than current {self.suggestibility} amount. Suggestibility unchanged.", "float_text_blue")
        self.suggest_bag.append(amount) #Add it to the bag, so we can check to see if it is max later.

    def remove_suggest_effect(self, amount: int):
        if amount in self.suggest_bag: # Avoid removing the "amount" if we don't actually have it in the bag.
            self.change_suggest(- builtins.max(self.suggest_bag or [0]), add_to_log = False) #Subtract the max
            self.suggest_bag.remove(amount)
            self.change_suggest(builtins.max(self.suggest_bag or [0]), add_to_log = False) # Add the new max. If we were max, it is now lower, otherwise it cancels out.

    def max_stat_change_calc(self, max_change = 100, serum_check = None, stat_cap = 100):
        def get_max_suggestibility_modifier(suggestibility: int) -> int:
            if suggestibility == 0:
                return 0
            if suggestibility < 20:
                return builtins.int(suggestibility / 5.0)
            if suggestibility < 60:
                return 2 + builtins.int(suggestibility / 10.0)
            if suggestibility < 80:
                return 8 + builtins.int(suggestibility / 20.0)
            return 12

        max_change += get_max_suggestibility_modifier(self.suggestibility)
        if serum_check:
            max_change += (int(max_change * 1.2)) * int(self.active_serum_with_hidden_tag(serum_check))
        max_change = min(max_change, stat_cap)
        return max_change

    def change_love(self, amount: int, max_amount: int = 100, add_to_log = True) -> int:
        if amount == 0:
            return 0
        max_cap = self.max_stat_change_calc(max_change = max_amount, serum_check = "Love", stat_cap = 100)
        amount = builtins.int(amount)

        if amount > 0:
            if self.love > max_cap:
                return 0    # prevent decreasing of love
            # linger effect caused by serum trait (max 20% over calculated maximum)
            # min_change = 1 if self.love < min(100, int(max_amount * 1.2)) and self.active_serum_with_hidden_tag("Love") else 0
            if self.love + amount > max_cap:
                amount = max_cap - self.love

        if self.love + amount < -100:
            amount = -100 - self.love
        elif self.love + amount > 100:
            amount = 100 - self.love

        self.love += amount

        if add_to_log:
            if amount == 0:
                mc.log_event(f"Love limit reached for interaction, Max:({max_cap:.0f}", "float_text_love")
            elif amount < 0:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=red_heart_token_small}}", "float_text_love")
            else:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=red_heart_token_small}}({max_cap:.0f})", "float_text_love")
        return amount

    @property
    def sluttiness(self) -> int:
        return max(min(self._sluttiness + sum(amount for (amount, _) in self.situational_sluttiness.values()), 100), 0)

    def change_slut(self, amount: int, max_amount: int = 100, add_to_log = True) -> int:
        if amount == 0:
            return 0
        max_cap = self.max_stat_change_calc(max_change = max_amount, serum_check = "Slut", stat_cap = 100)

        if amount > 0:
            if self._sluttiness > max_cap:  # prevent decreasing of sluttiness
                return 0
            # linger effect caused by serum trait (max 20% over calculated maximum)
            # min_change = 1 if self._sluttiness < min(100, int(max_amount * 1.2)) and self.active_serum_with_hidden_tag("Slut") else 0
            if self._sluttiness + amount > max_cap:
                amount = max_cap - self._sluttiness

        amount = builtins.int(amount)
        if self._sluttiness + amount < 0:
            amount = -self._sluttiness
        elif self._sluttiness + amount > 100:
            amount = 100 - self._sluttiness

        self._sluttiness += amount

        if add_to_log:
            if amount == 0:
                mc.log_event(f"No Effect on Sluttiness, Max:({max_cap:.0f})", "float_text_slut")
            elif amount < 0:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=gold_heart_token_small}}", "float_text_slut")
            else:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=gold_heart_token_small}}({max_cap:.0f})", "float_text_slut")
        return amount

    def add_situational_slut(self, source: str, amount: int, description = ""):
        self.situational_sluttiness[source] = (amount, description)

    def clear_situational_slut(self, source: str):
        self.situational_sluttiness.pop(source, None)

    def change_happiness(self, amount: int, max_amount: int = 300, add_to_log = True) -> int:
        max_amount = min(max_amount, 300)

        if amount > 0 and self.happiness > max_amount:  # prevent decreasing of happiness
            return 0

        amount = builtins.int(amount * self.trance_multiplier)
        if self.happiness + amount < 0:
            amount = 0 - self.happiness
        if self.happiness + amount > max_amount:
            amount = max_amount - self.happiness

        self.happiness += amount

        if add_to_log and amount != 0:
            mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=happy_token_small}}", "float_text_yellow")
        return amount

    @property
    def obedience(self) -> int:
        return max(min(self._obedience + sum(amount for (amount, _) in self.situational_obedience.values()), 300), 0)

    @obedience.setter
    def obedience(self, value: int):    # consider removal of direct setter
        write_log(f"{self.name} set obedience {value}")
        self._obedience = builtins.int(value)

    def change_obedience(self, amount: int, max_amount: int = 300, add_to_log = True) -> int:
        if amount == 0:
            return 0
        max_cap = self.max_stat_change_calc(max_change = max_amount, serum_check = "Obedience", stat_cap = 300)
        amount = builtins.int(amount)

        if amount > 0:
            if self._obedience > max_cap:
                return 0 # prevent decreasing of obedience
            # linger effect caused by serum trait (max 10% over calculated maximum -> say 140 obed with 10 from suggest would allow for max of 165 (150 + 10% of 150))
            #min_change = 1 if self._obedience < min(300, int(max_amount * 1.1)) and self.active_serum_with_hidden_tag("Obedience") else 0
            if self._obedience + amount > max_cap:
                amount = max_cap - self._obedience

        if self._obedience + amount < 0:
            amount = -self._obedience
        elif self._obedience + amount > max_cap:
            amount = max_cap - self._obedience

        self._obedience += amount

        if add_to_log and amount != 0: #If we don't know the title don't add it to the log, because we know nothing about the person
            if amount < 0:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=triskelion_token_small}}", "float_text_obedience")
            else:
                mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=triskelion_token_small}}({max_cap:.0f})", "float_text_obedience")
        return amount

    def add_situational_obedience(self, source: str, amount: int, description = ""):
        self.situational_obedience[source] = (amount, description)

    def clear_situational_obedience(self, source: str):
        self.situational_obedience.pop(source, None)

    def change_cha(self, amount: int, add_to_log = True) -> int:
        self.charisma += self.charisma_debt #Set our charisma to be our net score
        self.charisma_debt = 0 #We are currently holding no stat debt.

        self.charisma += amount #Adjust our stat now, may be positive or negative.
        if self.charisma < 0:
            self.charisma_debt = self.charisma #If we are less than 0 store it as a debt.
            self.charisma = 0

        if amount != 0 and add_to_log:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Charisma", "float_text_blue")
        return amount

    def change_int(self, amount: int, add_to_log = True) -> int:
        self.int += self.int_debt
        self.int_debt = 0

        self.int += amount
        if self.int < 0:
            self.int_debt = self.int
            self.int = 0

        if amount != 0 and add_to_log:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Intelligence", "float_text_blue")
        return amount

    def change_focus(self, amount: int, add_to_log = True) -> int: #See charisma for full comments
        self.focus += self.focus_debt
        self.focus_debt = 0

        self.focus += amount
        if self.focus < 0:
            self.focus_debt = self.focus
            self.focus = 0

        if amount != 0 and add_to_log:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Focus", "float_text_blue")
        return amount

    def change_hr_skill(self, amount: int, add_to_log = True):
        if amount + self.hr_skill < 0:
            amount = -self.hr_skill #Min 0
        self.hr_skill += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} HR Skill", "float_text_yellow")

    def change_market_skill(self, amount: int, add_to_log = True):
        if amount + self.market_skill < 0:
            amount = -self.market_skill #Min 0
        self.market_skill += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Market Skill", "float_text_yellow")

    @property
    def extra_market_skill(self) -> int:
        '''
        Returns the extra market skill of the person when enhanced by duty
        '''
        if not self.has_duty(work_for_tips_duty):
            return 0

        value = self.foreplay_sex_skill
        if self.sluttiness > 50:
            value += self.oral_sex_skill
        return value

    def change_research_skill(self, amount: int, add_to_log = True):
        if amount + self.research_skill < 0:
            amount = -self.research_skill #Min 0
        self.research_skill += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Research Skill", "float_text_yellow")

    def change_production_skill(self, amount: int, add_to_log = True):
        if amount + self.production_skill < 0:
            amount = -self.production_skill #Min 0
        self.production_skill += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Production Skill", "float_text_yellow")

    def change_supply_skill(self, amount: int, add_to_log = True):
        if amount + self.supply_skill < 0:
            amount = -self.supply_skill #Min 0
        self.supply_skill += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Supply Skill", "float_text_yellow")

    @property
    def research_potential(self):
        result = (3 * self.int) + (self.focus) + (2 * self.research_skill) + 10
        if mc.business.head_researcher:
            bonus_percent = (mc.business.head_researcher.int - 2) * 0.05
            result *= (1.0 + bonus_percent) #Every point above int 2 gives a 5% bonus.
        else:
            result *= 0.9 #No head researcher is treated like int 0.
        return builtins.int(result)

    @property
    def human_resource_potential(self):
        return builtins.int(((3 * self.charisma) + self.int + (2 * self.hr_skill) + 15) / 5)

    @property
    def marketing_potential(self):
        if self.is_employee:
            return builtins.int((3 * self.charisma) + self.focus + (2 * (self.market_skill + self.extra_market_skill)) + 20)
        # for hiring screen assume duty that will apply bonus
        return builtins.int((3 * self.charisma) + self.focus + (2 * (self.market_skill + 5)) + 20)

    @property
    def production_potential(self):
        return builtins.int(((3 * self.focus) + self.int + (2 * self.production_skill) + 10))

    @property
    def supply_potential(self):
        return builtins.int(((5 * self.focus) + (3 * self.charisma) + (3 * self.supply_skill) + 20))

    def increase_work_skill(self, skill: int | str, max_value = 6, add_to_log = True):
        if skill == 0 or skill == "hr_skill":
            self.update_work_skill("hr_skill", min(max_value, self.hr_skill + 1), add_to_log = add_to_log)
        elif skill == 1 or skill == "market_skill":
            self.update_work_skill("market_skill", min(max_value, self.market_skill + 1), add_to_log = add_to_log)
        elif skill == 2 or skill == "research_skill":
            self.update_work_skill("research_skill", min(max_value, self.research_skill + 1), add_to_log = add_to_log)
        elif skill == 3 or skill == "production_skill":
            self.update_work_skill("production_skill", min(max_value, self.production_skill + 1), add_to_log = add_to_log)
        elif skill == 4 or skill == "supply_skill":
            self.update_work_skill("supply_skill", min(max_value, self.supply_skill + 1), add_to_log = add_to_log)

    def decrease_work_skill(self, skill: int | str, add_to_log = True):
        if skill in (0, "hr_skill"):
            self.update_work_skill("hr_skill", max(0, self.hr_skill - 1), add_to_log = add_to_log)
        elif skill in (1, "market_skill"):
            self.update_work_skill("market_skill", max(0, self.market_skill - 1), add_to_log = add_to_log)
        elif skill in (2, "research_skill"):
            self.update_work_skill("research_skill", max(0, self.research_skill - 1), add_to_log = add_to_log)
        elif skill in (3, "production_skill"):
            self.update_work_skill("production_skill", max(0, self.production_skill - 1), add_to_log = add_to_log)
        elif skill in (4, "supply_skill"):
            self.update_work_skill("supply_skill", max(0, self.supply_skill - 1), add_to_log = add_to_log)

    def update_work_skill(self, skill: int | str, score: int, add_to_log = True):
        skill_name = None
        if skill in (0, "hr_skill"):
            skill_name = "HR Skill"
            current = self.hr_skill
        elif skill in (1, "market_skill"):
            skill_name = "Market Skill"
            current = self.market_skill
        elif skill in (2, "research_skill"):
            skill_name = "Research Skill"
            current = self.research_skill
        elif skill in (3, "production_skill"):
            skill_name = "Production Skill"
            current = self.production_skill
        elif skill in (4, "supply_skill"):
            skill_name = "Supply Skill"
            current = self.supply_skill

        if skill_name is None:
            return

        if current == score:
            return
        if skill_name == "HR Skill":
            self.hr_skill = score
        elif skill_name == "Market Skill":
            self.market_skill = score
        elif skill_name == "Research Skill":
            self.research_skill = score
        elif skill_name == "Production Skill":
            self.production_skill = score
        elif skill_name == "Supply Skill":
            self.supply_skill = score

        if add_to_log:
            mc.log_event(f"{self.display_name} {skill_name.lower()} is now at level {score}", "float_text_green")

    def change_sex_skill(self, skill_name: str, amount: int, add_to_log = True):
        '''
        Change sex skill by passed amount -> skill cannot go lower than 0
        skill_name: "Foreplay", "Oral", "Vaginal", "Anal"
        '''
        if skill_name not in self.sex_skills:
            return

        self.update_sex_skill(skill_name, self.sex_skills[skill_name] + amount, add_to_log)

    def increase_sex_skill(self, skill: str, max_value = 5, add_to_log = True):
        '''
        Increase passed sex skill by 1 but not higher than max_value
        skill: "Foreplay", "Oral", "Vaginal", "Anal"
        max_value: maximum value for skill
        '''
        if skill not in self.sex_skills:
            return

        score = self.sex_skills[skill]
        if score < max_value:
            self.update_sex_skill(skill, score + 1, add_to_log)

    def decrease_sex_skill(self, skill: str, add_to_log = True):
        '''
        Decrease passed sex skill by 1 -> skill cannot go lower than 0
        skill: "Foreplay", "Oral", "Vaginal", "Anal"
        '''
        if skill not in self.sex_skills:
            return

        score = self.sex_skills[skill]
        if score > 0:
            self.update_sex_skill(skill, score - 1, add_to_log)

    def update_sex_skill(self, skill: str, score, add_to_log = True):
        '''
        Update sex skill to passed value
        skill: "Foreplay", "Oral", "Vaginal", "Anal"
        score: new value for skill (cannot go lower than 0)
        '''
        if skill not in self.sex_skills:
            return

        current = self.sex_skills[skill]
        if current == score:
            return

        self.sex_skills[skill] = max(score, 0)
        if add_to_log:
            mc.log_event(f"{self.display_name} {skill.lower()} skill is now at level {score}", "float_text_green")

    def change_stats(self, obedience: int | None = None, happiness: int | None = None, arousal: int | None = None, love: int | None = None,
                    slut: int | None = None, max_slut: int = 100, max_love: int = 100, max_obedience: int = 300,
                    energy: int | None = None, novelty: int | None = None, add_to_log = True):
        message = []
        if happiness is not None:
            amount = self.change_happiness(happiness, add_to_log = False)
            if amount != 0:
                message.append(f"{amount:+.0f} {{image=happy_token_small}}")
        if obedience is not None and obedience != 0:
            amount = self.change_obedience(obedience, max_obedience, add_to_log = False)

            max_cap = self.max_stat_change_calc(max_change = max_obedience, serum_check = "Obedience")
            if amount < 0:
                message.append(f"{amount:+.0f} {{image=triskelion_token_small}}")   #Don't show cap if we are subtracting
            else:
                message.append(f"{amount:+.0f} {{image=triskelion_token_small}} ({max_cap:.0f})")
        if arousal is not None:
            amount = self.change_arousal(arousal, add_to_log = False)
            if amount != 0:
                message.append(f"{amount:+.0f} {{image=arousal_token_small}}")
        if love is not None and love != 0:
            amount = self.change_love(love, max_love, add_to_log = False)
            max_cap = self.max_stat_change_calc(max_change = max_love, serum_check = "Love")
            if amount < 0:
                message.append(f"{amount:+.0f} {{image=red_heart_token_small}}")
            else:
                message.append(f"{amount:+.0f} {{image=red_heart_token_small}}({max_cap:.0f})")
        if slut is not None and slut != 0:
            amount = self.change_slut(slut, max_slut, add_to_log = False)
            #if amount != 0:
            max_cap = self.max_stat_change_calc(max_change = max_slut, serum_check = "Slut")
            if amount < 0:
                message.append(f"{amount:+.0f} {{image=gold_heart_token_small}}")
            else:
                message.append(f"{amount:+.0f} {{image=gold_heart_token_small}}({max_cap:.0f})")
        if energy is not None:
            amount = self.change_energy(energy, add_to_log = False)
            if amount != 0:
                percentage = amount * 1.0 / max(self.max_energy, 1)
                message.append(f"{percentage:+.0%} {{image=energy_token_small}}")
        if novelty is not None:
            amount = self.change_novelty(novelty, add_to_log = False)
            if amount != 0:
                message.append(f"{amount:+.0f} Novelty")
        if add_to_log and message:
            mc.log_notification(f"{self.display_name}: {' '.join(message)}", "float_text_yellow")

    def change_arousal(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if self.arousal + amount < 0:
            amount = 0 - self.arousal

        self.arousal += amount
        if add_to_log and amount != 0:
            mc.log_notification(f"{self.display_name}: {amount:+.0f} {{image=arousal_token_small}}", "float_text_red")
        return amount

    def reset_arousal(self):
        base_arousal = self.sluttiness / 10.0
        base_arousal += self.opinion.masturbating
        base_arousal += self.opinion.showing_her_tits
        base_arousal += self.opinion.showing_her_ass
        base_arousal += self.opinion.not_wearing_underwear

        if base_arousal < 0:
            base_arousal = 0

        self.arousal = builtins.int(base_arousal)

    def change_max_arousal(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.max_arousal < 20:
            amount = -(self.max_arousal - 20)

        self.max_arousal += amount

        if add_to_log and amount != 0:
            mc.log_event(f"{self.display_name}: {amount:+.0f} Max Arousal", "float_text_red")
        return amount

    def change_novelty(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.novelty > 100:
            amount = 100 - self.novelty
        elif amount + self.novelty < 0:
            amount = self.novelty
        self.novelty += amount

        if add_to_log and amount != 0:
            mc.log_notification(f"{self.display_name}: {amount:+.0f} Novelty", "float_text_yellow")
        return amount

    def change_energy(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.energy > self.max_energy:
            amount = self.max_energy - self.energy
        elif amount + self.energy < 0:
            amount = -self.energy

        self.energy += amount

        if add_to_log and amount != 0:
            percentage = amount * 1.0 / max(self.max_energy, 1)
            mc.log_notification(f"{self.display_name}: {percentage:+.0%} {{image=energy_token_small}}", "float_text_energy")
        return amount

    def change_max_energy(self, amount: int, add_to_log = True) -> int:
        amount = builtins.int(builtins.round(amount))
        if amount + self.max_energy < 20:
            amount = -(self.max_energy - 20)
        if amount + self.max_energy > 200:  # max energy for person 200
            amount = 200 - self.max_energy

        self.max_energy += amount

        if self.energy > self.max_energy: #No having more energy than max
            self.energy = self.max_energy

        if add_to_log and amount != 0:
            percentage = amount * 1.0 / max(self.max_energy, 1)
            mc.log_event(f"{self.display_name}: {percentage:+.0%} Max Energy", "float_text_energy")
        return amount

    ## STRIP OUTFIT TO MAX SLUTTINESS EXTENSION
    # Strips down the person to a clothing their are comfortable with (starting with top, before bottom)
    # narrator_messages: narrator voice after each item of clothing stripped, use '[person.<title>]' for titles and '[strip_choice.name]' for clothing item.
        # Can be an array of messages for variation in message per clothing item or just a single string or None for silent stripping
    # scene manager parameter is filled from that class so that all people present in scene are drawn
    def strip_outfit_to_max_sluttiness(self, top_layer_first = True, exclude_upper = False, exclude_lower = False, exclude_feet = True, delay = 1, narrator_messages = None, display_transform = None, lighting: list[float] | None = None, temp_sluttiness_boost = 0, position: str = "default", emotion: str | None = None, scene_manager: Scene | None = None, wipe_scene = False) -> bool:
        '''
        Returns True: when a clothing item has been removed
        '''
        def get_strip_choice_max(outfit, top_layer_first, exclude_upper, exclude_lower, exclude_feet) -> Clothing | None:
            strip_choice = None
            if not exclude_upper:
                strip_choice = outfit.remove_random_upper(top_layer_first)
            if strip_choice is None:
                strip_choice = outfit.remove_random_any(top_layer_first, exclude_upper, exclude_lower, exclude_feet)
            return strip_choice

        def get_messages(narrator_messages):
            messages = []
            if not narrator_messages:
                pass
            elif not isinstance(narrator_messages, list):
                messages = [narrator_messages]
            else:
                messages = narrator_messages
            return messages

        messages = get_messages(narrator_messages)
        msg_count = builtins.len(messages)

        test_outfit = self.outfit.get_copy()
        removed_something = False

        strip_choice = get_strip_choice_max(test_outfit, top_layer_first, exclude_upper, exclude_lower, exclude_feet)
        # renpy.say(None, strip_choice.name + "  (required: " + str(test_outfit.outfit_slut_score) +  ", sluttiness: " +  str(self.effective_sluttiness() + temp_sluttiness_boost) + ")")
        while strip_choice and self.judge_outfit(test_outfit, temp_sluttiness_boost):
            if delay > 0:
                self.draw_quick_removal(strip_choice, display_transform = display_transform, position = position, emotion = emotion, lighting = lighting, scene_manager = scene_manager, wipe_scene = wipe_scene) #Draw the strip choice being removed from our current outfit
                if msg_count == 0:
                    renpy.pause(delay) # if no message to show, wait a short while before automatically continue stripping
            else:
                test_outfit.remove_clothing(strip_choice)
            self.apply_outfit(test_outfit, ignore_base = True) #Swap our current outfit out for the test outfit.
            removed_something = True
            if msg_count > 0:   # do we need to show a random message and replace titles and outfit name
                msg_idx = renpy.random.randint(1, msg_count)
                msg = messages[msg_idx - 1]
                msg = Text(msg, substitute = True).get_all_text().replace("$clothing$", strip_choice.display_name)
                renpy.say(None, msg)

            strip_choice = get_strip_choice_max(test_outfit, top_layer_first, exclude_upper, exclude_lower, exclude_feet)

        return removed_something

    def strip_top_to_underwear(self, visible_enough = True, prefer_half_off = False, avoid_nudity = False, position = "default", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping routine for removing all upper outer clothing
        [Deprecated]visible_enough = False will use is_availabe check instead of is_visible check
        prefer_half_off = True will half_off (partially hide) instead of remove the clothing items
        avoid_nudity = True will not strip clothing that would result in nudity
        '''
        strip_list = self.outfit.get_underwear_top_strip_list(avoid_nudity = avoid_nudity)
        self.__strip_outfit_strip_list(strip_list, position = position, emotion = emotion, display_transform = display_transform, lighting = lighting, half_off_instead = prefer_half_off, scene_manager = scene_manager, wipe_scene = wipe_scene, delay = delay)

    def strip_bottom_to_underwear(self, visible_enough = True, prefer_half_off = False, avoid_nudity = False, position = "default", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping routine for removing all lower outer clothing
        [Deprecated]visible_enough = False will use is_availabe check instead of is_visible check
        prefer_half_off = True will half_off (partially hide) instead of remove the clothing items
        avoid_nudity = True will not strip clothing that would result in nudity
        '''
        strip_list = self.outfit.get_underwear_bottom_strip_list(avoid_nudity = avoid_nudity)
        self.__strip_outfit_strip_list(strip_list, position = position, emotion = emotion, display_transform = display_transform, lighting = lighting, half_off_instead = prefer_half_off, scene_manager = scene_manager, wipe_scene = wipe_scene, delay = delay)

    def strip_to_underwear(self, visible_enough = True, prefer_half_off = False, avoid_nudity = False, position = "default", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping routine for removing all outer clothing
        [Deprecated]visible_enough = False will use is_availabe check instead of is_visible check
        prefer_half_off = True will half_off (partially hide) instead of remove the clothing items
        avoid_nudity = True will not strip clothing that would result in nudity
        '''
        if self.opinion.showing_her_ass > self.opinion.showing_her_tits:
            self.strip_bottom_to_underwear(visible_enough, prefer_half_off, avoid_nudity, position, emotion, display_transform, lighting, scene_manager, wipe_scene, delay)
            self.strip_top_to_underwear(visible_enough, prefer_half_off, avoid_nudity, position, emotion, display_transform, lighting, scene_manager, wipe_scene, delay)
        else:
            self.strip_top_to_underwear(visible_enough, prefer_half_off, avoid_nudity, position, emotion, display_transform, lighting, scene_manager, wipe_scene, delay)
            self.strip_bottom_to_underwear(visible_enough, prefer_half_off, avoid_nudity, position, emotion, display_transform, lighting, scene_manager, wipe_scene, delay)

    def strip_to_tits(self, visible_enough = True, prefer_half_off = False, position = "default", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping routine for removing all upper body clothing
        [Deprecated]visible_enough = False will use is_availabe check instead of is_visible check
        prefer_half_off = True will half_off (partially hide) instead of remove the clothing items
        avoid_nudity = True will not strip clothing that would result in nudity
        '''
        half_off_instead = False
        if prefer_half_off and self.outfit.can_half_off_to_tits(visible_enough):
            strip_list = self.outfit.get_half_off_to_tits_list(visible_enough)
            half_off_instead = True
        else:
            strip_list = self.outfit.get_tit_strip_list()
        self.__strip_outfit_strip_list(strip_list, position = position, emotion = emotion, display_transform = display_transform, lighting = lighting, half_off_instead = half_off_instead, scene_manager = scene_manager, wipe_scene = wipe_scene, delay = delay)

    def strip_to_vagina(self, visible_enough = True, prefer_half_off = False, position = "default", emotion = None, display_transform = None, lighting = None, scene_manager = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping routine for removing all lower body clothing
        [Deprecated]visible_enough = True will use is_visible check instead of is_available check
        prefer_half_off = True will half_off (partially hide) instead of remove the clothing items
        avoid_nudity = True will not strip clothing that would result in nudity
        '''
        half_off_instead = False
        if prefer_half_off and self.outfit.can_half_off_to_vagina(visible_enough):
            strip_list = self.outfit.get_half_off_to_vagina_list(visible_enough)
            half_off_instead = True
        else:
            strip_list = self.outfit.get_vagina_strip_list()
        self.__strip_outfit_strip_list(strip_list, position = position, emotion = emotion, display_transform = display_transform, lighting = lighting, half_off_instead = half_off_instead, scene_manager = scene_manager, wipe_scene = wipe_scene, delay = delay)

    def strip_full_outfit(self, strip_feet = False, strip_accessories = False, position: str = "default", emotion: str | None = None, display_transform = None, lighting: list[float] | None = None, scene_manager: Scene | None = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping routine for removing all clothing
        strip_feet = True will also remove shoes and stockings
        strip_accessories = True will also remove any accessories she is wearing
        '''
        strip_list = self.outfit.get_full_strip_list(strip_feet = strip_feet, strip_accessories = strip_accessories)
        self.__strip_outfit_strip_list(strip_list, position = position, emotion = emotion, display_transform = display_transform, lighting = lighting, scene_manager = scene_manager, wipe_scene = wipe_scene, delay = delay)

    def remove_clothing(self, clothing: list[Clothing] | Clothing, position: str = "default", emotion: str | None = None, display_transform = None, lighting: list[float] | None = None, scene_manager: Scene | None = None, wipe_scene = False, delay = 1):
        '''
        Use for on-screen stripping of passed clothing list
        '''
        if not clothing:
            return
        if not isinstance(clothing, list):
            clothing = [clothing]

        self.__strip_outfit_strip_list(clothing, position = position, emotion = emotion, display_transform = display_transform, lighting = lighting, scene_manager = scene_manager, wipe_scene = wipe_scene, delay = delay)

    def strip_outfit(self, top_layer_first = True, exclude_upper = False, exclude_lower = False, exclude_feet = True, delay = 1, display_transform = None, position = "default", emotion = None, lighting = None, scene_manager = None, wipe_scene = False):
        def extra_strip_check(person: Person, exclude_upper: bool, exclude_lower: bool, exclude_feet: bool):
            done = exclude_upper or person.tits_available
            if done and (exclude_lower or person.vagina_available):
                if done and (exclude_feet or person.outfit.feet_available):
                    return False

            return True # not done continue stripping

        if position == "default" or position is None:
            self.position = self.idle_pose

        if emotion is None:
            self.emotion = self.get_emotion()

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        if display_transform is None:
            display_transform = character_right

        strip_choice = self.outfit.remove_random_any(top_layer_first, exclude_upper, exclude_lower, exclude_feet, do_not_remove = True)
        while strip_choice is not None and extra_strip_check(self, exclude_upper, exclude_lower, exclude_feet):
            if delay > 0:
                self.draw_quick_removal(strip_choice, display_transform = display_transform, position = position, emotion = emotion, lighting = lighting, scene_manager = scene_manager, wipe_scene = wipe_scene) #Draw the strip choice being removed from our current outfit
            else:
                self.outfit.remove_clothing(strip_choice)
            strip_choice = self.outfit.remove_random_any(top_layer_first, exclude_upper, exclude_lower, exclude_feet, do_not_remove = True)

        # special case where she is wearing a two-part item that blocks her vagina, but we need it be available
        if not exclude_lower and not self.vagina_available:
            strip_choice = self.outfit.remove_random_any(top_layer_first, False, exclude_lower, exclude_feet, do_not_remove = True)
            while strip_choice is not None:
                if delay > 0:
                    self.draw_quick_removal(strip_choice, display_transform = display_transform, position = position, emotion = emotion, lighting = lighting, scene_manager = scene_manager, wipe_scene = wipe_scene) #Draw the strip choice being removed from our current outfit
                else:
                    self.outfit.remove_clothing(strip_choice)
                strip_choice = self.outfit.remove_random_any(top_layer_first, False, exclude_lower, exclude_feet, do_not_remove = True)

    def choose_strip_clothing_item(self) -> Clothing | None:
        '''
        Will determine a random clothing item to strip, based on personal preferences if any
        '''
        clothing = None
        # If she has a preference (even a least-bad preference) she'll strip that down first.
        if self.opinion.showing_her_tits > self.opinion.showing_her_ass:
            clothing = self.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, exclude_lower = True, do_not_remove = True)
        elif self.opinion.showing_her_tits < self.opinion.showing_her_ass:
            clothing = self.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, exclude_upper = True, do_not_remove = True)
        if clothing is None: #Either our previous checks failed to produce anything OR they were equal
            clothing = self.outfit.remove_random_any(top_layer_first = True, exclude_feet = True, do_not_remove = True)
        return clothing

    def get_no_condom_threshold(self, situational_modifier: int = 0) -> int:
        if self.knows_pregnant:
            return 0 #You can't get more pregnant, so who cares?

        if self.has_breeding_fetish:
            return 0 #She _wants_ to get knocked up. This will probably trigger other dialogue as well.

        no_condom_threshold = 50 + (self.opinion.bareback_sex * -10) + situational_modifier
        if self.is_family:
            no_condom_threshold += 10

        if persistent.pregnancy_pref == 0:
            no_condom_threshold += 10 #If pregnancy content is being ignored we return to the baseline of 60
        elif self.on_birth_control: #If there is pregnancy content then a girl is less likely to want a condom when using BC, much more likely to want it when not using BC.
            no_condom_threshold -= 20

        return no_condom_threshold

    def wants_condom(self, situational_modifier: int = 0, use_taboos = True) -> bool:
        if use_taboos and self.effective_sluttiness("condomless_sex") < self.get_no_condom_threshold(situational_modifier = situational_modifier):
            return True
        if self.effective_sluttiness() < self.get_no_condom_threshold(situational_modifier = situational_modifier):
            return True
        return False

    @property
    def has_family_taboo(self) -> bool: #A check to see if we should use an incest taboo modifier.
        if self.opinion.incest > 1: #If she thinks incest is hot she doesn't have an incest taboo modifier. Maybe she should, but it should just be reduced? For now this is fine.
            return False
        if self.is_family:
            return True
        return False

    @property
    def has_large_tits(self) -> bool: #Returns true if the girl has large breasts. "D" cups and up are considered large enough for tit-fucking, swinging, etc.
        return Person.rank_tits(self.tits) >= 4

    def increase_tit_size(self):
        new_tits = Person.get_larger_tit(self.tits)
        if new_tits != self.tits:
            self.tits = new_tits

    def decrease_tit_size(self):
        new_tits = Person.get_smaller_tit(self.tits)
        if new_tits != self.tits:
            self.tits = new_tits

    @property
    def wants_creampie(self) -> bool: #Returns True if the girl is going to use dialogue where she wants you to creampie her, False if she's going to be angry about it. Used to help keep dialogue similar throughout events
        # when breeding fetish, she always wants a creampie
        if self.has_breeding_fetish:
            return True
        if persistent.pregnancy_pref == 3 and self.is_highly_fertile and self.baby_desire > 40:
            return True
        if persistent.pregnancy_pref == 3 and self.is_highly_fertile and self.baby_desire <= 40:
            return False    #On realistic, girls don't want creampies when fertile, unless they really want a baby.

        creampie_threshold = 75
        if self.on_birth_control:
            creampie_threshold -= 20 #Much more willing to let you creampie her if she's on BC

        if self.is_girlfriend:
            creampie_threshold -= 10 + (5 * self.opinion.being_submissive) #Desire to be a "good wife"

        if self.is_family: # If she hates incest, it increases the threshold
            creampie_threshold += 10 - (10 * self.opinion.incest)

        # if she hates bareback sex, it increases the threshold
        creampie_threshold += (-10 * self.opinion.bareback_sex)

        if self.is_highly_fertile:  # she's fertile, increases her need to get filled up
            creampie_threshold -= 10

        effective_slut = self.sluttiness + (10 * self.opinion.creampies) + (10 * self.opinion.anal_creampies)
        if effective_slut >= creampie_threshold or self.knows_pregnant:
            return True

        return False

    @property
    def days_from_ideal_fertility(self) -> int:
        day_difference = abs((day % 30) - self.ideal_fertile_day)
        if day_difference > 15:
            day_difference = 30 - day_difference #Wrap around to get correct distance between months.
        return day_difference

    @property
    def bc_status_known(self) -> bool:
        return "birth_control_status" in self.event_triggers_dict

    def update_birth_control_knowledge(self, force_known_state: bool | None = None, force_known_day: int | None = None): #Called any time a girl gives you information about her BC. Allows for an up to date detailed info screen that doesn't give more than you know
        if force_known_state is None: #Useful when you an event changes a girls BC and you can expect that she's not going to be on birth control the next day.
            known_state = self.on_birth_control
        else:
            known_state = force_known_day

        if force_known_day is None:
            known_day = day
        else:
            known_day = force_known_day

        self.event_triggers_dict["birth_control_status"] = known_state
        self.event_triggers_dict["birth_control_known_day"] = known_day

    @property
    def on_birth_control(self) -> bool:
        return self.is_infertile or self.fertility_percent < 0 or self._birth_control

    @on_birth_control.setter
    def on_birth_control(self, value: bool):
        self.set_event_day("changed_bc")
        self._birth_control = value

    @property
    def is_mc_father(self) -> bool:
        '''
        Only valid while girl is pregnant
        Only use in conjunction with is_pregnant or knows_pregnant
        '''
        return self.event_triggers_dict.get("preg_mc_father", True)

    @property
    def has_child_with_mc(self) -> bool:
        '''
        Will only return True after girl has given birth not during pregnancy
        '''
        return self.sex_record.get("Children with MC", 0) > 0

    @property
    def number_of_children_with_mc(self) -> int:
        return self.sex_record.get("Children with MC", 0)

    @property
    def had_sex_today(self) -> bool:
        return self.sex_record.get("Last Sex Day", -1) == day

    @property
    def is_pregnant(self) -> bool:
        return self.has_role(pregnant_role)

    @property
    def is_pregnancy_wanted(self) -> bool:
        return (
            self.is_pregnant
            and self.event_triggers_dict.get("preg_wanted", False)
        )

    @property
    def is_lactating(self) -> bool:
        return self.lactation_sources > 0

    @property
    def knows_pregnant(self) -> bool:
        return (
            self.is_pregnant
            and self.event_triggers_dict.get("preg_knows", False)
        )

    @knows_pregnant.setter
    def knows_pregnant(self, value: bool):
        if value and self.is_pregnant: # only set True when she is pregnant
            self.event_triggers_dict["preg_knows"] = True
        else:
            self.event_triggers_dict["preg_knows"] = False

    @property
    def pregnancy_due_day(self) -> int:
        if self.is_pregnant:
            return self.event_triggers_dict.get("preg_finish_announce_day", 0)
        return -1

    @property
    def pregnancy_is_visible(self) -> bool:
        if self.is_pregnant:
            return day >= self.pregnancy_show_day
        return False

    @property
    def pregnancy_show_day(self) -> int:
        if self.is_pregnant:
            return self.event_triggers_dict.get("preg_transform_day", 0)
        return -1

    @property
    def baby_desire(self) -> int:
        return self._baby_desire

    def change_baby_desire(self, value: int):
        self._baby_desire += value
        self._baby_desire = min(max(-100, self._baby_desire), 100)

    @property
    def is_highly_fertile(self) -> bool:
        if self.is_pregnant or self.is_infertile:
            return False
        if persistent.pregnancy_pref < 2:
            return False
        day_difference = builtins.abs((day % 30) - self.ideal_fertile_day) # Gets the distance between the current day and the ideal fertile day.
        if day_difference > 15:
            day_difference = 30 - day_difference #Wrap around to get correct distance between months.
        if day_difference < 4:  #This is actually 3 on realistic for odds, but girls probably don't know their actual fertility start to within 1 day, so this gives a realistic buffer.
            return True
        return False

    @property
    def is_infertile(self) -> bool:
        return self.fertility_percent <= -500

    def effective_sluttiness(self, taboos: str | list[str] | None = None) -> int: #Used in sex scenes where the girl will be more aroused, making it easier for her to be seduced.
        if taboos is None:
            taboos = []
        elif not isinstance(taboos, list): #Handles handing over a single item without pre-wrapping it for "iteration".
            taboos = [taboos]

        return_amount = builtins.int(self.sluttiness + (self.arousal / 4))

        for taboo in taboos:
            if taboo not in self.broken_taboos: #If any of the taboo handed over are not already broken this person has a -15 effective sluttiness.
                return_amount -= 10
                break #Only applies once, so break once applied.

        return max(min(return_amount, 100), 0)

    # runner method for triggering orgasm in serums or day loops (from dialogs use .have_orgasm())
    def run_orgasm(self, show_dialogue: bool = True, force_trance: bool = False,
            trance_chance_modifier: int = 0, add_to_log: bool = True,
            sluttiness_increase_limit: int = 30, reset_arousal: bool = True, fire_event: bool = True):
        self.change_slut(1, sluttiness_increase_limit, add_to_log = add_to_log)
        if fire_event:
            mc.listener_system.fire_event("girl_climax", the_person = self)
        if renpy.random.randint(0, 100) < self.suggestibility + trance_chance_modifier or force_trance:
            self.increase_trance(show_dialogue = show_dialogue, reset_arousal = reset_arousal, add_to_log = add_to_log)

    @property
    def is_in_trance(self) -> bool:
        return self.has_role([trance_role, heavy_trance_role, very_heavy_trance_role])

    @property
    def is_in_very_heavy_trance(self) -> bool:
        return self.has_exact_role(very_heavy_trance_role)

    @property
    def trance_training_available(self) -> bool:
        return self.is_in_trance and self.event_triggers_dict.get("trance_training_available", True)

    def increase_trance(self, show_dialogue = True, reset_arousal = True, add_to_log = True):
        mc.stats.change_tracked_stat("Corruption", "Mind Breaks", 1)

        if not self.has_role(trance_role):
            self.add_role(trance_role)
            mc.listener_system.fire_event("girl_trance", the_person = self)
            if add_to_log:
                mc.log_event(f"{self.display_name} sinks into a trance!", "float_text_red")
                if show_dialogue:
                    renpy.say(None, capitalize_first_word(self.possessive_title) + "'s eyes lose focus slightly as she slips into a climax induced trance.")

        elif self.has_exact_role(trance_role):
            self.remove_role(trance_role)
            self.add_role(heavy_trance_role)
            if add_to_log:
                mc.log_event(f"{self.display_name} sinks deeper into a trance!", "float_text_red")
                if show_dialogue:
                    renpy.say(None, capitalize_first_word(self.possessive_title) + " seems to lose all focus as her brain slips deeper into a post-orgasm trance.")

        elif self.has_exact_role(heavy_trance_role):
            self.remove_role(heavy_trance_role)
            self.add_role(very_heavy_trance_role)
            if add_to_log:
                mc.log_event(f"{self.display_name} sinks deeper into a trance!", "float_text_red")
                if show_dialogue:
                    renpy.say(None, capitalize_first_word(self.possessive_title) + "'s eyes glaze over, and she sinks completely into an orgasm induced bliss.")

        if reset_arousal:
            self.reset_arousal()

    @property
    def trance_multiplier(self) -> float:
        if self.has_exact_role(trance_role):
            return 1.5
        if self.has_exact_role(heavy_trance_role):
            return 2.0
        if self.has_exact_role(very_heavy_trance_role):
            return 3.0
        return 1.0

    @property
    def is_tipsy(self) -> bool:
        return self.drink_level > 2

    @property
    def is_drunk(self) -> bool:
        return self.drink_level >= (self.serum_tolerance + 4)

    @property
    def is_wasted(self) -> bool:
        return self.drink_level >= (self.serum_tolerance + 8)

    def increase_drink_level(self, drink_count):
        self.drink_level += drink_count
        # mc.listener_system.fire_event("girl_drinks", the_person = self)
        # mc.stats.change_tracked_stat("Corruption", "Alcoholic Drinks", drink_count)

        if not self.has_role(drunk_role):
            self.add_role(drunk_role)
            mc.listener_system.fire_event("girl_trance", the_person = self)
        self.update_drink_level()
        return

    def update_drink_level(self):
        # Gives a girl situational obedience & sluttiness based on how many drinks they've had.
        # Based on personality, this would be a good place to do unique girl overrides as well if we want to do that.
        self.clear_situational_obedience("drinks")
        self.clear_situational_slut("drinks")
        slut_level = 0
        obedience_level = 0
        if self.personality.personality_type_prefix == "bimbo": #Any excuse to get sluttier for bimbos
            slut_level = 3 * self.drink_level
            obedience_level = 1 * self.drink_level
        elif self.personality.personality_type_prefix == "introvert":   #Gets more submissive with alcohol
            slut_level = 1 * self.drink_level
            obedience_level = 3 * self.drink_level
        elif self.personality.personality_type_prefix == "reserved":    #Similar, but reserved has more muted reactions overall
            slut_level = 1 * self.drink_level
            obedience_level = 2 * self.drink_level
        elif self.personality.personality_type_prefix == "wild":    #Sluttier, but also gets wilder and less obedient.
            slut_level = 3 * self.drink_level
            obedience_level = -2 * self.drink_level
        elif self.personality.personality_type_prefix == "alpha":
            slut_level = 2 * self.drink_level
            obedience_level = -1 * self.drink_level
        elif self.personality.personality_type_prefix == "cougar":  #Older women tend to be able to handle their drinks better. Confidence booster makes her less obedient.
            slut_level = 1 * self.drink_level
            obedience_level = -1 * self.drink_level
        else:   #Relaxed and all other personalities. Even gains of obedience and sluttiness.
            slut_level = 2 * self.drink_level
            obedience_level = 2 * self.drink_level

        self.add_situational_slut("drinks", slut_level, "I've had a few drinks.")
        self.add_situational_obedience("drinks", obedience_level, "I've had a few drinks.")
        return

    def reset_drunk_level(self):
        self.clear_situational_obedience("drinks")
        self.clear_situational_slut("drinks")
        self.drink_level = 0
        return

    def allow_position(self, position: Position) -> bool:
        '''
        Returns False when position is not possible (condition or hate) -> reason can be retrieved by Position.build_position_rejection_string
        '''
        if position == spanking and self.spank_level > 4:
            return False        # don't allow spanking is she has been recently spanked

        if position.requires_large_tits and not self.has_large_tits:
            return False        # her tits are too small

        if self.is_slave and self.obedience > 200:
            return True # obedient slave does what she is told
        if perk_system.has_ability_perk("Serum: Aura of Compliance") and mc_serum_aura_obedience.trait_tier >= 3:
            return True # strong compliance ability perk overrides her opinions
        if position.position_tag == "vaginal" and perk_system.has_ability_perk("Serum: Aura of Fertility") and mc_serum_aura_fertility.trait_tier >= 2:
            return True # strong breeding ability perk overrides her opinions on vaginal sex

        if any(x for x in position.opinion_tags if self.known_opinion(x) == -2):
            return False   # she hates something about this position

        return True

    def is_position_filtered(self, position: Position) -> bool:
        pos_filter = _character_position_filter(self, position.skill_tag)
        return not pos_filter(position)

    def is_willing(self, position: Position, private = True, slut_bonus = 0) -> bool:
        final_slut_requirement, _ = position.calculate_position_requirements(self, False)
        final_slut_requirement -= slut_bonus    #Use slut bonus to determine if an extra X sluttiness would make a girl willing
        # DON'T USE EFFECTIVE SLUTTINESS IN THIS FUNCTION
        # IT CAN HAVE THE MODIFIERS THAT THIS FUNCTION EMULATES
        # TO VALIDATE PRIOR TO ACTUALLY STARTING THE SEX LOOP
        # IT VALIDATES IF SHE IS WILLING BY HERSELF (NOT USING OBEDIENCE)

        # quick exit for hate / custom blocking of position (story line)
        if not self.allow_position(position) \
                or self.is_position_filtered(position) \
                or any(x for x in position.opinion_tags if self.opinion(x) <= -2):
            return False

        # print("Initial requirement: {}".format(final_slut_requirement))
        if self.has_job(prostitute_job):
            final_slut_requirement -= 20        # prostitutes are more willing by nature
        elif self.relationship == "Girlfriend":
            final_slut_requirement -= (self.opinion.cheating_on_men - 2) * 2  # love negates requirement penalty
        elif self.relationship == "Fiancée":
            final_slut_requirement -= (self.opinion.cheating_on_men - 2) * 3  # love negates requirement penalty
        elif self.relationship == "Married":
            final_slut_requirement -= (self.opinion.cheating_on_men - 2) * 5 # love negates requirement penalty

        if not private:
            multiplier = 5 if self.sluttiness < 50 else 2
            final_slut_requirement -= (self.opinion.public_sex - 2) * multiplier # love negates requirement penalty

        if self.love < 0:   # the more they hate you the higher the requirement
            final_slut_requirement += self.love * .2
        else:
            if self.has_relation_with_mc:       # lowers requirement by love
                final_slut_requirement -= self.love * .2
            elif self.is_family:
                final_slut_requirement -= (self.love - 50) * .2     # family only lowers if they love you enough
            else:
                final_slut_requirement -= (self.love - 50) * .1     # default only lowers if they love you enough

        final_slut_requirement -= (self.happiness - 120) * .2       # happiness only lowers requirement if they have a good mood

        # obedience can lower / increase requirement by up to 30 points
        # at default obedience of 100 increases requirement by 10 points
        final_slut_requirement -= (self.obedience - 150) * .2

        # print("Position: " + the_position.name + "[Sluttiness: " + str(self.sluttiness) + ", Required: " + str(final_slut_requirement) + "]")
        return self.sluttiness >= final_slut_requirement

    def unlock_spanking(self, add_to_log = True) -> bool:
        if self.can_be_spanked:
            return False
        self.event_triggers_dict["unlock_spanking"] = True
        if add_to_log:
            mc.log_event(f"{self.display_name} can now be spanked during sex.", "float_text_green")
        return True

    def slap_ass(self, update_stats = True):
        """
            Plays spank sound with dialog text of slap
            Based on spanking level and enjoyment of target, modifies stats

            Update Stats: True -> increases spank_level, change girl stats and updates enjoyment level (negative)
                          False -> play spank sound with dialog text without level change
        """
        if update_stats:
            arousal_change = self.spank_enjoyment_level * ((mc.foreplay_sex_skill / 10) + 1)
            if self.spank_enjoyment_level > 5: # loves it
                self.change_stats(arousal = arousal_change, slut = self.spank_enjoyment_level - 5, max_slut = 30)
            elif self.spank_enjoyment_level > 0: # likes it (small obedience increase)
                self.change_stats(arousal = arousal_change, obedience = self.spank_enjoyment_level - 2)
            elif self.spank_enjoyment_level > -5: # dislikes it (larger obedience increase)
                self.change_stats(arousal = arousal_change, obedience = -(self.spank_enjoyment_level + 3))
            else: # hates it (increase obedience at cost of love)
                self.change_stats(arousal = arousal_change, obedience = -self.spank_enjoyment_level, love = self.spank_enjoyment_level)

            self.spank_level += 1

        play_spank_sound()
        renpy.say(None, renpy.random.choice(["*{b}SLAP{/b}*", "*{b}SMACK{/b}*", "*{b}SWAT{/b}*", "*{b}THWACK{/b}*"]))

    @property
    def spank_enjoyment_level(self):
        return 3 + (self.opinion.being_submissive * 3) - self.spank_level

    @property
    def can_be_spanked(self) -> bool:
        return self.event_triggers_dict.get("unlock_spanking", False)

    @property
    def spank_level(self):
        return self.event_triggers_dict.get("spank_level", 0)

    @spank_level.setter
    def spank_level(self, value: int):
        self.event_triggers_dict["spank_level"] = value
        self.set_event_day("last_day_spanked")

    @property
    def ass_spank_description(self) -> str:
        if self.spank_level < 2:
            return "flawless. It is perky and ready for you to discipline."
        if self.spank_level < 4:
            return "slightly red. There are a few marks, but it still looks ripe for further discipline."
        if self.spank_level < 6:
            return "red. It looks like she has been disciplined properly."
        if self.spank_level < 8:
            return "bright red. There are a few small bruises. She has been thoroughly punished."
        return "bruised. She has been punished nearly to her limit. You might want to stop soon."

    @property
    def generic_orgasm_arousal_modifier(self) -> int:
        total_amount = 0
        if not mc.condom:
            total_amount += 2 * self.opinion.bareback_sex
        else:
            total_amount -= 2 * self.opinion.bareback_sex
        if self.has_significant_other:
            total_amount += 2 * self.opinion.cheating_on_men
        return total_amount

    @property
    def birthcontrol_efficiency(self) -> int:
        if not self.on_birth_control:
            return 0

        PERCENTAGES = (100, 100, 90, 99)
        return max(PERCENTAGES[persistent.pregnancy_pref] - self.bc_penalty, 0)

    @property
    def effective_fertility(self) -> float:
        if persistent.pregnancy_pref == 0 or self.fertility_percent < 0:
            return 0

        fertility = self.fertility_percent
        if persistent.pregnancy_pref > 1:
            day_difference = self.days_from_ideal_fertility # Gets the distance between the current day and the ideal fertile day.
            if persistent.pregnancy_pref < 3:
                multiplier = 2 - (float(day_difference) / 10.0) # The multiplier is 2 when the day difference is 0, 0.5 when the day difference is 15.
            else:
                if day_difference > 3:
                    return 1    #1% chance when not in fertile period
                multiplier = 0.3    #Base chance is 20%, which is far too high for completely realistic scenario. This should produce results 3-6%
            fertility = self.fertility_percent * multiplier

        #Commented out by Starbuck. Let's use baby_desire to determine the girl's reaction to getting knocked up, instead of of odds.
        # if persistent.pregnancy_pref == 3:
        #     if self.baby_desire < -400:
        #         fertility = fertility / 4
        #     elif self.baby_desire < 400:
        #         fertility = fertility / 2
        return fertility

    @property
    def pregnancy_chance(self) -> float:
        if self.effective_fertility <= 0:
            return 0
        return (self.effective_fertility / 100) * (100 - self.birthcontrol_efficiency)

    def did_she_become_pregnant(self, mc_father = True) -> bool:
        if persistent.pregnancy_pref == 0 or self.has_role(pregnant_role):
            return False

        # Pregnancy Check #
        if renpy.random.randint(0, 100) < self.effective_fertility: #There's a chance she's pregnant
            if renpy.random.randint(0, 100) > self.birthcontrol_efficiency: # Birth control failed to prevent the pregnancy
                become_pregnant(self, mc_father = mc_father) #Function in role_pregnant establishes all of the pregnancy related variables and events.
                return True

        return False

    def cum_in_mouth(self, add_to_record = True): #Add the appropriate stuff to their current outfit, and perform any personal checks if required.
        mc.listener_system.fire_event("sex_cum_mouth", the_person = self)
        self.outfit.add_mouth_cum()
        self.change_slut(self.opinion.drinking_cum, add_to_log = add_to_record)
        self.change_happiness(5 * self.opinion.drinking_cum, add_to_log = add_to_record)
        self.discover_opinion("drinking cum", add_to_log = add_to_record)

        if add_to_record:
            self.sex_record["Cum in Mouth"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["mouth_cum"] = report_log.get("mouth_cum", 0) + 1
            report_log["drinking cum"] = report_log.get("drinking cum", 0) + 1

        self.set_event_day("LastCumFetish") # also satisfies her fetish

        perk_system.perk_on_cum(self, "drinking cum", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.drinking_cum, add_to_log = add_to_record)

    def cum_in_vagina(self, add_to_record = True):
        mc.listener_system.fire_event("sex_cum_vagina", the_person = self)
        self.outfit.add_creampie_cum()

        slut_change_amount = self.opinion.creampies

        if self.wants_creampie:
            self.change_happiness(5 * self.opinion.creampies, add_to_log = add_to_record)
        else:
            self.change_happiness(-5 + (5 * self.opinion.creampies), add_to_log = add_to_record)
            self.change_love(-2 + self.opinion.creampies, add_to_log = add_to_record)
            slut_change_amount += self.opinion.being_submissive

        self.change_slut(slut_change_amount, add_to_log = add_to_record)
        if not mc.condom:
            self.discover_opinion("creampies", add_to_log = add_to_record)
            self.break_taboo("creampie")
            if add_to_record:
                self.sex_record["Vaginal Creampies"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["creampies"] = report_log.get("creampies", 0) + 1

        self.did_she_become_pregnant()

        self.set_event_day("last_insemination")
        self.set_event_day("LastCumFetish") # also satisfies her fetish
        self.set_event_day("LastBreedingFetish") # also satisfies her fetish

        perk_system.perk_on_cum(self, "creampies", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.creampies, add_to_log = add_to_record)

    def cum_in_ass(self, add_to_record = True):
        mc.listener_system.fire_event("sex_cum_ass", the_person = self)
        #TODO: Add an anal specific cumshot once we have renders for it.
        self.outfit.add_creampie_cum()

        if not self.wants_creampie:
            self.change_love(-2 + self.opinion.anal_creampies, add_to_log = add_to_record)

        self.change_happiness(5 * self.opinion.anal_creampies, add_to_log = add_to_record)
        self.change_slut(self.opinion.anal_creampies, add_to_log = add_to_record)

        if not mc.condom:
            self.discover_opinion("anal creampies", add_to_log = add_to_record)
            self.break_taboo("anal creampie")
            if add_to_record:
                self.sex_record["Anal Creampies"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["anal creampies"] = report_log.get("anal creampies", 0) + 1

        self.set_event_day("LastAnalFetish")    # also satisfies her fetish
        self.set_event_day("LastCumFetish")     # also satisfies her fetish

        perk_system.perk_on_cum(self, "anal creampies", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.anal_creampies, add_to_log = add_to_record)

    def cum_on_face(self, add_to_record = True):
        mc.listener_system.fire_event("sex_cum_on_face", the_person = self)
        self.outfit.add_face_cum()

        self.change_slut(self.opinion.cum_facials, add_to_log = add_to_record)
        self.change_happiness(5 * self.opinion.cum_facials, add_to_log = add_to_record)
        self.discover_opinion("cum facials", add_to_log = add_to_record)

        self.change_slut(self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.change_happiness(5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.discover_opinion("being covered in cum", add_to_log = add_to_record)

        if add_to_record:
            self.sex_record["Cum Facials"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["facials"] = report_log.get("facials", 0) + 1

        self.set_event_day("LastCumFetish") # also satisfies her fetish

        perk_system.perk_on_cum(self, "cum facials", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.cum_facials, add_to_log = add_to_record)

    def cum_on_tits(self, add_to_record = True):
        mc.listener_system.fire_event("sex_cum_on_tits", the_person = self)
        self.outfit.add_tits_cum()

        self.change_slut(self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.change_happiness(5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.discover_opinion("being covered in cum", add_to_log = add_to_record)

        if add_to_record:
            self.sex_record["Cum Covered"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["body_cum"] = report_log.get("body_cum", 0) + 1
            report_log["cum on tits"] = report_log.get("cum on tits", 0) + 1

        self.set_event_day("LastCumFetish") # also satisfies her fetish

        perk_system.perk_on_cum(self, "being covered in cum", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)

    def cum_on_stomach(self, add_to_record = True):
        mc.listener_system.fire_event("sex_cum_on_stomach", the_person = self)
        self.outfit.add_stomach_cum()

        self.change_slut(self.opinion.being_covered_in_cum, 80, add_to_log = add_to_record)
        self.change_happiness(5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.discover_opinion("being covered in cum", add_to_log = add_to_record)

        if add_to_record:
            self.sex_record["Cum Covered"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["body_cum"] = report_log.get("body_cum", 0) + 1
            report_log["cum on stomach"] = report_log.get("cum on stomach", 0) + 1

        self.set_event_day("LastCumFetish") # also satisfies her fetish

        perk_system.perk_on_cum(self, "being covered in cum", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)

    def cum_on_ass(self, add_to_record = True):
        mc.listener_system.fire_event("sex_cum_on_ass", the_person = self)
        self.outfit.add_ass_cum()

        self.change_slut(self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.change_happiness(5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)
        self.discover_opinion("being covered in cum", add_to_log = add_to_record)

        if add_to_record:
            self.sex_record["Cum Covered"] += 1

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["body_cum"] = report_log.get("body_cum", 0) + 1
            report_log["cum on ass"] = report_log.get("cum on ass", 0) + 1

        self.set_event_day("LastCumFetish") # also satisfies her fetish

        perk_system.perk_on_cum(self, "being covered in cum", add_to_log = add_to_record)
        self.change_arousal(self.generic_orgasm_arousal_modifier + 5 * self.opinion.being_covered_in_cum, add_to_log = add_to_record)

    def calculate_job_efficiency(self) -> float:
        if self.is_at_work:
            return self.current_job.productivity_adjustment * self.productivity_adjustment
        return 1.0

    @property
    def stripclub_salary(self) -> float:
        job = self.get_job((stripper_job, stripclub_stripper_job, stripclub_waitress_job, stripclub_bdsm_performer_job, stripclub_manager_job, stripclub_mistress_job))
        if not job:
            return 0
        return job.daily_wage

    @property
    def stripclub_profit(self) -> float:
        salary = self.stripclub_salary
        if salary == 0:
            return 0

        factor = renpy.random.random() + .5
        if self.has_job(stripclub_waitress_job):
            factor -= .2

        factor += self.opinion.showing_her_tits / 10.0
        factor += self.opinion.showing_her_ass / 10.0
        factor += self.opinion.skimpy_uniforms / 10.0
        factor += self.opinion.high_heels / 10.0
        factor += min(self.charisma / 20.0, .5)
        factor += (self.sluttiness / 4.0) / 100.0   # max 0.25

        return salary * factor * 2

    def set_schedule(self, location: Room, day_slots: list[int] | None = None, time_slots: list[int] | None = None):
        '''
        Sets the scheduled location in personal schedule
        When day_slots is None, all days of the week are scheduled
        When time_slots is None, all timeslots of the day are scheduled
        '''
        self.schedule.set_schedule(location, day_slots, time_slots)

    def set_override_schedule(self, location: Room, day_slots = None, time_slots = None):
        '''
        Sets the override schedule location (overrides default and any Job schedules)
        When day_slots is None, all days of the week are scheduled
        When time_slots is None, all timeslots of the day are scheduled
        '''
        self.override_schedule.set_schedule(location, day_slots, time_slots)

    def copy_schedule(self) -> Schedule: #Returns a properly formatted dict without references to the current schedule.
        return self.schedule.get_copy()

    def get_destination(self, day_slot: int | None = None, time_slot: int | None = None) -> Room | None:
        '''
        Return schedule Room or None if no location scheduled
        Priority -> override schedule, job schedule (based on job and priority), personal schedule
        '''
        if not self.is_available:  # special case to make people disappear (used in pregnancy)
            return purgatory

        location = self.override_schedule.get_destination(day_slot, time_slot)
        if location:
            return location

        for job in self.jobs:
            location = job.schedule.get_destination(day_slot, time_slot)
            if location:
                return location

        return self.schedule.get_destination(day_slot, time_slot) #Otherwise, go where we want.

    def get_random_destination(self) -> Room:
        exclude_list = []
        if strip_club_is_closed():  # exclude stripclub from random destinations
            exclude_list.extend((strip_club.identifier, bdsm_room.identifier))
        else:
            if not bdsm_room.visible or self.sluttiness < 40:
                exclude_list.append(bdsm_room.identifier)
            if self.sluttiness < 30:
                exclude_list.append(strip_club.identifier)
        if not (self.opinion.sports > 0 or self.opinion.yoga > 0): # she must like any gym activity
            exclude_list.extend((gym.identifier, gym_shower.identifier))
        if not (self.has_role(college_intern_role) or self.has_job((nora_professor_job, university_professor_job, student_job, sister_student_job))):
            exclude_list.extend((x.identifier for x in university_hub.locations))
        if not (self.has_job((secretary_job, office_worker_job, lawyer_job, architect_job, interior_decorator_job, fashion_designer_job))):
            exclude_list.append(mom_office_lobby.identifier)

        choice = get_random_from_list([x for x in list_of_places if x.is_public and x.identifier not in exclude_list], self.home)
        if not choice.is_accessible:
            return self.home
        return choice

    def create_formatted_title(self, title: str) -> str:
        return f"{{color={self.char.who_args['color']}}}{{font={self.char.what_args['font']}}}{title}{{/font}}{{/color}}"

    @property
    def relation_possessive_title(self) -> str:
        '''
        Returns the possessive title always as family relationship if person is family.
        When person is not family will return appropriate relationship reference.
        Usage: for dialogues where you specifically want to refer to your family relationship
        '''
        if not self.is_family:
            if self.is_girlfriend:
                return "your girlfriend"
            if self.is_affair:
                return "your mistress"
            if self.vaginal_sex_count > 9:
                return "your booty call"
            return "your friend"
        if self == mom:
            return "your mother"
        if self == lily:
            return "your sister"
        if self == aunt:
            return "your aunt"
        if self == cousin:
            return "your cousin"
        return "your family"

    def set_title(self, title: str | None = None): #Takes the given title and formats it so that it will use the characters font colours when the_person.title is used.
        '''
        title: None -> set random title
        '''
        if not title:
            title = self.get_random_title()
        self.char.name = title #This ensures the dialogue name is correct for the new title.
        self.title = self.create_formatted_title(title)

    def set_possessive_title(self, title: str | None = None):
        '''
        title: None -> set random title
        '''
        if not title:
            title = self.get_random_possessive_title()
        self.possessive_title = self.create_formatted_title(title)

    def set_mc_title(self, title: str | None = None):
        '''
        title: None -> set random title
        '''
        if not title:
            title = self.get_random_player_title()
        self.mc_title = title

    def personalise_text(self, what: str) -> str:
        for text_modifier in self.text_modifiers:
            what = text_modifier(self, what)

        return what

    def is_at_job(self, job: str | JobDefinition | Iterable[JobDefinition]) -> bool:
        '''
        Return True when person is current working at any of passed JobDefinition(s) or JobTitle
        '''
        if not self.is_at_work:
            return False

        if isinstance(job, JobDefinition):
            return self.current_job.job_definition == job
        if isinstance(job, str):
            return self.current_job.job_definition.job_title == job
        if isinstance(job, (list, tuple, set)):
            return any(x for x in job if x == self.current_job.job_definition)
        return False

    def has_job(self, job: str | JobDefinition | Iterable[JobDefinition]) -> bool:
        '''
        Return True when person has any job is based on passed JobDefinition(s) or Job Title
        '''
        if isinstance(job, JobDefinition):
            return job in (x.job_definition for x in self.jobs)
        if isinstance(job, str):
            return job in (x.job_title for x in self.jobs)
        return any(x.job_definition in job for x in self.jobs)

    def is_primary_job(self, job: str | JobDefinition | Iterable[JobDefinition]) -> bool:
        if not self.has_job(job):
            return False
        if isinstance(job, JobDefinition):
            return self._get_job_index(job) == 0
        if isinstance(job, str):
            return self._get_job_index(next(x for x in self.jobs if x.job_title == job), -1) == 0
        if isinstance(job, (list, tuple, set)):
            return any(x for x in self.jobs for y in job if x.job_definition == y and self._get_job_index(y) == 0)
        return False

    def get_job(self, job: str | JobDefinition | Iterable[JobDefinition]) -> ActiveJob | None:
        '''
        Return ActiveJob based on passed JobDefinition(s) or Job Title
        '''
        if isinstance(job, JobDefinition):
            return next((x for x in self.jobs if x.job_definition == job), None)
        if isinstance(job, str):
            return next((x for x in self.jobs if x.job_title == job), None)
        if isinstance(job, (list, tuple, set)):
            return next((x for x in self.jobs for y in job if x.job_definition == y), None)
        return None

    def has_job_role(self, job_role: str | Role | Iterable[Role]) -> bool:
        '''
        Returns True when any job has the passed role(s) or role_name
        '''
        if isinstance(job_role, Role):
            return job_role in self.job_roles
        if isinstance(job_role, str):
            return any(x for x in self.job_roles if x.role_name == job_role)
        if isinstance(job_role, (list, tuple, set)):
            return any(x for x in job_role for y in self.job_roles if x == y)
        return False

    @property
    def jobs(self) -> tuple[ActiveJob, ...]:
        '''
        Returns the list of ActiveJobs, ordered by their prevalance (scheduling priority)
        Priority: side_job <- primary_job <- secondary_job
        '''
        return tuple(filter(None, (self.side_job, self.primary_job, self.secondary_job)))

    @property
    def salary(self) -> float:
        return round(sum(x.salary for x in self.jobs if x.is_paid), 2)

    @property
    def job_roles(self) -> tuple[Role, ...]:
        '''
        Returns all roles linked to her jobs
        '''
        return tuple(role for job in self.jobs for role in job.job_roles)

    @property
    def current_job_roles(self) -> tuple[Role, ...]:
        '''
        Returns all roles for her current job
        '''
        if not self.current_job:
            return ()
        return tuple(x for x in self.special_role if x in self.current_job.job_roles)

    @property
    def current_job_actions(self) -> tuple[Action, ...]:
        '''
        Returns all actions related to her current job roles
        '''
        if not self.current_job or not self.current_job.job_known:
            return ()

        return tuple(action for x in self.current_job_roles for action in x.actions)

    @property
    def current_job_internet_actions(self) -> tuple[Action, ...]:
        '''
        Returns all internet actions related to her current job roles
        '''
        if not self.current_job or not self.current_job.job_known:
            return ()
        return tuple(action for x in self.current_job_roles for action in x.internet_actions)

    @property
    def duties(self) -> tuple[Duty, ...]:
        '''
        Returns all duties related to her jobs
        '''
        return tuple(duty for job in self.jobs for duty in job.duties)

    def has_duty(self, duty: Duty):
        '''
        Returns True when passed duty is active in any of her jobs
        '''
        return any(x for x in self.duties if x == duty)

    @property
    def active_duties(self) -> tuple[Duty, ...]:
        '''
        Returns the currently active duties in relation to current job
        '''
        return tuple(x for x in self.duties if not x.only_at_work or (self.is_at_work and self.current_job.has_duty(x)))

    @property
    def daily_duties(self) -> tuple[Duty, ...]:
        '''
        Returns all duties active for this day in relation to worked jobs
        '''
        return tuple(x for x in self.duties if not x.only_at_work or any(y for y in self.jobs if y.shifts > 0 and y.has_duty(x)))

    @property
    def current_duty_actions(self) -> tuple[Action, ...]:
        '''
        Returns all duty actions currently available
        '''
        return tuple(x for job in self.jobs for x in job.duty_actions)

    @property
    def current_duty_internet_actions(self) -> tuple[Action, ...]:
        '''
        Returns all internet actions currently available
        '''
        return tuple(x for job in self.jobs for x in job.duty_internet_actions)

    def _add_job(self, new_job: JobDefinition, index = 0, job_known = True, start_day: int = -1):
        '''
        Creates an ActiveJob from a jobdefinition
        Index: 0 - primary, 1 - secondary, 2 - side job
        start_day: Day when job starts -> -1 is today
        '''
        if not isinstance(new_job, JobDefinition):
            write_log(f"Cannot add job based on empty job_definition for {self.name}")
            return
        if new_job in self.jobs:
            write_log(f"Cannot add {new_job.job_title} for {self.name}, since she already has this job.")
            return

        job = ActiveJob(self, new_job, job_known, seniority_level = self.work_experience, start_day = start_day)
        job.recalculate_salary()
        for role in job.job_roles:
            self.add_role(role)

        if index == 0:
            self.primary_job = job
        elif index == 1:
            self.secondary_job = job
        else:
            self.side_job = job
        return job

    def _get_job_index(self, job: JobDefinition) -> int:
        '''
        Return the index of the job
        Index: 0 - primary, 1 - secondary, 2 - side job
        '''
        if self.secondary_job and job == self.secondary_job.job_definition:
            return 1
        if self.side_job and job == self.side_job.job_definition:
            return 2
        return 0    # primary_job

    def change_job(self, new_job: JobDefinition, is_primary = True, job_known = True, start_day: int = -1) -> ActiveJob:
        '''
        Change job to passed definition, by default sets primary_job,
        is_primary: False to set secondary job
        To set side-job -> call Person.set_side_job()
        start_day: -1 for now, else passed start_day when start_day < day it does the same as passing -1
        '''
        if not isinstance(new_job, JobDefinition):
            return

        self._clear_location_cache()
        mc.business._clear_employee_cache()

        if is_primary:
            for role in self.primary_job.job_roles:
                self.remove_role(role)
            return self._add_job(new_job, 0, job_known, start_day)
        else:
            if self.secondary_job:
                self.quit_job(self.secondary_job)
            return self._add_job(new_job, 1, job_known, start_day)

    def change_job_assignment(self, old_job: JobDefinition, new_job: JobDefinition, new_location: Room | None = None):
        '''
        Can be used for promotion like behaviour, where the underlying job, work locations and salary
        calculations are changed to the new 'JobDefinition', but the work-schedule is preserved from the
        old job. Use this method where the work schedule is not fixed to the one in the job definition.
        '''
        found = self.get_job(old_job)
        if not found:
            return False

        # copy current schedule and update location
        schedule = copy.deepcopy(found.schedule)
        schedule.update_scheduled_location(new_location)

        jobindex = self._get_job_index(old_job)

        self.quit_job(old_job)
        job = self._add_job(new_job, jobindex, True)
        job.schedule = schedule

        self._clear_location_cache()
        return True

    def set_side_job(self, new_job: JobDefinition, job_known = True, start_day: int = -1) -> ActiveJob:
        '''
        The sidejob is a special job that overrides the workschedule of the primary job
        THe secondary job fills the gaps in the primary-job / side-job schedule only
        It can be used for example with a student who also works a paying job in town to bolster her income
        during studies or the college athlete who trains during study hours
        When start_day is passed the job starts on that day else -1 is today
        '''
        if not isinstance(new_job, JobDefinition):
            return

        self._clear_location_cache()
        mc.business._clear_employee_cache()

        if self.side_job:
            self.quit_job(self.side_job)
        return self._add_job(new_job, 2, job_known = job_known, start_day = start_day)

    def quit_job(self, job: ActiveJob | JobDefinition | Iterable[JobDefinition]):
        '''
        She quits passed job, if primary her job will be unemployed else removes secondary/side job
        '''
        if isinstance(job, Iterable):
            result = False
            for x in job:
                if self.quit_job(x):
                    result = True
            return result

        if not isinstance(job, (ActiveJob, JobDefinition)):
            return False

        self._clear_location_cache()
        mc.business._clear_employee_cache()

        found = next((x for x in self.jobs if x == job or x.job_definition == job), None)
        if not found:
            return False

        # remove roles
        for role in found.job_roles:
            self.remove_role(role)

        if found == self.primary_job:
            self._add_job(unemployed_job, 0, self.primary_job.job_known)
        else:
            if found == self.secondary_job:
                self.secondary_job = None
            if found == self.side_job:
                self.side_job = None
        return True

    def add_role(self, role: Role) -> bool:
        if not isinstance(role, Role):
            write_log(f"Passed object to Person.add_role is not a Role object but a {type(role).__name__}")
            return False

        # don't add role if we already have a that role or a role that matches
        if self.has_role(role):
            return False

        self.special_role.append(role)

        # special condition if she hates kissing, but becomes your girlfriend or paramour she would allow kissing
        if self.opinion.kissing <= -2 and self.has_relation_with_mc:
            self.increase_opinion_score("kissing")

        # special situation if she gets girlfriend role, she loses affair role and SO
        if role == girlfriend_role:
            self.remove_role(affair_role)
            self.relationship = "Single" #Technically they aren't "single", but the MC has special roles for their girlfriend.
            self.SO_name = None

        # special situation when she goes to harem, she will loose the girlfriend role
        if role == harem_role:
            self.remove_role(girlfriend_role)
            mc.event_triggers_dict["harem_mansion_unlocked"] = True

        return True

    def remove_role(self, role: Role, remove_linked = True) -> bool:
        if role in self.special_role:
            if role == pregnant_role:   # reset pregnant knows flag
                self.knows_pregnant = False
            self.special_role.remove(role)
            if remove_linked:
                for linked_role in role.linked_roles:
                    self.remove_role(linked_role, remove_linked)
            return True
        return False

    def has_role(self, role: str | Role | Iterable[Role]) -> bool:
        '''
        Returns True: When one of the passed roles is found
        '''
        if isinstance(role, Role):  # most used so first check
            return role in self.special_role \
                or any(x for x in self.special_role if x.check_parent_role(role))
        if isinstance(role, str):
            return any(x for x in self.special_role if x.role_name == role) \
                or any(x for x in self.special_role if x.check_parent_role(role))
        if isinstance(role, (list, tuple, set)):
            return any(x in self.special_role for x in role) \
                or any(y.check_parent_role(x) for y in self.special_role for x in role)
        return False

    def has_exact_role(self, role: Role) -> bool: #As has_role, but checks against all roles and all of their looks_like roles.
        return role in self.special_role

    def add_action(self, action: Action):
        self.base_role.add_action(action)

    def remove_action(self, action: Action):
        self.base_role.remove_action(action)

    def has_action(self, action: Action | str) -> bool:
        '''
        Returns True: When passed action is associated with person base role
        These actions are handled by Person.add_action() / Person.remove_action()
        '''
        return self.base_role.has_action(action)

    def get_role_reference(self, role: Role | str) -> Role | None:
        '''
        [Deprecated] Get special-role by Role object
        Note: Role objects are static, to modify actions for a role, you need to get
              the reference assigned to the person.
        '''
        found = None
        if isinstance(role, Role):
            found = next((x for x in self.special_role if x == role), None)
        if isinstance(role, str):
            found = next((x for x in self.special_role if x.role_name == role), None)
        return found

    @property
    def is_sleeping(self) -> bool:
        return self.is_family and self.has_queued_event("sleeping_walk_in_label")

    def has_queued_event(self, action: Action | str) -> bool:
        '''
        Returns True when action / label name is an event in the room_enter or talk_event lists
        '''
        return self.on_room_enter_event_list.has_action(action) \
            or self.on_talk_event_list.has_action(action)

    def remove_queued_event(self, action: Action | str):
        '''
        Removes passed action from room_enter or talk_event action list
        '''
        if self.on_room_enter_event_list.has_action(action):
            self.on_room_enter_event_list.remove_action(action)
        if self.on_talk_event_list.has_action(action):
            self.on_talk_event_list.remove_action(action)

    def add_infraction(self, infraction: Infraction, add_to_log = True, require_policy = True):
        if office_punishment.is_active or not require_policy:
            self.infractions.append(infraction)
            if add_to_log:
                mc.log_event(f"{self.display_name} committed infraction: {infraction.name}, Severity {infraction.severity}", "float_text_grey")

    def remove_infraction(self, infraction: Infraction | str):
        found = None
        if isinstance(infraction, Infraction):
            found = next((x for x in self.infractions if x == infraction), None)
        if isinstance(infraction, str):
            found = next((x for x in self.infractions if x.name == infraction), None)
        if found:
            self.infractions.remove(found)

    def match_skin(self, color: str):
        if " skin" in color: # If using the_person.body_images.name as a reference, remove the " skin" part.
            color = color[:-5]
        self.skin = str(color)

    def set_eye_colour(self, new_colour: Color):
        eye_colour_name = closest_eye_color(new_colour).capitalize()
        self.eyes = (eye_colour_name, list(new_colour.rgba))

    def set_hair_colour(self, new_colour: Color, change_pubes = True, darken_pubes_amount = 0.07):
        hair_colour_name = closest_hair_colour(new_colour).capitalize()
        self.hair_colour = (hair_colour_name, list(new_colour.rgba))
        self.hair_style.colour = self.hair_colour[1]

        if change_pubes:
            pubes_colour = darken_colour(self.hair_colour[1], darken_pubes_amount)
            self.pubes_colour = list(pubes_colour.rgba)
            self.pubes_style.colour = self.pubes_colour

    def lighten_hair_colour(self, factor: float = .07):
        new_colour = lighten_colour(self.hair_colour[1], factor)
        if new_colour:
            self.set_hair_colour(new_colour, change_pubes = False)

    def darken_hair_colour(self, factor: float = .07):
        new_colour = darken_colour(self.hair_colour[1], factor)
        if new_colour:
            self.set_hair_colour(new_colour, change_pubes = False)

    @property
    def maximum_milk_in_breasts(self) -> int:
        return Person.rank_tits(self.tits) * 2

    @property
    def so_title(self) -> str:
        if self.has_significant_other:
            return SO_relationship_to_title(self.relationship)
        return "friend" # fallback

    @property
    def so_girl_title(self) -> str:
        if self.has_significant_other:
            return girl_relationship_to_title(self.relationship)
        return "friend" # fallback

    def get_titles(self) -> list[str]: #Returns a list of character titles this person can have. A title is what you call a person, often but not always their name or based on their name.
        list_of_titles = self.personality.get_personality_titles(self)
        if isinstance(list_of_titles, str):  # lock personality to one title
            return [list_of_titles]

        if self.sluttiness > 20 and self.obedience > 150:
            list_of_titles.append("Slave")

        if self.sluttiness > 60:
            list_of_titles.append("Slut")
            if self.obedience > 140:
                list_of_titles.append("Cocksleeve")
                list_of_titles.append("Cock Slave")

            if Person.rank_tits(self.tits) >= 9:
                list_of_titles.append("Melony")
            elif Person.rank_tits(self.tits) == 0:
                list_of_titles.append("Sweet Pea")
            elif Person.rank_tits(self.tits) >= 4:
                list_of_titles.append("Big Tits")
            else:
                list_of_titles.append("Little Tits")

            if self.vaginal_creampie_count >= 20:
                list_of_titles.append("Breeding Material")

        if self.sluttiness > (70 - (self.opinion.drinking_cum * 5 + self.opinion.creampies * 5 + self.opinion.cum_facials * 5 + self.opinion.being_covered_in_cum * 5)):
            if self.cum_facial_count > 5 or self.cum_mouth_count > 5 or self.cum_covered_count > 5:
                list_of_titles.append("Cumslut")

        if self.is_cum_dump:
            list_of_titles.append("Cumdump")
        if self.is_cum_bucket:
            list_of_titles.append("Cumbucket")

        if self.is_free_use:
            list_of_titles.append("Free-Use Slut")

        if self.love >= 60 and self.is_girlfriend:
            list_of_titles.append("Love")

        if self.love < 0:
            list_of_titles.append("Cunt")
            list_of_titles.append("Bitch")

        if self.love >= 95:
            list_of_titles.append("Honey")
            list_of_titles.append("Darling")

        if self.kids > 0:
            if self.sluttiness > 30:
                list_of_titles.append("Naughty MILF")
            if self.sluttiness > 60:
                list_of_titles.append("Slutty MILF")

        if not self.is_unique:
            if self.love > 30 and self.height > 1.1:
                list_of_titles.append("Sexy Legs")
                list_of_titles.append("Sky High")

            if self.love > 30 and self.height < 0.8:
                list_of_titles.append("Tinkerbell")
                list_of_titles.append("Little Lady")

            if self.love > 30 and self.sluttiness > 20 and self.opinion.high_heels >= 2:
                list_of_titles.append("Killer Heels")

            if self.sluttiness > 80:
                list_of_titles.append("Whore")

            if self.sluttiness > 50 and self.has_job(stripper_job):
                list_of_titles.append("Pole-Slut")
            if self.love > 50 and self.has_job(stripclub_mistress_job):
                list_of_titles.append("Milady")
            if self.sluttiness > 60 and self.has_job(stripclub_mistress_job):
                list_of_titles.append("Mistress")

        if self.has_child_with_mc or (self.knows_pregnant and self.is_mc_father):
            list_of_titles.append("Wife")
            list_of_titles.append("Waifu")

        return list(set(list_of_titles))

    def get_random_title(self) -> str:
        return get_random_from_list(self.get_titles())

    def get_possessive_titles(self) -> list[str]:
        list_of_titles = self.personality.get_personality_possessive_titles(self)
        if isinstance(list_of_titles, str):  # lock personality to one title
            return [list_of_titles]

        if self.is_employee:
            list_of_titles.append("your employee")
            if self.sluttiness > 60:
                list_of_titles.append("your office slut")

        if self.love > 10:
            list_of_titles.append("your friend")

        if self.obedience > 150:
            list_of_titles.append("your slave")
            if self.sluttiness > 60:
                list_of_titles.append("your dedicated cocksleeve")

        if self.kids > 0:
            if self.sluttiness > 30:
                list_of_titles.append("your naughty MILF")
            if self.sluttiness > 60:
                list_of_titles.append("your slutty MILF")

        if self.sluttiness > 60:
            if self.int <= 1 and self.has_large_tits:
                list_of_titles.append("your airhead bimbo")

            if self.love > 50:
                list_of_titles.append("your personal slut")
            elif self.love < 0:
                list_of_titles.append("your hate-fuck slut")
            else:
                list_of_titles.append("your slut")

            if self.has_significant_other:
                list_of_titles.append("your cheating slut")

            if self.vaginal_creampie_count >= 20:
                list_of_titles.append("your breeder")

        if self.sluttiness > (70 - (self.opinion.drinking_cum * 5 + self.opinion.creampies * 5 + self.opinion.cum_facials * 5 + self.opinion.being_covered_in_cum * 5)):
            if self.cum_facial_count > 5 or self.cum_mouth_count > 5 or self.cum_covered_count > 5:
                list_of_titles.append("your cumslut")

        if self.is_cum_dump:
            list_of_titles.append("your cumdump")
        if self.is_cum_bucket:
            list_of_titles.append("your cum bucket")

        if self.is_free_use:
            list_of_titles.append("your free-use slut")

        if self.love >= 60 and self.is_girlfriend:
            list_of_titles.append("your love")
            list_of_titles.append("your girlfriend")

        if self.love >= 60 and self.is_affair:
            list_of_titles.append("your lover")

        if self.has_role([generic_student_role]):
            list_of_titles.append("your student")

        if not self.is_unique:
            if self.sluttiness > 80:
                list_of_titles.append("your whore")

            if self.has_job(stripper_job):
                list_of_titles.append("your exotic dancer")
            if self.love > 50 and self.has_job(stripclub_mistress_job):
                list_of_titles.append("your burlesque queen")
            if self.sluttiness > 50 and self.has_job(stripclub_mistress_job):
                list_of_titles.append("your kinky mistress")
            if self.has_job(stripclub_waitress_job):
                list_of_titles.append("your waitress")
            if self.sluttiness > 50 and self.has_job(stripclub_manager_job):
                list_of_titles.append("your naughty manager")

        if self.sluttiness > 80 and self.anal_sex_skill >= 5:
            list_of_titles.append("your buttslut")

        if self.has_cum_fetish:
            list_of_titles.append("your cum guzzler")
            list_of_titles.append("your cum catcher")

        if self.has_child_with_mc or (self.knows_pregnant and self.is_mc_father):
            list_of_titles.append("your wife")
            list_of_titles.append("your partner")
            list_of_titles.append("your waifu")

        return list(set(list_of_titles))

    def get_random_possessive_title(self) -> str:
        return get_random_from_list(self.get_possessive_titles())

    def get_player_titles(self) -> list[str]:
        list_of_titles = self.personality.get_personality_player_titles(self)
        if isinstance(list_of_titles, str):  # lock personality to one title
            return [list_of_titles]

        list_of_titles.append(f"Mr. {mc.last_name}")
        list_of_titles.append(mc.name)
        if self.love >= 95:
            list_of_titles.append("Honey")
            list_of_titles.append("Darling")

        if self.is_employee:
            if self.obedience > 120:
                list_of_titles.append("Sir")
            elif self.obedience < 80 and self.is_employee:
                list_of_titles.append("Boss")

        if self.obedience > 140 and self.sluttiness > 50:
            list_of_titles.append("Master")

        if self.sluttiness > 50:
            if self.love > 50:
                list_of_titles.append("Daddy")
            elif self.love < 0:
                list_of_titles.append("Fuck Meat")
                list_of_titles.append("Cunt Slave")
            else:
                list_of_titles.append("Boy Toy")

        if self.has_role([generic_student_role]):
            list_of_titles.append("Teacher")

        if self.has_child_with_mc or (self.knows_pregnant and self.is_mc_father):
            list_of_titles.append("Husband")
            list_of_titles.append("Hubby")

        return list(set(list_of_titles))

    def get_random_player_title(self) -> str:
        return get_random_from_list(self.get_player_titles())

    def change_personality(self, personality: Personality):
        if not self.personality == personality:
            self.event_triggers_dict["original_personality"] = self.personality.personality_type_prefix
            self.personality = personality

    def restore_original_personality(self):
        if self.personality in list_of_personalities:   # we already have a base personality
            return

        original_personality = None
        if "original_personality" in self.event_triggers_dict:
            original_personality = next((x for x in list_of_personalities if x.personality_type_prefix == self.event_triggers_dict["original_personality"]), None)
        if not original_personality:
            original_personality = get_random_from_list(list_of_personalities)
        if original_personality:
            self.personality = original_personality

    def remove_person_from_game(self):
        if self in list_of_people:  # remove from global people list
            list_of_people.remove(self)

        if self.home in list_of_places:
            # only remove home when not 'dungeon' | 'clone facility' or any other character has same home location
            if self.home not in (dungeon, clone_facility) and not any(x.home == self.home for x in list_of_people if x != self):
                list_of_places.remove(self.home) # remove home location from list_of_places
        if self.home in mc.known_home_locations:
            mc.known_home_locations.remove(self.home) # remove home location from known_home_locations

        # cleanup crisis events where person is in argument list
        for crisis_store in (mc.business.mandatory_crises_list, mc.business.mandatory_morning_crises_list):
            for crisis in crisis_store[:]:
                args = crisis.args
                if not isinstance(args, list):
                    args = [args]

                if any(x for x in args if x == self):
                    crisis_store.remove(crisis)

        # remove special job assignments
        mc.business.remove_employee_assignment(self)

        # remove from relationships array
        town_relationships.remove_all_relationships(self)

        self.base_outfit = None
        self.planned_outfit = None

        if self.wardrobe:
            self.wardrobe.clear_wardrobe()
            self.wardrobe = None

        if self.special_role:
            self.special_role.clear()
        if self.on_room_enter_event_list:
            self.on_room_enter_event_list.clear()
        if self.on_talk_event_list:
            self.on_talk_event_list.clear()
        if self.event_triggers_dict:
            self.event_triggers_dict.clear()
        if self.suggest_bag:
            self.suggest_bag.clear()
        if self.broken_taboos:
            self.broken_taboos.clear()
        if self.sex_record:
            self.sex_record.clear()
        if self.opinions:
            self.opinions.clear()
        if self.sexy_opinions:
            self.sexy_opinions.clear()

        # clear all references held by person object.
        self.schedule = None
        self.override_schedule = None
        self.primary_job = None
        self.secondary_job = None
        self.side_job = None
        self.relationship = None
        self.personality = None
        self.char = None
        self.face_style = None
        self.hair_colour = None
        self.hair_style = None
        self.pubes_style = None
        self.skin = None
        self.eyes = None
        self.serum_effects = None
        self.situational_sluttiness = None
        self.situational_obedience = None
        # now let the Garbage Collector do the rest (we are no longer referenced in any objects).

    def __strip_outfit_strip_list(self, strip_list: list[Clothing], position: str = "default", emotion: str | None = None, display_transform = None, lighting: list[float] | None = None, scene_manager: Scene | None = None, wipe_scene = False, half_off_instead = False, delay = 1):
        if position == "default" or position is None:
            self.position = self.idle_pose

        if emotion is None:
            self.emotion = self.get_emotion()

        if lighting is None:
            lighting = mc.location.get_lighting_conditions()

        if display_transform is None:
            display_transform = character_right

        for item in strip_list:
            if delay > 0:
                self.draw_quick_removal(item, display_transform = display_transform, position = position, emotion = emotion, lighting = lighting, half_off_instead = half_off_instead, scene_manager = scene_manager, wipe_scene = wipe_scene) #Draw the strip choice being removed from our current outfit
            else:
                self.outfit.remove_clothing(item)

#############################
# Phone Message Information #
#############################

    @property
    def has_instapic_post(self):
        return (self.event_triggers_dict.get("insta_generate_pic", False)
            or self.event_triggers_dict.get("insta_new_boobs_brag", False))

    @property
    def instapic_known(self):
        return self.has_role(instapic_role) and self.event_triggers_dict.get("insta_known", False)

    def learn_instapic(self, force_role = True):
        if force_role and not self.has_role(instapic_role):
            self.add_role(instapic_role)
        self.event_triggers_dict["insta_known"] = True

    @property
    def has_onlyfan_post(self):
        return (self.event_triggers_dict.get("onlyfans_new_boobs_brag", False)
            or not self.event_triggers_dict.get("onlyfans_visited_today", True))

    @property
    def onlyfans_known(self):
        return self.has_role(onlyfans_role) and self.event_triggers_dict.get("onlyfans_known", False)

    def learn_onlyfans(self, force_role = True):
        if force_role and not self.has_role(onlyfans_role):
            self.add_role(onlyfans_role)
        self.event_triggers_dict["onlyfans_known"] = True

    @property
    def has_dikdok_post(self):
        return (self.event_triggers_dict.get("dikdok_new_boobs_brag", False)
            or self.event_triggers_dict.get("dikdok_generate_video", False))

    @property
    def dikdok_known(self):
        return self.has_role(dikdok_role) and self.event_triggers_dict.get("dikdok_known", False)

    def learn_dikdok(self, force_role = True):
        if force_role and not self.has_role(dikdok_role):
            self.add_role(dikdok_role)
        self.event_triggers_dict["dikdok_known"] = True

##########################################
# Expose outfit methods on Person object #
##########################################

    @property
    def is_naked(self) -> bool:
        return len(self.outfit.upper_body) + len(self.outfit.lower_body) + len(self.outfit.feet) == 0

    @property
    def tits_available(self) -> bool:
        return self.outfit.tits_available

    @property
    def tits_visible(self) -> bool:
        return self.outfit.tits_visible

    @property
    def vagina_available(self) -> bool:
        return self.outfit.vagina_available

    @property
    def vagina_visible(self) -> bool:
        return self.outfit.vagina_visible

    @property
    def underwear_visible(self) -> bool:
        return self.outfit.underwear_visible

    @property
    def wearing_bra(self) -> bool:
        return self.outfit.wearing_bra

    @property
    def wearing_panties(self) -> bool:
        return self.outfit.wearing_panties

    @property
    def bra_covered(self) -> bool:
        return self.outfit.bra_covered

    @property
    def panties_covered(self) -> bool:
        return self.outfit.panties_covered

    @property
    def has_underwear(self) -> bool:
        '''
        True when wearing bra and panties
        '''
        return self.outfit.has_underwear

    @property
    def is_wearing_underwear(self) -> bool:
        '''
        True when wearing either bra or panties
        '''
        return self.outfit.is_wearing_underwear

    @property
    def is_bra_visible(self) -> bool:
        return self.outfit.is_bra_visible

    @property
    def are_panties_visible(self) -> bool:
        return self.outfit.are_panties_visible

    @property
    def bra(self) -> Clothing | None:
        '''
        Returns current worn barn or None when not wearing one
        '''
        return self.outfit.get_bra()

    @property
    def panties(self) -> Clothing | None:
        '''
        Returns current worn panties or None when not wearing any
        '''
        return self.outfit.get_panties()

    @property
    def can_remove_bra(self) -> bool:
        return self.outfit.can_remove_bra

    @property
    def can_remove_panties(self) -> bool:
        return self.outfit.can_remove_panties

    @property
    def cum_covered(self) -> bool:
        return self.outfit.cum_covered

    @property
    def has_mouth_cum(self) -> bool:
        return self.outfit.has_mouth_cum

    @property
    def has_tits_cum(self) -> bool:
        return self.outfit.has_tits_cum

    @property
    def has_stomach_cum(self) -> bool:
        return self.outfit.has_stomach_cum

    @property
    def has_face_cum(self) -> bool:
        return self.outfit.has_face_cum

    @property
    def has_ass_cum(self) -> bool:
        return self.outfit.has_ass_cum

    @property
    def has_creampie_cum(self) -> bool:
        return self.outfit.has_creampie_cum

    @property
    def shows_off_her_ass(self) -> bool:
        return self.outfit.shows_off_her_ass

    @property
    def shows_off_her_tits(self) -> bool:
        return self.outfit.shows_off_her_tits

    @property
    def has_dress(self) -> bool:
        return self.outfit.has_dress

    @property
    def has_skirt(self) -> bool:
        return self.outfit.has_skirt

    @property
    def has_pants(self) -> bool:
        return self.outfit.has_pants

    @property
    def has_shirt(self) -> bool:
        return self.outfit.has_shirt

    @property
    def has_socks(self) -> bool:
        return self.outfit.has_socks

    @property
    def has_low_socks(self) -> bool:
        return self.outfit.has_low_socks

    @property
    def has_thigh_high_socks(self) -> bool:
        return self.outfit.has_thigh_high_socks

    @property
    def has_shoes(self) -> bool:
        return self.outfit.has_shoes

    @property
    def has_boots(self) -> bool:
        return self.outfit.has_boots

    @property
    def has_high_heels(self) -> bool:
        return self.outfit.has_high_heels

    @property
    def has_one_piece(self) -> bool:
        return self.outfit.has_one_piece

    @property
    def has_bracet(self) -> bool:
        return self.outfit.has_bracelet

    @property
    def has_glasses(self) -> bool:
        return self.outfit.has_glasses

    def restore_all_clothing(self):
        return self.outfit.restore_all_clothing()

    def get_full_strip_list(self, strip_feet = True, strip_accessories = False) -> list[Clothing]:
        return self.outfit.get_full_strip_list(strip_feet, strip_accessories)

    def get_underwear_strip_list(self, visible_enough = True, avoid_nudity = False) -> list[Clothing]:
        return self.outfit.get_underwear_strip_list(visible_enough, avoid_nudity)

    def can_half_off_to_tits(self, visible_enough = True) -> bool:
        return self.outfit.can_half_off_to_tits(visible_enough)

    def get_half_off_to_tits_list(self, visible_enough = True) -> list[Clothing]:
        return self.outfit.get_half_off_to_tits_list(visible_enough)

    def get_tit_strip_list(self, visible_enough = True) -> list[Clothing]:
        '''
        param:
            visible_enough [DEPRECATED] has no effect
        '''
        return self.outfit.get_tit_strip_list()

    def can_half_off_to_vagina(self, visible_enough = True) -> bool:
        return self.outfit.can_half_off_to_vagina(visible_enough)

    def get_half_off_to_vagina_list(self, visible_enough = True) -> list[Clothing]:
        return self.outfit.get_half_off_to_vagina_list(visible_enough)

    def get_vagina_strip_list(self, visible_enough = True) -> list[Clothing]:
        '''
        param:
            visible_enough [DEPRECATED] has no effect
        '''
        return self.outfit.get_vagina_strip_list()

    # wrapper for girl in charge
    def get_sex_goal(self) -> str | None:
        goal = self.event_triggers_dict.get("sex_goal", None)
        # she switches the goal
        if goal in ("vaginal creampie", "anal creampie") and not self.wants_creampie:
            goal = "get mc off"
        return goal

    # determine girl cum preference
    def facial_or_swallow(self) -> str:    #Use this function to determine if girl wants a facial or to swallow cum. If neither is preferred, return one at random.
        if self.has_cum_fetish or self.opinion.cum_facials == self.opinion.drinking_cum:
            return renpy.random.choice(["swallow", "facial"])
        if self.opinion.cum_facials > self.opinion.drinking_cum:
            return "facial"
        return "swallow"

##################################################
#    Body descriptor python wrappers             #
##################################################

    @property
    def body_is_thin(self) -> bool:
        return self.body_type == "thin_body"

    @property
    def body_is_average(self) -> bool:
        return self.body_type == "standard_body"

    @property
    def body_is_thick(self) -> bool:
        return self.body_type == "curvy_body"

    @property
    def body_is_pregnant(self) -> bool:
        return self.body_type == "standard_preg_body"

##################################################
#     Fetish related wrappers                    #
##################################################

    @property
    def fetish_count(self) -> int:
        return builtins.len([x for x in self.special_role if x in (anal_fetish_role, cum_fetish_role, breeding_fetish_role, exhibition_fetish_role)])

    @property
    def has_anal_fetish(self) -> bool:
        return self.has_role(anal_fetish_role)

    @property
    def has_cum_fetish(self) -> bool:
        return self.has_role(cum_fetish_role)

    @property
    def has_breeding_fetish(self) -> bool:
        return self.has_role(breeding_fetish_role)

    @property
    def has_exhibition_fetish(self) -> bool:
        return self.has_role(exhibition_fetish_role)

    @property
    def has_started_anal_fetish(self) -> bool:
        return self.event_triggers_dict.get("anal_fetish_start", False)

    @property
    def has_started_breeding_fetish(self) -> bool:
        return self.event_triggers_dict.get("breeding_fetish_start", False)

    @property
    def has_started_cum_fetish(self) -> bool:
        return self.event_triggers_dict.get("cum_fetish_start", False)

    @property
    def has_started_exhibition_fetish(self) -> bool:
        return self.event_triggers_dict.get("exhibition_fetish_start", False)

##########################################
# Roleplay functions                     #
##########################################

    def change_to_lingerie(self):
        if self.event_triggers_dict.get("girlfriend_sleepover_lingerie", None):
            self.apply_outfit(self.event_triggers_dict.pop("girlfriend_sleepover_lingerie"))
        elif self.event_triggers_dict.get("favourite_lingerie", None):
            self.apply_outfit(self.event_triggers_dict.get("favourite_lingerie", None))
        elif self.wardrobe.underwear_count > 0:
            self.apply_outfit(get_random_from_list(self.wardrobe.underwear_sets))
        else:
            self.apply_outfit(lingerie_wardrobe.pick_random_outfit())

    def roleplay_mc_title_swap(self, title: str):
        self.event_triggers_dict["backup_mc_title"] = self.mc_title
        self.set_mc_title(title)

    def roleplay_mc_title_revert(self):
        self.mc_title = self.event_triggers_dict.get("backup_mc_title", mc.name)

    def roleplay_title_swap(self, title: str):
        self.event_triggers_dict["backup_title"] = self.title
        self.set_title(title)

    def roleplay_title_revert(self):
        self.title = self.event_triggers_dict.get("backup_title", self.name)

    def roleplay_possessive_title_swap(self, title: str):
        self.event_triggers_dict["backup_possessive_title"] = self.possessive_title
        self.set_possessive_title(title)

    def roleplay_possessive_title_revert(self):
        self.possessive_title = self.event_triggers_dict.get("backup_possessive_title", self.name)

    def roleplay_personality_swap(self, personality: Personality):
        self.event_triggers_dict["backup_personality"] = self.personality
        self.personality = personality

    def roleplay_personality_revert(self):
        self.personality = self.event_triggers_dict.get("backup_personality", relaxed_personality)

##########################################
# Misc                                   #
##########################################

    @property
    def is_intern(self) -> bool:
        return self.has_role(college_intern_role)

    @property
    def is_jealous(self) -> bool:
        if self.love > 90 or self.obedience > 200:
            return False
        if not self.has_relation_with_mc:
            return False
        if self == sarah and sarah_threesomes_unlocked():
            return False
        return self.event_triggers_dict.get("is_jealous", True)

    @property
    def is_free_use(self) -> bool:  #Use this function to determine if the girl is very slutty and basically down for anything.
        if self.has_role(employee_freeuse_role) and self.is_at_work:
            return True

        if self.sluttiness < 80:
            return False
        # Doesn't hate any sexual actions
        if any(x for x in self.sexy_opinions if self.opinion(x) < -1):
            return False
        # likes or love public sex and loves vaginal and anal sex
        if self.opinion.public_sex < 1 or self.opinion.vaginal_sex < 2 or self.opinion.anal_sex < 2:
            return False

        return self.is_cum_dump or self.is_cum_bucket

    def have_orgasm(self, half_arousal = True, force_trance = False, trance_chance_modifier = 0, sluttiness_increase_limit = 30, reset_arousal = False, add_to_log = True):
        play_female_orgasm()
        mc.listener_system.fire_event("girl_climax", the_person = self)

        self.run_orgasm(show_dialogue = add_to_log, force_trance = force_trance, trance_chance_modifier = trance_chance_modifier, add_to_log = add_to_log, sluttiness_increase_limit = sluttiness_increase_limit, reset_arousal = reset_arousal, fire_event = False)
        self.change_happiness(3, add_to_log = add_to_log)

        if half_arousal:
            self.change_arousal(-self.arousal / 2, add_to_log = add_to_log)
        elif "report_log" in globals() and isinstance(report_log, dict):
            self.change_arousal(-builtins.max((self.arousal / (report_log.get("girl orgasms", 0) + 2)) + 20, self.arousal - self.max_arousal - 1), add_to_log = add_to_log)
        else:
            self.change_arousal(-self.arousal, add_to_log = add_to_log)

        if "report_log" in globals() and isinstance(report_log, dict):
            report_log["girl orgasms"] = report_log.get("girl orgasms", 0) + 1

    @property
    def favourite_colour(self) -> str:
        favourite_colour = self.event_triggers_dict.get("favourite_colour", None)

        #check if current favourite is still in list_of favourites
        list_of_favourites = [x for x in WardrobeBuilder.color_prefs if self.opinion(x) == 2]
        if favourite_colour in list_of_favourites:
            return favourite_colour

        # we need to find a new favourite colour going forward
        if len(list_of_favourites) > 0:
            new_favourite = renpy.random.choice(list_of_favourites)
        else:
            new_favourite = renpy.random.choice(list(WardrobeBuilder.color_prefs.keys()))
            self.set_opinion(new_favourite, 2)

        self.event_triggers_dict["favourite_colour"] = new_favourite
        return new_favourite

    @property
    def has_story(self) -> bool:
        return self.progress.has_description

    @cached_property
    def progress(self) -> Progression:
        return Progression(self)

    def clean_cache(self):
        global character_cache
        partial = f"ID:{self.identifier}"
        obsolete = [x for x in character_cache if partial in x]
        for x in obsolete:
            del character_cache[x]

    @property
    def current_position(self):
        if not hasattr(self, "_current_position"):
            self._current_position = None
        return self._current_position

    @current_position.setter
    def current_position(self, value: Position):
        self._current_position = value

##########################################
# event day functions                    #
##########################################
    def has_event_day(self, dict_key: str) -> bool:
        '''
        Return True when event day is set
        '''
        return dict_key in self.event_triggers_dict

    def has_event_delay(self, dict_key: str, delay: int = 7) -> bool:
        '''
        Retruns True when dict_key is not set or delay for dict_key has passed
        delay: number of days passed since dict_key was set
        '''
        return not self.has_event_day(dict_key) or self.days_since_event(dict_key) > delay

    def set_event_day(self, dict_key: str, set_day = None):
        '''
        Set event day with passed key, when no set_day is passed, current day is set
        '''
        self.event_triggers_dict[dict_key] = day if set_day is None else set_day

    def get_event_day(self, dict_key: str) -> int:
        '''
        Returns the day value set for key
        When key doesn't exist returns 0
        '''
        return self.event_triggers_dict.get(dict_key, 0)

    def days_since_event(self, dict_key: str) -> int:
        '''
        Number of days passed since value set for key
        When key does not exist returns 0
        '''
        return day - self.event_triggers_dict.get(dict_key, day)

    def story_event_ready(self, dict_key: str) -> bool:
        if self.days_since_event("story_event") < TIER_1_TIME_DELAY:        #In general, we want to keep tier 1 between all events with a certain person
            return False
        if self.days_since_event(dict_key + "_event") >= TIER_2_TIME_DELAY:           #Events of the same type should be spaced out a little further
            return self.is_available
        return False

    def story_event_log(self, dict_key: str):
        self.set_event_day(dict_key + "_event")
        self.set_event_day("story_event")

    def string_since_event(self, dict_key: str) -> str: #Returns a string describing how long it has been since an event
        since = self.days_since_event(dict_key)

        if since < 1:
            return "earlier"
        if since == 1:
            return "yesterday"
        if since <= 4:
            return "a few days ago"
        if since <= 10:
            return "a week ago"
        if since <= 19:
            return "a couple weeks ago"
        if since <= 28:
            return "a few weeks ago"
        if since <= 45:
            return "a month ago"
        if since <= 75:
            return "a couple months ago"
        if since <= 145:
            return "a few months ago"
        return "quite some time ago"

#########################
# Get To Know Functions #
#########################

    def set_gtk_list(self, new_gtk_list: ActionList = []):
        '''
        Input should be an actionlist with a set of get to know back story conversations for unique characters
        Technically setable though so we could add new ones at any point, including non unique girls.
        '''
        self.gtk_list = new_gtk_list
        return

    @property
    def has_gtk_list(self) -> bool:
        if self.gtk_list is None:
            return False
        return len(self.gtk_list) > 0

    @property
    def has_gtk_avail(self) -> bool:
        if self.gtk_list is None:
            return False
        if len(self.gtk_list) == 0:
            return False
        for act in self.gtk_list:
            if act.is_action_enabled(self):
                return True
        return False

    def build_gtk_list(self):
        gtk_actions_list = ["Get to Know Her"]
        for act in self.gtk_list:
            gtk_actions_list.append(act)
        gtk_actions_list.sort(key = sort_display_list, reverse = True)
        return gtk_actions_list

############################
# Jealous Sister Functions #
############################
    @property
    def is_jealous_sister(self) -> bool:
        return self.has_role(jealous_sister_role)

    def add_jealous_event(self, the_description: str, the_act: str):  #Add the tuple to the list and add to her jealousy score
        if self.is_jealous_sister:
            self.event_triggers_dict["jealous_list"].append((the_description, the_act))
            self.jealous_change_score(jealous_act_get_score(the_act))

    def get_jealous_description(self):
        if self.is_jealous_sister:
            this_tuple = self.get_jealous_list()[-1]
            return this_tuple[0]
        return "I'm not jealous of anyone right now, I just want to fuck!"

    def get_jealous_act(self):
        if self.is_jealous_sister:
            return self.event_triggers_dict.get("jealous_list", [("", "vaginal")])[-1][1]
        return "vaginal"

    def reset_jealous_list(self):
        self.event_triggers_dict["jealous_list"] = []

    def get_jealous_list(self):
        return self.event_triggers_dict.get("jealous_list", [("", "")])

    @property
    def jealous_score(self) -> int:
        return self.event_triggers_dict.get("jealous_score", 0)

    def jealous_score_reset(self):
        self.event_triggers_dict["jealous_score"] = 0

    def jealous_change_score(self, amount):
        self.event_triggers_dict["jealous_score"] = self.jealous_score + amount

    def reset_all_jealousy(self):
        self.reset_jealous_list()
        self.jealous_score_reset()
        self.event_triggers_dict["jealous_public_act"] = []

    def jealous_witness_public_sex(self, the_act):
        self.event_triggers_dict["jealous_public_act"].append(the_act)

    def jealous_witness_publix_sex_list(self):
        return self.event_triggers_dict.get("jealous_public_act", [])

    def jealous_sister_get_target_ident(self):
        return self.event_triggers_dict.get("jealous_target", None)

    def jealous_sister_get_revenge_tuple(self):   #Use a combination of her sluttiness and what acts she has witnessed to determine how she settles the score.
        target_score = 0
        #TODO use specific act scores so we can take opinions into account
        if self.sluttiness <= 20: #Look for foreplay events.
            target_score = 1
        if self.sluttiness <= 40:
            target_score = 2
        if self.sluttiness <= 60:
            target_score = 3
        target_score = 4

        for i in range(len(self.get_jealous_list()) - 1, -1, -1): #Iterate through the list backwards until we find a matching event for her to get revenge for.
            if self.get_jealous_list()[i][1] == target_score:
                return self.get_jealous_list()[i]
        # No matching event, so we just return the most recent event.
        return self.get_jealous_list()[-1]

##########################################
# Unique crisis addition functions       #
##########################################
    # Use these extensions to add only unique crisis. Checks to see if the event has already been added, so it won't duplicate.
    def add_unique_on_talk_event(self, action: Action) -> bool:
        '''
        Return True when action added to talk event list
        '''
        if action not in self.on_talk_event_list:
            self.on_talk_event_list.append(action)
            return True
        return False

    def add_unique_on_room_enter_event(self, action: Action) -> bool:
        '''
        Return True when action added to room event list
        '''
        if action not in self.on_room_enter_event_list:
            self.on_room_enter_event_list.append(action)
            return True
        return False

    def remove_on_talk_event(self, action: Action | str):
        if isinstance(action, str):
            if found := next((x for x in self.on_talk_event_list if action in (x.effect, x.name)), None):
                self.on_talk_event_list.remove(found)

        if action in self.on_talk_event_list:
            self.on_talk_event_list.remove(action)

    def remove_on_room_enter_event(self, action: Action | str):
        if isinstance(action, str):
            if found := next((x for x in self.on_room_enter_event_list if action in (x.effect, x.name)), None):
                self.on_room_enter_event_list.remove(found)

        if action in self.on_room_enter_event_list:
            self.on_room_enter_event_list.remove(action)

######################
# Sex skill wrappers #
######################

    @property
    def foreplay_sex_skill(self) -> int:
        return self.sex_skills["Foreplay"]

    @property
    def oral_sex_skill(self) -> int:
        return self.sex_skills["Oral"]

    @property
    def vaginal_sex_skill(self) -> int:
        return self.sex_skills["Vaginal"]

    @property
    def anal_sex_skill(self) -> int:
        return self.sex_skills["Anal"]

##########################
# opinion score wrappers #
##########################

    @cached_property
    def opinion(self) -> Opinion:
        return Opinion(self)

    @cached_property
    def known_opinion(self) -> Opinion:
        return Opinion(self, True)

#######################
# Sex Record Wrappers #
#######################

    def increase_handjobs(self):
        self.sex_record["Handjobs"] = self.sex_record.get("Handjobs", 0) + 1

    def increase_cunnilingus(self):
        self.sex_record["Cunnilingus"] = self.sex_record.get("Cunnilingus", 0) + 1

    def increase_tit_fucks(self):
        self.sex_record["Tit Fucks"] = self.sex_record.get("Tit Fucks", 0) + 1

    def increase_blowjobs(self):
        self.sex_record["Blowjobs"] = self.blowjob_count + 1

    def increase_vaginal_sex(self):
        self.sex_record["Vaginal Sex"] = self.vaginal_sex_count + 1

    def increase_anal_sex(self):
        self.sex_record["Anal Sex"] = self.anal_sex_count + 1

    def increase_fill_up_condom(self):
        self.sex_record["Filled Condom"] = self.sex_record.get("Filled Condom", 0) + 1

    @property
    def blowjob_count(self) -> int:
        return self.sex_record.get("Blowjobs", 0)

    @property
    def vaginal_sex_count(self) -> int:
        return self.sex_record.get("Vaginal Sex", 0)

    @property
    def anal_sex_count(self) -> int:
        return self.sex_record.get("Anal Sex", 0)

    @property
    def vaginal_creampie_count(self) -> int:
        return self.sex_record.get("Vaginal Creampies", 0)

    @property
    def anal_creampie_count(self) -> int:
        return self.sex_record.get("Anal Creampies", 0)

    @property
    def cum_facial_count(self) -> int:
        return self.sex_record.get("Cum Facials", 0)

    @property
    def cum_mouth_count(self) -> int:
        return self.sex_record.get("Cum in Mouth", 0)

    @property
    def cum_covered_count(self) -> int:
        return self.sex_record.get("Cum Covered", 0)

    @property
    def public_sex_count(self) -> int:
        return self.sex_record.get("Public Sex", 0)

    @property
    def cum_exposure_count(self) -> int:
        return (self.vaginal_creampie_count
            + self.anal_creampie_count
            + self.cum_facial_count
            + self.cum_mouth_count
            + self.cum_covered_count)

    @property
    def is_cum_dump(self) -> bool:
        return (self.vaginal_creampie_count > 1
            and self.anal_creampie_count > 1
            and self.cum_facial_count > 1
            and self.cum_mouth_count > 1
            and self.cum_covered_count > 1)

    @property
    def is_cum_bucket(self) -> bool:
        return (self.vaginal_creampie_count > 5
            and self.anal_creampie_count > 5
            and self.cum_mouth_count > 5)
