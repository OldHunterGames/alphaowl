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

    @property
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

    def make_talanted(self):
        self.talent = True

    def get_expirience(self, power):
        available_slots = [n for n in range(power, 0, -1)]
        for skill in self.owner.skills:
            if skill.expirience_slot in available_slots:
                available_slots.remove(skill.expirience_slot)
        if len(available_slots) > 0:
            self.expirience_slot = max(available_slots)
            self.expirience = True
        expirienced = {skill.expirience_slot: skill for skill in self.owner.skills if skill.expirience_slot != 0}
        if len(expirienced.keys()) > 1:
            max_skill = expirienced[max(expirienced.keys())]
            ind = self.owner.skills.index(max_skill)
            self.owner.skills[ind].specialization = True
            self.owner.specialized_skill = max_skill




