# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy

class Person(object):

    def __init__(self):
        self.firstname = "Антон"
        self.surname = "Сычов"
        self.nickname = "Сычуля"
        self.gender = "male"
        self.age = "junior"
        self.alignment = {
            "Orderliness": "Conformal",   # "Lawful", "Conformal" or "Chaotic"
            "Activity": "Reasonable",        # "Ardent", "Reasonable" or "Timid"
            "Morality": "Selfish",       # "Good", "Selfish" or "Evil"
        }
        self.features = ["healthy_weight"]          # gets Feature() objects and their child's
        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.skills = {
            "training":  [],        # List of skills. Skills get +1 bonus
            "experience":  [],      # List of skills. Skills get +1 bonus
            "specialisation": [],   # List of skills. Skills get +1 bonus
            "talent": [],           # List of skills. Skills get +1 bonus
        }
        self.needs = {              # List of persons needs
            "general":  {"level": 3, "status": "relevant"},        # Need {level(1-5), status (relevant, satisfied, overflow, tension, frustration)}
            "nutrition":  {"level": 3, "status": "relevant"},
            "wellness":  {"level": 3, "status": "relevant"},
            "comfort":  {"level": 3, "status": "relevant"},
            "activity":  {"level": 3, "status": "relevant"},
            "communication":  {"level": 3, "status": "relevant"},
            "amusement":  {"level": 3, "status": "relevant"},
            "prosperity":  {"level": 3, "status": "relevant"},
            "authority":  {"level": 3, "status": "relevant"},
            "ambition":  {"level": 3, "status": "relevant"},

        }
        self.appetite = 0

    def description(self):
        txt = self.firstname + ' "' + self.nickname + '" ' + self.surname
        txt += '\n'
        for feature in self.features:
            txt += feature
            txt += ','

        return txt

    def food_demand(self):
        """
        Evaluate optimal food consumption to maintain current weight.
        :return:
        """
        demand = self.attribute("phy")
        demand += self.appetite
        if "starving" in self.features:
            demand += 1

        if demand < 1:
            demand = 1

        return demand

    def food_desire(self):
        """
        Evaluate ammount of food character likes to consume.
        :return:
        """
        desire = self.food_demand()
        nutrition_modifier = 3
        if "nutrition" in self.needs:
            nutrition_modifier = self.needs["nutrition"]["level"]
        desire += nutrition_modifier - 3

        if "chubby" in self.features:
            desire -= 1
        if "obese" in self.features:
            desire -= 1
        if "slim" in self.features:
            desire += 1
        if "emaciated" in self.features:
            desire += 2

        if desire < 1:
            desire = 1

        return desire

    def attribute(self, attribute):
        """
        Evaluates base attribute value of person based on features, age, gender, etc.
        :param attribute: physique, agility, spirit, mind, sensitivity.
        :return: attribute value average is 3, no less than 1
        """
        value = 3
        if self.age == "junior":
            value -= 1
        if attribute == "physique" or attribute == "phy":
            if self.age == "mature":
                value += 1
            if self.gender == "male":
                value += 1
            elif self.gender == "female":
                value -= 1

        if attribute == "sensitivity" or attribute == "sns":
            if self.age == "junior":
                value += 2
            if self.gender == "male":
                value -= 1
            elif self.gender == "female":
                value += 1

        if attribute == "agility" or attribute == "agi":
            if self.age == "junior":
                value += 1              # to be equally as high as mature and adolescent
            elif self.age == "elder":
                value -= 1

        if attribute == "mind" or attribute == "mnd":
            if self.age == "elder":
                value += 1

        for feature in self.features:
            if feature.name == "blood":
                for key in feature.modifiers:
                    if attribute == key:
                        value += feature.modifiers[key]

        if value < 1:
            value = 1
        return value

