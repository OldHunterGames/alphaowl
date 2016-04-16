# -*- coding: UTF-8 -*-
from copy import deepcopy


needs_names = ["general", "nutrition", "wellness", "comfort", "activity", "communication", "amusement", "prosperity",
            "authority", "ambition", "debauch", "care", "order", "independence", "approval", "trill", "altruism", "power"]

_default_need = {"level": 3, "shift": 0, "status": "relevant"}

def init_needs(owner):
    l = []
    for name in needs_names:
        l.append(Need(owner, name))
    return l
class Need(object):
    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.level = _default_need['level']
        self.shift = _default_need['shift']
        self._status = _default_need['status']


    @property
    def status(self):
        s = self._status
        if self.level == 0:
            s = 'relevant'
        return s
    

    @status.setter
    def status(self, value):
        self._status = value
    

    def set_shift(self, value):
        n = value*self.shift
        if n < 0:
            self.shift += value
        elif abs(value) > abs(self.shift):
            self.shift = value

    def status_change(self):
            high_treshold = 8-self.owner.sensitivity-self.level
            if high_treshold < 1:
                high_treshold = 1
            low_treshold = (6-self.owner.sensitivity-self.level)*(-1)
            if low_treshold > -1:
                low_treshold = -1
            if self.status == 'frustrated':
                if self.owner.mood() > 0:
                    if self.shift > high_treshold:
                        self.status = 'relevant'
            elif self.status == 'overflow':
                if self.shift < low_treshold:
                    self.owner.determination -= 1
                    self.status = 'relevant'
            else:
                if self.shift > high_treshold:
                   self.status = 'satisfied'
                elif self.shift < low_treshold:
                    self.status = 'tense'
                else:
                    self.status = 'relevant'
            self.shift = 0

    def overflow(self):
        threshold = 8-self.owner.sensitivity-self.level
        l = ['frustrated', 'tense', 'relevant', 'satisfied', 'overflow']
        ind = l.index(self.status)
        if self.shift > threshold:
            if ind != 0:
                ind += 1
                if ind == 4:
                    if self.owner.mood() > 0:
                        owner.determination += 1
                    else:
                        ind -= 1
                self.status = l[ind]


