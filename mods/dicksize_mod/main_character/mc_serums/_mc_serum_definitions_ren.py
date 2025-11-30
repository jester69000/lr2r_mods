from __future__ import annotations
import renpy
from game.helper_functions.list_functions_ren import find_serum_trait_by_name
from game.main_character.mc_serum_trait_ren import MC_Serum_Trait, list_of_mc_traits
from game.main_character.perks.Perks_ren import Ability_Perk, Stat_Perk, perk_system
from game.major_game_classes.character_related.Person_ren import Person, mc

day = 0
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init 2 python:
"""

def perk_feat_hypnotist_small():
    return Ability_Perk(description = "You gain the ability to hypnotize a woman into a trance. Costs 30 energy.",
                        usable = False)

def perk_feat_hypnotist_med():
    return Ability_Perk(description = "You get a 20% discount on trance training and gain the ability to hypnotize a woman into a deep trance. Costs 30 energy.",
                        usable = False)

def perk_feat_hypnotist_large():
    return Ability_Perk(description = "You get a 40% discount on trance training and gain the ability to hypnotize a woman into a very deep trance. Costs 30 energy.",
                        usable = False)

def perk_feat_hypnotist_advance_req_01():
    serum = find_serum_trait_by_name("Permanent Bimbofication")
    return serum and serum.mastery_level >= 5

def perk_serum_workaholic_on_apply():
    bonus = mc_serum_workaholic.trait_tier
    if mc.business.is_weekend:
        bonus *= 2
    perk_system.add_stat_perk(Stat_Perk(description = "Your workaholic serum has increased all your work related stats.",
            hr_bonus = bonus, market_bonus = bonus, research_bonus = bonus, production_bonus = bonus, supply_bonus = bonus, skill_cap = bonus,
            bonus_is_temp = True, duration = 2), "Workaholic Stats")

def perk_serum_workaholic_on_remove():
    perk_system.remove_perk("Workaholic Stats")

def perk_workaholic_small_update():
    return

def perk_workaholic_med_update():
    if mc.is_at_office:
        mc.change_energy(int(mc.max_energy * .1), add_to_log = False)

def perk_workaholic_large_update():
    if mc.is_at_office:
        mc.change_energy(int(mc.max_energy * .2), add_to_log = False)

def perk_workaholic_small():
    return Ability_Perk(description = "You have slightly increased work stats. Bonus doubles on the weekend.",
                        usable = False, update_func = perk_workaholic_small_update)

def perk_workaholic_med():
    return Ability_Perk(description = "You have moderately increased work stats and 10% gain energy while working. Bonus doubles on the weekend.",
                        usable = False, update_func = perk_workaholic_med_update)

def perk_workaholic_large():
    return Ability_Perk(description = "You have increased work stats and 20% energy while working. Bonus doubles on the weekend.",
                        usable = False, update_func = perk_workaholic_large_update)

def perk_workaholic_advance_req_01():
    serum = find_serum_trait_by_name("Quick Release Nootropics")
    return serum and serum.mastery_level >= 5

def perk_feat_orgasm_control_on_apply():
    mc.business.event_triggers_dict['orgasm_control_active'] = True

def perk_feat_orgasm_control_on_remove():
    mc.business.event_triggers_dict['orgasm_control_active'] = False

def perk_feat_orgasm_control_small():
    return Ability_Perk(description = "During sex, you can hold off orgasm indefinitely, but orgasms cost 20 energy.",
                        usable = False)

def perk_feat_orgasm_control_med():
    return Ability_Perk(description = "During sex, cum early or hold off indefinitely, but orgasms cost 20 energy.",
                        usable = False)

def perk_feat_orgasm_control_large():
    return Ability_Perk(description = "During sex, cum early or hold off indefinitely, and once per day you can quickly orgasm during a conversation before the other person can react. Orgasms cost 20 energy.",
                        usable = False)

def perk_feat_orgasm_control_advance_req_01():
    serum = find_serum_trait_by_name("Mind Control Agent")
    return serum and serum.mastery_level >= 5

def perk_energy_regen_small_update():
    mc.change_energy(int(mc.max_energy * .1), add_to_log = False)

def perk_energy_regen_med_update():
    mc.change_energy(int(mc.max_energy * .2), add_to_log = False)

def perk_energy_regen_large_update():
    mc.change_energy(int(mc.max_energy * .3), add_to_log = False)

def perk_energy_regen_small():
    return Ability_Perk(description = "You naturally regenerate 10% amount of energy throughout the day.",
                        usable = False, update_func = perk_energy_regen_small_update)

def perk_energy_regen_med():
    return Ability_Perk(description = "You naturally regenerate 20% amount of energy throughout the day. ",
                        usable = False, update_func = perk_energy_regen_med_update)

def perk_energy_regen_large():
    return Ability_Perk(description = "You naturally regenerate 30% amount of energy throughout the day. During sex, only lose erection when low on Energy.",
                        usable = False, update_func = perk_energy_regen_large_update)

def perk_energy_regen_advance_req_01():
    serum = find_serum_trait_by_name("Refined Stimulants")
    return serum and serum.mastery_level >= 5

def perk_libido_enhancer_small_update():
    mc.change_locked_clarity(5)

def perk_libido_enhancer_med_update():
    mc.change_locked_clarity(10)

def perk_libido_enhancer_large_update():
    mc.change_locked_clarity(15)

def perk_libido_enhancer_small():
    return Ability_Perk(description = "Your lust increases faster over time.",
                        usable = False, update_func = perk_libido_enhancer_small_update)

def perk_libido_enhancer_med():
    return Ability_Perk(description = "Your lust increases even faster over time, and sex actions cost slightly less energy.",
                        usable = False, update_func = perk_libido_enhancer_med_update)

def perk_libido_enhancer_large():
    return Ability_Perk(description = "You lust increases rapidly throughout the day, and sex actions cost significantly less energy.",
                        usable = False, update_func = perk_libido_enhancer_large_update)

def perk_libido_enhancer_advance_req_01():
    serum = find_serum_trait_by_name("Libido Stimulants")
    return serum and serum.mastery_level >= 5

def perk_libido_enhancer_energy_mult():
    if perk_system.has_ability_perk("Serum: Libido Enhancement") and mc_serum_libido_enhancer.trait_tier >= 2:
        return 0.7
    if perk_system.has_ability_perk("Serum: Libido Enhancement") and mc_serum_libido_enhancer.trait_tier >= 1:
        return 0.85
    return 1

##

def perk_cum_suggest_small_on_cum(person: Person, opinion: str, add_to_log = True):
    person.change_modded_suggestibility(1, max_amt = 10, add_to_log = add_to_log)

def perk_cum_suggest_med_on_cum(person: Person, opinion: str, add_to_log = True):
    person.change_modded_suggestibility(1, max_amt = 20, add_to_log = add_to_log)

def perk_cum_suggest_large_on_cum(person: Person, opinion: str, add_to_log = True):
    person.change_modded_suggestibility(1, max_amt = 30, add_to_log = add_to_log)

def perk_cum_suggest_small():
    return Ability_Perk(description = "When exposed to your cum, increases girls suggestibility by 1% to a maximum of 10%.",
                        usable = False, cum_func = perk_cum_suggest_small_on_cum)

def perk_cum_suggest_med():
    return Ability_Perk(description = "When exposed to your cum, increases girls suggestibility by 1% to a maximum of 20%.",
                        usable = False, cum_func = perk_cum_suggest_med_on_cum)

def perk_cum_suggest_large():
    return Ability_Perk(description = "When exposed to your cum, increases girls suggestibility by 1% to a maximum of 30%.",
                        usable = False, cum_func = perk_cum_suggest_large_on_cum)

def perk_cum_suggest_advance_req_01():
    serum = find_serum_trait_by_name("Mind Control Agent")
    return serum and serum.mastery_level >= 5

def perk_cum_obedience_small_on_cum(person: Person, opinion: str, add_to_log = True):
    person.change_obedience(1, 140, add_to_log = add_to_log)

def perk_cum_obedience_med_on_cum(person: Person, opinion: str, add_to_log = True):
    person.change_obedience(2, 180, add_to_log = add_to_log)
    person.increase_opinion_score(opinion, max_value = 0, add_to_log = add_to_log)

def perk_cum_obedience_large_on_cum(person: Person, opinion: str, add_to_log = True):
    person.change_obedience(2, 220, add_to_log = add_to_log)
    person.increase_opinion_score(opinion, max_value = 2, add_to_log = add_to_log)
    if not person.is_in_trance:
        person.increase_trance(show_dialogue = True, reset_arousal = False, add_to_log = add_to_log)

def perk_cum_obedience_small():
    return Ability_Perk(description = "When exposed to your cum, girls gain up to 1 obedience, to a maximum of 140.",
                        usable = False, cum_func = perk_cum_obedience_small_on_cum)

def perk_cum_obedience_med():
    return Ability_Perk(description = "When exposed to your cum, girls gain up to 1 obedience, to a maximum of 180 and if disliked, her opinion of the cumshot is shifted positively.",
                        usable = False, cum_func = perk_cum_obedience_med_on_cum)

def perk_cum_obedience_large():
    return Ability_Perk(description = "When exposed to your cum, girls gain up to 2 obedience, to a maximum of 220 and her opinion of the cumshot is shifted positively. If she isn't already in a trance, she is put in one.",
                        usable = False, cum_func = perk_cum_obedience_large_on_cum)

def perk_cum_obedience_advance_req_01():
    serum = find_serum_trait_by_name("Stress Inhibitors")
    return serum and serum.mastery_level >= 5

def perk_aura_obedience_small_update():
    for person in mc.nearby_people:
        if person.obedience < 150 and renpy.random.randint(0, 100) < 15:   # 15% chance
            person.change_obedience(1, 140, add_to_log = False)

def perk_aura_obedience_med_update():
    for person in mc.nearby_people:
        if person.obedience < 200 and renpy.random.randint(0, 100) < 20:    # 20% chance
            person.change_obedience(1, 180, add_to_log = False)

def perk_aura_obedience_large_update():
    for person in mc.nearby_people:
        if person.obedience < 220 and renpy.random.randint(0, 100) < 25:    # 20% chance
            person.change_obedience(1, 220, add_to_log = False)

def perk_aura_obedience_small():
    return Ability_Perk(description = "Girls near you slowly gain obedience up to 140 and never refuse small favours.",
                        usable = False, update_func = perk_aura_obedience_small_update)

def perk_aura_obedience_med():
    return Ability_Perk(description = "Girls near you slowly gain obedience up to 180 and never refuse small or medium favours, and have +10 obedience during sex.",
                        usable = False, update_func = perk_aura_obedience_med_update)

def perk_aura_obedience_large():
    return Ability_Perk(description = "Girls near you slowly gain obedience up to 220 and never refuse any favours, have +20 obedience during sex, and never refuse a sex position based on her opinions.",
                        usable = False, update_func = perk_aura_obedience_large_update)

def perk_aura_obedience_advance_req_01():
    serum = find_serum_trait_by_name("Obedience Enhancer")
    return serum and serum.mastery_level >= 5

def perk_aura_arousal_small_update():
    for person in mc.nearby_people:
        if person.arousal_perc < 25:
            person.change_arousal(1, add_to_log = False)

def perk_aura_arousal_med_update():
    for person in mc.nearby_people:
        if person.arousal_perc < 25:
            person.change_arousal(2, add_to_log = False)
        elif person.arousal_perc < 50:
            person.change_arousal(1, add_to_log = False)

def perk_aura_arousal_large_update():
    for person in mc.nearby_people:
        if person.arousal_perc < 30:
            person.change_arousal(1, add_to_log = False)
        elif person.arousal_perc < 50:
            person.change_arousal(1, add_to_log = False)
        elif person.arousal_perc < 70:
            person.change_arousal(1, add_to_log = False)

def perk_aura_arousal_small():
    return Ability_Perk(description = "Girls near you slowly gain up to 30% arousal.",
                        usable = False, update_func = perk_aura_arousal_small_update)

def perk_aura_arousal_med():
    return Ability_Perk(description = "Girls near you slowly gain up to 50% arousal, and never find vaginal and anal positions boring.",
                        usable = False, update_func = perk_aura_arousal_med_update)

def perk_aura_arousal_large():
    return Ability_Perk(description = "Girls near you slowly gain up to 70% arousal, and never find any sexual positions boring.",
                        usable = False, update_func = perk_aura_arousal_large_update)

def perk_aura_arousal_advance_req_01():
    serum = find_serum_trait_by_name("Pleasure Center Stimulator")
    return serum and serum.mastery_level >= 5

def perk_aura_fertility_small_update():
    for person in (x for x in mc.nearby_people if x.fertility_percent >= 0):
        if person.baby_desire < 40:
            person.change_baby_desire(1)
        if person.fertility_percent >= 0 and person.fertility_percent < 15.0:
            person.fertility_percent += 0.2

def perk_aura_fertility_med_update():
    for person in (x for x in mc.nearby_people if x.fertility_percent >= 0):
        if person.baby_desire < 60:
            person.change_baby_desire(1)
        if person.fertility_percent >= 0 and person.fertility_percent < 20.0:
            person.fertility_percent += 0.3

def perk_aura_fertility_large_update():
    for person in (x for x in mc.nearby_people if x.fertility_percent >= 0):
        if person.baby_desire < 80:
            person.change_baby_desire(1)
        if person.fertility_percent >= 0 and person.fertility_percent < 25.0:
            person.fertility_percent += 0.5

def perk_aura_fertility_small():
    return Ability_Perk(description = "Girls near you slowly gain fertility and desire to get pregnant increases.",
                        usable = False, update_func = perk_aura_fertility_small_update)

def perk_aura_fertility_med():
    return Ability_Perk(description = "Girls near you gain significant fertility and desire to get pregnant. Girls won't refuse vaginal sex based on sexual opinions.",
                        usable = False, update_func = perk_aura_fertility_med_update)

def perk_aura_fertility_large():
    return Ability_Perk(description = "Girls near you quickly gain unnatural fertility and are prone to baby fever. Girls won't refuse vaginal sex based on sexual opinions.",
                        usable = False, update_func = perk_aura_fertility_large_update)

def perk_aura_fertility_advance_req_01():
    serum = find_serum_trait_by_name("Pregnancy Acceleration Hormones")
    return serum and serum.mastery_level >= 5

###jes: Dick growth serum functions
def perk_feat_dick_growth_small():
    mc.change_dick_size(1, add_to_log = False)

def perk_feat_dick_growth_med():
    mc.change_dick_size(1, add_to_log = False)

def perk_feat_dick_growth_large():
    mc.change_dick_size(1, add_to_log = False)

def perk_feat_dick_growth_advance_req_01():
    serum = find_serum_trait_by_name("height_increase")
    return serum and serum.mastery_level >= 5


def init_mc_traits():
    global mc_serum_feat_hypnotist
    mc_serum_feat_hypnotist = MC_Serum_Trait("Serum: Feat of Hypnotism",
        "Medical Amphetamines",
        "physical",
        [perk_feat_hypnotist_small, perk_feat_hypnotist_med, perk_feat_hypnotist_large],
        [perk_feat_hypnotist_advance_req_01],
        "perk_feat_hypnotist_upg_label",
        upg_string = "Master the Permanent Bimbofication trait to upgrade this serum formula.")
    global mc_serum_workaholic
    mc_serum_workaholic = MC_Serum_Trait("Serum: Workaholic",
        "Clinical Testing Procedures",
        "energy",
        [perk_workaholic_small, perk_workaholic_med, perk_workaholic_large],
        [perk_workaholic_advance_req_01],
        "perk_workaholic_upg_label",
        upg_string = "Master the Quick Release Nootropics trait to upgrade this serum formula.",
        on_apply = perk_serum_workaholic_on_apply,
        on_remove = perk_serum_workaholic_on_remove)
    global mc_serum_feat_orgasm_control
    mc_serum_feat_orgasm_control = MC_Serum_Trait("Serum: Feat of Orgasm Control",
        "Pleasure Center Stimulator",
        "physical",
        [perk_feat_orgasm_control_small, perk_feat_orgasm_control_med, perk_feat_orgasm_control_large],
        [perk_feat_orgasm_control_advance_req_01],
        "perk_feat_orgasm_control_upg_label",
        upg_string = "Master the Mind Control Agent trait to upgrade this serum formula.",
        on_apply = perk_feat_orgasm_control_on_apply,
        on_remove = perk_feat_orgasm_control_on_remove)
    global mc_serum_energy_regen
    mc_serum_energy_regen = MC_Serum_Trait("Serum: Energy Regeneration",
        "Caffeine Infusion",
        "energy",
        [perk_energy_regen_small, perk_energy_regen_med, perk_energy_regen_large],
        [perk_energy_regen_advance_req_01],
        "perk_energy_regen_upg_label",
        upg_string = "Master the Refined Stimulants trait to upgrade this serum formula.")
    global mc_serum_libido_enhancer
    mc_serum_libido_enhancer = MC_Serum_Trait("Serum: Libido Enhancement",
        "Distilled Aphrodisiac",
        "energy",
        [perk_libido_enhancer_small, perk_libido_enhancer_med, perk_libido_enhancer_large],
        [perk_libido_enhancer_advance_req_01],
        "perk_libido_enhancer_upg_label",
        upg_string = "Master the Libido Stimulants trait to upgrade this serum formula.")
    global mc_serum_cum_suggest
    mc_serum_cum_suggest = MC_Serum_Trait("Serum: Cum of Change",
        "Off Label Pharmaceuticals",
        "cum",
        [perk_cum_suggest_small, perk_cum_suggest_med, perk_cum_suggest_large],
        [perk_cum_suggest_advance_req_01],
        "perk_cum_suggest_upg_label",
        upg_string = "Master the Mind Control Agent trait to upgrade this serum formula.")
    global mc_serum_cum_obedience
    mc_serum_cum_obedience = MC_Serum_Trait("Serum: Seed of Submission",
        "Obedience Enhancer",
        "cum",
        [perk_cum_obedience_small, perk_cum_obedience_med, perk_cum_obedience_large],
        [perk_cum_obedience_advance_req_01],
        "perk_cum_obedience_upg_label",
        upg_string = "Master the Stress Inhibitors trait to upgrade this serum formula.")
    global mc_serum_aura_obedience
    mc_serum_aura_obedience = MC_Serum_Trait("Serum: Aura of Compliance",
        "Low Concentration Sedatives",
        "aura",
        [perk_aura_obedience_small, perk_aura_obedience_med, perk_aura_obedience_large],
        [perk_aura_obedience_advance_req_01],
        "perk_aura_obedience_upg_label",
        upg_string = "Master the Obedience Enhancer trait to upgrade this serum formula.")
    global mc_serum_aura_arousal
    mc_serum_aura_arousal = MC_Serum_Trait("Serum: Aura of Arousal",
        "Distilled Aphrodisiac",
        "aura",
        [perk_aura_arousal_small, perk_aura_arousal_med, perk_aura_arousal_large],
        [perk_aura_arousal_advance_req_01],
        "perk_aura_arousal_upg_label",
        upg_string = "Master the Pleasure Centre Stimulator trait to upgrade this serum formula.")
    global mc_serum_aura_fertility
    mc_serum_aura_fertility = MC_Serum_Trait("Serum: Aura of Fertility",
        "Fertility Enhancement",
        "aura",
        [perk_aura_fertility_small, perk_aura_fertility_med, perk_aura_fertility_large],
        [perk_aura_fertility_advance_req_01],
        "perk_aura_fertility_upg_label",
        upg_string = "Master the Pregnancy Acceleration Hormones trait to upgrade this serum formula.")
    ###jes: Dick growth serum
    global mc_serum_feat_dick_growth
    mc_serum_feat_dick_growth = MC_Serum_Trait("Serum: Dick Growth",
        "Human Growth Rebooter",
        "anatomical",
        [perk_feat_dick_growth_small, perk_feat_dick_growth_med, perk_feat_dick_growth_large],
        [perk_feat_dick_growth_advance_req_01],
        "perk_feat_dick_growth_upg_label",
        upg_string = "Master the Human Growth Rebooter trait to upgrade this serum formula.")

    global list_of_mc_traits
    list_of_mc_traits = [
        mc_serum_feat_hypnotist,
        mc_serum_workaholic,
        mc_serum_feat_orgasm_control,
        mc_serum_energy_regen,
        mc_serum_libido_enhancer,
        mc_serum_cum_suggest,
        mc_serum_cum_obedience,
        mc_serum_aura_obedience,
        mc_serum_aura_arousal,
        mc_serum_aura_fertility,
        mc_serum_feat_dick_growth, ###jes: add dick growth
    ]
