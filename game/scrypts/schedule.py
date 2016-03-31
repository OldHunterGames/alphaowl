# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
actions = {}
def register_action(name, lbl_name, atype=None):
    actions[name] = (lbl_name, atype)


class ScheduledAction(object):
    def __init__(self, owner, name, lbl, slot, target=None):
        self.owner = owner
        self.slot = slot
        self.name = name
        self.lbl = lbl
        self.target = target

    def call(self):
        if self.target:
            renpy.call_in_new_context(self.lbl, self.owner, self.target)
        else:
            renpy.call_in_new_context(self.lbl, self.owner)


class Schedule(object):
    def __init__(self, person):
        self.actions = []
        self.owner = person
        self.add_torture = self.add_action(self.owner.torture, 'torture')
    
    def add_action(self, action, target=None):
        if action in actions:
            act = ScheduledAction(self.owner, action, actions[action][0], actions[action][1], target)
            for a in self.actions:
                if a.slot == act.slot:
                    self.actions.remove(a)
            self.actions.append(act)
    def use_actions(self):
        for action in self.actions:
            action.call()


