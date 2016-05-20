# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *
from events import events_list
def pros_cons_tokens(character, morality):
    cons = []
    pros = []
    cons.append('cons:')
    pros.append('pros')
    master = character.master
    if character.sensitivity > master.spirit:
        pros.append('emphaty')
    else:
        cons.append('stern')
    if master.mood()[0] > 0:
        pros.append("master mood")
    elif master.mood()[0] < 0:
        cons.append('master mood')
    if character.mood()[0] > 0:
        cons.append('too cheerful')
    elif character.mood()[0] < 0:
        pros.append('miserable slave')
    if morality < 0:
        pros.append('mercy')
    else:
        cons.append('sadism')
    if master.authority.intensity == 0:
        cons.append('indifference')
    if master.authority.intensity > master.favor():
        cons.append('tyrannous')
    elif master.authority.intensity < master.favor():
        pros.append('indulgence')
    return (pros, cons)
def get_power(pros_cons):
    p = len(pros_cons[0]) - len(pros_cons[1])
    if p < 0:
        p = 0
    elif p > 5:
        p = 5
    return p
class Engine(object):

    def __init__(self):
        self.mother = Person()
        self.child = Person()
        self.characters = [self.child, self.mother]
        self.player = None
        self.time = 1
        self.tenge = 0
        self.mom_stuff = []
        self.events_list = events_list
        self.mode = 'son'
        self.studies = [
            'major',
            'military',
            'gym',
            'labs',
            'practice',
        ]
        self.evn_skipcheck = True

    def choose_study(self):
        if self.studies:
            study = choice(self.studies)
        else:
            study = False

        return study

    def new_turn(self):
        self.time += 1
        self.player.ap = 1
        return "label_new_day"
    

    #def possible_events(self, kind, who = None):
    #   """
    #    :param kind:
    #    "turn" - end-of-turn event
    #    "char" - event with one of player faction main characters
    #    "faction" - event for one of active factions beside player faction
    #    :return: the RenPu location with the choosen event
    #    """
    #    list_of_events = []
    #    for event in self.events_list:
    #        if kind in event.natures:
    #                list_of_events.append(event)

    #    return list_of_events
    

    def end_turn_event(self):
        shuffle(self.events_list)
        possible = self.events_list
        char = choice(self.characters)
        for ev in possible:
            r = ev.trigger(char)
            if r:
                return  

    

    def job_sex(self, worker, forced=False):
        skill = 'sex'
        efficiency = 20
        quality = person.use_skill(skill, forced)
        self.tenge += efficiency*quality

    def torture(self, target=None, taboos=[], power=0):#should use at least one taboo
        _taboos = [t for t in taboos]
        taboo = _taboos.pop(0)
        for i in _taboos:
            if target.taboo(taboo).value < target.taboo(i).value:
                taboo = i
        effect = target.pain_effect_threshold(taboo)
        tear = target.pain_tear_threshold(taboo)
        tokens = []
        if power > tear:
            target.anxiety += 1
            tokens.append('dread')
        elif power > effect:
            tokens.append('dread')
        if len(tokens) < 1:
            return
        target.taboo(taboo).use(power)
        for i in tokens:
            target.add_token(i)
        return


    def train(self, target, power=0):
        target_resistance = target.training_resistance()
        if target_resistance < power:
            target.add_token('discipline')

    def remorse(self, morality):
        power = renpy.call_in_new_context('lbl_skill_check', pros_cons_tokens(self.player, morality), self.player)
        power = get_power(power)
        renpy.call_in_new_context('lbl_notify', self.player, power)
        if power > self.player.master.tokens_difficulty['compassion']:
            target.add_token('compassion')
    def duty(self, target, power):
        if power > target.duty_threshold():
            target.add_token('confidence')
    def gratifaction(self, target, power, needs):
        if power > target.gratifaction_threshold(needs):
            target.add_token('craving')

    def suggestion(self, target, power):
        if power > target.suggestion_check():
            return True
        return False


    def reliance(self, target, power):
        if power > target.reliance.threshold():
            target.add_token('reliance')

    def kindness(self, target, power):
        if power > target.kindness_threshold():
            target.add_token('kindness')

    def attraction(self, target, power):
        if power > target.attraction_threshold():
            target.add_token('attraction')
