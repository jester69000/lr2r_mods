from __future__ import annotations
import renpy
from game.major_game_classes.game_logic.Action_ren import Action, Limited_Time_Action
from game.major_game_classes.game_logic.Role_ren import Role
from game.major_game_classes.character_related.Person_ren import Person, mc

day = 0
time_of_day = 0
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""
def init_pregnant_role():
    global pregnant_role
    pregnant_role = Role("Pregnant", [], hidden = True)

def pregnant_announce_requirement(person: Person, *args):
    return day >= person.event_triggers_dict.get("preg_announce_day", 0)

def pregnant_transform_requirement(person: Person):
    return day >= person.event_triggers_dict.get("preg_transform_day", 0)

def pregnant_tits_requirement(person: Person):
    return day >= person.event_triggers_dict.get("preg_tits_date", 0)

def preg_finish_announcement_requirement(person: Person):
    if day >= person.event_triggers_dict.get("preg_finish_announce_day", 0):
        return not person.is_sleeping
    return False

def abort_pregnancy(person: Person):
    if not person or not person.is_pregnant:
        return False

    person.remove_role(pregnant_role)
    if "pre_preg_body" in person.event_triggers_dict:
        person.body_type = person.event_triggers_dict.pop("pre_preg_body")
    person.tits = person.event_triggers_dict["pre_preg_tits"]
    for x in ("breeder_pregnant_announce", "pregnant_announce", "silent_pregnant_announce"):
        person.remove_on_room_enter_event(x)

    for x in ("pregnant_tits_start", "silent_pregnant_tits_start", "pregnant_finish_announce", "silent_pregnant_finish_announce", "pregnant_transform", "silent_pregnant_transform"):
        mc.business.remove_mandatory_crisis(x)
    return True

def become_pregnant(person: Person, mc_father = True, progress_days = 0, breeder_announce = False, no_announcement = False): # Called when a girl is knocked up. Establishes all of the necessary bits of info.
    # prevent issues when function is called for already pregnant person / clones are sterile
    if not person or person.is_pregnant or person.is_clone:
        return

    # she recently had a child, so block pregnancy for at least 21 days (allow all events to play out)
    if person.has_event_day("last_birth") and person.days_since_event("last_birth") < 21:
        return

    # special trigger that can be set to prevent character from getting pregnant during normal sex routines
    if person.event_triggers_dict.get("no_pregnancy", False):
        return

    # clear any party schedules
    if not person.is_unique:
        person.set_override_schedule(None, time_slots = [4])
    # historic start date of pregnancy
    start_day = day - progress_days

    person.event_triggers_dict["immaculate_conception"] = person.has_taboo("vaginal_sex")
    person.event_triggers_dict["preg_accident"] = person.on_birth_control # If a girl is on birth control the pregnancy is an accident.
    person.event_triggers_dict["preg_start_date"] = start_day
    person.event_triggers_dict["preg_announce_day"] = start_day + renpy.random.randint(7, 11)
    person.event_triggers_dict["preg_tits_date"] = start_day + 14 + renpy.random.randint(0, 5)
    person.event_triggers_dict["preg_transform_day"] = start_day + 30 + renpy.random.randint(0, 10)
    person.event_triggers_dict["preg_finish_announce_day"] = start_day + 90 + renpy.random.randint(0, 10)
    person.event_triggers_dict["pre_preg_tits"] = person.tits
    person.event_triggers_dict["preg_mc_father"] = mc_father
    person.event_triggers_dict["preg_wanted"] = person.baby_desire >= 40

    if day > person.event_triggers_dict.get("preg_start_date", 0) + 14:
        person.knows_pregnant = True
    elif no_announcement:
        pass
    elif breeder_announce:
        person.add_unique_on_room_enter_event(
            Limited_Time_Action(
                Action("Breeder Pregnancy Announcement", pregnant_announce_requirement, "breeder_pregnant_announce", priority = 30,
                       event_duration = (5 * 10) + (5 * 5)))
        )
    else:
        target_label = "pregnant_announce" if person.is_mc_father else "silent_pregnant_announce"
        if renpy.has_label(f"{person.func_name}_{target_label}"):
            target_label = f"{person.func_name}_{target_label}"

        person.add_unique_on_room_enter_event(
            Limited_Time_Action(
                Action("Pregnancy Announcement", pregnant_announce_requirement, target_label, priority = 30,
                       event_duration = (5 * 10) + (5 * 5), silent = not person.is_mc_father))
        ) #LTA is turns valid, not days (5 slots per day), yield 5 days after it becomes active

    if day > person.event_triggers_dict.get("preg_tits_date", 0):
        person.knows_pregnant = True
        person.increase_tit_size()
    else:
        target_label = "pregnant_tits_start" if person.is_mc_father else "silent_pregnant_tits_start"
        if renpy.has_label(f"{person.func_name}_{target_label}"):
            target_label = f"{person.func_name}_{target_label}"

        mc.business.add_mandatory_morning_crisis(
            Action("Pregnancy Tits Grow", pregnant_tits_requirement, target_label, args = person, requirement_args = person, silent = True)
        )

    if day > person.event_triggers_dict.get("preg_transform_day", 0):
        person.event_triggers_dict["pre_preg_body"] = person.body_type
        person.body_type = "standard_preg_body"
        person.increase_tit_size()
        person.lactation_sources += 1

        target_label = "pregnant_finish_announce" if person.is_mc_father else "silent_pregnant_finish_announce"
        if renpy.has_label(f"{person.func_name}_{target_label}"):
            target_label = f"{person.func_name}_{target_label}"

        mc.business.add_mandatory_crisis(
            Action("Pregnancy Finish Announcement", preg_finish_announcement_requirement, target_label, args = person, requirement_args = person)
        )
    else:
        target_label = "pregnant_transform" if person.is_mc_father else "silent_pregnant_transform"
        if renpy.has_label(f"{person.func_name}_{target_label}"):
            target_label = f"{person.func_name}_{target_label}"

        mc.business.add_mandatory_morning_crisis(
            Action("Pregnancy Transform", pregnant_transform_requirement, target_label, args = person, requirement_args = person, silent = True)
        ) #This event adds an announcement event the next time you enter the same room as the girl.

    person.add_role(pregnant_role)

    mc.listener_system.fire_event("girl_pregnant", the_person = person)

def pregnant_tits_announcement_requirement(person: Person):
    return not person.is_sleeping

def pregnant_tits_start_person(person: Person):
    person.knows_pregnant = True
    person.increase_tit_size()

    target_label = "pregnant_tits_announce"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    person.add_unique_on_talk_event(
        Limited_Time_Action(
            Action("Announce Pregnant Tits", pregnant_tits_announcement_requirement, target_label,
                args = day, event_duration = 5 * 5)
        )
    )

def silent_pregnant_tits_start_person(person: Person):
    person.knows_pregnant = True
    person.increase_tit_size()

    if not person.is_stranger:    # don't announce pregnancy for unknown girls
        target_label = "pregnant_tits_announce" if person.is_mc_father else "silent_pregnant_tits_announce"
        if renpy.has_label(f"{person.func_name}_{target_label}"):
            target_label = f"{person.func_name}_{target_label}"

        person.add_unique_on_talk_event(
            Limited_Time_Action(
                Action("Announce Pregnant Tits", pregnant_tits_announcement_requirement, target_label,
                    args = day, event_duration = 15))
        )

def preg_transform_announce_requirement(person: Person):
    return not person.is_sleeping

def pregnant_transform_person(person: Person):
    if "pre_preg_body" in person.event_triggers_dict:
        renpy.say("Warning", f"Something went wrong with pregnancy transform for {person.name}, she is already transformed.")
        return # already transformed

    person.event_triggers_dict["pre_preg_body"] = person.body_type
    person.body_type = "standard_preg_body"
    person.increase_tit_size()
    person.lactation_sources += 1

    target_label = "pregnant_transform_announce"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    person.add_unique_on_room_enter_event(
        Limited_Time_Action(
            Action("Pregnancy Transform Announcement", preg_transform_announce_requirement, target_label, priority = 30,
                args = day, event_duration = 5 * 5))
    )

    target_label = "pregnant_finish_announce"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    mc.business.add_mandatory_crisis(
        Action("Pregnancy Finish Announcement", preg_finish_announcement_requirement, "pregnant_finish_announce", args = person, requirement_args = person)
    )
    return

def silent_pregnant_transform_person(person: Person):
    if "pre_preg_body" in person.event_triggers_dict:
        renpy.say("Warning", f"Something went wrong with pregnancy transform for {person.name}, she is already transformed.")
        return # already transformed

    person.event_triggers_dict["pre_preg_body"] = person.body_type
    person.body_type = "standard_preg_body"
    person.increase_tit_size()
    person.lactation_sources += 1

    if not person.is_stranger:    # don't announce pregnancy for unknown girls
        target_label = "pregnant_transform_announce" if person.is_mc_father else "silent_pregnant_transform_announce"
        if renpy.has_label(f"{person.func_name}_{target_label}"):
            target_label = f"{person.func_name}_{target_label}"

        person.add_unique_on_room_enter_event(
            Limited_Time_Action(
                Action("Pregnancy Transform Announcement", preg_transform_announce_requirement, target_label, priority = 30,
                    args = day, event_duration = 15))
        )

    target_label = "pregnant_finish_announce" if person.is_mc_father else "silent_pregnant_finish_announce"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    mc.business.add_mandatory_crisis(
        Action("Pregnancy Finish Announcement", preg_finish_announcement_requirement, target_label, args = person, requirement_args = person)
    )

def preg_finish_requirement(person: Person, trigger_day):
    return day >= trigger_day and not person.is_sleeping

def pregnant_finish_announce_person(person: Person):
    person.available = False

    target_label = "pregnant_finish"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    mc.business.add_mandatory_morning_crisis(
        Action("Pregnancy Finish", preg_finish_requirement, target_label, args = person, requirement_args = [person, day + renpy.random.randint(4, 7)])
    )

def silent_pregnant_finish_announce_person(person: Person):
    person.available = False
    target_label = "pregnant_finish" if person.is_mc_father else "silent_pregnant_finish"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    mc.business.add_mandatory_morning_crisis(
        Action("Pregnancy Finish", preg_finish_requirement, target_label, args = person, requirement_args = [person, day + renpy.random.randint(4, 7)])
    )


def tit_shrink_requirement(person: Person, trigger_day):
    return day >= trigger_day

def pregnant_finish_person(person: Person):
    if "pre_preg_body" not in person.event_triggers_dict:
        renpy.say("Warning", f"Something went wrong with restoring the pregnancy of {person.name}")
        return False # she is not giving birth

    person.body_type = person.event_triggers_dict.pop("pre_preg_body")
    person.available = True
    person.change_location(person.home) # she goes back home (unlock from purgatory)

    person.kids += 1
    person.set_event_day("last_birth")  # record last day giving birth

    ###jes: Reduce tightness
    if person.vagina_tightness < 5:
        person.vagina_tightness = 5

    mc.business.add_mandatory_morning_crisis(
        Action("Tits Shrink One", tit_shrink_requirement, "tits_shrink", args = [person, True, add_tits_shrink_one_announcement], requirement_args = [person, day + renpy.random.randint(7, 10)], silent = True)
    ) #Events for her breasts to return to their normal size.

    mc.business.add_mandatory_morning_crisis(
        Action("Tits Shrink Two", tit_shrink_requirement, "tits_shrink", args = [person, False, add_tits_shrink_two_announcement], requirement_args = [person, day + renpy.random.randint(17, 20)], silent = True)
    )

    if person.is_mc_father:
        person.sex_record["Children with MC"] = person.sex_record.get("Children with MC", 0) + 1

    person.remove_role(pregnant_role)
    return True

def tit_shrink_announcement_requirement(person: Person):
    return not person.is_sleeping

def add_tits_shrink_one_announcement(person: Person):

    target_label = "tits_shrink_announcement_one"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    person.add_unique_on_talk_event(
        Limited_Time_Action(
            Action("Tits Shrink One Announcement", tit_shrink_announcement_requirement, target_label,
                event_duration = 15))
    )

def add_tits_shrink_two_announcement(person: Person):
    target_label = "tits_shrink_announcement_two"
    if renpy.has_label(f"{person.func_name}_{target_label}"):
        target_label = f"{person.func_name}_{target_label}"

    person.add_unique_on_talk_event(
        Limited_Time_Action(
            Action("Tits Shrink Two Announcement", tit_shrink_announcement_requirement, target_label,
                event_duration = 15))
    )
