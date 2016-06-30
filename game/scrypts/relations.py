# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy


class Relations(object):
    _fervor = {-1: "intense", 0: "plain", 1: "delicate"}
    _distance = {-1: "intimate", 0: "close", 1: "formal"}
    _congruence = {-1: "contradictor", 0: "associate", 1: "supporter"}
    def __init__(self, person1, person2):
        self.persons = [person1, person2]
        self._fervor = 1
        self._distance = 1
        self._congruence = 1
        self.is_player_relations()
            

    def is_player_relations(self):
        if self.persons[0].player_controlled or self.persons[1].player_controlled:
            if not hasattr(self, 'player') and not hasattr(self, 'npc'):
                for p in self.persons:
                    if p.player_controlled:
                        self.player = p
                    else:
                        self.npc = p
            return True
        else:
            return False

    @property
    def fervor(self):
        if self.is_player_relations():
            return self._fervor
        fervor = self._fervor + self.persons[0].alignment.activity + self.persons[1].alignment.activity
        if fervor < -1:
            fervor = -1
        elif fervor > 1:
            fervor = 1
        return fervor
    def show_fervor(self):
        return Relations._fervor[self.fervor]
    

    @property
    def distance(self):
        if self.is_player_relations():
            return self._distance
        distance = self._distance + self.persons[0].alignment.orderliness + self.persons[1].alignment.orderliness
        if distance < -1:
            distance = -1
        elif distance > 1:
            distance = 1
        return distance
    def show_distance(self):
        return Relations._distance[self.distance]
    

    @property
    def congruence(self):
        if self.is_player_relations():
            return self._congruence
        congruence = self._distance + self.persons[0].alignment.morality + self.persons[1].alignment.morality
        if congruence < -1:
            congruence = -1
        elif congruence > 1:
            congruence = 1
        return congruence
    def show_congruence(self):
        return Relations._congruence[self.congruence]

    
    def set_axis(self, axis, value):
        ax = '_%s'%(axis)
        if hasattr(self, ax) and value in range(-1, 1):
            self.__dict__[ax] = value

    def description(self):
        return (self.show_fervor(), self.show_distance(), self.show_congruence())
        
    def change(self, axis, direction):
        if not self.is_player_relations():
            return
        ax = getattr(self, '_%s'%(axis))
        if direction == "+":
            ax += 1
            if ax > 1:
                if axis == 'distance':
                    if self.npc.alignment.orderliness == 'chaotic':
                        self.npc.add_token('accordance')
                    elif self.npc.alignment.orderliness == 'lawful':
                        self.npc.add_token('antagonism')
                if axis == 'fervor':
                    if self.npc.alignment.activity == 'timid':
                        self.npc.add_token('accordance')
                    elif self.npc.alignment.activity == 'ardent':
                        self.npc.add_token('antagonism')
                if axis == 'congruence':
                    if self.npc.alignment.morality == 'good':
                        self.npc.add_token('accordance')
                    elif self.npc.alignment.morality  == 'evil':
                        self.npc.add_token('antagonism')
                ax = 2
        elif direction == '-':
            ax -= 1
            if ax < -1:
                if axis == 'distance':
                    if self.npc.alignment.orderliness == 'chaotic':
                        self.npc.add_token('antagonism')
                    elif self.npc.alignment.orderliness == 'lawful':
                        self.npc.add_token('accordance')
                if axis == 'fervor':
                    if self.npc.alignment.activity == 'timid':
                        self.npc.add_token('antagonism')
                    elif self.npc.alignment.activity == 'ardent':
                        self.npc.add_token('accordance')
                if axis == 'congruence':
                    if self.npc.alignment.morality == 'good':
                        self.npc.add_token('antagonism')
                    elif self.npc.alignment.morality == 'evil':
                        self.npc.add_token('accordance')
                ax = 0


