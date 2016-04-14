# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *
from events import events_list

class Engine(object):

    def __init__(self):
        self.mother = Person()
        self.child = Person()
        self.characters = [self.child, self.mother]
        self.player = None
        self.time = 1
        self.tenge = 100
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
            tokens.append('angst')
            tokens.append('dread')
        elif power > effect:
            tokens.append('dread')
        if len(tokens) < 1:
            return
        target.taboo(taboo).use(power)
        if not target.player_controlled:
            if power - effect < target.willpower and target.willpower != 0:
                 res = target.use_resource('willpower')
                 if res > 0:
                    tokens.remove('dread')
            else:
                if target.determination > 0:
                    target.determination -= 1
                    tokens.remove('dread')
            for i in tokens:
                target.add_token(i)

        else:
            for i in tokens:
                decision = renpy.call_in_new_context('lbl_resist', i)
                if decision=='willpower':
                    res = target.use_resource('willpower')
                    if res > 0:
                        res = True
                    else:
                        res = False
                        target.tokens.append(i) 
                    renpy.call_in_new_context('lbl_resist_result', i, res)  
                elif decision == 'determination':
                    if target.determination > 0:
                        target.determination -= 1
                        res = True
                    else:
                        res = False
                    renpy.call_in_new_context('lbl_resist_result', i, res)
                else:
                    target.add_token(i)
                    res = False
                    renpy.call_in_new_context('lbl_notify', i)
        return


    def train(self, target, power=0):
        target_resistance = target.training_resistance()
        if target_resistance < power:
            if target.player_controlled:
                result = renpy.call_in_new_context('lbl_resist', 'discipline')
                if result == 'determination':
                    if target.determination > 0:
                        target.determination -= 1
                        result = True
                    else:
                        result = False
                    renpy.call_in_new_context('lbl_resist_result', 'discipline', result)
                elif result == 'willpower':
                    r = target.use_resource('willpower')
                    if r > 0:
                        result = True
                    else:
                        result = False
                    renpy.call_in_new_context('lbl_resist_result', 'discipline', result)
                if result == False:
                    renpy.call_in_new_context('lbl_notify', 'discipline')
                    target.add_token('discipline')
                return

            if target.slave_stance.lower() == 'rebellious':
                if target.use_resource('willpower') <= 0:
                    if target.determination > 0:
                        target.determination -= 1
                        return
                else:
                    return
            elif target.willpower > target.obedience():
                if target.use_resource('willpower') > 0:
                    return
            target.add_token('discipline')