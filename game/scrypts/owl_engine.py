# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from obj_character import *

class Engine(object):

    def __init__(self):
        self.mother = Person()
        self.child = Person()
        self.player = None
        self.time = 1
        self.tenge = 100
        self.mom_stuff = []
        self.events_list = []
        self.mode = 'son'
        self.studies = [
            'major',
            'military',
            'gym',
            'labs',
            'practice',
        ]

    def choose_study(self):
        if self.studies:
            study = choice(self.studies)
        else:
            study = False

        return study

    def new_turn(self):
        self.time += 1
        self.player.ap = 1
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
        for event in self.events_list:
            if event.check():
                if kind in event.natures:
                        list_of_events.append(event)

        return list_of_events
    
    def end_turn_event(self):
        possible = self.possible_events('turn_end')
        if len(possible) > 0:
            choice(possible).trigger()
            return
        else:
            return

    def job_sex(self, person):
        skill = 'sex'
        efficiency = 20
        resource = True
        quality = person.use_skill(skill, resource)
        self.tenge += efficiency*quality

