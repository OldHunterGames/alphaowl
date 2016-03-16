# -*- coding: UTF-8 -*-

skills_data = {
    'coding': 'concentration',
    'sports': 'physique',
    'sex': 'glamour',
    'conversation': 'willpower',
}


class Skill(object):
    def __init__(self, name, attribute='spirit'):
        self.name = name
        self.attribute = attribute
        self.training = False
        self.expirience = False
        self.specialisation = False
        self.talent = False


    def level(self):
        level = 0
        if self.training:
            level += 1
        if self.expirience:
            level += 1
        if self.specialisation:
            level += 1
        if self.talent:
            level += 1
        return level
