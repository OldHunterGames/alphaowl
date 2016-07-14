# -*- coding: UTF-8 -*-
from random import *
import collections
import copy

import renpy.store as store
import renpy.exports as renpy
from obj_character import *

from events import events_list
from action import Action, Skillcheck

remembered_needs = collections.defaultdict(list)
class UsedNeeds(object):
    def __init__(self, needs, owner):
        self.needs = copy(needs)
        self.owner = owner

    def is_used(self, needs, target):
        if target != self.owner:
            return True
        for need in needs:
            if need not in self.needs:
                return False
        return True
def remember_needs(target, token, needs):
    if not is_needs_used(target, token, needs):
        remembered_needs[token].append(UsedNeeds(needs, target))
    
def is_needs_used(target, token, needs):
    for used in remembered_needs[token]:
        if used.is_used(needs, target):
            return True
    return False
def get_max_need(target, *args):
    maxn_name = None
    maxn = None
    needs = target.get_needs()
    for arg in args:
        if arg in needs.keys():
            level = needs[arg].level
            if level > maxn:
                maxn = level
                maxn_name = arg
    return maxn, maxn_name


def encolor_text(text, value):
    if value < 0:
        value = 0
    colors = ['ff0000', 'ff00ff', '00ffff', '0000FF', '00ff00', 'DAA520', '000000']
    return '{b}{color=#%s}%s{/color}{/b}'%(colors[value], text)
class Engine(object):

    def __init__(self):
        self.mother = Person()
        self.child = Person()
        self.characters = [self.child, self.mother]
        self._player = None
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
        self._resources_consumption = []
        self.resources = {'drugs': 0, 'money': 0, 'provision': 0}


    @property
    def player(self):
        if not self._player:
            raise Exception("Player person is not selected")
        return self._player

    @property
    def money(self):
        return self.resources['money']
    @money.setter
    def money(self, value):
        if not value < 0:
            self.resources['money'] = value
    @property
    def provision_consumption(self):
        return self.resource_consumption('provision')
    @property
    def drugs(self):
        return self.resources['drugs']
    @drugs.setter
    def drugs(self, value):
        if not value < 0:
            self.resources['drugs'] = value
    @property
    def provision(self):
        return self.resources['provision']
    @provision.setter
    def provision(self, value):
        if not value < 0:
            self.resources['provision'] = value
    

    def set_player(self, person):
        self._player = person
        person.player_controlled = True


    def resource(self, res):
        return self.resources[res]
    

    def resource_consumption(self, res):
        value = 0
        for i in self._resources_consumption:
            if i[0] == res:
                try:
                    value += i[1]()
                except TypeError:
                    value += i[1]
        return value
    

    def resource_consumption_remove(self, name):
        for i in self._resources_consumption:
            if i[3] == name:
                self.resources.remove(i)

    def resource_consumption_tick(self):
        for i in self._resources_consumption:
            try:
                i[2] -= 1
                if i[2] < 1:
                    self._resources_consumption.remove(i)
            except TypeError:
                pass
    

    def res_to_money(self, res):
        return -(self.resources[res]-self.resource_consumption(res))*3
    
    def consumption_remove_by_name(self, name):
        for res in self._resources_consumption:
            if res[3] == name:
                self._resources_consumption.remove(res)
    def res_add_consumption(self, name, res, value, time=1):
        self.consumption_remove_by_name(name)
        self._resources_consumption.append([res, value, time, name])
    


    def can_consume(self, res):
        if self.resources[res] - self.resource_consumption(res) >= 0:
            return True
        else:
            return False
    

    def res_consume(self):
        for res in self.resources.keys():
            if self.can_consume(res):
                self.resources[res] -= self.resource_consumption(res)
            elif self.has_money(self.res_to_money(res)):
                self.resources[res] = 0
                self.use_money(self.res_to_money(res))

    
    def has_money(self, value):
        if self.money >= value:
            return True
        else:
            return False
    

    def use_money(self, value):
        if self.has_money(value):
            self.money -= value
        else:
            return

    def can_skip_turn(self):
        money = 0
        for res in self.resources.keys():
            if res!='money':
                if not self.can_consume(res) and not self.has_money(self.res_to_money(res)):
                    return False
                else:
                    money += self.res_to_money(res)
        if self.has_money(money):
            return True
        else:
            return False


    
    def choose_study(self):
        if self.studies:
            study = choice(self.studies)
        else:
            study = False

        return study

    def new_turn(self):
        self.res_consume()
        self.child.rest()
        self.mother.rest()
        self.batya.rest()
        self.resource_consumption_tick()
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
    
    def end_turn_event(self, skipcheck=True):
        shuffle(self.events_list)
        possible = self.events_list
        char = choice(self.characters)
        for ev in possible:
            r = ev.trigger(char, skipcheck)
            if r:
                return  

    

    def job_sex(self, worker, forced=False):
        skill = 'sex'
        efficiency = 20
        quality = person.use_skill(skill, forced)
        self.tenge += efficiency*quality



    def suggestion(self, target, power):
        if power > target.suggestion_check():
            return True
        return False

    

    def token_difficulty(self, target, token, *args):
        d = {'conquest': 'spirit', 'convention': 'mind', 'contribution': 'sensitivity'}

        check = getattr(target, d[token])
        if target.vitality < 1:
            check -= 1
        if target.mood < 1:
            check -= 1
        check += (3-get_max_need(target, *args)[0])
        check -= target.stance(self.player).value
        harmony = target.relations(self.player).harmony()[0]
        if harmony > 0:
            check -= harmony
        if check < 0:
            check = 0
        return check

    def threshold_skillcheck(self, actor, skill, difficulty=0, tense_needs=[], satisfy_needs=[], beneficiar=None,
                            morality=0, success_threshold=0, special_motivators=[]):
        success_threshold += 1
        result = self.skillcheck(actor, skill, difficulty, tense_needs, satisfy_needs, beneficiar, morality, special_motivators, success_threshold)
        if success_threshold < result:
            threshold_result = True
        else:
            threshold_result = False
        return threshold_result, result


    def skillcheck(self, actor, skill, difficulty=0, tense_needs=[], satisfy_needs=[], beneficiar=None,
                    morality=0, special_motivators=[], threshold=None):
        skill = actor.skill(skill)
        motivation = actor.motivation(skill, tense_needs, satisfy_needs, beneficiar)
        # factors['attraction'] and equipment bonuses not implemented yet
        factors = {'level': 1+skill.level,
                    skill.attribute: skill.attribute_value(),
                    'focus': skill.focus,
                    'mood': actor.mood,
                    'motivation': motivation,
                    'vitality': actor.vitality,
                    'bonus': actor.count_modifiers(skill.name)}
        result = 1+skill.level
        used = []
        found = False
        while result != 0:
            difficulty_check = 1
            used = []
            for k, v in factors.items():
                if difficulty < difficulty_check:
                    found = True
                elif k != 'level' and v >= result:
                    difficulty_check += 1
                    used.append(k)
            if difficulty < difficulty_check:
                found = True
            if not found:
                result -= 1
            else:
                break
        if motivation < 1:
            result = -1
        renpy.call_in_new_context('lbl_skillcheck_info', result, factors, skill, used, threshold, difficulty)
        if result >= 0:
            for need in tense_needs:
                getattr(actor, need).set_tension()
            for need in satisfy_needs:
                getattr(actor, need).satisfaction = result
            actor.use_skill(skill)
        return result

        