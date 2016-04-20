# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy


class Relations(object):
    _fervor = ['delicate', 'plain', 'intense']
    _distance = ['formal', 'close', 'intimate']
    _congruence = ['contradictor', 'associate', 'supporter']
    def __init__(self, owner, target):
        self.owner = owner
        self.target = target
        self.fervor = 'plain'
        self.distance = 'close'
        self.congruence = 'associate'
        self.slave_stance = 'rebellious' # can be 'rebellious', 'forced', 'accustomed', 'willing'
        self.master_stance = 'cruel' # can be 'cruel', 'opressive', 'rightful', 'benevolent'
        self.recognition_stance = ''
        self.respect = None
        self._tokens = []
        self.tokens_difficulty = {'dread': 0, 'dependence': 0, 'discipline': 0, 'compassion': 0, 'confidence': 0, 'craving': 0}
        self.dread = 0
        self.dependence = 0
        self.discipline = 0
        self.confidence = 0
        self.compassion = 0
        self.craving = 0

    @property
    def tokens(self):
        return self.owner.relations_tokens(self.target)
    def add_token(self, token, power=None):
        if not self.has_token(token):
            if power:
                if power > self._tokens_difficulty[token]:
                    self.owner.relations_tokens(self.target).append(token)
            else:
                self.owner.relations_tokens(self.target).append(token)
            renpy.call_in_new_context('lbl_notify', self.owner, token)

 
    def has_token(self, token):
        if token in self.owner.relations_tokens(self.target):
            return True
        return False

    def use_token(self, token):
        if has_token(token):
            self.owner.relations_tokens(self.target).remove(token)
            self._tokens_difficulty[token] += 1
            self.target.relations(self)._tokens_difficulty[token] += 1
        else:
            return "%s has no token named %s"%(self.owner.name(), token)
    def change(self, axis, direction):
        z = '_%s'%(axis)
        ax = getattr(Relations, z)
        rel = getattr(self, axis)
        ind = ax.index(rel)
        if direction == "+":
            ind += 1
            if ind > 2:
                if axis == 'distance':
                    if self.owner.alignment['orderliness'] == 'chaotic':
                        self.add_token('accordance')
                    elif self.owner.alignment['orderliness'] == 'lawful':
                        self.add_token('antagonism')
                if axis == 'fervor':
                    if self.owner.alignment['activity'] == 'timid':
                        self.add_token('accordance')
                    elif self.owner.alignment['activity'] == 'ardent':
                        self.add_token('antagonism')
                if axis == 'congruence':
                    if self.owner.alignment['morality'] == 'good':
                        self.add_token('accordance')
                    elif self.owner.alignment['morality'] == 'evil':
                        self.add_token('antagonism')
                ind = 2
        elif direction == '-':
            ind -= 1
            if ind < 0:
                if axis == 'distance':
                    if self.owner.alignment['orderliness'] == 'chaotic':
                        self.add_token('antagonism')
                    elif self.owner.alignment['orderliness'] == 'lawful':
                        self.add_token('accordance')
                if axis == 'fervor':
                    if self.owner.alignment['activity'] == 'timid':
                        self.add_token('antagonism')
                    elif self.owner.alignment['activity'] == 'ardent':
                        self.add_token('accordance')
                if axis == 'congruence':
                    if self.owner.alignment['morality'] == 'good':
                        self.add_token('antagonism')
                    elif self.owner.alignment['morality'] == 'evil':
                        self.add_token('accordance')
                ind = 0
        rel = ax[ind]
        self.__dict__[axis] = rel

    def description(self):
        return (self.fervor, self.distance, self.affection)

