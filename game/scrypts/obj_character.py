# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
import features_data
from copy import deepcopy
from food import *


def features_lookup(person, stat):
    if not isinstance(person, Person):
        raise "No features outside person"
    value = 0
    for f in person.features:
        if stat in f.modifiers.keys():
            value = f.modifiers[stat]
    return value


class Person(object):

    def __init__(self):
        self.firstname = u"Антон"
        self.surname = u"Сычов"
        self.nickname = u"Сычуля"
        self.gender = "male"
        self.age = "junior"
        self.alignment = {
            "Orderliness": "Conformal",   # "Lawful", "Conformal" or "Chaotic"
            "Activity": "Reasonable",        # "Ardent", "Reasonable" or "Timid"
            "Morality": "Selfish",       # "Good", "Selfish" or "Evil"
        }
        self.features = []          # gets Feature() objects and their child's. Add new Feature only with self.add_feature()
        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.ration = {
            "amount": 'unlimited',   # 'unlimited', 'limited' by price, 'regime' for figure, 'starvation' no food
            "food_type": "cosine",   # 'forage', 'sperm', 'dry', 'canned', 'cosine'
            "target": 0,           # figures range -2:2
            "limit": 0,             # maximum resources spend to feed character each turn
            "overfeed": 0,
        }
        self.accommodation = 'makeshift'
        self.job = 'idle'
        self.skills = {
            "training":  [],        # List of skills. Skills get +1 bonus
            "experience":  [],      # List of skills. Skills get +1 bonus
            "specialisation": [],   # List of skills. Skills get +1 bonus
            "talent": [],           # List of skills. Skills get +1 bonus
        }
        self.needs = {              # List of persons needs
            "general":  3,        # Need {level(1-5), status (relevant, satisfied, overflow, tension, frustration)}
            "nutrition":  3,
            "wellness":  3,
            "comfort":  3,
            "activity":  3,
            "communication":  3,
            "amusement":  3,
            "prosperity":  3,
            "authority":  3,
            "ambition":  3,

        }

        self.attributes = {
        'physique': 3,
        'mind': 3,
        'spirit': 3,
        'agility': 3,
        'sensitivity':3
        }

        self.inner_resources = {
        'max_stamina': self.physique,
        'max_acuracy': self.agility,
        'max_concentration': self.mind,
        'max_willpower': self.spirit,
        'max_glamour': self.sensitivity
        }

        self.inner_resources['stamina'] = self.max_stamina
        self.inner_resources['acuracy'] = self.max_acuracy
        self.inner_resources['concentration'] = self.max_concentration
        self.inner_resources['willpower'] = self.max_willpower
        self.inner_resources['glamour'] = self.max_glamour
        self.appetite = 0
        self.calorie_storage = 0
        self.mood = 0       # Hidden mood-meter 0 is normal, - bad, + good

    def __getattr__(self, key):
        if key in self.attributes:
            value = self.attributes[key]
            value += features_lookup(self, key)
            if value < 1:
                value = 1
            if value > 5:
                value = 5
            return value
        if key in self.needs:
            value = self.needs[key]
            value += features_lookup(self, key)
            if value < 1:
                value = 1
            if value > 5:
                value = 5
            return value
        if key in self.inner_resources:
            value = self.__dict__['inner_resources'][key]
            value += features_lookup(self, key)
            if value < 0:
                value = 0
            return value
        else:
            raise AttributeError

    def add_feature(self, name):    # adds features to person, if mutually exclusive removes old feature
        new_feature = deepcopy(features_data.person_features[name])
        for f in self.features:
            if f.name == name:
                return
            if new_feature.slot and new_feature.slot == f.slot:
                self.features.remove(f)
        self.features.append(new_feature)
    
    def feature_by_slot(self, slot):        # finds feature which hold needed slot
        for f in self.features:
            if f.slot == slot:
                return f
    def feature(self, name):                # finds feature with needed name if exist
        for f in self.features:
            if f.name == name:
                return f
        return None
    def remove_feature(self, feature):       # feature='str' or Fearutere()
        if isinstance(feature, str):
            r = self.feature(feature)
            self.features.remove(r)
            return
        else:
            self.features.remove(feature)
            return
    def description(self):
        txt = self.firstname + ' "' + self.nickname + '" ' + self.surname
        txt += '\n'
        for feature in self.features:
            txt += feature.name
            txt += ','

        return txt
    
    def rest(self):
        self.fatness_change()

    def use_resource(self, resource, value=1, difficulty=0):    # method for using our inner resources for some actions
        """
        :return: True if we are able to do action
        """
        res_to_use = self.__getattr__(resource)
        if res_to_use < difficulty:
            return False
        if not res_to_use - value < 0:
            self.__dict__['inner_resources'][resource] -= value
            return True
        return False

    def food_demand(self):
        """
        Evaluate optimal food consumption to maintain current weight.
        :return:
        """
        demand = self.physique
        demand += self.appetite
        demand += features_lookup(self, 'food_demand')

        if demand < 1:
            demand = 1

        return demand

    def food_desire(self):
        """
        Evaluate ammount of food character likes to consume.
        :return:
        """
        desire = self.food_demand()
        nutrition_modifier = self.nutrition
        desire += nutrition_modifier - 3
        desire += features_lookup(self, "food_desire")

        if desire < 1:
            desire = 1

        return desire

    def consume_food(self):
        food_consumed = self.food_desire()
        fatness = self.feature_by_slot('shape')
        if fatness:
            fatness = fatness.value
        else:
            fatness = 0
        if self.ration['amount'] == 'starvation':
            food_consumed = 0

        if self.ration['amount'] == 'limited':
            if food_consumed > self.ration["limit"]:
                food_consumed = self.ration["limit"]

        if self.ration['amount'] == 'regime':
            food_consumed = self.food_demand()
            if self.ration['target'] > fatness:
                food_consumed += 1+self.appetite
            if self.ration['target'] < fatness:
                food_consumed -= 1
        return food_consumed

    def fatness_change(self):
        calorie_difference = self.consume_food() - self.food_demand()
        self.calorie_storage += calorie_difference
        fatness = self.feature_by_slot('shape')
        if fatness:
            fatness = fatness.value
        else:
            fatness = 0
        if self.calorie_storage < 0:
            chance = randint(-10, -1)
            if self.calorie_storage <= chance:
                if self.feature('starving'):
                    self.add_feature('dead')
                else:
                    fatness -= 1
                    self.calorie_storage = 0
                    if fatness == 0:
                        self.remove_feature(self.feature_by_slot('shape'))
                    if self.feature('dyspnoea'):
                        self.remove_feature('dyspnoea')
                    if fatness >= -2:
                        for f in features_data.person_features.values():
                            if f.slot == 'shape' and f.value == fatness:
                                self.add_feature(f.name)
                    else:
                        self.add_feature('starving')
        if self.calorie_storage > 0:
            chance = randint(1, 10)
            if self.calorie_storage >= chance:
                fatness += 1
                self.calorie_storage = 0
                if fatness == 0:
                        self.remove_feature(self.feature_by_slot('shape'))
                if fatness <= 2:
                    if self.feature('starving'):
                        self.remove_feature('starving')
                    for f in features_data.person_features.values():
                        if f.slot == 'shape' and f.value == fatness:
                            self.add_feature(f.name)
                else:
                    if not self.feature("dyspnoea"):
                        self.add_feature('dyspnoea')
                    else:
                        self.add_feature('diabetes')





    def nutrition_change(self, food_consumed):
        if food_consumed < self.food_demand():
            self.ration["overfeed"] -= 1
            chance = randint(-10, -1)
            if self.ration["overfeed"] <= chance:
                self.ration["overfeed"] = 0


        return


