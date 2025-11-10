from __future__ import annotations
import builtins
import renpy
from game.bugfix_additions.mapped_list_ren import generate_identifier
from game.helper_functions.list_functions_ren import get_random_from_list
from game.main_character.MainCharacter_ren import MainCharacter
from game.main_character.mc_serums._mc_serum_definitions_ren import mc_serum_aura_arousal
from game.main_character.mc_serum_trait_ren import perk_system
from game.major_game_classes.game_logic.Room_ren import Room, RoomObject
from game.major_game_classes.character_related.Person_ren import Person, Clothing, mc
from game.main_character.mc_serums._mc_serum_definitions_ren import perk_libido_enhancer_energy_mult
from game.sex_positions._position_definitions_ren import spanking

list_of_positions: list[Position]
list_of_girl_positions: list[Position]
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -5 python:
"""
class Position():
    @classmethod
    def parseReturnToNewPostionAndObject(cls, value: any):
        position = None
        roomobject = None
        if isinstance(value, tuple) and len(value) == 2:
            if isinstance(value[0], Position):
                position = value[0]
            if isinstance(value[1], RoomObject):
                roomobject = value[1]
        return position, roomobject

    def __init__(self, name: str, slut_requirement: int, slut_cap: int, requires_hard: bool, requires_large_tits: bool,
            position_tag: str, requires_location: str, requires_clothing: str, skill_tag: str,
            girl_arousal: int, girl_energy: int, guy_arousal: int, guy_energy: int, connections: list[Position],
            intro, scenes, outro, transition_default,
            strip_description, strip_ask_description,
            orgasm_description,
            taboo_break_description,
            verb = "fuck", verbing = None, opinion_tags = [], record_class = None,
            gic_tags = [],
            associated_taboo = None,
            girl_outro = None,
            double_orgasm = None):

        self.name = name
        self.slut_requirement = slut_requirement #The required slut score of the girl. Obedience will help fill the gap if possible, at a happiness penalty. Value from 0 (almost always possible) to ~100
        self.slut_cap = slut_cap #The maximum sluttiness that this position will have an effect on.
        self.requires_hard = requires_hard
        self.requires_large_tits = requires_large_tits        

        self.girl_arousal = girl_arousal # The base arousal the girl receives from this position.
        self.girl_energy = girl_energy # The amount of energy the girl spends on this position.

        self.guy_arousal = guy_arousal # The base arousal the guy receives from this position.
        self.guy_energy = guy_energy # The base energy the guy spends on this position.

        self.position_tag = position_tag # The tag used to get the correct position image set.
        self.requires_location = requires_location # A tag that must match an object to have sex on it (eg. "lean", which needs something like a wall to lean against)
        self.requires_clothing = requires_clothing # A tag that notes what (lack of) clothing requirements the position has. Vaginal requires access to her vagina, tits her tits.
        self.skill_tag = skill_tag #The skill that will provide a bonus to this position.
        self.opinion_tags = opinion_tags #The opinion that will be checked each round.
        self.gic_tags = gic_tags # tags for girl in charge
        self.connections: list[Position] = connections
        self.intro = intro
        self.taboo_break_description = taboo_break_description #Called instead of the intro/transition when you break a taboo with someone. Should include call to personality taboo specific dialogue.
        self.scenes = scenes
        self.outro = outro
        self.transition_default = transition_default
        self.transitions: list[tuple[Position, str]] = []
        self.strip_description = strip_description
        self.strip_ask_description = strip_ask_description
        self.orgasm_description = orgasm_description
        self.verb = verb #A verb used to describe the position. "Fuck" is default, and mostly used for sex positions or blowjobs etc. Kiss, Fool around, etc. are also possibilities.
        if verbing is None: #The verb used as "Go back to [verbing] her.". Added specifically to support things like grope/groping, which have different spellings depending.
            self.verbing = verb + "ing"
        else:
            self.verbing = verbing
        self.record_class = record_class #A key to Person.sex_record[] that is updated once (and only once!) per sexual encounter if this position is picked.

        self.current_modifier = None #We will update this if the position has a special modifier that should be applied, like blowjob.
        self.associated_taboo = associated_taboo #What taboo tag, if any, is associated with this position. Until broken a taboo makes a position harder to select, but the taboo is broken once it is done once.

        self.girl_outro = girl_outro # possible override for GIC
        self.double_orgasm = double_orgasm  # special scene when both MC and Girl come simultaneously
        self.last_scene = None # store last run scene, to prevent running same scene twice
        self.identifier = generate_identifier(name)

        # Current sex-related taboo are:
        # kissing, touching_body, touching_penis, touching_vagina, sucking_cock, licking_pussy, vaginal_sex, anal_sex
        # And as a special case for vaginal sex: condomless_sex

    def __hash__(self) -> int:
        return self.identifier

    def __eq__(self, other: Position) -> bool:
        if not isinstance(other, Position):
            return NotImplemented
        return self.name == other.name

    def link_positions(self, other: Position, transition_label: str) -> None: #This is a one way link!
        self.connections.append(other)
        self.transitions.append((other, transition_label))

    def link_positions_two_way(self, other: Position, transition_from_this_label: str, transition_from_other_label: str) -> None: #Link it both ways. Great for adding a modded position without modifying other positions.
        self.link_positions(other, transition_from_this_label)
        other.link_positions(self, transition_from_other_label)

    def call_intro(self, person: Person, location: Room, the_object: RoomObject):
        renpy.call(self.intro, person, location, the_object)

    def call_taboo_break(self, person: Person, location: Room, the_object: RoomObject):
        self._discover_opinions(person)
        renpy.call(self.taboo_break_description, person, location, the_object)

    def call_scene(self, person: Person, location: Room, the_object: RoomObject):
        choice_list = [x for x in self.scenes if not x == self.last_scene]
        new_scene = get_random_from_list(choice_list) if choice_list else get_random_from_list(self.scenes)
        self.last_scene = new_scene
        renpy.call(new_scene, person, location, the_object)

    def call_outro(self, person: Person, location: Room, the_object: RoomObject):
        if self.girl_outro:  #Rely on girl outro tocall default outro if appropriate
            renpy.call(self.girl_outro, person, location, the_object)
        else:
            self.call_default_outro(person, location, the_object)

    def call_default_outro(self, person: Person, location: Room, the_object: RoomObject):
        #print("Call default outro: {} {} {} {}".format(self.name, person.name, location.name, the_object.name))
        renpy.call(self.outro, person, location, the_object)

    def call_transition(self, new_position: Position | None, person: Person, location: Room, room_object: RoomObject) -> None:
        def get_position_name(position):
            return position.name.lower().replace(" ", "_")

        if new_position is not None:
            # we are not switching at all -> quick exit
            if get_position_name(self) == get_position_name(new_position):
                return

            transition_scene = f"transition_{get_position_name(self)}_{get_position_name(new_position)}"
            #renpy.say(None, "Custom transition function is: " + transition_scene)
            if renpy.has_label(transition_scene):
                #renpy.say(None, "Calling custom transition function: " + transition_scene)
                renpy.call(transition_scene, person, location, room_object)

            transition_scene = new_position.transition_default
            for position_tuple in self.transitions:
                if position_tuple[0] == new_position: ##Does the position match the one we are looking for?
                    transition_scene = position_tuple[1] ##If so, set it's label as the one we are going to change to.

            #renpy.say(None, "Default transition scene is: " + transition_scene)
            if renpy.has_label(transition_scene):
                #renpy.say(None, "Calling default transition scene: " + transition_scene)
                renpy.call(transition_scene, person, location, room_object)

        else: # we are calling from the new position (we don't have an old position to start from)
            transition_scene = self.transition_default
            if renpy.has_label(transition_scene):
                #renpy.say(None, "Calling default transition: " + transition_scene)
                renpy.call(transition_scene, person, location, room_object)

    # try different types of taboo break, the final choice is the break for the actual position broken
    # added an extra check to make sure the label exists, if not the taboo is broken without dialog
    def call_transition_taboo_break(self, new_position: Position | None, person: Person, location: Room, the_object: RoomObject) -> None:
        def get_position_name(position):
            return position.name.lower().replace(" ", "_")

        self._discover_opinions(person)

        if new_position is not None:
            transition_scene = f"transition_{get_position_name(self)}_to_{get_position_name(new_position)}_taboo_break_label"
            #renpy.say(None, "Custom taboo break function is: " + transition_scene)
            if renpy.has_label(transition_scene):
                #renpy.say(None, "Calling custom taboo break: " + transition_scene)
                renpy.call(transition_scene, person, location, the_object)

            #renpy.say(None, "Default taboo break function: " + new_position.taboo_break_description)
            if renpy.has_label(new_position.taboo_break_description):
                #renpy.say(None, "Calling default taboo break: " + new_position.taboo_break_description)
                renpy.call(new_position.taboo_break_description, person, location, the_object)

            transition_scene = new_position.transition_default
            for position_tuple in self.transitions:
                if position_tuple[0] == new_position: ##Does the position match the one we are looking for?
                    transition_scene = position_tuple[1] ##If so, set it's label as the one we are going to change to.

            #renpy.say(None, "Default transition scene is: " + transition_scene)
            if renpy.has_label(transition_scene):
                #renpy.say(None, "Calling default transition scene: " + transition_scene)
                renpy.call(transition_scene, person, location, the_object)

        else: # we are calling from the new position (we don't have an old position to start from)
            #renpy.say(None, "Default taboo break function: " + self.taboo_break_description)
            if renpy.has_label(self.taboo_break_description):
                #renpy.say(None, "Calling default taboo break: " + self.taboo_break_description)
                renpy.call(self.taboo_break_description, person, location, the_object)

            transition_scene = self.transition_default
            if renpy.has_label(transition_scene):
                #renpy.say(None, "Calling default transition: " + transition_scene)
                renpy.call(transition_scene, person, location, the_object)

    def call_strip(self, person: Person, clothing: Clothing, location: Room, the_object: RoomObject):
        renpy.call(self.strip_description, person, clothing, location, the_object)

    def call_strip_ask(self, person: Person, clothing: Clothing, location: Room, the_object: RoomObject):
        renpy.call(self.strip_ask_description, person, clothing, location, the_object)

    def call_orgasm(self, person: Person, location: Room, the_object: RoomObject):
        #print("Call double orgasm: {} {} {} {}".format(self.name, person.name, location.name, the_object.name))
        renpy.call("double_orgasm_label", self, person, location, the_object)

    def check_clothing(self, person: Person) -> bool:
        if self.requires_clothing == "Vagina":
            return person.vagina_available
        if self.requires_clothing == "Tits":
            return person.tits_available
        return True ##If you don't have one of the requirements listed above just let it happen.

    def calculate_position_requirements(self, person: Person, ignore_taboo = False, only_known_opinions = False) -> tuple[int, int]:
        '''
        Return (final_slut_requirement, final_slut_cap)
        '''
        position_taboo = self.associated_taboo
        if ignore_taboo:
            position_taboo = None

        final_slut_requirement = self.slut_requirement
        final_slut_cap = self.slut_cap
        if self.skill_tag == "Anal" and person.has_family_taboo:
            final_slut_requirement -= 5 #It's easier to convince a family member to have anal sex, since it's not "real" incest or something.
            final_slut_cap -= 5
        elif self.skill_tag == "Vaginal" and person.has_family_taboo:
            final_slut_requirement += 10 #It's harder to convince a family member to have vaginal sex
            final_slut_cap += 10

        if only_known_opinions:
            modifier = person.known_opinion(self.opinion_tags) * 5
            final_slut_cap -= modifier
            final_slut_requirement -= modifier
        else:
            modifier = person.opinion(self.opinion_tags) * 5
            final_slut_cap -= modifier
            final_slut_requirement -= modifier

        if person.has_taboo(position_taboo):
            final_slut_requirement += 10    # when she has a taboo increase slut requirement
            final_slut_cap += 10

        return final_slut_requirement, final_slut_cap

    def redraw_scene(self, person: Person, emotion: str | None = None): #redraws the scene, call this when something is modified.
        person.draw_person(self.position_tag, emotion = emotion, special_modifier = self.current_modifier)

    def her_position_willingness_check(self, person: Person, ignore_taboo = False): #Checks if the given girl would/can pick this position. A mirror of the main character's options.
        possible = True

        position_taboo = self.associated_taboo
        if ignore_taboo:
            position_taboo = None

        final_slut_requirement = self.slut_requirement
        final_slut_cap = self.slut_cap
        if self.skill_tag == "Anal" and person.has_family_taboo:
            final_slut_requirement += -10 #It's easier to convince a family member to have anal sex, since it's not "real" incest or something.
            final_slut_cap += -10
        elif self.skill_tag == "Vaginal" and person.has_family_taboo:
            final_slut_requirement += 10 #It's harder to convince a family member to have vaginal sex
            final_slut_cap += 10

        if final_slut_requirement > person.effective_sluttiness(position_taboo):
            possible = False # Too slutty for her.
        elif not self.check_clothing(person):
            possible = False # Clothing is in the way.
        elif mc.energy < self.guy_energy or person.energy < self.girl_energy:
            possible = False # One of them is too tired.
        elif self.requires_hard and mc.recently_orgasmed:
            possible = False # The mc has cum recently and isn't hard.
        elif self.requires_large_tits and not person.has_large_tits:
            possible = False # You need large tits for this and she doesn't have it.

        return possible
    
    ###jes:Added function to calculate acceptable dick size
    def calc_acceptable_size_difference(self, person: Person) -> int:
        # Calculate acceptable size difference
        acceptable_size_difference = 2
        if person.opinion.big_dicks > 0: # Positive opinion on big dicks, bonus based on vaginal skill  
            acceptable_size_difference += floor(person.vaginal_sex_skill/(4-person.opinion.big_dicks))
        elif person.opinion.big_dicks < 0: # Negative opinion on big dicks, works as penalty
            acceptable_size_difference += person.opinion.big_dicks

        return acceptable_size_difference


    def build_position_willingness_string(self, person: Person, ignore_taboo = False) -> str: #Generates a string for this position that includes a tooltip and coloured willingness for the person given.
        #Generates a list of strings for this position that includes a tooltip and coloured willingness for the person given.

        willingness_string = ""
        tooltip_string = ""

        (guy_energy_percent, girl_energy_percent) = self._estimate_energy_values(person)
        (guy_arousal_percent, girl_arousal_percent) = self._estimate_arousal_values(person)

        energy_string = f"   {{color=#A3A3FF}}{guy_energy_percent:.0f}%{{/color}}/{{color=#FF6EC7}}{girl_energy_percent:.0f}%{{/color}} {{image=energy_token_small}}"
        arousal_string = f", {{color=#A3A3FF}}{guy_arousal_percent:.0f}%{{/color}}/{{color=#FF6EC7}}{girl_arousal_percent:.0f}%{{/color}} {{image=arousal_token_small}}"

        disable = False
        position_taboo = self.associated_taboo

        if ignore_taboo:
            position_taboo = None

        final_slut_requirement, final_slut_cap = self.calculate_position_requirements(person, ignore_taboo, only_known_opinions = True)

        taboo_break_string = ""
        if person.has_taboo(position_taboo):
            taboo_break_string = " {image=taboo_break} "

        opinion_score = self.get_opinion_score(person)

        if person.effective_sluttiness(position_taboo) > final_slut_cap:
            if opinion_score < 1 and person.arousal > final_slut_cap:
                willingness_string = "{color=#6b6b6b}Boring{/color}" #No sluttiness gain AND half arousal gain
                tooltip_string = " (tooltip) This position is too boring to interest her when she is this horny. No sluttiness increase and her arousal gain is halved."
            else:
                willingness_string = "{color=#A3A3FF}Comfortable{/color}" #No sluttiness
                tooltip_string = " (tooltip) This position is too tame for her tastes. No sluttiness increase, but it may still be a good way to get warmed up and ready for other positions."
        elif person.effective_sluttiness(position_taboo) >= final_slut_requirement:
            willingness_string = "{color=#3DFF3D}Exciting{/color}" #Normal sluttiness gain
            tooltip_string = " (tooltip) This position pushes the boundary of what she is comfortable with. Increases temporary sluttiness, which may become permanent over time or with serum application."
        elif person.effective_sluttiness(position_taboo) + person.obedience - 100 >= final_slut_requirement:
            willingness_string = "{color=#FFFF3D}Likely Willing if Commanded{/color}"
            tooltip_string = " (tooltip) This position is beyond what she would normally consider. She is obedient enough to do it if she is commanded, at the cost of some happiness."
        else:
            willingness_string = "{color=#FF3D3D}Likely Too Slutty{/color}"
            tooltip_string = " (tooltip) This position is so far beyond what she considers appropriate that she would never dream of it."

        if person.has_taboo(position_taboo):
            tooltip_string += f"\nSuccessfully selecting this position will break a taboo, making it easier to convince {'her' if person.is_stranger else person.display_name} to do it and similar acts in the future."

        if not self.check_clothing(person):
            disable = True
            willingness_string += "\nObstructed by clothing"
        elif mc.recently_orgasmed and self.requires_hard:
            disable = True
            willingness_string += "\nRecently orgasmed"
        elif mc.energy < self.guy_energy and person.energy < self.girl_energy:
            disable = True
            willingness_string += "\nYou're both too tired"
        elif mc.energy < self.guy_energy:
            disable = True
            willingness_string += "\nYou're too tired"
        elif person.energy < self.girl_energy:
            disable = True
            willingness_string += "\nShe's too tired"

        position_opinion = ""
        opinion_score = person.known_opinion(self.opinion_tags)
        if opinion_score > 0:
            position_opinion = " {image=thumbs_up}"
        elif opinion_score < 0:
            position_opinion = " {image=thumbs_down}"

        if disable:
            return taboo_break_string + self.name + position_opinion + "\n{size=12}" + willingness_string + "{/size}" + " (disabled)" #Don't show the arousal and energy string if it's disabled to prevent overrun
        return taboo_break_string + self.name + position_opinion + "\n{size=12}" + willingness_string + energy_string + arousal_string + "{/size}" + tooltip_string

    def build_position_rejection_string(self, person: Person) -> str:
        '''
        Returns the information for when Person.allow_position() returns False
        '''
        if self == spanking and person.spank_level > 4:
            return f"{self.name}\nToo recently spanked (disabled)"

        if self.requires_large_tits and not person.has_large_tits:
            return f"{self.name}\nBreasts too small (disabled)"

        result = self.name + "\nHates: "
        result += " - ".join((x for x in self.opinion_tags if person.known_opinion(x) == -2))
        result += " (disabled)"
        return result

    def calculate_energy_cost(self, person: Person | MainCharacter) -> int: # Calculates this positions's true energy cost based on the skill of the participants.
        base_energy = 0
        if isinstance(person, Person):
            base_energy = self.girl_energy
        else:
            base_energy = self.guy_energy
        return builtins.int(base_energy * ((1 - (0.05 * person.sex_skills[self.skill_tag])) * perk_libido_enhancer_energy_mult()))

    def build_energy_string(self, person: Person) -> str:
        (guy_energy_percent, girl_energy_percent) = self._estimate_energy_values(person)
        return f"{{color=#A3A3FF}}{guy_energy_percent:.0f}%{{/color}}/{{color=#FF6EC7}}{girl_energy_percent:.0f}%{{/color}} {{image=energy_token_small}}"

    def build_arousal_string(self, person: Person) -> str:
        (guy_arousal_percent, girl_arousal_percent) = self._estimate_arousal_values(person)
        return f"{{color=#A3A3FF}}{guy_arousal_percent:.0f}%{{/color}}/{{color=#FF6EC7}}{girl_arousal_percent:.0f}%{{/color}} {{image=arousal_token_small}}"

    def build_energy_arousal_line(self, person: Person) -> str:
        return f"{{size=18}}{self.build_energy_string(person)} | {self.build_arousal_string(person)}{{/size}}"

    def get_opinion_score(self, person: Person) -> int:
        opinion_score = 0
        for opinion_tag in self.opinion_tags:
            opinion_score += person.opinion(opinion_tag) #Add a bonus or penalty if she likes or dislikes the position.
        if opinion_score <= 0 and perk_system.has_ability_perk("Serum: Aura of Arousal") and mc_serum_aura_arousal.trait_tier >= 2:
            opinion_score = 0
            if self.skill_tag in ("Vaginal", "Anal"):
                opinion_score += 1
            if mc_serum_aura_arousal.trait_tier >= 3:
                opinion_score += 1
        return opinion_score

    def get_trance_chance_modifier(self, person: Person) -> int:
        '''
        Modifier is based on cumulative opinion score for this position
        When she has a negative score, the modifier will be negative
        '''
        return 2 * person.opinion(self.opinion_tags)

    def _discover_opinions(self, person: Person):
        '''
        Auto-discover passed persons opinions for this position
        '''
        for opinion in self.opinion_tags:   # auto-discover opinions on breaking taboo for position
            person.discover_opinion(opinion)

    def _estimate_arousal_values(self, person: Person):
        girl_expected_arousal = builtins.int(self.girl_arousal * (1 + 0.1 * mc.sex_skills[self.skill_tag])) + self.get_opinion_score(person)
        guy_expected_arousal = builtins.int(self.guy_arousal * (1 + 0.1 * person.sex_skills[self.skill_tag])) - (2 if self.skill_tag in ("Vaginal", "Anal") and mc.condom else 0)

        guy_arousal_percent = (guy_expected_arousal / (max(mc.max_arousal, 1) * 1.0)) * 100.0
        girl_arousal_percent = (girl_expected_arousal / (max(person.max_arousal, 1) * 1.0)) * 100.0

        return (guy_arousal_percent, girl_arousal_percent)

    def _estimate_energy_values(self, person: Person):
        guy_energy_percent = (self.calculate_energy_cost(mc) / (max(mc.max_energy, 1) * 1.0)) * 100.0
        girl_energy_percent = (self.calculate_energy_cost(person) / (max(person.max_energy, 1) * 1.0)) * 100.0
        return (guy_energy_percent, girl_energy_percent)
