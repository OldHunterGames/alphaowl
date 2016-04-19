# -*- coding: UTF-8 -*-
from copy import deepcopy


needs_names = ["general", 'purpose', "nutrition", "wellness", "comfort", "activity", "communication", "amusement",
             "prosperity", "authority", "ambition", "eros", "order", "independence", "approval", "trill", "altruism", "power"]

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
        if self.level == 0:
            return
        high_treshold = 8-self.owner.sensitivity-self.level
        if high_treshold < 1:
            high_treshold = 1
        low_treshold = (6-self.owner.sensitivity-self.level)*(-1)
        if low_treshold > -1:
            low_treshold = -1
        l = ['tense', 'relevant', 'satisfied', 'overflow']
        ind = l.index(self.status)
        if ind == 0:
            ind += 1
        if ind == 3:
            if self.shift < low_treshold:
                self.owner.determination -= 1
                ind = 1
                self.status = l[ind]
                self.shift = 0
                return
        if self.level == 5:
            if ind == 1:
                ind = 0
        else:
            if ind == 0:
                ind += 1
            elif ind == 2:
                ind -= 1
        if self.shift > high_treshold:
                ind += 1
        elif self.shift < low_treshold:
                ind -= 1
        if ind > 2:
            ind = 2
        if ind < 0:
            ind = 0
        self.shift = 0
        self.status = l[ind]
        return

    def overflow(self):
        if self.level == 0:
            return
        threshold = 8-self.owner.sensitivity-self.level
        l = ['tense', 'relevant', 'satisfied', 'overflow']
        ind = l.index(self.status)
        if self.shift > threshold:
            ind += 1
            if ind == 3:
                if self.owner.mood() > 0:
                    owner.determination += 1
                else:
                    ind -= 1
            self.status = l[ind]

    def increase(self):
        l = ['tense', 'relevant', 'satisfied', 'overflow']
        ind = l.index(self.status)
        ind += 1
        if ind > 2:
            ind = 2
        self.status = l[ind]
        return

    def reduce(self):
        l = ['tense', 'relevant', 'satisfied', 'overflow']
        ind = l.index(self.status)
        ind -= 1
        if ind < 0:
            ind = 0
        self.status = l[ind]
        return



