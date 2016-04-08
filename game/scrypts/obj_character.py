# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from features import Feature
from skills import Skill, skills_data
from needs import init_needs
from copy import copy
from copy import deepcopy
from food import *
from schedule import *
from taboos import init_taboos
from relations import Relations




class Person(object):

    def __init__(self, age='adolescent', gender='male'):
        self.player_controlled = False
        self.firstname = u"Антон"
        self.surname = u"Сычов"
        self.nickname = u"Сычуля"
        self.alignment = {
            "orderliness": "conformal",   # "Lawful", "Conformal" or "Chaotic"
            "activity": "reasonable",        # "Ardent", "Reasonable" or "Timid"
            "morality": "selfish",       # "Good", "Selfish" or "Evil"
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
        self.modifiers = []
        # init starting features
        self.add_feature(age)
        self.add_feature(gender)

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
        self.specialized_skill = None
        self.focused_skill = None
        self.focus = 0
        self.skills_used = []
        self.factors = []
        self.needs = init_needs(self)


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
        self.taboos = init_taboos(self)
        self.appetite = 0
        self.calorie_storage = 0
        self.money = 0
        self._determination = 0
        self.rewards = []
        self.used_rewards = []

        # Other persons known and relations with them, value[1] = [needed points, current points]
        self._relations = []
        self.tokens_difficulty = {'fear': 0, 'dependence': 0, 'discipline': 0}
        self.selfesteem = 0

    def count_modifiers(self, key):
        val = 0
        for mod in self.__dict__['modifiers']:
            for k in mod:
                if k==key:
                    val += mod[k]
        return val
    def __getattr__(self, key):
        if key in self.attributes:
            value = self.attributes[key]
            value += self.count_modifiers(key)
            if value < 1:
                value = 1
            if value > 5:
                value = 5
            return value
        if key in self.inner_resources:
            value = self.inner_resources[key]
            value += self.count_modifiers(key)
            if value <= 0:
                self.inner_resources[key] = 0
                value = 0
            max_value = getattr(self, self.attr_relations[key])
            if value > max_value:
                value = max_value
            return value
        for need in self.needs:
            if need.name == key:
                return need
        else:
            raise AttributeError(key)


    def __setattr__(self, key, value):
        if 'inner_resources' in self.__dict__:
            if key in self.inner_resources:
                value -= self.count_modifiers(key)
                self.inner_resources[key] = value
                if self.inner_resources[key] < 0:
                    self.inner_resources[key] = 0
        if 'attributes' in self.__dict__:
            if key in self.attributes:
                value -= self.count_modifiers(key)
                self.attributes[key] = value
                if self.attributes[key] < 0:
                    self.attributes[key] = 0
        super(Person, self).__setattr__(key, value)

    @property
    def determination(self):
        return self._determination
    @determination.setter
    def determination(self, value):
        self._determination = value
        if self._determination < 0:
            self._determination = 0


    @property
    def gender(self):
        return self.feature_by_slot('gender').name
    @property
    def age(self):
        return self.feature_by_slot('age').name

    def show_taboos(self):
        d = {}
        for taboo in self.taboos:
            if taboo.value != 0:
                d[taboo.name] = taboo.value
        return d


    def show_needs(self, key=None):
        d = {}
        if not key:
            for need in self.needs:
                d[need.name] = {'status': need.status, 'level': need.level}
        elif key:
            for need in self.needs:
                if need.status == key:
                    d[need.name] = {'status': need.status, 'level': need.level}
        return d

    def show_features(self):
        d = {}
        for feature in self.features:
            if feature.visible:
                d[feature.name] = feature.modifiers
        return d


    def taboo(self, name):
        for t in self.taboos:
            if t.name == name:
                return t
        return "No taboo named %s"%(name)


    def ddd_mod(self, d):
        modifier = d + self.dread + self.discipline + self.dependence - 3
        if modifier < 0:
            modifier = 0
        return modifier

    def pain_effect_threshold(self, taboo):
        threshold = 3 + self.attributes["spirit"] + self.ddd_mod(self.dread) - self.attributes["sensitivity"] - self.taboo(taboo).value
        threshold += self.tokens_difficulty['fear']
        return threshold

    def pain_tear_threshold(self, taboo):
        threshold = 7 + self.attributes["spirit"] + - self.attributes["sensitivity"] - self.taboo(taboo).value
        return threshold

    

    def skill(self, skillname):
        skill = None
        for i in self.skills:
            if i.name == skillname:
                skill = i
                return skill
        if skillname in skills_data:
            skill = Skill(self, skillname, skills_data[skillname])
        else:
            skill = Skill(self, skillname)
        self.skills.append(skill)
        return skill






    def use_resource(self, resource):
        value = getattr(self, resource)
        self.inner_resources[resource] -= 1
        return value

    def skillcheck(self, skill=None, forced = False, needs=[], taboos=[]):
        resource = False
        determination = False
        sabotage = False
        res_to_use = self.skill(skill).resource if skill else None
        check = 0
        skill_lvl = 0
        
        if self.player_controlled:
            resource, determination, sabotage = renpy.call_in_new_context('lbl_skill_check', self, skill, self.skill(skill).resource)
        else:
            motivation = self.motivation(skill=skill, needs=needs, forced=forced, taboos=taboos)
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
            check = -1
            if self.player_controlled:
                renpy.call_in_new_context('lbl_check_result', check)
            return check
        if skill:
            skill_lvl = self.skill(skill).level
            self.skills_used.append(skill)
        else:
            check += self.discipline
        for need in needs:
            getattr(self, need[0]).set_shift(need[1])
        for taboo in taboos:
            self.taboo(taboo[0]).use(taboo[1])
        if skill_lvl <= 0:
            if self.player_controlled:
                renpy.call_in_new_context('lbl_check_result', check)
            return check
        check = check + skill_lvl + self.mood() - 3
        res = self.use_resource(res_to_use) if resource else 0
        if determination and self.determination > 0:
            self.determination -= 1
            if res <= 0:
                check += getattr(self, self.skill(skill).attribute)
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
        if self.player_controlled:
            renpy.call_in_new_context('lbl_check_result', check)
        return check
    

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
            if self.focused_skill in result:
                self.focus += 1
                self.skills_used = []
                returnpl
            self.skill(random.choice(result)).set_focus()
            self.focus = 1
        self.skills_used = []

    def mood(self):
        mood = 0
        for need in self.needs:
            if need.status == "tense":
                mood -= 1
            elif need.status == "frustrated":
                mood -= 1
            elif need.status == "satisfied":
                mood += 1
        if self.esteem > 0:
            mood += 1
        elif self.esteem < 0:
            mood -= 1
        if mood < (-self.determination-self.sensitivity):
            return -1
        elif mood > self.sensitivity:
            return 1

        return 0

    def frustrate_need(self):
        if self.mood < 0:
            min_lvl = 1
            l = []
            for n in self.needs:
                if n.level == min_lvl:
                    min_lvl = n.level
                    l.append(n)
                elif n.level > min_lvl:
                    min_lvl = n.level
                    l = []
                    l.append(n)
            need = choice(l)
            need.status = 'frustrated'
        return


    
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
    

    
    def reduce_overflow(self):
        max_level = 5
        needs_list = []
        for need in self.needs:
            if need.status == 'overflow':
                needs_list.append(need)
        if self.determination > len(needs_list):
            return
        needs_list = []
        while True:
            for need in self.needs:
                if need.level == max_level and need.status == 'overflow':
                    needs_list.append(need)
            if len(needs_list) > 0:
                n = choice(needs_list)
                n.status = 'relevant'
                return
            max_level -= 1
            if max_level < 1:
                return


    def motivation(self, skill=None, needs=[], forced=False, taboos=[]):# needs should be a list of tuples[(need, shift)]
        motiv = 0
        motiv += self.mood()
        if skill:
            if self.skill(skill).talent:
                motiv += self.spirit
        for need in needs:
            status = getattr(self, need[0]).status
            shift = need[1]
            if shift < 0:
                if status == 'frustrated' or status == 'tense':
                    motiv -= getattr(self, need.level)
                elif status == 'overflow':
                    motiv -= 1
            if shift > 0:
                if status == 'frustrated' or status == 'tense': 
                    motiv += getattr(self, need).level
                elif status == 'relevant':
                    motiv -= 1
        if len(taboos)>0:
            for taboo in taboos:
                motiv -= self.taboo(taboo[0]).value
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
        Feature(self, name)
    
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
            for f in self.features:
                if f.name == feature:
                    f.remove()
        else:
            i = self.features.index(feature)
            self.features[i].remove()
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
        for need in self.needs:
            need.status_change()
        self.frustrate_need()
        self.bribe()
        self.reduce_esteem()


    def food_demand(self):
        """
        Evaluate optimal food consumption to maintain current weight.
        :return:
        """
        demand = self.physique
        demand += self.appetite
        demand += self.count_modifiers('food_demand')

        if demand < 1:
            demand = 1

        return demand

    def food_desire(self):
        """
        Evaluate ammount of food character likes to consume.
        :return:
        """
        desire = self.food_demand()
        nutrition_modifier = self.nutrition.level
        desire += nutrition_modifier -3
        desire += self.count_modifiers("food_desire")

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


    def set_relations(self, person):
        for relation in self._relations:
            if relation.target == person:
                return
        if self.player_controlled or person.player_controlled:
            self._relations.append(Relations(self, person))
            person._relations.append(Relations(person, self))
        else:
            # simple relations model needed for npc-npc relations
            return


    def relations(self, person):
        self.set_relations(person)
        for relation in self._relations:
            if relation.target == person:
                return relation
        

    def relations_tokens(self, person):
        if self.player_controlled:
            for rel in self._relations:
                if rel.target == person:
                    return rel._tokens
        else:
            for rel in self._relations:
                if isinstance(rel, Relations):
                    return rel.target.relations(self)._tokens



    def add_reward(self, name, need):
        self.rewards.append((name, need))

    def bribe_threshold(self):
        threshold = 6 + self.ddd_mod(self.dependence) + self.spirit - self.sensitivity - self.comfort.level
        threshold += self.tokens_difficulty['dependence']
        return threshold

    def bribe(self):
        tensed_needs = []
        for need in self.needs:
            status = need.status
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
                    self.add_token('dependence')
                    return

    def training_resistance(self):
        return 1 + (self.mind - self.master.mind) + (self.spirit - self.master.spirit) + self.ddd_mod(self.discipline) + self.tokens_difficulty['discipline']
    

    def add_token(self, token):
        if not token in self.tokens or token=='angst':
            self.tokens.append(token)


    def use_token(self, token):
        if self.has_token(token):
            self.tokens.remove(token)
            if token in self.tokens_difficulty:
                self.tokens_difficulty[token] += 1
            else:
                self.tokens_difficulty[token] = 1

    def has_token(self, token):
        if token in self.tokens:
            return True
        return False


    def moral_action(self, target=None, orderliness=None, activity=None, morality=None):
        result = 0
        act = {'ardent': 1, 'reasonable': 0, 'timid': -1}
        moral = {'good': 1, 'selfish': 0, 'evil': -1}
        order = {'lawful': 1, 'conformal': 0, 'chaotic': -1}
        if orderliness:
            valself = order[self.alignment['orderliness']]
            valact = order[orderliness]
            if valself != 0:
                if valself + valact == 0:
                    result -= 1
                elif abs(valself + valact) == 2:
                    result += 1
            elif target:
                if valact == 1:
                    if self.relations(target).distance == 'formal':
                        result += 1
                    elif self.relations(target).distance == 'intimate':
                        result -= 1
                elif valact == -1:
                    if self.relations(target).distance == 'formal':
                        result -= 1
                    elif self.relations(target).distance == 'intimate':
                        result += 1
        if activity:
            valself = act[self.alignment['activity']]
            valact = act[activity]
            if valself != 0:
                if valself + valact == 0:
                    result -= 1
                elif abs(valself + valact) == 2:
                    result += 1
            elif target:
                if valact == 1:
                    if self.relations(target).consideration == 'significant':
                        result += 1
                    elif self.relations(target).consideration == 'miserable':
                        result -= 1
                elif valact == -1:
                    if self.relations(target).consideration == 'miserable':
                        result -= 1
                    elif self.relations(target).consideration == 'significant':
                        result += 1
        if morality:
            valself = moral[self.alignment['morality']]
            valact = moral[morality]
            if valself != 0:
                if valself + valact == 0:
                    result -= 1
                elif abs(valself + valact) == 2:
                    result += 1
            elif target:
                if valact == 1:
                    if self.relations(target).affection == 'friend':
                        result += 1
                    elif self.relations(target).consideration == 'foe':
                        result -= 1
                elif valact == -1:
                    if self.relations(target).consideration == 'foe':
                        result -= 1
                    elif self.relations(target).consideration == 'friend':
                        result += 1
        self.selfesteem += result

    def reduce_esteem(self):
        if self.selfesteem == 0:
            return
        val = 5-self.sensitivity
        if self.selfesteem > 0:
            self.selfesteem -= val
        elif self.esteem < 0:
            self.selfesteem += val

