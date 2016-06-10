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
        self.characters = [self.owner, self.target]
        self._fervor = 1
        self._distance = 1
        self._congruence = 1
    @property
    def fervor(self):
        if self.target.player_controlled:
            return Relations._fervor[self._fervor]
        else:
            f = 1
            d = {'timid': 1, 'ardent': -1, 'reasonable':0}
            f += d[self.owner.alignment['activity']]
            f += d[self.owner.alignment['activity']]
            if f > 2:
                f = 2
            if f < 0:
                f = 0
            return Relations._fervor[f]
    @property
    def distance(self):
        if self.target.player_controlled:
            return Relations._distance[self._distance]
        else:
            f = 1
            d = {'chaotic': 1, 'lawful': -1, 'conformal':0}
            f += d[self.owner.alignment['orderliness']]
            f += d[self.owner.alignment['orderliness']]
            if f > 2:
                f = 2
            if f < 0:
                f = 0
            return Relations._distance[f]
    @property
    def congruence(self):
        if self.target.player_controlled:
            return Relations._congruence[self._congruence]
        else:
            f = 1
            d = {'good': 1, 'evil': -1, 'selfish':0}
            f += d[self.owner.alignment['morality']]
            f += d[self.owner.alignment['morality']]
            if f > 2:
                f = 2
            if f < 0:
                f = 0
            return Relations._congruence[f]
        
    def change(self, axis, direction):
        if not target.player_controlled:
            return
        ax = getattr(self, '_%s'%(axis))
        if direction == "+":
            ax += 1
            if ax > 2:
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
                ax = 2
        elif direction == '-':
            ax -= 1
            if ax < 0:
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
                ax = 0

    def description(self):
        return (self.fervor, self.distance, self.congruence)

