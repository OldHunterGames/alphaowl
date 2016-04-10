# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
actions = {}
def register_actions():
    lbl_list = renpy.get_all_labels()
    l = []
    for label in lbl_list:
        lb = label.split('_')
        if lb[0] == 'shd':
            l.append(lb)
    for action in l:
        z = '_'
        z = z.join(action)
        actions[action[2]] = (z, action[1])


class ScheduledAction(object):
    def __init__(self, owner, name, lbl, slot, target=None, use_once=False):
        self.owner = owner
        self.slot = slot
        self.name = name
        self.lbl = lbl
        self.target = target
        self.use_once = use_once

    def call(self):
        if self.target:
            renpy.call_in_new_context(self.lbl, self.owner, self.target)
        else:
            renpy.call_in_new_context(self.lbl, self.owner)
        return


class Schedule(object):
    def __init__(self, person):
        self.actions = []
        self.owner = person
    
    def add_action(self, action, target=None, use_once=False):
        if action in actions.keys():
            act = ScheduledAction(self.owner, action, actions[action][0], actions[action][1], target, use_once)
            if act.slot != None:
                for a in self.actions:
                    if a.slot == act.slot:
                        self.actions.remove(a)
            if act in self.actions:
                return
            self.actions.append(act)
    def use_actions(self):
        for action in self.actions:
            action.call()
            if action.use_once:
                self.actions.remove(action)
    def remove_action(self, action, target=None):
        if target:
            for a in self.actions:
                if a.name == action and a.target == target:
                    self.actions.remove(a)
        else:
            for a in self.actions:
                if a.name == action:
                    self.actions.remove(a)



