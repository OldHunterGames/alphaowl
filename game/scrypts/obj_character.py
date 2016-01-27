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
        self.master = None          # If this person is a slave, the master will be set
        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.ration = {
            "amount": 'unlimited',   # 'unlimited', 'limited' by price, 'regime' for figure, 'starvation' no food
            "food_type": "cosine",   # 'forage', 'sperm', 'dry', 'canned', 'cosine'
            "target": 0,           # figures range -2:2
            "limit": 0,             # maximum resources spend to feed character each turn
            "overfeed": 0,
        }
        self.accommodation = 'makeshift'
        self.job = {'name': 'idle', 'efficiency': 0,'skill': None, 'effort': "bad"} #effort can be "bad", "good", "will" or "full"
        self.skills = {
            "training":  {'coding': 'mind', 'communication': 'spirit', 'sex': 'sensitivity', 'sport': 'physique'},        # List of skills. Skills get +1 bonus
            "experience":  {},      # List of skills. Skills get +1 bonus
            "specialisation": {},   # List of skills. Skills get +1 bonus
            "talent": {},           # List of skills. Skills get +1 bonus
        }
        self.focused_skill = None
        self.focus = 0
        self.skills_used = []
        self.factors = []
        self.needs = {              # List of persons actual needs, with levels and statuses
            # Need {level(1-5), shift(-/+ N) status (relevant, satisfied, overflow, tense, frustrated)}
            "general":  {"level": 3, "shift": 0, "status": "relevant"},
            "nutrition":  {"level": 3, "shift": 0, "status": "relevant"},
            "wellness":  {"level": 3, "shift": 0, "status": "relevant"},
            "comfort":  {"level": 3, "shift": 0, "status": "relevant"},
            "activity":  {"level": 3, "shift": 0, "status": "relevant"},
            "communication":  {"level": 3, "shift": 0, "status": "relevant"},
            "amusement":  {"level": 3, "shift": 0, "status": "relevant"},
            "prosperity":  {"level": 3, "shift": 0, "status": "relevant"},
            "authority":  {"level": 3, "shift": 0, "status": "relevant"},
            "ambition":  {"level": 3, "shift": 0, "status": "relevant"},

        }
        self.taboo = {              # Persons moral code.
            "submission":  3,
            "sexplotation":  3,
            "pain":  3,
            "disgrace":  3,
            "deprivation":  3,
            "abuse":  3,
        }

        self.attributes = {
        'physique': 3,
        'mind': 3,
        'spirit': 3,
        'agility': 3,
        'sensitivity':3
        }
        self.university = {'name': 'study', 'effort': 'bad', 'auto': False}
        self.attr_relations = {
        'stamina': 'physique',
        'concentration': 'mind',
        'willpower': 'spirit',
        'accuracy': 'agility',
        'glamour': 'sensitivity'
        }
        
        self.inner_resources = {
        'stamina': self.physique,
        'accuracy': self.agility,
        'concentration': self.mind,
        'willpower': self.spirit,
        'glamour': self.sensitivity
        }

        self.appetite = 0
        self.calorie_storage = 0
        self.money = 0
        self.determination = 0

        # Other persons known and relations with them
        self.relations = {
            "Old friend": {                         # for example, actually a Person() object must be here
                "connection": "unrelated",            # unrelated, slave, subordinate, supervisor or master
                "consideration": "respectful",     # significant, respectful or miserable
                "distance": "close",                # intimate, close or distant
                "affection": "friend",              # friend, associate or foe
            }
        }

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
            value = self.inner_resources[key]
            value += features_lookup(self, key)
            if value <= 0:
                self.inner_resources[key] = 0
                value = 0
            max_value = getattr(self, self.attr_relations[key])
            if value > max_value:
                value = max_value
            return value
        else:
            raise AttributeError(key)

    
    def __setattr__(self, key, value):
        if 'inner_resources' in self.__dict__:
            if key in self.inner_resources:
                self.inner_resources[key] = value
                if self.inner_resources[key] < 0:
                    self.inner_resources[key] = 0
        super(Person, self).__setattr__(key, value)

    def skill_level(self, skillname):
        value = 0
        for key in self.skills.keys():
            if skillname in self.skills[key]:
                value += 1
        return value
    def skill_resource(self, skillname):
        res = None
        inverted = {v: k for k,v in self.attr_relations.items()}
        attr = self.skill_attribute(skillname)
        for key in self.skills.keys():
            if skillname in self.skills[key]:
                res = inverted[attr]
                break
        return res

    def skill_attribute(self, skillname):
        skill_attr = None
        for key in self.skills.keys():
            if skillname in self.skills[key]:
                skill_attr = self.skills[key][skillname]
                break
        return skill_attr
    

            
    def use_resource(self, resource):
        value = getattr(self, resource)
        newval = value - 1
        setattr(self, resource, newval)
        return value
    def use_skill(self, skill, resource=False, determination=False, sabotage=False):
        if sabotage:
            return 0
        skill_lvl = self.skill_level(skill)
        
        if skill_lvl <= 0:
            return 0 
        check = skill_lvl + self.mood() - 3
        res = self.use_resource(self.skill_resource(skill)) if resource else 0
        if determination and self.determination > 0:
            self.determination -= 1
            if res <= 0:
                check += getattr(self, self.skill_attribute(skill))
            else:
                check += 1
                check += res
                if skill == self.focused_skill:
                    if check<self.focus:
                        check = focus
        else:
            check += res
        if check < 0:
            check = 0
        if check > 0:
            self.skills_used.append(skill)
        return check
    
    def set_focus(self, skill):
        if not skill == self.focused_skill:
            self.focus = 0
            self.focused_skill = skill
        else:
            self.focused_skill = skill



    def calc_focus(self):
        if self.focused_skill in self.skills_used:
            self.focus += 1
        elif len(self.skills_used)>0:
            from collections import Counter
            counted = Counter()
            for s in self.skills_used:
                counted[s]+=1
            maximum = max(counted.values())
            result = []
            for skill in counted:
                if counted[skill] == maximum:
                    result.append(skill)
            self.set_focues(random.choice(result))
            self.focus += 1
        self.skills_used = []



    def mood(self):
        mood = 0
        for need in self.needs:
            if self.needs[need]["status"] == "tense":
                mood -= 1
            elif self.needs[need]["status"] == "frustrated":
                mood -= 1
            elif self.needs[need]["status"] == "satisfied":
                mood += 1

        if mood < 0:
            return -1
        elif mood > 0:
            return 1

        return 0
   

    def motivation(self, skill, need=None, shift=0, orderer=None, taboo=None):
        motiv = 0
        motiv += self.mood()
        if skill in self.skills['talent']:
            motiv += self.spirit
        if need:
            status = self.needs[need]['status']
            self.needs[need]['shift'] += shift
            if shift > 0:
                if status == 'frustrated' or status == 'tense':
                    motiv += self.needs[need]['level']
                elif status == 'overflow':
                    motiv -= 1
            if shift < 0:
                if status == 'frustrated' or status == 'tense': 
                    motiv -= self.needs[need]['level']
                elif status == 'relevant':
                    motiv -= 1
        if orderer:
            #self.calc_submission()
            pass
        if taboo:
            motiv += self.taboo[taboo]
        return motiv



    def calc_needs_factor(self): #better change nothing here...
        factors_dict = {}
        for i in self.factors:
            if i[1] in factors_dict.keys():
                factors_dict[i[1]].append(i[0])
            else:
                factors_dict[i[1]] = [i[0]]
        priority = {'stamina': 5, 'accuracy': 4, 'concentration': 3, 'willpower': 2, 'glamour': 1}
        needed = {}
        max_d = {}
        result = []
        for i in factors_dict.values():
            for n in i:
                result.append(n)
        for k in priority:
            needed[k] = getattr(self, self.attr_relations[k]) - self.inner_resources[k]
            max_d[k] = 0
        for i in max_d:
            for n in factors_dict.keys():
                if i in factros_dict[n]:
                    max_d[i] += 1
        for i in result:
            while not result.count(i) == needed[i]:
                result.remove(i)
        for i in result:
            if result.count(i) > max_d[i]:
                result.remove(i)
        rd = {k: v for v, k in priority.items()}
        revresult = []
        for i in result:
            revresult.append(priority[i])
        while len(revresult) != len(factors_dict.keys()):
            revresult.remove(min(revresult))
        result = []
        for i in revresult:
            result.append(rd[i])
        for i in result:
            self.inner_resources[i] += 1
        self.factors = []
    

    def add_factor(self, factor, level):
        self.factors.append((factor, level))



        
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


