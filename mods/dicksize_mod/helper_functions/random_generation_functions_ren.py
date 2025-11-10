from __future__ import annotations
import builtins
import copy
from typing import Iterable
import renpy
from math import floor
from renpy import persistent
from renpy.exports import write_log
from game.random_lists_ren import get_random_font, get_random_from_weighted_list, get_random_job, get_random_personality, get_random_readable_color, colour_yellow
from game.bugfix_additions.ActionMod_ren import ActionMod
from game.helper_functions.list_functions_ren import get_random_from_list
from game.business_policies.recruitment_policies_ren import recruitment_skill_improvement_policy, recruitment_stat_improvement_policy
from game.clothing_lists_ren import diamond_ring, modern_glasses, big_glasses, sweater_dress, copper_bracelet, gold_bracelet, colourful_bracelets
from game.game_roles.stripclub._stripclub_role_definitions_ren import strip_club_is_closed, bdsm_room_available
from game.personality_types._personality_definitions_ren import wild_personality, bimbo_personality, relaxed_personality, introvert_personality, reserved_personality, alpha_personality, cougar_personality
from game.major_game_classes.game_logic.Room_ren import Room, strip_club, bdsm_room, downtown_bar, downtown_hotel, downtown, hospital
from game.major_game_classes.character_related._job_definitions_ren import JobDefinition, prostitute_job, stripper_job
from game.major_game_classes.character_related.Person_ren import Person, list_of_patreon_characters, tan_images_dict
from game.major_game_classes.clothing_related.Outfit_ren import Outfit
from game.major_game_classes.clothing_related.Wardrobe_ren import Wardrobe, default_wardrobe
from game.major_game_classes.clothing_related.wardrobe_builder_ren import WardrobeBuilder
from game.major_game_classes.clothing_related.wardrobe_preferences_ren import WardrobePreference


"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -1 python:
"""
# This will be called in game when a person is created original function in script.rpy
def make_person(name = None, name_list = None, last_name = None, last_name_list = None, age = None, age_range = None, body_type = None, body_type_list = None, face_style = None, face_style_list = None, tits = None, tits_range = None, height = None, height_range = None,
        hair_colour = None, hair_colour_list = None, hair_style = None, hair_style_list = None, pubes_style = None, pubes_style_list = None, skin = None, skin_list = None, eyes = None, eyes_list = None, job: JobDefinition = None, job_list: list[JobDefinition] = None,
        personality = None, personality_list = None, custom_font = None, custom_font_list = None, name_color = None, name_color_list = None, dial_color = None, dial_color_list = None, starting_wardrobe = None, starting_wardrobe_list = None, stat_array = None, stat_range_array = None, skill_array = None, skill_range_array = None,
        sex_skill_array = None, sex_skill_range_array = None, sluttiness = None, sluttiness_range = None, obedience = None, obedience_range = None, happiness = None, happiness_range = None, love = None, love_range = None, start_home = None,
        title = None, possessive_title = None, mc_title = None, relationship = None, relationship_list = None, kids = None, kids_range = None, kids_floor = None, kids_ceiling = None, SO_name = None, SO_name_list = None, base_outfit = None, base_outfit_list = None,
        generate_insta = None, generate_dikdok = None, generate_onlyfans = None, vagina_tightness = None, ###jes:Added vagina_tightness
        suggestibility = None, suggestibility_range = None, work_experience = None, work_experience_range = None,
        tan_style: str = None, serum_tolerance = None, 
        forced_opinions: Iterable[tuple[str, int, bool]] = None, forced_sexy_opinions: Iterable[tuple[str, int, bool]] = None, type = 'random', allow_premade = False) -> Person:

    return_character = None
    if type == "random" and allow_premade and renpy.random.randint(1, 100) < 20:
        return_character = get_premade_character(age_range, tits_range, height_range, kids_range, relationship_list)

    if return_character is None: #Either we aren't getting a pre-made, or we are out of them.
        return_character = create_random_person(name = name, name_list = name_list, last_name = last_name, last_name_list = last_name_list, age = age, age_range = age_range, body_type = body_type, body_type_list = body_type_list, face_style = face_style, face_style_list = face_style_list, tits = tits, tits_range = tits_range, height = height, height_range = height_range,
            hair_colour = hair_colour, hair_colour_list = hair_colour_list, hair_style = hair_style, hair_style_list = hair_style_list, pubes_style = pubes_style, pubes_style_list = pubes_style_list, skin = skin, skin_list = skin_list, eyes = eyes, eyes_list = eyes_list, job = job, job_list = job_list,
            personality = personality, personality_list = personality_list, custom_font = custom_font, custom_font_list = custom_font_list, name_color = name_color, name_color_list = name_color_list, dial_color = dial_color, dial_color_list = dial_color_list, starting_wardrobe = starting_wardrobe, starting_wardrobe_list = starting_wardrobe_list, stat_array = stat_array, stat_range_array = stat_range_array, skill_array = skill_array, skill_range_array = skill_range_array,
            sex_skill_array = sex_skill_array, sex_skill_range_array = sex_skill_range_array, sluttiness = sluttiness, sluttiness_range = sluttiness_range, obedience = obedience, obedience_range = obedience_range, happiness = happiness, happiness_range = happiness_range, love = love, love_range = love_range, start_home = start_home, tan_style = tan_style, serum_tolerance = serum_tolerance,
            title = title, possessive_title = possessive_title, mc_title = mc_title, relationship = relationship, relationship_list = relationship_list, kids = kids, kids_range = kids_range, kids_floor = kids_floor, kids_ceiling = kids_ceiling, SO_name = SO_name, SO_name_list = SO_name_list, base_outfit = base_outfit, base_outfit_list = base_outfit_list,
            generate_insta = generate_insta, generate_dikdok = generate_dikdok, generate_onlyfans = generate_onlyfans, vagina_tightness = vagina_tightness, ###jes:Added vagina_tightness
            suggestibility = suggestibility, suggestibility_range = suggestibility_range, work_experience = work_experience, work_experience_range = work_experience_range, type = type)

    # apply forced opinions after we 'update opinions', so we don't override them there
    if forced_opinions and isinstance(forced_opinions, (list, tuple, set)):
        for opinion in forced_opinions:
            return_character.opinions[opinion[0]] = [opinion[1], opinion[2]]

    if forced_sexy_opinions and isinstance(forced_sexy_opinions, (list, tuple, set)):
        for opinion in forced_sexy_opinions:
            return_character.sexy_opinions[opinion[0]] = [opinion[1], opinion[2]]

    if return_character.base_outfit and len(return_character.base_outfit.accessories) == 0 and return_character.opinion.makeup > 0:
        WardrobeBuilder.add_make_up_to_outfit(return_character, return_character.base_outfit)

    if return_character.type == 'random':
        create_party_schedule(return_character)

    return return_character

# create_random_person is used to generate a Person object from a list of random or provided stats. use "make_a_person" to properly get premade characters mixed with random.
def create_random_person(name = None, name_list = None, last_name = None, last_name_list = None, age = None, age_range = None, body_type = None, body_type_list = None, face_style = None, face_style_list = None, tits = None, tits_range = None, height = None, height_range = None,
        hair_colour = None, hair_colour_list = None, hair_style = None, hair_style_list = None, pubes_style = None, pubes_style_list = None, skin = None, skin_list = None, eyes = None, eyes_list = None, job: JobDefinition = None, job_list: list[JobDefinition] = None,
        personality = None, personality_list = None, custom_font = None, custom_font_list = None, name_color = None, name_color_list = None, dial_color = None, dial_color_list = None, starting_wardrobe: Wardrobe | None = None, starting_wardrobe_list = None, stat_array = None, stat_range_array = None, skill_array = None, skill_range_array = None,
        sex_skill_array = None, sex_skill_range_array = None, sluttiness = None, sluttiness_range = None, obedience = None, obedience_range = None, happiness = None, happiness_range = None, love = None, love_range = None, start_home: Room | None = None, tan_style: str = None, serum_tolerance = None,
        title = None, possessive_title = None, mc_title = None, relationship = None, relationship_list = None, kids = None, kids_range = None, kids_floor = None, kids_ceiling = None, SO_name = None, SO_name_list = None, base_outfit = None, base_outfit_list = None,
        generate_insta = None, generate_dikdok = None, generate_onlyfans = None, vagina_tightness = None, ###jes:Added vagina_tightness
        suggestibility = None, suggestibility_range = None, work_experience = None, work_experience_range = None, type="random") -> Person:

    if personality is None:
        personality = (
            get_random_personality()
            if personality_list is None
            else get_random_from_list(personality_list)
        )

    if generate_insta is None:
        generate_insta = renpy.random.randint(0, 100) < personality.insta_chance

    if generate_dikdok is None:
        generate_dikdok = renpy.random.randint(0, 100) < personality.dikdok_chance

    if generate_onlyfans is None:
        generate_onlyfans = False

    if name is None:
        name = (
            Person.get_random_name()
            if name_list is None
            else get_random_from_list(name_list)
        )

    if last_name is None:
        last_name = (
            Person.get_random_last_name()
            if last_name_list is None
            else get_random_from_list(last_name_list)
        )

    if job is None:
        job = get_random_job() if job_list is None else get_random_from_list(job_list)

    if age is None:
        if age_range is None:
            if job and job.age_range:
                age_range = job.age_range
            else:
                age_range = [Person.get_age_floor(), Person.get_age_ceiling()]

        if age_range[0] > age_range[1]: #Make sure range is correct order
            age_range.reverse()

        # use linear decreasing distribution in age range (more young than old)
        age = builtins.int(
            floor(
                abs(renpy.random.random() - renpy.random.random())
                * (1 + age_range[1] - age_range[0])
                + age_range[0],
            ),
        )

    if body_type is None:
        if body_type_list is None:
            body_type = Person.get_random_body_type()
        else:
            body_type = get_random_from_list(body_type_list)
    if tits is None:
        tits = (
            Person.get_random_tit()
            if tits_range is None
            else get_random_from_weighted_list(tits_range)
        )
    if height is None:
        if height_range is None:
            height = renpy.random.uniform(Person.get_height_floor(), Person.get_height_ceiling())
        else:
            if height_range[0] > height_range[1]:
                height_range.reverse()
            height = renpy.random.uniform(height_range[0], height_range[1])
    if hair_colour is None: #If we pass nothing we can pick a random hair colour
        if hair_colour_list is None:
            hair_colour = Person.generate_hair_colour() #Hair colour is a list of [string, [colour]], generated with variations by this function,
        else:
            hair_colour = get_random_from_list(hair_colour_list)
    if isinstance(hair_colour, str):
        hair_colour = Person.generate_hair_colour(hair_colour) #If we pass a string assume we want to generate a variation based on that colour.
    #else: we assume a full colour list was passed and everything is okay.

    if hair_style is None:
        if hair_style_list is None:
            hair_style = Person.get_random_hair_style()
        else:
            hair_style = get_random_from_list(hair_style_list)

    hair_style = hair_style.get_copy()
    hair_style.colour = hair_colour[1]

    if pubes_style is None:
        if pubes_style_list is None:
            pubes_style = Person.get_random_pubes_style()
        else:
            pubes_style = get_random_from_list(pubes_style_list).get_copy()

    if eyes is None:
        eyes = (
            Person.generate_eye_colour()
            if eyes_list is None
            else get_random_from_list(eyes_list)
        )
    if isinstance(eyes, str):
        eyes = Person.generate_eye_colour(eyes) #If it's a string assume we want a variation within that eye category
    # else: we assume at this point what was passed is a correct [description, colour] list.

    if skin is None:
        skin = (
            Person.get_random_skin()
            if skin_list is None
            else get_random_from_list(skin_list)
        )

    if face_style is None:
        face_style = (
            Person.get_random_face()
            if face_style_list is None
            else get_random_from_list(face_style_list)
        )

    if tan_style is None and renpy.random.randint(0, 1) == 1: # 50% chance on random tan (could be no_tan)
        tan_style = get_random_from_list((x for x in tan_images_dict), "No Tan")

    if suggestibility is None:
        if suggestibility_range is None:
            suggestibility_range = [Person.get_suggestibility_floor(), Person.get_suggestibility_ceiling()]

        if personality.base_personality_prefix == wild_personality.personality_type_prefix:
            suggestibility_range[0] += 5
        elif personality.base_personality_prefix == bimbo_personality.personality_type_prefix:
            suggestibility_range[0] += 10
        elif personality.base_personality_prefix == relaxed_personality.personality_type_prefix:
            suggestibility_range[0] += 3
        elif personality.base_personality_prefix == introvert_personality.personality_type_prefix:
            suggestibility_range[1] -= 3
        elif personality.base_personality_prefix == reserved_personality.personality_type_prefix:
            suggestibility_range[1] -= 5

    if custom_font is None:
        if custom_font_list is None:
            #Get a font
            custom_font = get_random_font()
        else:
            custom_font = get_random_from_list(custom_font_list)
    if name_color is None:
        if name_color_list is None:
            # Get a color
            name_color = get_random_readable_color()
        else:
            name_color = get_random_from_list(name_color_list)

    if dial_color is None:
        if dial_color_list is None:
            # Use name_color
            dial_color = copy.copy(name_color) #Take a copy
        else:
            dial_color = get_random_from_list(dial_color)

    if skill_array is None:
        if skill_range_array is None:
            skill_range_array = [
                [Person.get_skill_floor(), Person.get_skill_ceiling()]
                for x in range(0, 5)
            ]
        skill_array = [
            renpy.random.randint(skill_range[0], skill_range[1])
            for skill_range in skill_range_array
        ]

    if stat_array is None:
        if stat_range_array is None:
            stat_range_array = [
                [Person.get_stat_floor(), Person.get_stat_ceiling()]
                for x in range(0, 3)
            ]
        stat_array = [
            renpy.random.randint(stat_range[0], stat_range[1])
            for stat_range in stat_range_array
        ]

    if sex_skill_array is None:
        if sex_skill_range_array is None:
            sex_skill_range_array = [
                [Person.get_sex_skill_floor(), Person.get_sex_skill_ceiling()]
                for x in range(0, 4)
            ]
        sex_skill_array = [
            renpy.random.randint(sex_skill_range[0], sex_skill_range[1])
            for sex_skill_range in sex_skill_range_array
        ]

    if love is None:
        if love_range is None:
            love_range = [Person.get_love_floor(), Person.get_love_ceiling()]
        love = renpy.random.randint(love_range[0], love_range[1])

    if happiness is None:
        if happiness_range is None:
            happiness_range = [Person.get_happiness_floor(), Person.get_happiness_ceiling()]
        happiness = renpy.random.randint(happiness_range[0], happiness_range[1])

    if suggestibility is None:
        if suggestibility_range is None:
            suggestibility_range = [Person.get_suggestibility_floor(), Person.get_suggestibility_ceiling()]
        suggestibility = renpy.random.randint(suggestibility_range[0], suggestibility_range[1])

    if obedience is None:
        if obedience_range is None:
            obedience_range = [Person.get_obedience_floor(), Person.get_obedience_ceiling()]
        obedience = renpy.random.randint(obedience_range[0], obedience_range[1])

    if sluttiness is None:
        if sluttiness_range is None:
            sluttiness_range = [Person.get_sluttiness_floor(), Person.get_sluttiness_ceiling()]
        sluttiness = renpy.random.randint(sluttiness_range[0], sluttiness_range[1])

    if work_experience is None:
        if work_experience_range is None:
            work_experience_range = [Person.get_work_experience_floor(), Person.get_work_experience_ceiling()]
        work_experience = renpy.random.randint(work_experience_range[0], work_experience_range[1])

    if relationship is None:
        if relationship_list is None:
            relationship_list = Person.get_potential_relationships_list()
        relationship_list = Person.finalize_relationships_weight(relationship_list, age)
        relationship = get_random_from_weighted_list(relationship_list)

    if starting_wardrobe is None and starting_wardrobe_list is not None:
        starting_wardrobe = get_random_from_list(starting_wardrobe_list)

    if base_outfit is None:
        if base_outfit_list is None:
            base_outfit = Outfit(name + "'s base accessories")
            if relationship in ("Fiancée", "Married"):
                base_outfit.add_accessory(diamond_ring.get_copy(), colour_yellow)

            if renpy.random.randint(0, 100) < age:
                #They need/want glasses.
                the_glasses = (
                    modern_glasses.get_copy()
                    if renpy.random.randint(0, 100) < 50
                    else big_glasses.get_copy()
                )
                the_glasses.colour = [.212, .271, .31, .95]
                base_outfit.add_accessory(the_glasses)

            if renpy.random.randint(0, 3) == 0:
                bracelet = get_random_from_list([copper_bracelet, gold_bracelet, colourful_bracelets])
                bracelet.colour = get_random_from_list([[.98, .92, .36, .95], [.529, .808, .922, 0.95], [.890, .258, .203, .95], [.7, .7, .7, .95]])
                base_outfit.add_accessory(bracelet)
        else:
            base_outfit = get_random_from_list(base_outfit_list)
    if kids is None:
        #Need to define these if unknown
        if age_range is None:
            age_range = [age, age]
        if relationship_list is None:
            relationship_list = [relationship]
        if kids_range is None:
            kids_range = Person.get_initial_kids_range(age_range, relationship_list)
        kids_range = Person.finalize_kids_range(kids_range, age_range, relationship_list, age, relationship)
        kids = renpy.random.randint(kids_range[0], kids_range[1])
        if kids_floor is None:
            kids_floor = 0
        kids = max(kids, kids_floor)
        if kids_ceiling is not None:
            kids = min(kids, kids_ceiling)

    ###jes:Added vagina_tightness
    if vagina_tightness is None:
        if kids >= 1:
            vagina_tightness = 5
        elif sex_skill_array[2] == 0:
            vagina_tightness = 0
        else:
            vagina_tightness = renpy.random.randint(sex_skill_array[2]-2, sex_skill_array[2]+2)
            if vagina_tightness >= 6:
                vagina_tightness = 5
            elif vagina_tightness < 1:
                vagina_tightness = 1

    if relationship != "Single" and SO_name is None:
        SO_name = (
            Person.get_random_male_name()
            if SO_name_list is None
            else get_random_from_list(SO_name_list)
        )

    if serum_tolerance is None:
        serum_tolerance = get_random_from_weighted_list([[0, 5], [1, 20], [2, 40], [3, 30], [4, 5]])

    person = Person(name, last_name, age, body_type, tits, height, hair_colour, hair_style, pubes_style, skin, eyes, job, starting_wardrobe, personality,
        stat_array, skill_array, sex_skill_list = sex_skill_array, sluttiness= sluttiness, obedience = obedience, suggest = suggestibility, love=love, happiness=happiness, home = start_home,
        font = custom_font, name_color = name_color, dialogue_color = dial_color, vagina_tightness = vagina_tightness, ###jes:Added vagina_tightness
        face_style = face_style, tan_style = tan_style, serum_tolerance = serum_tolerance,
        title = title, possessive_title = possessive_title, mc_title = mc_title,
        relationship = relationship, kids = kids, SO_name = SO_name, base_outfit = base_outfit,
        generate_insta = generate_insta, generate_dikdok = generate_dikdok, generate_onlyfans = generate_onlyfans,
        work_experience = work_experience, type=type)

    person.init_person_variables()
    person.reset_event_parameters()

    write_log(
        f"Created: {person.name} {person.last_name},"
        f" Age: {person.age},"
        f" Stats: {stat_array},"
        f" Skills: {skill_array},"
        f" Relation: {person.relationship},"
        f" Kids: {person.kids},"
        f" Sluttiness: {person.sluttiness},"
        f" Suggestibility: {person.suggestibility},"
        f" Job Experience: {person.work_experience},"
        f" Job: {person.primary_job.job_title}",
    )

    # update opinions and personality
    update_person_opinions(person)
    if not person.is_unique:
        update_special_personalities(person)    # set optional alpha / cougar personalities

    # init wardrobe after creating the person class so we can use updated opinions for outfit creation
    rebuild_wardrobe(person)

    if persistent.mark_unique_as_favourite and type == "story":
        person.toggle_favourite()

    # girl has ended her menopause and is no longer able to have children
    # TODO: maybe add a story line for these characters to make them produce eggs again
    if persistent.pregnancy_pref != 0 and person.age > renpy.random.randint(49, 53):
        person.fertility_percent = -1000

    # make her dress using the newly created wardrobe
    person.planned_outfit = person.decide_on_outfit()
    person.apply_outfit(person.planned_outfit)
    return person

def get_premade_character(age_range, tits_range, height_range, kids_range, relationship_list):
    allowed_characters = [x for x in list_of_patreon_characters
        if x.age >= age_range[0] and x.age <= age_range[1] and
        x.height >= height_range[0] and x.height <= height_range[1] and
        x.kids >= kids_range[0] and x.kids <= kids_range[1] and
        x.tits in (x[0] for x in tits_range) and
        x.relationship in (x[0] for x in relationship_list)]

    if len(allowed_characters) == 0: # no more pre-made left or do not conform to hire restrictions
        return None

    person = renpy.random.choice(allowed_characters)

    # improve stats for pre-made characters to be on par with random generated characters
    if recruitment_skill_improvement_policy.is_active:
        person.hr_skill += renpy.random.randint(1, 2)
        person.market_skill += renpy.random.randint(1, 2)
        person.research_skill += renpy.random.randint(1, 2)
        person.production_skill += renpy.random.randint(1, 2)
        person.supply_skill += renpy.random.randint(1, 2)

    if recruitment_stat_improvement_policy.is_active:
        person.charisma += renpy.random.randint(1, 2)
        person.int += renpy.random.randint(1, 2)
        person.focus += renpy.random.randint(1, 2)

    list_of_patreon_characters.remove(person)
    return person

def create_hooker(add_to_game = True):
    person = make_person(sluttiness = renpy.random.randint(20, 35),
        sex_skill_range_array = [[2, Person.get_sex_skill_ceiling()] for x in range(4)],
        job = prostitute_job,
        forced_opinions = [
            ["flirting", 2, True],
            ["high heels", 2, True],
            ["makeup", 1, True],
            ["pants", -2, False],
            ["skirts", 2, True]],
        forced_sexy_opinions = [
            ["bareback sex", -2, True],
            ["being submissive", 1, False],
            ["giving blowjobs", 2, False],
            ["public sex", 2, False],
            ["showing her tits", 1, False],
            ["skimpy outfits", 2, True],
            ["vaginal sex", 2, False]],
        work_experience = 1)

    person.set_mc_title("Honey")
    if add_to_game:
        person.generate_home().add_person(person)
    return person

def create_old_hooker_with_daughter():
    person = create_hooker()
    person.age = 43
    daughter = person.generate_daughter(job = prostitute_job)
    # make sure minimum hooker opinions are set for daughter
    daughter.set_opinion("high heels", 2, True)
    daughter.set_opinion("pants", -2, False)
    daughter.set_opinion("skirts", 2, True)
    daughter.set_opinion("bareback sex", -2, True)
    daughter.set_opinion("giving blowjobs", 2, False)
    daughter.set_opinion("skimpy outfits", 2, True)
    daughter.set_opinion("vaginal sex", 2, False)
    daughter.set_mc_title("Daddy")
    return daughter

def create_stripper():
    person = make_person(sluttiness = renpy.random.randint(15, 30),
        job = stripper_job,
        forced_opinions = [
            ["small talk", 1, True],
            ["conservative outfits", -2, True],
            ["flirting", 2, True],
            ["high heels", 2, True],
            ["work uniforms", 1, True]],
        forced_sexy_opinions = [
            ["showing her tits", 2, True],
            ["showing her ass", 2, True],
            ["skimpy outfits", 2, True],
            ["taking control", 2, True]],
        work_experience = 1)

    person.set_mc_title("Honey")
    person.generate_home()
    person.home.add_person(person)
    return person

def update_person_opinions(person: Person):
    ensure_opinion_on_subject(person, ["dresses", "pants", "skirts"])
    ensure_opinion_on_subject(person, ["boots", "high heels"])
    ensure_opinion_on_subject(person, ["classical music", "heavy metal music", "jazz", "punk music", "pop music"])
    ensure_opinion_on_subject(person, ["Mondays", "Fridays", "the weekend"])
    ensure_opinion_on_subject(person, ["hiking", "sports", "yoga"])

    ensure_sexy_opinion_on_subject(person, ["lingerie", "showing her tits", "showing her ass"])
    ensure_sexy_opinion_on_subject(person, ["skimpy outfits", "not wearing underwear", "skimpy uniforms"])

    # skew anal sex to negative
    if person.anal_sex_skill > 2:
        person.sex_skills["Anal"] -= 2

    # by default there is a negative skew opinion on incest / threesomes / cheating (66%)
    if person.opinion.incest == 0 and renpy.random.randint(0, 2) != 1:
        person.set_opinion("incest", renpy.random.choice([-2, -1]), False)

    if person.opinion.threesomes == 0 and renpy.random.randint(0, 2) != 1:
        person.set_opinion("threesomes", renpy.random.choice([-2, -1]), False)

    if person.opinion.cheating_on_men == 0 and renpy.random.randint(0, 2) != 1:
        person.set_opinion("cheating on men", renpy.random.choice([-2, -1]), False)

    # do we have sexual preferences / dislikes?
    ensure_opinion_on_sexual_preference(person, "Foreplay", ["kissing", "being fingered", "giving handjobs"])
    ensure_opinion_on_sexual_preference(person, "Oral", ["giving blowjobs", "getting head", "drinking cum"])
    ensure_opinion_on_sexual_preference(person, "Vaginal", ["missionary style sex", "vaginal sex", "creampies"])
    ensure_opinion_on_sexual_preference(person, "Anal", ["anal sex", "anal creampies", "doggy style sex"])

    # fix opinion contradictions (one cannot exclude other)
    fix_opinion_contradiction(person, "drinking cum", ["giving blowjobs"])
    fix_opinion_contradiction(person, "bareback sex", ["creampies", "anal creampies"])
    fix_opinion_contradiction(person, "skimpy outfits", ["showing her tits", "showing her ass", "high heels"])
    fix_opinion_contradiction(person, "masturbating", ["being fingered"])
    fix_opinion_contradiction(person, "vaginal sex", ["creampies"])
    fix_opinion_contradiction(person, "anal sex", ["anal creampies"])

    # choose at least three colours for an opinion (one from primary, one from b/w, one from secondary)
    ensure_opinion_on_subject(person, ["the colour red", "the colour green", "the colour blue"])
    ensure_opinion_on_subject(person, ["the colour black", "the colour white"])
    ensure_opinion_on_subject(person, ["the colour pink", "the colour purple", "the colour orange", "the colour yellow", "the colour brown"])

    # fix opinion exclusion (one excludes other)
    fix_opinion_exclusion(person, "lingerie", ["not wearing underwear", "not wearing anything"])
    fix_opinion_exclusion(person, "skimpy outfits", ["not wearing anything", "conservative outfits"])
    fix_opinion_exclusion(person, "the colour red", ["the colour pink", "the colour purple"]) # red and pink/purple clash
    fix_opinion_exclusion(person, "the colour pink", ["the colour purple", "the colour red"]) # pink and purple/red clash
    fix_opinion_exclusion(person, "the colour purple", ["the colour pink", "the colour red", "the colour blue"]) # purple and pink/red/blue clash
    fix_opinion_exclusion(person, "the colour blue", ["the colour purple"]) # pink and purple clash
    fix_opinion_exclusion(person, "the colour orange", ["the colour yellow"]) # orange and yellow clash
    fix_opinion_exclusion(person, "the colour yellow", ["the colour orange"]) # yellow and orange clash

    # set work opinions (based on stats / skills)
    if not person.is_unique:
        set_work_opinion(person, "research work", person.int, person.research_skill)
        set_work_opinion(person, "marketing work", person.charisma, person.market_skill)
        set_work_opinion(person, "HR work", person.charisma, person.hr_skill)
        set_work_opinion(person, "supply work", person.focus, person.supply_skill)
        set_work_opinion(person, "production work", person.focus, person.production_skill)

def set_work_opinion(person, skill, stat_level, skill_level):
    known = True # renpy.random.randint(0, 2) == 1
    if skill_level < 2 and stat_level < 3:
        person.opinions[skill] = [-2, known]
    elif skill_level < 3 and stat_level < 4:
        person.opinions[skill] = [-1, known]
    elif skill_level > 4 and stat_level > 5:
        person.opinions[skill] = [2, known]
    elif skill_level > 3 and stat_level > 4:
        person.opinions[skill] = [1, known]
    elif skill in person.opinions:
        del person.opinions[skill]

# when she doesn't like base_topic, she should not like / love related topic (invert likeness of related topic)
def fix_opinion_contradiction(person: Person, base_topic, related_topics):
    for related_topic in related_topics:
        # first skew related to positive base
        if person.opinion(base_topic) > 0 and person.opinion(related_topic) < 0:
            person.update_opinion_with_score(related_topic, -person.opinion(related_topic), add_to_log = False)
        if person.opinion(base_topic) < 0 and person.opinion(related_topic) > 0:
            person.update_opinion_with_score(related_topic, -person.opinion(related_topic), add_to_log = False)

def fix_opinion_exclusion(person: Person, base_topic, related_topics):
    for related_topic in related_topics:
        if person.opinion(base_topic) > 0 and person.opinion(related_topic) > 0:
            person.update_opinion_with_score(related_topic, -person.opinion(related_topic), add_to_log = False)
        if person.opinion(base_topic) < 0 and person.opinion(related_topic) < 0:
            person.update_opinion_with_score(related_topic, -person.opinion(related_topic), add_to_log = False)

def ensure_opinion_on_subject(person: Person, opinions):
    if not any(x[0] in person.opinions for x in opinions):
        the_opinion_key = get_random_from_list(opinions)
        degree = renpy.random.choice([-2, -1, 1, 2])
        person.opinions[the_opinion_key] = [degree, False]

def ensure_sexy_opinion_on_subject(person: Person, opinions):
    if not any(x[0] in person.opinions for x in opinions):
        the_opinion_key = get_random_from_list(opinions)
        degree = renpy.random.choice([-2, -1, 1, 2])
        person.sexy_opinions[the_opinion_key] = [degree, False]

def ensure_opinion_on_sexual_preference(person: Person, sex_skill, opinions):
    if not any(x[0] in person.sexy_opinions for x in opinions):
        the_opinion_key = get_random_from_list(opinions)
        if person.sex_skills[sex_skill] >= 5: # positive skew
            degree = renpy.random.choice([1, 2])
        elif person.sex_skills[sex_skill] < 2: # negative skew
            degree = renpy.random.choice([-2, -1])
        else: # random
            degree = renpy.random.choice([-2, -1, 1, 2])
        person.sexy_opinions[the_opinion_key] = [degree, False]

def enhance_existing_wardrobe(person: Person, max_outfits):
    outfit_builder = WardrobeBuilder(person)

    while person.wardrobe.outfit_count <= max_outfits:    # add some generated outfits
        (min_slut, max_slut) = WardrobeBuilder.get_clothing_min_max_slut_value(renpy.random.randint(20, 100))
        outfit = outfit_builder.build_outfit("full", max_slut, min_slut)
        if outfit.has_overwear and person.approves_outfit_color(outfit):
            person.wardrobe.add_outfit(outfit)

    while person.wardrobe.overwear_count <= max_outfits:    # add some generated outfits
        (min_slut, max_slut) = WardrobeBuilder.get_clothing_min_max_slut_value(renpy.random.randint(20, 100))
        overwear = outfit_builder.build_outfit("over", max_slut, min_slut)
        if overwear.is_suitable_overwear_set and person.approves_outfit_color(overwear):
            person.wardrobe.add_overwear_set(overwear)

    while person.wardrobe.underwear_count <= max_outfits:    # add some generated outfits
        (min_slut, max_slut) = WardrobeBuilder.get_clothing_min_max_slut_value(renpy.random.randint(20, 100))
        underwear = outfit_builder.build_outfit("under", max_slut, min_slut)
        if underwear.is_suitable_underwear_set and person.approves_outfit_color(underwear):
            person.wardrobe.add_underwear_set(underwear)

def rebuild_wardrobe(person: Person, force = False):
    # skip personalized wardrobes
    if not (force or person.wardrobe is None):
        return

    base_wardrobe = Wardrobe(f"{person.name}_{person.last_name}_wardrobe")
    if not force and persistent.low_memory_wardrobes:
        person.wardrobe = base_wardrobe
        return

    preferences = WardrobePreference(person)

    outfit: Outfit
    for outfit in renpy.random.sample(default_wardrobe.outfit_sets, default_wardrobe.outfit_count):
        if not outfit.has_clothing(sweater_dress) and outfit.has_overwear and preferences.evaluate_outfit(outfit, 999) and person.approves_outfit_color(outfit):
            base_wardrobe.add_outfit(outfit.get_copy())
        if base_wardrobe.outfit_count > 5:
            break

    overwear: Outfit
    for overwear in renpy.random.sample(default_wardrobe.overwear_sets, default_wardrobe.overwear_count):
        if not overwear.has_clothing(sweater_dress) and overwear.is_suitable_overwear_set and preferences.evaluate_outfit(overwear, 999) and person.approves_outfit_color(overwear):
            base_wardrobe.add_overwear_set(overwear.get_copy())
        if base_wardrobe.overwear_count > 5:
            break

    underwear: Outfit
    for underwear in renpy.random.sample(default_wardrobe.underwear_sets, default_wardrobe.underwear_count):
        if underwear.is_suitable_underwear_set and preferences.evaluate_outfit(underwear, 999) and person.approves_outfit_color(underwear):
            base_wardrobe.add_underwear_set(underwear.get_copy())
        if base_wardrobe.underwear_count > 5:
            break

    # ensure we have at least 2 base wardrobe outfits by removing surplus, but keep the most decent outfit from default wardrobe
    while base_wardrobe.outfit_count > 3:
        base_wardrobe.remove_outfit(sorted(base_wardrobe.outfit_sets, key = lambda x: x.outfit_slut_score)[renpy.random.randint(1, base_wardrobe.outfit_count - 1)])
    while base_wardrobe.overwear_count > 3:
        base_wardrobe.remove_outfit(sorted(base_wardrobe.overwear_sets, key = lambda x: x.outfit_slut_score)[renpy.random.randint(1, base_wardrobe.overwear_count - 1)])
    while base_wardrobe.underwear_count > 3:
        base_wardrobe.remove_outfit(sorted(base_wardrobe.underwear_sets, key = lambda x: x.outfit_slut_score)[renpy.random.randint(1, base_wardrobe.underwear_count - 1)])

    person.wardrobe = base_wardrobe

    # add make-up to base outfit (based on pref)
    WardrobeBuilder.add_make_up_to_outfit(person, person.base_outfit)

    # add some auto generated outfits (max 4 outfits per category)
    enhance_existing_wardrobe(person, 4)

def get_party_destinations():
    party_destinations = [downtown_bar, downtown_hotel, downtown, hospital]
    if not strip_club_is_closed():
        party_destinations.append(strip_club)
        if bdsm_room_available():
            party_destinations.append(bdsm_room)
    return party_destinations

def create_party_schedule(person: Person):
    if person.is_unique:
        return  # don't touch unique characters
    if person.is_strip_club_employee:
        return  # no party for the working girls
    if person.pregnancy_is_visible:
        return  # no party for girls who already show the baby bump
    if person.has_job(prostitute_job):
        return  # working girls always have a party

    # clear old party schedule (clear after stripper check as to not clear her override schedule during foreclosed phase)
    person.set_override_schedule(None, time_slots = [4])

    count = 0
    party_destinations = get_party_destinations()
    if person.opinion("Mondays") > 0:
        person.set_override_schedule(renpy.random.choice(party_destinations), day_slots = [0], time_slots=[4])
        count += 1
    if person.opinion("Fridays") > 0:
        person.set_override_schedule(renpy.random.choice(party_destinations), day_slots = [4], time_slots=[4])
        count += 1
    if person.opinion("the weekend") > 0:
        person.set_override_schedule(renpy.random.choice(party_destinations), day_slots = [5], time_slots=[4])
        person.set_override_schedule(renpy.random.choice(party_destinations), day_slots = [6], time_slots=[4])
        count += 2

    while count < 2:
        rnd_day = renpy.random.randint(0, 6)
        person.set_override_schedule(renpy.random.choice(party_destinations), day_slots = [rnd_day], time_slots=[4])
        count += 1
    return

def update_special_personalities(person: Person):
    # turn cougars on or off
    update_cougar_personality(person)
    # turn alpha personality on or off
    update_alpha_personality(person)

def update_cougar_personality(person: Person):
    # change personality to cougar if we meet age requirement
    if ActionMod.is_mod_enabled("cougar_personality_dummy_label"):
        if person.age > 45 and not person.is_unique:
            person.change_personality(cougar_personality)
            # mc.log_event((person.display_name) + "  A:" + str(person.age) + ": " + person.personality.personality_type_prefix, "float_text_grey")
    elif person.personality == cougar_personality and not person.is_unique:
        person.restore_original_personality()
        # mc.log_event((person.display_name) + " D:" + str(person.age) + ": " + person.personality.personality_type_prefix, "float_text_grey")


def update_alpha_personality(person: Person):
    # change personality to alpha if we meet requirements
    if ActionMod.is_mod_enabled("alpha_personality_dummy_label"):
        if (
            person.age > 25
            and person.charisma >= 5
            and person.int >= 4
            and person.opinion.taking_control > 0
            and not person.is_unique
        ) and person.personality != alpha_personality:
            person.change_personality(alpha_personality)
            # mc.log_event((person.display_name) + "  A:" + str(person.age) + ": " + person.personality.personality_type_prefix, "float_text_grey")
    elif person.personality == alpha_personality and not person.is_unique:
        person.restore_original_personality()
        # mc.log_event((person.display_name) + " D:" + str(person.age) + ": " + person.personality.personality_type_prefix, "float_text_grey")
