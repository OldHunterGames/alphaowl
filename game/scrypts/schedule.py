# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

persons_schedules = {}
class Schedule(object):
	def __init__(self, person):
		self.actions = {}
		persons_schedules[person] = self
	def add_action(self, func, action_type=None, *args, **kwargs):
		l = [func, {}]
		for k, v in kwargs.items():
			l[1][k] = v
		if action_type:
		    self.actions[action_type] = l
		else:
			if 'other' in self.actions:
			    self.actions['other'].append(l)
			else:
				self.actions['other'] = [l]

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


