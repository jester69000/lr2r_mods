# Overwrite label 
# check_position_willingness to integrate dick size check into girl willingness
# sex_description to integrate dick size effect
# also rename from labels of calls

init 5:
    # Override original labels
    define config.label_overrides = {
        "check_position_willingness": "check_position_willingness_withDickSize",
        "_call_should_ask_for_condom_check_position_willingness" : "_call_should_ask_for_condom_check_position_willingness_withDickSize",
        "sex_description": "sex_description_withDickSize",
        "_call_lactation_description": "_call_lactation_description_withDickSize",
        "_call_describe_girl_climax_2": "_call_describe_girl_climax_2_withDickSize",
        "_call_climax_check_sex_description": "_call_climax_check_sex_description_withDickSize",
        "_call_watcher_check": "_call_watcher_check_withDickSize",
        "_call_walk_in_watcher_check": "_call_walk_in_watcher_check_withDickSize",
        "_call_advance_time_gym_training":"_call_advance_time_gym_training_withDickSize",
        "_call_fuck_person_gym_training":"_call_fuck_person_gym_training_withDickSize"
        }

    #
    python:
        kegel_exercise_in_gym_action = ActionMod("Schedule Kegel Exercise Session {image=time_advance}", gym_requirement, "select_person_for_kegel_exercise",
        initialization = gym_initialization, menu_tooltip = "Book a kegel exercise session for a person to retighten their vagina.", category="Mall")


label check_position_willingness_withDickSize(the_person, the_position, ignore_taboo = False, skip_dialog = False, skip_condom_ask = False): #Returns if hte person is willing to do this position or not, and charges the appropriate happiness hit if they needed obedience to be willing.
    $ willing = 1

    $ the_taboo = the_position.associated_taboo
    if ignore_taboo:
        $ the_taboo = None

    if the_person == kaya:  # she never asks for a condom
        $ skip_condom_ask = True

    $ final_slut_requirement, final_slut_cap = the_position.calculate_position_requirements(the_person, ignore_taboo)
    $ hates_position = len([the_person.discover_opinion(x) for x in the_position.opinion_tags if the_person.opinion(x) == -2]) != 0

    if ignore_taboo:
        # ignore taboo, also ignores willingness (we got here in a special way)
        # so we also go into the position (no escape because she hates is)
        pass
    elif not hates_position and the_person.effective_sluttiness(the_taboo) >= final_slut_requirement:
        if not (skip_dialog or the_person.has_taboo(the_taboo)):
            $ the_person.call_dialogue("sex_accept", the_position)

    elif not hates_position and the_person.effective_sluttiness(the_taboo) + (the_person.obedience-100) >= final_slut_requirement:
        "[the_person.possessive_title!c] doesn't seem enthusiastic, but a little forceful encouragement would probably convince her."
        menu:
            "Order her":
                mc.name "[the_person.title], this is going to happen."
                python:
                    happiness_drop = the_person.effective_sluttiness(the_taboo) - final_slut_requirement #Our initial conditions mean this is a negative number
                    the_person.change_arousal(the_person.opinion.being_submissive*2)
                    the_person.discover_opinion("being submissive")
                    if not the_person.is_submissive:
                        the_person.change_happiness(int(happiness_drop / (3 + the_person.opinion.being_submissive)))

                if not the_person.has_taboo(the_taboo):
                    $ the_person.call_dialogue("sex_obedience_accept")

                $ report_log["used_obedience"] = True
                $ willing = 2
            "Try something else":
                mc.name "Let's try something else that you might be more comfortable with."
                $ willing = 0

    elif not hates_position and the_person.effective_sluttiness(the_taboo) > final_slut_requirement * .6:
        # She's not willing to do it, but gives you a soft reject.
        $ the_person.call_dialogue("sex_gentle_reject")
        $ willing = 0

    elif hates_position and the_person.effective_sluttiness(the_taboo) > final_slut_requirement * .6:
        #She hates the position but isn't so mad she ends sex outright.
        $ willing = -2

    else:
        # You're nowhere close to the required sluttiness or hates position, lose some love for even trying and end interaction
        python:
            ran_num = the_person.effective_sluttiness(the_taboo) - final_slut_requirement
            ran_num = builtins.abs(builtins.int(ran_num/5.0))
            the_person.change_love(-ran_num)
            willing = -1

        $ the_person.call_dialogue("sex_angry_reject")

    ###jes:Check if difference between dick size and vagina thigtness allows this position
    if the_position.skill_tag == "Vaginal":
        python:
            acceptable_size_difference = the_position.calc_acceptable_size_difference(the_person)
            size_difference = mc.dick_size - the_person.vagina_tightness
        if size_difference <= acceptable_size_difference: # She is willing to try
            $ willing = 1
            if size_difference >= 4:
                the_person "That's going to rearrange my guts."
            elif size_difference >= 2:
                the_person "That's going to be a tight fit. Be careful."
        else: # It won't fit
            the_person "No way that thing is going to fit into my pussy."
            "Increase her vaginal skill and/or improve her opinion on big dicks"
            $ willing = -1

    if willing == 1 and not skip_condom_ask:
        call should_ask_for_condom(the_person, the_position) from _call_should_ask_for_condom_check_position_willingness_withDickSize

    if willing == 1 and (the_position.skill_tag == "Vaginal" or the_position.skill_tag == "Anal" or the_position.name == "Dildo Fuck") and not the_person.vagina_visible:
        # make sure we move skirts out of the way when rendering
        python:
            for the_clothing in (x for x in the_person.outfit.get_lower_ordered() if not (x.underwear or x.half_off)):
                renpy.say(None, f"You move her {the_clothing.display_name} out of the way.")
                the_person.outfit.half_off_clothing(the_clothing)
                the_person.draw_person()

    return willing


label sex_description_withDickSize(the_person, the_position, the_object, private = True, report_log = None):
    # Processes a single normal "round" of sex. Removes energy, increases arousal, calls for dialogue from people nearby, etc. then returns to the main loop.

    # Draw the person and deliver the position specific description
    $ the_position.redraw_scene(the_person)
    $ the_position.call_scene(the_person, mc.location, the_object)

    # parse the positions scene to a new position/object
    $ forcedNewPosition, forcedNewObject = the_position.parseReturnToNewPostionAndObject(_return)

    $ mc.listener_system.fire_event("sex_event", the_person = the_person, the_position = the_position, the_object = the_object)

    if report_log is not None:
        $ report_log["total rounds"] = report_log.get("total rounds", 0) + 1
    if report_log:
        $ report_log["positions_used"].append(the_position)

    # this is the point where you definitely find out if she likes vaginal or anal
    if the_position.skill_tag == "Vaginal":
        $ the_person.discover_opinion("vaginal sex")
    if the_position.skill_tag == "Anal":
        $ the_person.discover_opinion("anal sex")

    # If we have a new position, transition to new position and skip arousal, climax and watcher
    if forcedNewPosition is not None:
        return (forcedNewPosition, forcedNewObject)

    # Change the arousal for both people:
    # Her arousal first
    $ her_arousal_change = the_position.girl_arousal * (1.0 + 0.1 * mc.sex_skills[the_position.skill_tag]) # Each level the other party has in the sex class adds 10% arousal.
    if the_position.skill_tag == "Vaginal":
        $ the_person.discover_opinion("bareback sex")
        if mc.condom:
            $ her_arousal_change += -1 # Condoms don't feel as good (but matter less for her)
            $ her_arousal_change += -2 * the_person.opinion.bareback_sex
        else:
            $ her_arousal_change += 2 * the_person.opinion.bareback_sex

        ###jes:Bonus if she has a positive opinion on big dicks        
        if the_person.opinion.big_dicks > 0:
            python:
                size_difference = mc.dick_size - the_person.vagina_tightness
            $ her_arousal_change += floor(size_difference/2) * the_person.opinion.big_dicks            

    $ opinion_score = the_position.get_opinion_score(the_person)
    $ her_arousal_change += opinion_score

    if the_person.effective_sluttiness() > the_position.slut_cap: #She's sluttier than this position, it's only good to warm her up.
        if opinion_score < 1 and the_person.arousal_perc > the_position.slut_cap: #Once her arousal is higher than the cap she's completely bored by it.
            $ mc.log_event(f"{the_person.display_name} is bored", "float_text_red")
            $ her_arousal_change = her_arousal_change / 2

    $ clothing_count = 0
    $ interfering_clothing = []
    if the_position.skill_tag == "Vaginal" or the_position.skill_tag == "Anal":
        python:
            for clothing in the_person.outfit.get_lower_ordered():
                if clothing.anchor_below and clothing.half_off_gives_access and clothing.half_off:
                    clothing_count += 1 #Each piece of clothing that's only half off lowers the amount of arousal gain for both parties
                    interfering_clothing.append(clothing)

    elif the_position.requires_large_tits:
        python:
            for clothing in the_person.outfit.get_upper_ordered():
                if clothing.anchor_below and clothing.half_off_gives_access and clothing.half_off:
                    clothing_count += 1 #Each piece of clothing that's only half off lowers the amount of arousal gain for both parties
                    interfering_clothing.append(clothing)

    if clothing_count > 0:
        $ clothing_string = format_list_of_clothing(interfering_clothing)
        $ obstruction_phrase = "get in the way" if " and " in clothing_string else "gets in the way"
        "[the_person.title]'s half–off [clothing_string] [obstruction_phrase], lowering your enjoyment somewhat."
    $ del interfering_clothing

    $ her_arousal_change += -clothing_count
    $ the_person.change_arousal(her_arousal_change)

    # Now his arousal change
    $ his_arousal_change = the_position.guy_arousal * (1.0 + 0.1 * the_person.sex_skills[the_position.skill_tag])
    $ his_arousal_change += -clothing_count
    if the_position.skill_tag in ("Vaginal", "Anal") and mc.condom:
        $ his_arousal_change -= 2 # Condoms don't feel as good.

    ###jes:Bonus/malus for vagina tightness relative to dick size
    if the_position.skill_tag == "Vaginal":
        $ size_difference = the_person.vagina_tightness - mc.dick_size 
        if size_difference < 2: # Bonus for tight fit
            if the_person.vagina_tightness <= 0: # Catch virgin case ? 
                $ his_arousal_change += 5
            else:
                $ his_arousal_change += floor(mc.dick_size/the_person.vagina_tightness)
                "Her vagina fits like a glove around your dick.."
        elif size_difference >= 4: # Penalty for not much feeling            
            "Her stretched out pussy doesn't offer much stimulation."
            $ his_arousal_change -= 2        
        

    $ mc.change_arousal(his_arousal_change)
    # $ amount = (the_person.sex_skills[the_position.skill_tag] + mc.sex_skills[the_position.skill_tag]) // 2    OLD lust increase.
    # lust gain based on sluttiness of the position and how naked she is
    # $ amount = (the_position.slut_cap + the_person.outfit.outfit_lust_score) // 4
    # if amount + mc.locked_clarity > 1000: # locked clarity maxes out at 1000
    #     $ amount = 1000 - mc.locked_clarity
    # $ mc.locked_clarity += amount
    # Fuck it, just call the locked clarity function. Will cause MC's arousal to rise faster maybe
    $ mc.change_locked_clarity(the_position.slut_cap // 4, person = the_person)
    if mc.recently_orgasmed and mc.arousal_perc >= 10:
        $ mc.recently_orgasmed = False
        "Your cock stiffens again, coaxed back to life by [the_person.title]."

    # Change their energy as well.
    python:
        the_person.change_energy(-the_position.calculate_energy_cost(the_person), add_to_log = False)
        mc.change_energy(-the_position.calculate_energy_cost(mc), add_to_log = False)

    # $ the_person.change_energy(-the_position.girl_energy, add_to_log = False) #NOTE: Don't show the energy cost to avoid energy notice spam. The energy cost is already displayed to the player.
    # $ mc.change_energy(-the_position.guy_energy, add_to_log = False)

    if the_person.lactation_sources > 0:
        call lactation_description(the_person, the_position, the_object, report_log) from _call_lactation_description_withDickSize

    # If someone orgasms describe that.
    if the_person.arousal_perc >= 100:
        call describe_girl_climax(the_person, the_position, the_object, private, report_log) from _call_describe_girl_climax_2_withDickSize

    if mc.arousal_perc >= 80: #NOTE: use to be mc.max_arousal, this number is now the threshold for being forced to cum.
        call climax_check() from _call_climax_check_sex_description_withDickSize
        $ is_cumming = _return

        if is_cumming:
            $ the_position.call_outro(the_person, mc.location, the_object)
            # parse the scene outro to a new position / object
            $ forcedNewPosition, forcedNewObject = the_position.parseReturnToNewPostionAndObject(_return)

            if the_person.effective_sluttiness(the_position.associated_taboo) < the_position.slut_requirement: # bonus obedience if she if she had to be ordered to do this position ("I guess I really am just doing this for him...")
                $ the_person.change_obedience(3 + the_person.opinion.being_submissive, 160)
            else:
                $ the_person.change_obedience(3, 160)

            $ mc.recently_orgasmed = True
            $ report_log["guy orgasms"] = report_log.get("guy orgasms", 0) + 1

    if not mc.recently_orgasmed:
        if not private:
            call watcher_check(the_person, the_position, the_object, report_log) from _call_watcher_check_withDickSize
        else:
            call walk_in_watcher_check(the_person, the_position, the_object, report_log) from _call_walk_in_watcher_check_withDickSize

    ###jes:Check if size difference is big enough to stretch vagina
    ### 5% chance per point in size difference
    if the_position.skill_tag == "Vaginal":
        python:
            size_difference = the_person.vagina_tightness - mc.dick_size 
            chance_tightness_change = int(min(5*max(size_difference, 0), 100))
        $ pussy_changed = the_person.change_tightness(1, chance_tightness_change)

    return (forcedNewPosition, forcedNewObject)       # pass back new object


#jes: kegel exercise to offer an alternative way to retighten
# copied from
label select_person_for_kegel_exercise():
    call screen main_choice_display(build_menu_items(
        [get_sorted_people_list(known_people_in_the_game(), "Book Kegel exercise session", "Back")]
        ))
    if isinstance(_return, Person):
        $ the_person = _return
        "You send a text message to [the_person.title] about a Kegel exercise session."
        "After some time you get a response..."

    # Limit the change that can be achieved by exercises to 3
    if the_person.vagina_tightness <=3:
        $ the_person.draw_person(emotion = "sad")
        the_person "Why do you think I would be in need of such exercise."
        $ the_person.change_obedience(-2)
        $ the_person.change_happiness(-5)
        $ clear_scene()
        return

    if the_person.happiness < 100 or the_person.obedience < 80:
        $ the_person.draw_person(emotion = "sad")
        the_person "I'm not in the mood for a kegel session, right now."
        $ the_person.change_obedience(-2)
        $ clear_scene()
        return

    if the_person.personality == bimbo_personality:
        the_person "Cumming right away, [the_person.mc_title]!"
    elif the_person.obedience > 140:
        the_person "Yes, Sir. I am on my way."
    elif the_person.sluttiness > 30:
        the_person "Yes, [the_person.mc_title]. I am on my way."
    elif the_person.happiness < 120 and the_person.love > 20:
        $ the_person.draw_person(emotion = "happy")
        the_person "Thanks for the attention, [the_person.mc_title]."
        $ the_person.change_happiness(+10)
    else:
        the_person "Sounds good, I'll be right there, [the_person.mc_title]."
        $ the_person.change_happiness(+10)

    # 
    python:        
        chance_tightness_change = int(min(33*max(the_person.vagina_tightness-3, 0), 100))     
    $ pussy_changed = the_person.change_tightness(-1, chance_tightness_change)
    
    if pussy_changed:
        the_person "I can already feel the improvement."
        if the_person.sluttiness > 40 or (the_person.sluttiness > 40 and the_person.love > 50):
            the_person "Let me give you a demonstration."
            menu:
                "Have Sex":
                    mc.name "Let's go to the shower room."
                    the_person "Lead the way, [the_person.mc_title]."
                    $ mc.change_location(gym_shower)

                    "As soon as you get into the showers, [the_person.possessive_title] moves closer and starts kissing you."
                    # intro breaks kissing taboo for the_person
                    $ the_person.break_taboo("kissing")
                    $ old_outfit = the_person.outfit.get_copy() # make a copy we can restore

                    call fuck_person(the_person, start_position = kissing, start_object = mc.location.get_object_with_name("floor"), skip_intro = True, girl_in_charge =True) from _call_fuck_person_gym_training_withDickSize
                    $ the_report = _return
                    if the_report.get("girl orgasms", 0) > 0:
                        "[the_person.possessive_title!c] takes a few minutes to catch her breath, while looking at you getting dressed."
                    $ the_person.apply_outfit(old_outfit) # she puts on her gym clothes
                    $ the_person.draw_person(emotion = "happy")
                    $ del old_outfit

                "Another Time":
                    mc.name "Sorry [the_person.title], another time."
                    $ the_person.change_happiness(-5)
    else:
        the_person "I should do this more often."
    
    # End of responses
    $ the_person.draw_person(position="walking_away")

    $ mc.business.change_funds(-gym_session_cost)
    "You pay for the Kegel exercise; $[gym_session_cost] has been deducted from the company's credit card."

    $ mc.change_location(gym)

    call advance_time() from _call_advance_time_gym_training_withDickSize
    
    return # Go back to main menu