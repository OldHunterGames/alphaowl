# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

class Schedule(object):
    def __init__(self, person):
        self.actions = {}
        self.owner = person
        self.add_torture = self.add_action(self.owner.torture, 'torture')
    
    def add_action(self, action, a_type=None, *args, **kwargs):
        def set_args(*args, **kwargs):
            l = [action, {}]
            for k, v in kwargs.items():
                if k != self:
                    l[1][k] = v
            if a_type:
                self.actions[a_type] = l
            else:
                if 'other' in self.actions:
                    self.actions['other'].append(l)
                else:
                    self.actions['other'] = [l]
            
        return set_args

    def use_actions(self):
        if not self.actions:
            return
        for l in self.actions:
            if l != 'other':
                action = self.actions[l]
                action[0](**action[1])
            else:
                for i in self.actions[l]:
                    action = i
                    action[0](**action[1])
    


