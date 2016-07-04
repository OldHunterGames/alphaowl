# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy
_needs_memory = []
class Need_memory(object):
    def __init__(self, actor, target):
        self.actor = actor
        self.target = target
        self.needs = {'gratify': {}, 'atrocity': {}}

    def set_memory(self, need, power, t):
        self.needs[t][need] = power
    def get_memory(self, need, t):
        if t in self.needs.keys():
            if need in self.needs[t].keys():
                return self.needs[t][need]
        else:
            set_memory(self, need, 0, t)
        return 0


class Action(object):
    

    @staticmethod
    def get_memory(actor, target, need, t):
        for mem in _needs_memory:
            if mem.actor == actor and mem.target == target:
                return mem.get_memory(need, t)


    @staticmethod
    def set_memory(actor, target, need, power, t):
        for mem in _needs_memory:
            if mem.actor == actor and mem.target == target:
                mem.set_memory(need, power, t)
    

    @staticmethod
    def max_intensity(target, needs):
        if needs:
            intensity = [0, None]
            for need in needs:
                i = getattr(target, need).intensity()
                if i > intensity[0]:
                    intensity[0] = i
                    intensity[1] = need
            return intensity
        else:
            raise Exception("Should use at least one need")


    def __init__(self, actor, target, name='template_name', difficulty=3, *args, **kwargs):
        self.name = name # name used for screen title
        self.actor = actor
        self.target = target
        self.difficulty = difficulty # 3 is default for most actions

        self.phobias = []
        self.phobias_inverted = False
        
        self._skill = None
        self._label = 'lbl_skill_check'
        self._power = 0
        self._reduced = 0
        self._power_text = []
        self._compare_with_power = 0
        self.motivation = None
        self.morality = 0

        
        
        self.pros = []
        self.cons = []

    
    def set_phobias(self, *args):
        for arg in args:
            if isinstance(arg, bool):
                self.phobias_inverted = arg
            else:
                self.phobias.append(arg)


    def set_respect_needs(self, *args):
        for arg in args:
            if isinstance(arg, bool):
                self._respect_needs = arg
            else:
                self._respect_needs.append(arg)
    

    def set_power(self, power, reduced, compare_value, pros_text, cons_text):
        self._power = power
        self._reduced = reduced
        self._compare_with_power = compare_value
        self._power_text.append(pros_text)
        self._power_text.append(cons_text)


    def set_skill(self, skill):
        self._skill = skill


    def special_motivators(self, *args):
        for arg in args:
            self._special_motivators.append(arg)



    def compare_two(self, value1, value2, pros_text, cons_text):
        if value1 > value2:
            self.pros.append(pros_text)
        elif value1 < value2:
            self.cons.append(cons_text)


    def activate(self):
        pros, cons = self._build_pros_cons()

        if 'unfortunate' in self.actor.conditions:
            cons.append('unfortunate')
        if self.actor.vigor < 1:
            cons.append('exausted')

        for p in self.pros:
            pros.append(p)
        for c in self.cons:
            cons.append(c)

        if self.actor.player_controlled:
            renpy.call_in_new_context(self._label, pros, cons, self.actor, self._skill, self.name) 
        else:
            if not self.motivation:
                raise Exception("npc action activated without motivation")
            motivated_check(self.actor, self.motivation, pros, cons)
        result = get_action_power(self.actor, pros, cons, self._skill, self.morality)
        
        if not 'unfortunate' in self.actor.conditions:
            if 'unlucky' in cons:
                self.actor.conditions.append('unfortunate')
        else:
            if result > 0:
                self.actor.conditions.remove('unfortunate')

        return result



    def _build_pros_cons(self):
        pros, cons = pros_cons_default()
        if self._skill:
            pros_cons_skill(self.actor, self._skill, self.difficulty, pros, cons)
        elif self._power > 0:
            self.compare_two(self._compare_with_power, self._reduced-self._power,
                            self._power_text[0], self._power_text[1])
        else:
            raise Exception("Action activated without power or skill")
        phobias_check(self.target, self.phobias, pros, cons, self.phobias_inverted)
        return pros, cons


class Skillcheck(Action):
    def __init__(self, actor, skill, *args, **kwargs):
        super(Skillcheck, self).__init__(actor, None, *args, **kwargs)
        self.set_skill(skill)
    

    def _build_pros_cons(self):
        pros, cons = pros_cons_default()
        
        if self._skill:
            pros_cons_skill(self.actor, self._skill, self.difficulty, pros, cons)
        else:
            raise Exception("Skillcheck activated without skill")

        return pros, cons


def phobias_check(target, phobias, pros, cons=None, inverted=False):
    for phobia in phobias:
        if phobia in target.phobias():
            if cons and inverted:
                cons.append('phobia')
            else:
                pros.append('phobia')
            return


def pros_cons_default():
    cons = []
    pros = []
    cons.append('cons:')
    pros.append('pros:')
    return pros, cons

def pros_cons_skill(character, skill, difficulty, pros, cons):
    skill = character.skill(skill)
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
    return pros, cons


def motivated_check(actor, motivation, pros, cons):
        if motivation < 0:
            cons.append('sabotage')
        if motivation == 0:
            pass
        if motivation > 6-actor.vigor and actor.vigor>0:
            pros.append('vigorous')
        if motivation > 5:
            pros.append('determined')
        if actor.feature('venturous'):
            dice = randint(1,2)
            if dice == 2:
                pros.append('lucky')
            else:
                cons.append('unlucky')


def get_action_power(person, pros, cons, skill=None, morality=0):
        if 'sabotage' in cons:
            return -1
        use_resources(person, pros, cons, skill, morality)
        p = len(pros) - len(cons)
        if p < 0:
            p = 0
        elif p > 5:
            p = 5
        return p

def use_resources(person, pros, cons, skill=None, morality=0):
        if 'sabotage' in cons:
            return
        if 'vigorous' in pros:
            person.drain_vigor()
        if 'determined' in pros:
            person.determination -= 1
        if skill:
            person.skills_used.append(skill)
        if morality:
            person.moral_action(morality)