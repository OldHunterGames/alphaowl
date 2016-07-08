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
        key = '{slot}_{name}'.format(slot=action[1], name=action[2])
        z = '_'
        z = z.join(action)
        actions[key] = (z, action[1])


class ScheduledAction(object):
    def __init__(self, owner, name, lbl, slot, single=False, special_values={}):
        self.owner = owner
        self.slot = slot
        self.name = name
        self.lbl = lbl
        self.single = single
        self.special_values = special_values

    def call(self):
        renpy.call_in_new_context(self.lbl, self)



class Schedule(object):
    def __init__(self, person):
        self.actions = []
        self.owner = person
    
    def add_action(self, action, single=False, special_values={}):
        if action in actions.keys():
            act = ScheduledAction(self.owner, action, actions[action][0], actions[action][1], single, special_values)
            if act.slot != None:
                for a in self.actions:
                    if a.slot == act.slot:
                        self.actions.remove(a)
            if act in self.actions:
                return
            self.actions.append(act)
    def use_actions(self):
        to_remove = []
        for action in self.actions:
            action.call()
            if action.single:
                to_remove.append(action)
        for a in to_remove:
            self.actions.remove(a)
    def remove_action(self, action):
        for a in self.actions:
            if a.name == action:
                self.actions.remove(a)
    def remove_by_slot(self, slot):
        for a in self.actions:
            if a.slot == slot:
                self.actions.remove(a)


    def find_by_slot(self, slot):
        for a in self.actions:
            if a.slot==slot:
                return a


    def find_by_name(self, name):
        for a in self.actions:
            if a.name == name:
                return a




