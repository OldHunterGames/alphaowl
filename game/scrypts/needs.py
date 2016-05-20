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
        self._negatives_storage = []
        self.cumulation = 0


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
        if self.level == 0:
            return
        if abs(value) > abs(self.shift):
            self.shift = value
        elif value < 0:
            self._negatives_storage.append(value)

    def threshold(self):
        val = 5-self.intensity()
        if val < 0:
            return 0
        return val
    def intensity(self):
        if self.level == 0:
            return 0
        if self.level == 1:
            return 1
        if self.level == 2:
            i = 0
            if self.status == 'tense':
                i = 1
            elif self.status == 'satisfied' or self.status == 'overflow':
                i = -1
            i += self.owner.sensitivity
            if i < 1:
                i = 1
            return i
        if self.level == 3:
            return 6
        if self.level == 4:
            return 6
    def status_change(self):
        if self.level == 0:
            return
        shift = None
        for val in self._negatives_storage:
            self.shift -= 1
        if self.shift < -5:
            self.shift = -5
        self._negatives_storage = []
        if self.threshold() < abs(self.shift):
            if self.shift < 0:
                shift = '-'
            elif self.shift > 0:
                shift = '+'
        l = ['tense', 'relevant', 'satisfied', 'overflow']
        ind = l.index(self.status)
        if ind == 0:
            ind += 1
        if ind == 3:
            if shift == '-':
                self.owner.determination -= 1
                ind = 1
                self.status = l[ind]
                self.shift = 0
                return
        if self.level == 4:
            if ind == 1:
                ind = 0
        else:
            if ind == 0:
                ind += 1
            elif ind == 2:
                ind -= 1
        if shift == '+':
                ind += 1
        elif shift == '-':
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



