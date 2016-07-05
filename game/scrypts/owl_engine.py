# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *
from events import events_list
from action import Action, Skillcheck



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

    

    def atrocity_power(self, *args, **kwargs):
        return self.atrocity(*args, **kwargs)

    def atrocity(self, actor, target, token='conquest', target_tense=['general'], power=0, 
                skill=None, phobias=[], morality=0, name='template_name', controlled=False,
                respect_needs=['authority', 'power'], difficulty=0, motivation=None):

        memory = False
        torture = Action(actor, target, name)
        torture.difficulty = difficulty if difficulty else target.spirit
        torture.motivation = motivation
        torture.morality = morality
        torture.compare_two(0, target.mood()[0], 'misery', 'hope')
        torture.set_phobias(*phobias)
        torture.set_skill(skill)
        torture.compare_two(target.stance(self.player), 0, 'wilingness', 'contradiction')
        torture.compare_two(morality, 0, 'morally sure', 'moral doubts')
        torture.compare_two(Action.max_intensity(actor, respect_needs)[0], target.stance(self.player).respect(),
                            'rigor', 'indulgence')
        torture.set_power(power, 6, Action.max_intensity(target, target_tense)[0], 'severe suffering', 'minor concern')
        if controlled:
            torture.add_button('minor', 'minor', 'cons', 'intensity')
            torture.add_button('severe', 'severe', 'pros', 'intensity')

        result = torture.activate()
        if result < 1:
            target.add_token('antagonism')
            return
        if result >= 0:
            actor.drain_vigor()
            target.drain_vigor()
        
        maxn = Action.max_intensity(target, target_tense)[0]
        if maxn > Action.get_memory(actor, target, maxn, 'atrocity') and result > target.token_difficulty(token):
            memory = True
        for need in target_tense:
            n = getattr(target, need)
            if result > 0 and not 'minor' in torture.cons:
                n.set_shift(-result)
            if memory:
                Action.set_memory(actor, target, n, result, 'atrocity')
        if 'severe' in torture.pros:
            target.general.set_shift(-5)
        if memory:
            target.add_token(token)
        return result


    def suffering_power(self, *args, **kwargs):
        if 'skill' in kwargs:
            raise Exception('Suffering_power is not for check with skill')
        return self.suffering(*args, **kwargs)
    def suffering(self, actor, target, token='conquest', actor_tense=['general'], power=0, 
                skill=None, phobias=[], morality=0, name='template_name',
                respect_needs=['authority', 'power'], difficulty=0, motivation=None, beneficiar=None):

        memory = False
        suffering = Action(actor, target, name, name)
        suffering.motivation = motivation
        suffering.morality = morality
        suffering.difficulty = difficulty if difficulty else actor.spirit
        suffering.set_power(power, 6, Action.max_intensity(actor, actor_tense)[0], 'severe suffering', 'minor concern')
        suffering.set_skill(skill)
        suffering.set_phobias(*phobias)
        if not skill:
            suffering.compare_two(target.mood()[0], 0, 'serene torturer', 'angry torturer')
        suffering.compare_two(target.stance(self.player), 0, 'wilingness', 'contradiction')
        suffering.compare_two(0, actor.mood()[0], 'miserable victim', 'cheerful victim')
        suffering.compare_two(0, morality, 'mercy', 'sadism')
        suffering.compare_two(target.stance(self.player).respect(), Action.max_intensity(target, respect_needs)[0],
                            'indulgence', 'rigor')
        result = suffering.activate()
        if beneficiar:
            target = beneficiar
        if result < 1:
            target.add_token('antagonism')
            return
        if result >= 0:
            actor.drain_vigor()

        maxn = Action.max_intensity(actor, actor_tense)[0]
        if maxn > Action.get_memory(actor, target, maxn, 'suffering') and result > target.token_difficulty(token):
            memory = True
        
        for need in actor_tense:
            n = getattr(actor, need)
            if result > 0:
                n.set_shift(-result)
            if memory:
                Action.set_memory(actor, target, n, result, 'suffering')
        if memory:
            target.add_token(token)
        return result


    def pleasing_power(self, *args, **kwargs):
        return self.pleasing(*args, **kwargs)
    def pleasing(self, actor, target, token='contribution', target_please=['general'], power=0, difficulty=0, name='template_name',
                skill=None, actor_needs=[], respect_needs=['authority', 'altruism'], morality=0, motivation=None):

        memory = False
        please = Action(actor, target, name)
        please.motivation = motivation
        please.morality = morality
        please.difficulty = difficulty if difficulty else target.sensitivity
        please.set_power(power, 6, Action.max_intensity(target, target_please)[0], 'desire', 'unconcerned')
        please.set_skill(skill)
        please.compare_two(target.stance(self.player), 0, 'wilingness', 'contradiction')
        please.compare_two(morality, 0, 'ardour', 'composure')
        please.compare_two(0, target.mood()[0], 'sorrow', 'already happy')
        please.compare_two(target.stance(self.player), Action.max_intensity(actor, respect_needs)[0], 'well-earned', 'connivance')
        result = please.activate()
        if result < 1:
            target.add_token('antagonism')
            return 
        if result >= 0:
            actor.drain_vigor()

        maxn = Action.max_intensity(target, target_please)[0]
        if maxn > Action.get_memory(actor, target, maxn, 'pleasing') and result > target.token_difficulty(token):
            memory = True
        for need in target_please:
            n = getattr(target, need)
            if result > 0:
                n.set_shift(-result)
            if memory:
                Action.set_memory(actor, target, n, result, 'pleasing')
        if memory:
            target.add_token(token)
        return result


    def intercommunion_power(self, *args, **kwargs):
        return self.intercommunion(*args, **kwargs)
    def intercommunion(self, actor, target, token='convention', power=0, skill=None, difficulty=0,
                        respect_needs=['communication'], morality=0, motivation=None, name='template_name'):

        commun = Action(actor, target, name)
        commun.difficulty = difficulty if difficulty else target.mind
        commun.motivation = motivation
        commun.morality = morality
        commun.set_skill(skill)
        commun.set_power(power, 6, Action.max_intensity(actor, respect_needs), 'confidence', 'disbelief')
        if not skill:
            commun.compare_two(actor.mood()[0], 0, 'mood', 'mood')
        commun.compare_two(target.stance(self.player), 0, 'wilingness', 'contradiction')
        commun.compare_two(actor.mind, target.mind, 'insightful', 'clueless')
        commun.compare_two(target.mood()[0], 0, 'cheerful', 'grumpy')
        commun.compare_two(morality, 0, 'morally sure', 'moral doubts')
        
        result = commun.activate()
        if result < 1:
            target.add_token('antagonism')
            return
        if result > target.token_difficulty(token):
            target.add_token(token)
        return result


    def skillcheck(self, actor, skill, motivation=None, morality=0, name='template_name'):
        sk = Skillcheck(actor, skill)
        sk.name = name
        sk.motivation = motivation
        sk.morality = morality
        result = sk.activate()
        if result >= 0:
            actor.drain_vigor()
        return result