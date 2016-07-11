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
        try:
            special = action[3]
        except IndexError:
            special = None
        if not special:
            actions[key] = [z, action[1], action[2]]


class ScheduledAction(object):
    def __init__(self, actor, name, lbl, slot, store_name, single=False, special_values={}):
        self.actor = actor
        self.slot = slot
        self.name = name
        self.store_name = store_name
        self.lbl = lbl
        self.single = single
        self.special_values = {}
        if special_values:
            for key in special_values:
                self.special_values[key] = special_values[key]

    def call(self):
        renpy.call_in_new_context(self.lbl, self)


    def call_on_remove(self):
        removal_label = self.lbl + '_' + 'remove'
        if renpy.has_label(removal_label):
            renpy.call_in_new_context(removal_label, self)


    def add_special_list_value(self, key, value):
        try:
            self.special_values[key].append(value)
        except KeyError:
            self.special_values[key] = [value]



class Schedule(object):
    def __init__(self, person):
        self.actions = []
        self.owner = person
    
    def add_action(self, action, single=True, special_values={}):
        if action in actions.keys():
            act = ScheduledAction(self.owner, actions[action][2], actions[action][0], actions[action][1], action, single, special_values)
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
            self.remove_by_handle(a)
    def remove_by_handle(self, action):
        action.call_on_remove()
        self.actions.remove(action)
    def remove_action(self, action):
        for a in self.actions:
            if a.store_name == action:
                self.remove_by_handle(a)
    def remove_by_slot(self, slot):
        for a in self.actions:
            if a.slot == slot:
                self.remove_by_handle(a)


    def find_by_slot(self, slot):
        for a in self.actions:
            if a.slot==slot:
                return a


    def find_by_name(self, name):
        for a in self.actions:
            if a.store_name == name:
                return a


    




