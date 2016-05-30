# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *
from events import events_list
def insanity_check(target, needs, pros_cons):
    for need in needs:
        if getattr(target, need).level == 4 and 'passion' not in pros_cons[0]:
            pros_cons[0].append('passion')
        elif getattr(target, need).level == 0 and 'indifference' not in pros_cons[1]:
            pros_cons[1].append('indifference')
    return
def phobias_check(target, phobias, pros_cons):
    for phobia in phobias:
        if phobia in target.phobias():
            pros.append('phobia')
            return
def max_intensity(target, needs):
    if needs:
        intensity = 0
        for need in needs:
            i = getattr(target, need).intensity()
            if i > intensity:
                intensity = i
        return intensity
    else:
        raise Exception("Should use at least one need")

def pros_cons_default(character):
    cons = []
    pros = []
    cons.append('cons:')
    pros.append('pros:')
    if character.vigor < 1:
        cons.append('exausted')
    return (pros, cons)
def pros_cons_skill(character, skill, difficulty):
    skill = character.skill(skill)
    pros_cons = pros_cons_default(character)
    pros = pros_cons[0]
    cons = pros_cons[1]
    i = difficulty
    i -= getattr(character, character.skill(skill).attribute)
    if i > 1:
        while i > 1:
            cons.append('very')
            i -= 1
    if i==1:
        cons.append('difficult')
    elif i < 0:
        pros.append('easy')
    if skill.talent:
        pros.append('talent')
    if skill.expirience:
        pros.append('expirience')
    if skill.specialization:
        pros.append('specialization')
    if skill.training:
        pros.append('training')
    if character.mood()[0] > 0:
        pros.append('mood')
    elif character.mood()[0] < 0:
        cons.append('mood')
    if skill == character.focused_skill and character.focus > 5 - character.mind:
        pros.append('focus')
    if character.anxiety > 0:
        cons.append('anxiety')
    #also will be bonuses for uniform or debuffs for something
    return (pros, cons)


def pros_cons_remorse(character, power=0, needs=[], morality=0, phobias=[]):
    pros, cons = pros_cons_default(character)
    master = character.master
    if not master or character.stance.type != 'slave':
        raise Exception("Remorse with character who is not slave")
    intensity = max_intensity(master, needs)
    insanity_check(master, needs, (pros, cons))
    phobias_check(character, phobias, (pros, cons))
    if power > intensity:
        cons.append('minor concern')
    elif power < intensity:
        pros.append('severe suffering')
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
    elif morality > 0:
        cons.append('sadism')
    if master.authority.intensity > master.favor():
        cons.append('tyrannous')
    elif master.authority.intensity < master.favor():
        pros.append('indulgence')
    return (pros, cons)
def pros_cons_duty(character, power, morality):
    pros, cons = pros_cons_default(character)
    master = character.master
    if master.authority.intensity() < power:
        pros.append('content')
    elif master.authority.intensity() > power:
        cons.append('dissatisfaction')
    if master.stance.value == 0:
        cons.append('cruel')
    elif master.stance.value == 3:
        pros.append('benevolent')
    if character.mind > master.mind:
        pros.append('insight')
    elif character.mind < master.mind:
        cons.append('insight')
    if character.mood()[0] > 0:
        pros.append('mood')
    elif character.mood()[0] < 0:
        cons.append('mood')
    if morality > 0:
        pros.append('discipline')
    elif morality < 0:
        cons.append('negiligence')
    return (pros, cons)

def pros_cons_gratifaction(character, needs, skill, morality=0):
    intensity = max_intensity(character.master, needs) 
    difficulty = 6-intensity
    pros, cons = pros_cons_skill(character, skill, difficulty)
    insanity_check(character.master, needs, (pros, cons))
    if morality > 0:
        pros.append('ardour')
    elif morality < 0:
        cons.append('composure')
    return (pros, cons)


def pros_cons_torture(target, source, morality, power, phobias=[], needs=[]):
    pros, cons = pros_cons_default(source)
    intensity = max_intensity(target, needs)
    insanity_check(target, needs, (pros, cons))
    phobias_check(target, phobias, (pros, cons))
    if intensity > power:
        pros.append('severe suffering')
    else:
        cons.append('minor concern')
    if target.mood()[0] > 0:
        cons.append('hopeful slave')
    elif target.mood()[0] < 0:
        pros.append('miserable slave')
    if morality < 0:
        cons.append('remorse')
    elif morality > 0:
        pros.append('malice')
    if target.obedience() > source.authority.intensity():
        cons.append('indulgence')
    elif target.obedience() < source.authority.intensity():
        pros.append('rigor')
    return (pros, cons)

def pros_cons_discipline(target, source, morality, skill='leadership', difficulty=0):
    pros, cons = pros_cons_skill(source, skill, difficulty)
    if target.stance.value == 0:
        cons.append('insurgency')
    elif target.stance.value == 3:
        pros.append('willingness')
    if morality > 0:
        pros.append('persistance')
    elif morality < 0:
        cons.append('incoherence')
    return (pros, cons)


def pros_cons_dependence(target, needs=[], power=0, morality=0):
    pros, cons = pros_cons_default(target.master)
    intensity = max_intensity(target, needs)
    insanity_check(target, needs, (pros, cons))
    if intensity > power:
        pros.append('desire')
    elif intensity < power:
        cons.append('unconcerned')
    if target.mood()[0] > 0:
        cons.append('complacent slave')
    elif target.mood()[0] < 0:
        pros.append('miserable slave')
    if morality < 0:
        cons.append('blunt offer')
    elif morality > 0:
        pros.append('diplomaty')
    if target.obedience() > target.master.authority.intensity():
        pros.append('well earned')
    elif target.obedience() < target.master.authority.intensity():
        cons.append('connivance')
    return (pros, cons)
def pros_cons_attraction(character, target, need, skill, morality):
    difficulty = 6-getattr(target, need).intensity()
    pros, cons = pros_cons_skill(character, skill, difficulty)
    insanity_check(target, [need], (pros, cons))
    if morality > 0:
        pros.append('ardour')
    elif morality < 0:
        cons.append('composure')
    return (pros, cons)
def pros_cons_kindness(character, target, morality):
    pros, cons = pros_cons_default(character)
    intensity = target.communication.intensity()
    if intensity+character.respect() > 6:
        pros.append('connection')
    elif intensity+character.respect() < 6:
        cons.append('distance')
    if target.stance.value == 3:
        pros.append('friendly')
    elif target.stance.value == 0:
        cons.append('distrustful')
    if character.mood()[0] > 0:
        pros.append('mood')
    elif character.mood()[0] < 0:
        cons.append('mood')
    if target.mood()[0] > 0:
        pros.append('cheerful')
    elif target.mood()[0] < 0:
        cons.append('grumpy')
    if morality > 0:
        pros.append('kindness')
    elif morality < 0:
        cons.append('discourtesy')
    return pros, cons
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

    def torture(self, target, needs, power, effects=[], source=None, benefic=None):
        if not source:
            source = target.supervisor
        if not benefic:
            benefic = target.master
        if source == self.player:
            moral = source.check_moral('evil', target)
        else:
            moral = source.check_moral('evil')
        pros_cons = pros_cons_torture(target, source, moral, power, effects, needs)
        p = renpy.call_in_new_context('lbl_skill_check', pros_cons, source, morality=moral, benefic=benefic)
        target.drain_vigor()
        broken = []
        for need in needs:
            n = getattr(target, need)
            n.set_shift(-power)
            if n.memory['torture'] > power:
                broken.append(need)
        if len(broken) == len(needs):
            return
        if p > target.tokens_difficulty['dread']:
            target.add_token('dread')
            for need in needs:
                n = getattr(target, need)
                if n.memory['torture'] < power:
                    n.memory['torture'] = power
        return p


    def train(self, target, source=None, skill='leadership', benefic=None):
        if not target.master:
            raise Exception("train call with target who have no master")
        if not benefic:
            benefic = target.master
        if not source:
            source = target.supervisor
        if source == self.player:
            moral = source.check_moral('evil', target)
        else:
            moral = source.check_moral('evil')
        difficulty = target.mind+target.anxiety
        if target.mood()[0] < 0:
            difficulty += 1
        elif target.mood()[0] > 0:
            difficulty -= 1
        pros_cons = pros_cons_discipline(target, source, moral, skill, difficulty)
        power = renpy.call_in_new_context('lbl_skill_check', pros_cons, source, skill=True, morality=moral, benefic=benefic)
        target.drain_vigor()
        if power > target.tokens_difficulty['discipline']:
            target.add_token('discipline')
        return power

    def bribe(self, target, needs=[], power=0):
        if not target.master:
            raise Exception("bribe should be used with slave target but %s is not slave"%(target.name()))
        moral = target.master.check_moral('timid', target)
        pros_cons = pros_cons_dependence(target, needs, power, moral)
        p = renpy.call_in_new_context('lbl_skill_check', pros_cons, target.master, vigor=False, morality=moral)
        target.master.moral_action('timid', target)
        bribed = []
        for need in needs:
            n = getattr(target, need)
            n.set_shift(power)
            if n.memory['bribe'] > power:
                bribed.append(need)
        if len(bribed) == len(needs):
            return renpy.call_in_new_context('lbl_notify', "подкуп не удался")
        if p > target.tokens_difficulty['dependence']:
            target.add_token('dependence')
            for need in needs:
                n = getattr(need, target)
                if n.memory['bribe'] < power:
                    n.memory['bribe'] = power
        return p


    def remorse(self, power, needs, phobias=[], slave=None):
        if not slave:
            slave = self.player
        if not slave.master:
            raise Exception("remorse called with slave who have no master")
        moral = slave.master.check_moral('evil', slave)
        pros_cons = pros_cons_remorse(slave, power, needs, moral, phobias)
        p = renpy.call_in_new_context('lbl_skill_check', pros_cons, slave)
        slave.master.moral_action('evil', slave)
        remorsed = []
        slave.master.drain_vigor()
        for need in needs:
            n = getattr(slave, need)
            n.set_shift(-power)
            if n.memory['remorse'] > power:
                remorsed.append(need)
        if len(remorsed) == len(needs):
            return
        if p > slave.master.tokens_difficulty['compassion']:
            slave.master.add_token('compassion')
        return p
    def duty(self, power, slave=None):
        if not slave:
            slave = self.player
        moral = slave.check_moral('lawful', slave.master)
        pros_cons = pros_cons_duty(slave, power, moral)
        power = renpy.call_in_new_context('lbl_skill_check', pros_cons, slave, vigor=False, morality=moral)
        slave.master.authority.set_shift(power)
        if not slave.master.stance.value == 3:
            slave.independence.set_shift(-power)
            slave.ambition.set_shift(-power)
        else:
            slave.stability.set_shift(power)
            slave.purpose.set_shift(power)
        if power > slave.master.tokens_difficulty['confidence']:
            slave.master.add_token('confidence')
        return power


    def gratifaction(self, skill, needs, slave=None):
        if not slave:
            slave = self.player
        morality = slave.master.check_moral('ardent', slave)
        pros_cons = pros_cons_gratifaction(slave, needs, skill, morality)
        slave.master.moral_action('ardent', slave)
        power = renpy.call_in_new_context('lbl_skill_check', pros_cons, slave, skill=True)
        craved = []
        for need in needs:
            n = getattr(slave.master, need)
            n.set_shift(power)
            if n.craving_memory:
                craved.append(n)
        if len(needs) == len(craved):
            return
        if power > slave.master.tokens_difficulty['craving']:
            slave.master.add_token('craving')
            for need in needs:
                getattr(need, slave.master).craving_memory = True
        return power



    def suggestion(self, target, power):
        if power > target.suggestion_check():
            return True
        return False


    def reliance(self, target, power):
        if power > target.tokens_difficulty['reliance']:
            target.add_token('reliance')

    def attraction(self, target, need, skill, source=None):
        if not source:
            source = self.player
        moral = source.check_moral('ardent', target)
        pros_cons = pros_cons_attraction(source, target, need, skill, moral)
        power = renpy.call_in_new_context('lbl_skill_check', pros_cons, source, skill=True, morality=moral)
        if getattr(target, need).attraction_memory:
            return
        if power > target.tokens_difficulty['attraction'] and not getattr(target, need).attraction_memory:
            target.add_token('attraction')
        return power

    def kindness(self, target, power, source=None):
        if not source:
            source = self.player
        source.power.set_shift(-power)
        source.ambition.set_shift(-power)
        source.communication.set_shift(power)
        if target.tokens_difficulty['kindness']+target.tokens.count('kindness') < 5:
            moral = source.check_moral('good', target)
            pros_cons = pros_cons_kindness(source, target, moral)
            power = renpy.call_in_new_context('lbl_skill_check', pros_cons, source, morality=moral)
            if power > target.tokens_difficulty['kindness']:
                target.add_token('kindness')
            return power
        return -1
