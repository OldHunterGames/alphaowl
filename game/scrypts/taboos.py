# -*- coding: UTF-8 -*-


taboos = ['submission', 'sexplotation', 'pain', 'disgrace', 'deprivation', 'abuse']
def init_taboos(owner):
    l = []
    for t in taboos:
        l.append(Taboo(t, owner))
    return l



class Taboo(object):
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self._value = 3
        self.max_counter = self.owner.spirit
        self.counter = self.max_counter

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self._value += value
        if self._value < 0:
            self._value = 0
        if self._value > 5:
            self._value = 5
    
    def use(self, power):
        if self.value == 0:
            return
        summ = self.value + power
        if summ == 6:
            self.value -= 1
        elif summ > 6:
            self.counter -= 1
            if self.counter == 0:
                if self.value < self.owner.spirit:
                    self.value += 1
                else:
                    self.value -= 1
                self.max_counter += 1
                self.counter = self.max_counter
                self.owner.tokens.append('angst')
        return
