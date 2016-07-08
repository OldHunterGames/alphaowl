# -*- coding: UTF-8 -*-
from copy import deepcopy


needs_names = ["general", 'purpose', "nutrition", "wellness", "comfort", "activity", "communication", "amusement",
             "prosperity", "authority", "ambition", "eros", "order", "independence", "approval", "trill", "altruism", "power"]

_default_need = {"level": 0}

def init_needs(owner):
    l = []
    for name in needs_names:
        l.append(Need(owner, name))
    return l

class Need(object):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self._level = _default_need['level']
        self._satisfaction = 0
        self.tension = False

    @property
    def satisfaction(self):
        return self._satisfaction
    
    @satisfaction.setter
    def satisfaction(self, value):
        levels = [0, self.owner.sensitivity, 5, 5]
        if value < 0:
            value = 0
        if value > levels[self.level]:
            value = levels[self.level]
        self._satisfaction = value
    
    def set_tension(self):
        self.tension = True


    @property
    def level(self):
        n = self.owner.alignment.special_needs()
        if self.name in n[0]:
            return 2
        elif self.name in n[1]:
            return 0
        return self._level


    def reset(self):
        self._satisfaction = 0
        self.tension = False