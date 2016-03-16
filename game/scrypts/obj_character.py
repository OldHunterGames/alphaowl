# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
import features_data
from skills import Skill
from copy import copy
from copy import deepcopy
from food import *
from schedule import *

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
        self.player_controlled = False
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
        self.tokens = []             # Special resources to activate various events
        self.master = None          # If this person is a slave, the master will be set
        self.slave_stance = 'rebellious'     # rebellious, forced, accustomed or willing
        self.supervisor = None
        self.slaves = []
        self.subordinates = []
        self.ap = 1
        self.schedule = Schedule(self)

        # Slave stats, for obedience:
        self.dread = 0
        self.discipline = 0
        self.dependence = 0

        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.ration = {
            "amount": 'unlimited',   # 'unlimited', 'limited' by price, 'regime' for figure, 'starvation' no food
            "food_type": "cosine",   # 'forage', 'sperm', 'dry', 'canned', 'cosine'
            "target": 0,           # figures range -2:2
            "limit": 0,             # maximum resources spend to feed character each turn
            "overfeed": 0,
        }
        self.accommodation = 'makeshift'
        self.job = {'name': 'idle', 'efficiency': 0,'skill': None, 'effort': "bad"}     #effort can be "bad", "good", "will" or "full"
        self.skills = []
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
        self._determination = 0
        self.rewards = []
        self.used_rewards = []

        # Other persons known and relations with them, value[1] = [needed points, current points]
        self.relations = {
            "Old friend": {                                   # for example, actually a Person() object must be here
                "connection": "unrelated",                    # unrelated, slave, subordinate, supervisor or master
                "consideration": ["respectful", [0, 0]],      # significant, respectful or miserable
                "distance": ["close", [0, 0]],                # intimate, close or distant
                "affection": ["friend", [0, 0]],              # friend, associate or foe
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

    @property
    def determination(self):
        return self._determination
    @determination.setter
    def determination(self, value):
        self._determination = value
        if self._determination < 0:
            self._determination = 0

    def ddd_mod(self, d):
        modifier = d + self.dread + self.discipline + self.dependence - 3
        if modifier < 0:
            modifier = 0
        return modifier

    def pain_effect_threshold(self, taboo):
        threshold = 3 + self.attributes["spirit"] + self.ddd_mod(self.dread) - self.attributes["sensitivity"] - self.taboo[taboo]
        return threshold

    def pain_tear_threshold(self, taboo):
        threshold = 7 + self.attributes["spirit"] + - self.attributes["sensitivity"] - self.taboo[taboo]
        return threshold

    def torture(self, power=0, taboos=[], target=None):#should use at least one taboo
        _taboos = copy(taboos)
        taboo = _taboos.pop(0)
        for i in _taboos:
            if target.taboo[taboo] < target.taboo[i]:
                taboo = i
        effect = target.pain_effect_threshold(taboo)
        tear = target.pain_tear_threshold(taboo)
        tokens = []
        if power > tear:
            tokens.append('angst')
            tokens.append('fear')
        elif power > effect:
            tokens.append('fear')
        if len(tokens) < 1:
            return
        if not target.player_controlled:
            if power - effect < target.willpower and target.willpower != 0:
                 res = target.use_resource('willpower')
                 if res > 0:
                    tokens.remove('fear')
            else:
                if target.determination > 0:
                    target.determination -= 1
                    tokens.remove('fear')
            for i in tokens:
                target.tokens.append(i)

        else:
            for i in tokens:
                decision = renpy.call_in_new_context('lbl_resist', i)
                if decision=='willpower':
                    res = target.use_resource('willpower')
                    if res > 0:
                        res = True
                    else:
                        res = False
                        target.tokens.append(i) 
                    renpy.call_in_new_context('lbl_resist_result', i, res)  
                elif decision == 'determination':
                    if target.determination > 0:
                        target.determination -= 1
                        res = True
                    else:
                        res = False
                    renpy.call_in_new_context('lbl_resist_result', i, res)
                else:
                    target.tokens.append(i)
                    res = False
                    renpy.call_in_new_context('lbl_notify', i)
        return

    def get_skill(self, skillname):
        skill = None
        for i in self.skills:
            if i.name == skillname:
                skill = i
        if skill:
            return skill
        else:
            raise "%s has no %s"%(self.description(), skillname)

    def skill_resource(self, skillname):
        res = None
        inverted = {v: k for k,v in self.attr_relations.items()}
        attr = self.get_skill(skillname).attribute
        res = inverted[attr]
        return res


    def use_resource(self, resource):
        value = getattr(self, resource)
        self.inner_resources[resource] -= 1
        return value

    def use_skill(self, skill, forced = False, need=None, shift='positive', taboo=None):
        resource = False
        determination = False
        sabotage = False
        res_to_use = self.skill_resource(skill)
        check = 0
        if self.player_controlled:
            resource, determination, sabotage = renpy.call_in_new_context('lbl_skill_check', self, skill, self.skill_resource(skill))
        else:
            if forced:
                motivation = self.motivation(skill, need, shift, forced, taboo)
                if motivation < 0:
                    sabotage = True
                if motivation > 0 and motivation < 5-getattr(self, res_to_use):
                    pass
                if motivation > 0 and motivation > 5-getattr(self, res_to_use):
                    resource = True
                if motivation > 5 and res_to_use < 1:
                    resource = False
                    determination = True
                if motivation > 10:
                    resource = True
                    determination = True
        if sabotage:
            if self.player_controlled:
                renpy.call_in_new_context('lbl_skill_check_result', skill, check)
            return check
        skill_lvl = self.skill_level(skill)
        
        if skill_lvl <= 0:
            if self.player_controlled:
                renpy.call_in_new_context('lbl_skill_check_result', skill, check)
            return check
        check = skill_lvl + self.mood() - 3
        res = self.use_resource(res_to_use) if resource else 0
        if determination and self.determination > 0:
            self.determination -= 1
            if res <= 0:
                check += getattr(self, self.get_skill(skill).attribute)
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
        if self.player_controlled:
            renpy.call_in_new_context('lbl_skill_check_result', skill, check)
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
        elif len(self.skills_used) > 0:
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

        if mood < (-self.determination-self.sensitivity):
            return -1
        elif mood > self.sensitivity:
            return 1

        return 0
    
    def obedience(self):
        obedience = 0

        if self.alignment["Orderliness"] == "Lawful":
            obedience += self.discipline*2
        elif self.alignment["Orderliness"] == "Chaotic":
            obedience += self.discipline/2
        else:
            obedience += self.discipline

        if self.alignment["Activity"] == "Timid":
            obedience += self.dependence*2
        elif self.alignment["Activity"] == "Ardent":
            obedience += self.dependence/2
        else:
            obedience += self.dependence

        if self.alignment["Morality"] == "Evil":
            obedience += self.dread*2
        elif self.alignment["Morality"] == "Good":
            obedience += self.dread/2
        else:
            obedience += self.dread

        return obedience
    

    def set_shift(self, need, value):
        self.needs[need]['shift'] += value
    
    def reduce_overflow(self):
        max_level = 5
        needs_list = []
        for need in self.needs:
            if self.needs[need]['status'] == 'overflow':
                needs_list.append(need)
        if self.determination > len(needs_list):
            return
        needs_list = []
        while True:
            for need in self.needs:
                if self.needs[need]['level'] == max_level and self.needs[need]['status'] == 'overflow':
                    needs_list.append(need)
            if len(needs_list) > 0:
                n = choice(needs_list)
                self.needs[n]['status'] = 'relevant'
                return
            max_level -= 1
            if max_level < 1:
                return

    def calc_needs_change(self):
        for need in self.needs:
            shift = self.needs[need]['shift']
            level = self.needs[need]['level']
            status = self.needs[need]['status']
            high_treshold = 9-self.sensitivity-level
            if high_treshold < 1:
                high_treshold = 1
            low_treshold = (6-self.sensitivity-level)*(-1)
            if low_treshold > -1:
                low_treshold = -1
            if status == 'frustrated':
                if self.mood() > 0:
                    if shift > high_treshold:
                        self.needs[need]['status'] = 'relevant'
            elif status == 'overflow':
                if shift < low_treshold:
                    self.determination -= 1
                    self.needs[need]['status'] = 'relevant'
            else:
                if shift > high_treshold:
                   self.needs[need]['status'] = 'satisfied'
                elif shift < low_treshold:
                    self.needs[need]['status'] = 'tense'
                else:
                    self.needs[need]['status'] = 'relevant'
            self.needs[need]['shift'] = 0

    def motivation(self, skill, need=None, shift='positive',  forced=True, taboo=None):#shift = 'negative' or 'postive'
        motiv = 0
        motiv += self.mood()
        if skill in self.skills['talent']:
            motiv += self.spirit
        if need:
            status = self.needs[need]['status']
            if shift == 'negative':
                if status == 'frustrated' or status == 'tense':
                    motiv -= self.needs[need]['level']
                elif status == 'overflow':
                    motiv -= 1
            if shift == 'positive':
                if status == 'frustrated' or status == 'tense': 
                    motiv += self.needs[need]['level']
                elif status == 'relevant':
                    motiv -= 1
        if taboo:
            motiv += self.taboo[taboo]
        if forced:
            if self.slave_stance == 'rebellious':
                if motiv > -1:
                    motiv = -1
            if self.slave_stance == 'forced':
                if motiv < 0:
                    motiv += self.obedience()
                if motiv > 0:
                    motiv = 0
            if self.slave_stance == 'accustomed':
                if motiv < 0:
                    motiv += self.obedience()
            if self.slave_stance == 'willing':
                motiv += self.obedience()
        
        return motiv

    def calc_resources_factor(self): #method for choosing best setup of factors
        factors_dict = {}
        for i in self.factors: #sets person's factors in dict format
            if i[1] in factors_dict.keys():
                if i[0] not in factors_dict[i[1]]:
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
        for k in priority: #looks up for amount of needed resources
            needed[k] = getattr(self, self.attr_relations[k]) - self.inner_resources[k]
            max_d[k] = 0
        for i in max_d: #maximum of a single factor available
            for n in factors_dict.keys():
                if i in factors_dict[n]:
                    max_d[i] += 1
        for i in result: #sets optimal amount of factors in result
            while not result.count(i) == needed[i]:
                result.remove(i)
        for i in result:
            if result.count(i) > max_d[i]:
                result.remove(i)
        rd = {k: v for v, k in priority.items()}
        revresult = []
        m = len(factors_dict.keys())
        for i in result:
            revresult.append(priority[i])
        result = []
        for k in factors_dict: #removes mutually exclusive factor from result
            for i in revresult:
                if rd[i] in factors_dict[k] and len(factors_dict[k]) == 1:
                    factors_dict[k].remove(rd[i])
                    result.append(rd[i])
                    revresult.remove(i)
                    m -= 1
            for n in factors_dict[k]:
                if needed[n] <= 0:
                    factors_dict[k].remove(n)
                if len(factors_dict[k]) == 1 and prior[n] not in revresult:
                    m -= 1
        while len(revresult) > m:
            revresult.remove(min(revresult))
        
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
        self.schedule.use_actions()
        self.fatness_change()
        self.reduce_overflow()
        self.calc_needs_change()
        self.bribe()


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
        nutrition_modifier = self.nutrition['level']
        desire += nutrition_modifier -3
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

    def relations_points(self, person=None, axis=None, value=1):    #axis = one of (consideration, distance, affection) 
        if person in self.relations:
            self.relations[person][axis][1][1] += value
    def set_relations(self, person):
        if person in self.relations:
            return
        else:
            default = {
                "connection": "unrelated",
                "consideration": ["respectful", [0, 0]],
                "distance": ["close", [0, 0]],
                "affection": ["associate", [0, 0]],              
            }
            self.relations[person] = default
        return

    def rel_change_available(self, person, axis):
        if person in self.relations:
            needed = self.relations[person][axis][1][0]
            current = self.relations[person][axis][1][1]
            direction = True if current > 0 else False
            if abs(current) > needed:
                return (True, direction)
            else:
                return (False, False)

    def get_relations(self, person, axis):
        if person not in self.relations:
            return 'You have no relations with character %s'%(person.description())
        if axis == 'connection':
            return self.relations[person][axis]
        return self.relations[person][axis][0]

    def change_relations(self, person, axis, direction=''):    #direction = '+' or '-'
        if person in self.relations:
            if axis == 'consideration':
                l = ['miserable', 'respectful', 'significant']
            if axis == 'distance':
                l = ['distant', 'close', 'friend']
            if axis == 'affection':
                l = ['foe', 'associate', 'friend']
            rel = self.relations[person][axis][0]
            num = l.index(rel)
            if direction == '+':
                num += 1
                if num > 2:
                    num = 2
            else:
                num -= 1
                if num < 0:
                    num = 0
            rel = l[num]
            self.relations[person][axis][0] = rel
            self.relations[person][axis][1][1] = 0
        return

    def add_reward(self, name, need):
        self.rewards.append((name, need))

    def bribe_threshold(self):
        threshold = 6 + self.ddd_mod(self.dependence) + self.spirit - self.sensitivity - self.comfort['level']
        return threshold

    def bribe(self):
        tensed_needs = []
        for need in self.needs:
            status = self.needs[need]['status']
            if status == 'frustrated' or status == 'tense':
                tensed_needs.append(need)
        tensed_num = len(tensed_needs)
        if tensed_num < self.bribe_threshold():
            return 
        needed_rewards = []
        needs = []
        for reward in self.rewards:
            need = reward[1]
            if need in tensed_needs and need not in needs:
                needed_rewards.append(reward)
                needs.append(need)
        if tensed_num - len(needed_rewards) <= self.bribe_threshold():
            for reward in needed_rewards:
                if reward not in self.used_rewards:
                    refuse_threshold = self.bribe_threshold() - (tensed_num - len(needed_rewards))
                    if self.slave_stance.lower() == 'rebellious' or self.alignment['Orderliness'].lower() == 'chaotic':
                        if self.use_resource('willpower') > 0:
                            return
                        elif self.determination > 0:
                            self.determination -= 1
                            return
                    elif self.willpower > refuse_threshold:
                        if self.use_resource('willpower') > 0:
                            return
                    self.used_rewards += self.rewards
                    self.rewards = []
                    self.tokens.append('dependence')
                    return

    def training_resistance(self, master):
        return 1 + (self.mind - master.mind) + (self.spirit - master.spirit) + self.ddd_mod(self.discipline)
    
    def train(self, target):
        target_resistance = target.training_resistance(self)
        training_power = self.use_skill('communication', True, True)
        if target_resistance < training_power:
            if target.player_controlled:
                result = renpy.call_in_new_context('lbl_resist', 'discipline')
                if result == 'determination':
                    if target.determination > 0:
                        target.determination -= 1
                        result = True
                    else:
                        result = False
                    renpy.call_in_new_context('lbl_resist_result', 'discipline', result)
                elif result == 'willpower':
                    r = target.use_resource('willpower')
                    if r > 0:
                        result = True
                    else:
                        result = False
                    renpy.call_in_new_context('lbl_resist_result', 'discipline', result)
                if result == False:
                    renpy.call_in_new_context('lbl_notify', 'discipline')
                    target.tokens.append('discipline')
                return

            if target.slave_stance.lower() == 'rebellious':
                if target.use_resource('willpower') <= 0:
                    if target.determination > 0:
                        target.determination -= 1
                        return
                else:
                    return
            elif target.willpower > target.obedience():
                if target.use_resource('willpower') > 0:
                    return
            target.tokens.append('discipline')


