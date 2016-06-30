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
        v = self._value
        for mod in self.owner.modifiers:
            for k in mod:
                if k == self.name:
                    v *= (-1)
                    break
        return v
    
    def use(self, power):
        if self._value == 0:
            return
        mod = -1 if self.value > 0 else 1
        summ = self._value + power
        if summ == 6:
            if self.value > 0:
                self._value += mod
        elif summ > 6:
            if mod < 0:
                return
            self.counter -= 1
            if self.counter == 0:
                if self.value < self.owner.spirit:
                    self._value += mod
                else:
                    self._value -= mod
                self.max_counter += 1
                self.counter = self.max_counter
                self.owner.tokens.append('angst')
        return


