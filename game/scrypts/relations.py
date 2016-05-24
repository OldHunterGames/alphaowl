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
                        self.owner.add_token('accordance')
                    elif self.owner.alignment['orderliness'] == 'lawful':
                        self.owner.add_token('antagonism')
                if axis == 'fervor':
                    if self.owner.alignment['activity'] == 'timid':
                        self.owner.add_token('accordance')
                    elif self.owner.alignment['activity'] == 'ardent':
                        self.owner.add_token('antagonism')
                if axis == 'congruence':
                    if self.owner.alignment['morality'] == 'good':
                        self.owner.add_token('accordance')
                    elif self.owner.alignment['morality'] == 'evil':
                        self.owner.add_token('antagonism')
                ind = 2
        elif direction == '-':
            ind -= 1
            if ind < 0:
                if axis == 'distance':
                    if self.owner.alignment['orderliness'] == 'chaotic':
                        self.owner.add_token('antagonism')
                    elif self.owner.alignment['orderliness'] == 'lawful':
                        self.owner.add_token('accordance')
                if axis == 'fervor':
                    if self.owner.alignment['activity'] == 'timid':
                        self.owner.add_token('antagonism')
                    elif self.owner.alignment['activity'] == 'ardent':
                        self.owner.add_token('accordance')
                if axis == 'congruence':
                    if self.owner.alignment['morality'] == 'good':
                        self.owner.add_token('antagonism')
                    elif self.owner.alignment['morality'] == 'evil':
                        self.owner.add_token('accordance')
                ind = 0
        rel = ax[ind]
        self.__dict__[axis] = rel

    def description(self):
        return (self.fervor, self.distance, self.congruence)

