# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *

class Engine(object):

    def __init__(self):
        self.player = Person()
        self.time = 1
        self.tenge = 100
        self.mom_stuff = []
        self.events_list = []

   
    def new_turn(self):
        self.time += 1
        return "label_new_day"
    

    def possible_events(self, kind, who = None):
        """
        :param kind:
        "turn" - end-of-turn event
        "char" - event with one of player faction main characters
        "faction" - event for one of active factions beside player faction
        :return: the RenPu location with the choosen event
        """
        list_of_events = []
        for event in self.event_list:
            if event.check():
                if kind in event.natures:
                        list_of_events.append(event)

        return list_of_events
    

    def end_turn_event(self):
        return choice(self.possible_events("turn_end")).trigger()
    

    def job_sex(self, person):
    	skill = 'sex'
    	efficiency = 20
    	return person.use_skill(skill)

