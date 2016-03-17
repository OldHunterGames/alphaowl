# -*- coding: UTF-8 -*-

skills_data = {
    'coding': 'concentration',
    'sports': 'stamina',
    'sex': 'glamour',
    'conversation': 'willpower',
}
attr_relations = {
            'stamina': 'physique',
            'concentration': 'mind',
            'willpower': 'spirit',
            'accuracy': 'agility',
            'glamour': 'sensitivity'
        }


class Skill(object):
    def __init__(self, owner, name, resource='willpower'):
        self.owner = owner
        self.name = name
        self.resource = resource
        self.attribute = attr_relations[resource]
        self.training = False
        self.expirience = False
        self.specialization = False
        self.talent = False
        self.expirience_slot = 0


    def level(self):
        level = 0
        if self.training:
            level += 1
        if self.expirience:
            level += 1
        if self.specialization:
            level += 1
        if self.talent:
            level += 1
        return level

    def get_expirience(self, power):
        if power > 5 or power < 1:
            return
        for skill in self.owner.skills:
            if skill.expirience_slot != power:
                self.expirience_slot = power
                self.expirience = True


