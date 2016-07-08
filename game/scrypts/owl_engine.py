# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *
from events import events_list
from action import Action, Skillcheck


def get_max_need(target, *args):
    maxn_value = 0
    maxn = None
    needs = target.get_needs()
    for arg in args:
        if arg in needs.keys():
            level = needs[arg].level
            if level > maxn:
                maxn = level
                maxn_name = arg
    return maxn, maxn_value
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
        self.resources = {'drugs': {'waste':0, 'current':0}, 'provision': {'waste': 0, 'current': 0}}
        self._drugs_per_turn = 0
        self._provision_per_turn = 0
        self.money = 0


    @property
    def player(self):
        if not self._player:
            raise Exception("Player person is not selected")
        return self._player


    def set_player(self, person):
        self._player = person
        person.player_controlled = True


    def resource(self, res):
        return self.resources[res]['current']
    def res_to_money(self, res):
        return -(self.resources[res]['current']-self.resources[res]['waste'])*3
    def res_set_waste(self, res, value):
        if value < 0:
            return
        self.resources[res]['waste'] = value
    def res_set(self, res, value):
        self.resources[res]['current'] = value
    def res_add(self, res, value):
        self.resources[res]['current'] = self.resources[res]['current'] + value


    def can_waste(self, res):
        if self.resources[res]['current'] - self.resources[res]['waste'] >= 0:
            return True
        else:
            return False
    def res_waste(self):
        for res in self.resources.keys():
            if self.can_waste(res):
                self.resources[res]['current'] -= self.resources[res]['waste']
            elif self.has_money(self.res_to_money(res)):
                self.res_set(res, 0)
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
            if not self.can_waste(res) or not self.has_money(self.res_to_money(res)):
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
        self.res_waste()
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
        check -= (3-get_max_need(target, *args)[1])
        return check


    def skillcheck(self, actor, skill, difficulty, motivation=0, success_threshold=0):
        skill = actor.skill(skill)
        # factors['attraction'] and equipment bonuses not implemented yet
        factors = {'level': 1+skill_level,
                    'attr': skill.attribute_value(),
                    'focus': skill.focus,
                    'mood': actor.mood,
                    'motivation': motivation,
                    'vitality': actor.vitality,
                    'bonus': actor.count_modifiers(skill.name)}
        result = 1+skill.level

        while result != 0:
            if difficulty < factors.values().count(result):
                break
            else:
                result -= 1
        if motivation < 1:
            result = -1
        if success_threshold:
            if result > success_threshold:
                result = True
            else:
                result = False
        return result

        