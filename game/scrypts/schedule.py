# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
actions = {}
def register_action(name, lbl_name, atype=None):
    actions[name] = (lbl_name, atype)

class Schedule(object):
    def __init__(self, person):
        self.actions = {}
        self.owner = person
        self.add_torture = self.add_action(self.owner.torture, 'torture')
    
    def add_action(self, action, target=None):
        if action in actions:
            act = actions[action]
            for a in self.actions.keys():
                if self.actions[a]['type'] == act[1]:
                    self.actions.__delitem__(a)
            self.actions[action] = {}
            self.actions[action]['lbl'] = act[0]
            self.actions[action]['type'] = act[1]
            self.actions[action]['target'] = target
    def use_actions(self):
        for action in self.actions:
            a = self.actions[action]
            if a['target']:
                renpy.call_in_new_context(a['lbl'], character=self.owner, target=a['target'])
            else:
                renpy.call_in_new_context(a['lbl'], character=self.owner)


