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

    def new_turn(self):
        self.time += 1
        return "label_new_day"

    def job_sex(self, person):
    	skill = 'sex'
    	efficiency = 20
    	return person.use_skill(skill)
