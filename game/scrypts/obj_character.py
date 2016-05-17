# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from features import Feature, person_features
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
            "orderliness": "conformal",   # "lawful", "conformal" or "chaotic"
            "activity": "reasonable",        # "ardent", "reasonable" or "timid"
            "morality": "selfish",       # "good", "selfish" or "evil"
        }
        self.features = []          # gets Feature() objects and their child's. Add new Feature only with self.add_feature()
        self.tokens = []             # Special resources to activate various events
        self.master = None          # If this person is a slave, the master will be set
        self.slave_stance = 'rebellious'     # rebellious, forced, accustomed or willing
        self.supervisor = None
        self.is_slave = False
        self.slaves = []
        self.subordinates = []
        self.ap = 1
        self.schedule = Schedule(self)
        self.modifiers = []
        # init starting features
        self.add_feature(age)
        self.add_feature(gender)
        self.availabe_actions = [] # used if we are playing slave-part


        self.allowance = 0         # Sparks spend each turn on a lifestyle
        self.ration = {
            "amount": 'unlimited',   # 'unlimited', 'limited' by price, 'regime' for figure, 'starvation' no food
            "food_type": "cousine",   # 'forage', 'sperm', 'dry', 'canned', 'cousine'
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
        self.restrictions = []
        self.needs = init_needs(self)


        self.attributes = {
            'physique': 3,
            'mind': 3,
            'spirit': 3,
            'agility': 3,
            'sensitivity':3
        }
        self.university = {'name': 'study', 'effort': 'bad', 'auto': False}
        self.vigor = 0
        self.fatigue = 0
        self.taboos = init_taboos(self)
        self.appetite = 0
        self.calorie_storage = 0
        self.money = 0
        self._determination = 0
        self._anxiety = 0
        self.rewards = []
        self.used_rewards = []

        # Other persons known and relations with them, value[1] = [needed points, current points]
        self._relations = []
        
        self.selfesteem = 0
        self.conditions = []

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
        for need in self.needs:
            if need.name == key:
                return need
        else:
            raise AttributeError(key)


    def __setattr__(self, key, value):
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
    def anxiety(self):
        return self._anxiety
    @anxiety.setter
    def anxiety(self, value):
        self._anxiety = value
        if self._anxiety < 0:
            self_anxiety = 0


    @property
    def gender(self):
        return self.feature_by_slot('gender').name
    @property
    def age(self):
        return self.feature_by_slot('age').name

    def insurgensy(self):
        val = self.vigor - self.obedience()
        if val < 0:
            val = 0
        return val

    def gain_vigor(self, power):
        if power > self.vigor:
            self.vigor += 1
    def drain_vigor(self):
        v = self.vigor
        self.appetite += 1
        if self.vigor > 0:
            self.vigor -= 1
        else:
            self.fatigue += 1
        return v
    def calc_vigor(self):
        mood = self.mood()
        vigor_left = self.vigor
        self.vigor = 0
        if mood[0] < 0:
            self.vigor -= 1
        if self.fatigue > 0:
            self.fatigue = 0
            self.vigor -= 1
        if mood[0] > 0:
            self.gain_vigor(mood[1])
        if vigor_left > 0:
            self.gain_vigor(vigor_left)
        self.gain_vigor(self.physique)
        self.gain_vigor(self.spirit)
        to_remove = []
        for cond in self.conditions:
            if isinstance(cond, tuple):
                if cond[0] == 'vigor':
                    if cond[1] > 0:
                        self.gain_vigor(cond[1])
                    elif cond[1] < 0:
                        self.vigor += cond[1]
                    to_remove.append(cond)
        for cond in to_remove:
            self.conditions.remove(cond)
        if self.vigor < 0:
            self.fatigue = self.vigor
            self.vigor = 0




    def show_taboos(self):
        s = ""
        for taboo in self.taboos:
            if taboo.value != 0:
                s += "{taboo.name}({taboo.value}), ".format(taboo=taboo)
        return s


    def show_needs(self, key=None):
        s = ""
        if not key:
            for need in self.needs:
                s += "{need.name}({need.level}), ".format(need=need)
        elif key:
            for need in self.needs:
                if need.status == key:
                    s += "{need.name}({need.level}), ".format(need=need)
        return s

    def show_features(self):
        s = ""
        for feature in self.features:
            if feature.visible:
                s += "{feature.name}, ".format(feature=feature)
        return s

    def show_focus(self):
        if isinstance(self.focused_skill, Skill):
            return self.focused_skill.name
        else:
            return "No focused skill"

    def show_skills(self):
        s = ""
        for skill in self.skills:
            s += "{skill.name}({skill.level})".format(skill=skill)
        return s

    def show_mood(self):
        m = {-1: 'gloomy', 0: 'content', 1: 'happy'}
        mood = self.mood()
        return "{mood}({val})".format(mood=m[mood[0]], val=mood[1])


    def name(self):
        s = self.firstname + " " + self.surname
        return s


    def taboo(self, name):
        for t in self.taboos:
            if t.name == name:
                return t
        return "No taboo named %s"%(name)



    def pain_effect_threshold(self, taboo):
        dif = self.relations(self.master).tokens_difficulty['dread'] if self.master else 0
        threshold = self.vigor + self.spirit + dif - self.taboo(taboo).value
        return threshold

    def pain_tear_threshold(self, taboo):
        threshold = self.vigor*2 + 6 - self.sensitivity - self.taboo(taboo).value
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




    def action(self, forced = False, needs=[], taboos=[], moral=0):
        if self.player_controlled:
            result = renpy.call_in_new_context('lbl_action_check', self)
        else:
            result = self.motivation(forced=forced, needs=needs, taboos=taboos, moral=moral)
        if result > 0:
            for need in needs:
                getattr(self, need[0]).set_shift(need[1])
            for taboo in taboos:
                self.taboo(taboo[0]).use(taboo[1])
        return result
    def skillcheck(self, skill=None, forced = False, needs=[], taboos=[], moral=0):
        vigor = False
        determination = False
        sabotage = False
        check = 0
        
        if self.player_controlled:
            vigor, determination, sabotage = renpy.call_in_new_context('lbl_skill_check', self)
        else:
            motivation = self.motivation(skill=skill, needs=needs, forced=forced, taboos=taboos, moral=moral)
            if motivation < 0:
                sabotage = True
            if motivation > 0 and motivation < 6-self.vigor:
                pass
            if motivation > 6-self.vigor and motivation < 5:
                vigor = True
            if motivation > 5 and res_to_use < 1:
                vigor = False
                determination = True
            if motivation > 10:
                vigor = True
                determination = True
        if sabotage:
            check = -1
            if self.player_controlled:
                renpy.call_in_new_context('lbl_check_result', check)
            return check
        for need in needs:
            getattr(self, need[0]).set_shift(need[1])
        for taboo in taboos:
            self.taboo(taboo[0]).use(taboo[1])
        self.skills_used.append(skill)
        check = check + self.mood()[0] - 3 + self.skill(skill).level
        if determination and self.determination > 0:
            self.determination -= 1
            if self.vigor < 1 or not vigor:
                check += getattr(self, self.skill(skill).attribute)
            else:
                check += 1
                check += getattr(self, self.skill(skill).attribute)
        else:
            val = max(self.vigor, getattr(self, self.skill(skill).attribute))
            check += val
        if vigor:
            self.drain_vigor()
        elif self.vigor < 1:
            self.drain_vigor()
        if self.focused_skill != None:
            if check < self.focus and skill == self.focused_skill.name:
                check += 1
        if check < 0:
            check = 0
        if self.player_controlled:
            renpy.call_in_new_context('lbl_check_result', check)
        return check
    

    def calc_focus(self):
        if self.focused_skill in self.skills_used:
            self.focus += 1
            return
        if len(self.skills_used) > 0:
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
                return
            self.skill(choice(result)).set_focus()
            self.focus = 1
        else:
            self.focused_skill = None
        self.skills_used = []

    def mood(self):
        mood = 0
        for need in self.needs:
            if need.status == "tense":
                mood -= 1
            elif need.status == "satisfied":
                mood += 1
        if self.selfesteem > 0:
            mood += 1
        elif self.selfesteem < 0:
            mood -= 1
        if mood < (-self.determination-self.sensitivity):
            return (-1, mood)
        elif mood > self.sensitivity:
            return (1, mood)

        return (0, mood)



    
    def obedience(self):
        if not self.is_slave or self.player_controlled:
            return 0
        obedience = 0

        if self.alignment["orderliness"] == "lawful":
            obedience += self.relations(self.master).discipline*2
        elif self.alignment["orderliness"] == "chaotic":
            obedience += self.relations(self.master).discipline/2
        else:
            obedience += self.relations(self.master).discipline

        if self.alignment["activity"] == "timid":
            obedience += self.relations(self.master).dependence*2
        elif self.alignment["activity"] == "ardent":
            obedience += self.relations(self.master).dependence/2
        else:
            obedience += self.relations(self.master).dependence

        if self.alignment["morality"] == "evil":
            obedience += self.relations(self.master).dread*2
        elif self.alignment["morality"] == "good":
            obedience += self.relations(self.master).dread/2
        else:
            obedience += self.relations(self.master).dread

        return obedience


    def favor(self):
        if not self.master or self.player_controlled:
            return 0
        favor = 0
        if self.master.alignment["orderliness"] == "lawful":
            favor += self.relations_player().confidence*2
        elif self.master.alignment["orderliness"] == "chaotic":
            favor += self.relations_player().confidence/2
        else:
            favor += self.relations_player().confidence

        if self.master.alignment["activity"] == "timid":
            favor += self.relations_player().craving*2
        elif self.master.alignment["activity"] == "ardent":
            favor+= self.relations_player().craving/2
        else:
            favor += self.relations_player().craving

        if self.master.alignment["morality"] == "evil":
            favor += self.relations_player().compassion*2
        elif self.master.alignment["morality"] == "good":
            favor += self.relations_player().compassion/2
        else:
            favor += self.relations_player().compassion
        return favor

    def duty_threshold(self):
        if self.player_controlled:
            return 0
        mod = self.relations_player().tokens_difficulty['confidence']
        threshold = self.authority.level + self.order.level - self.independence.level + mod
        return threshold

    def gratifaction_threshold(self, needs=[]):
        if self.player_controlled:
            return 0
        mod = self.relations_player().tokens_difficulty['craving']
        n = 0
        for need in needs:
            if getattr(self, need).level > n:
                n = getattr(self, need).level
        threshold = 3 + self.spirit + self.mood()[1] - n + mod
        return threshold

    def remorse_threshold(self):
        if self.player_controlled:
            return 0
        mod = self.relations_player().tokens_difficulty['compassion']
        threshold = self.ambition.level + self.power.level - self.altruism.level - self.sensitivity - self.mood()[1]
        if threshold < 0:
            threshold = 0
        threshold += mod
        return threshold

    def suggestion_threshold(self):
        if self.player_controlled:
            return 0
        return self.spirit + self.authority.level - self.mood()[1]

    def suggestion_check(self):
        threshold = self.suggestion_threshold()
        if self.relations_player().master_stance == 'cruel':
            return 100
        if self.relations_player().master_stance == 'opressive':
            threshold -= self.favor()
            if threshold < self.spirit:
                threshold = self.spirit
        if self.relations_player().master_stance == 'rightful':
            threshold -= self.favor()
        if self.relations_player().master_stance == 'benevolent':
            return 0
        return threshold

    
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


    def motivation(self, skill=None, needs=[], forced=False, taboos=[], moral=0):# needs should be a list of tuples[(need, shift)]
        motiv = 0
        motiv += self.mood()[0]
        motiv += moral
        if skill:
            if self.skill(skill).talent:
                motiv += self.vigor
        if self.vigor < 1:
            motiv -= 1
            motiv -= self.fatigue

        for need in needs:
            status = getattr(self, need[0]).status
            shift = need[1]
            if shift < 0:
                if status == 'tense':
                    motiv -= getattr(self, need[0]).level
                elif status == 'overflow':
                    motiv -= 1
            if shift > 0:
                if status == 'tense': 
                    motiv += getattr(self, need[0]).level
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
                if motiv < 5:
                    motiv = self.obedience()
                if motiv > 5:
                    motiv = 5
            if self.slave_stance == 'willing':
                motiv += self.obedience()
        
        return motiv

    

    def add_feature(self, name):    # adds features to person, if mutually exclusive removes old feature
        Feature(self, name)
    
    def feature_by_slot(self, slot):        # finds feature which hold needed slot
        for f in self.features:
            if f.slot == slot:
                return f
            else:
                return None

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
        self.bribe()
        self.fatness_change()
        for need in self.needs:
            need.status_change()
        self.reduce_overflow()
        self.calc_focus()
        self.calc_vigor()
        self.reduce_esteem()
        if not self.player_controlled and self.mood()[0] > 0:
            if self.determination < 1:
                self.determination = 1
        if self.feature('obese') or self.feature('emaciated'):
            self.vigor -= 1



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
        desire += self.nutrition.level
        desire += self.count_modifiers("food_desire")

        if desire < 1:
            desire = 1

        return desire

    def consume_food(self):
        food_consumed = self.food_desire()
        fatness = self.feature_by_slot('shape')
        if fatness:
            fatness = fatness.name
        flist = ['emaciated' ,'slim', None, 'chubby', 'obese']
        val = flist.index(fatness)
        if self.ration['amount'] == 'starvation':
            food_consumed = 0

        if self.ration['amount'] == 'limited':
            if food_consumed > self.ration["limit"]:
                food_consumed = self.ration["limit"]

        if self.ration['amount'] == 'regime':
            food_consumed = self.food_demand()
            if self.ration['target'] > val:
                food_consumed += 1+self.appetite
            if self.ration['target'] < val:
                food_consumed = self.food_demand() - 1
            if self.ration['target'] == val:
                food_consumed = self.food_demand()
        return food_consumed

    def fatness_change(self):
        calorie_difference = self.consume_food() - self.food_demand()
        if calorie_difference > 0:
            power = 5 - calorie_difference
            if power < 1:
                power = 1
            self.conditions.append(('vigor', power))
        if calorie_difference < self.food_desire():
            self.nutrition.set_shift(calorie_difference-self.food_desire())
        if self.ration['amount'] != 'starvation':
            d = {'sperm': -4, 'forage': -1, 'dry': -2, 'canned': 0, 'cousine': 3}
            self.nutrition.set_shift(d[self.ration['food_type']])
        self.calorie_storage += calorie_difference
        fatness = self.feature_by_slot('shape')
        if fatness != None:
            fatness = fatness.name
        flist = ['emaciated' ,'slim', None, 'chubby', 'obese']
        ind = flist.index(fatness)
        if self.calorie_storage < 0:
            chance = randint(-10, -1)
            self.conditions.append(('vigor', -1))
            if self.calorie_storage <= chance:
                ind -= 1
                if ind < 0:
                    ind = 0
                    if self.feature('starving'):
                        self.add_feature('dead')
                    else:
                        self.add_feature('starving')
                f = flist[ind]
                if f:
                    self.add_feature(flist[ind])
                else:
                    self.feature_by_slot('shape').remove()
        if self.calorie_storage > 0:
            chance = randint(1, 10)
            if self.calorie_storage >= chance:
                ind += 1
                if ind > 4:
                    ind = 4
                    if self.feature('dyspnoea'):
                        self.add_feature('diabetes')
                    else:
                        self.add_feature('dyspnoea')
                f = flist[ind]
                if f:
                    self.add_feature(f)
                else:
                    self.feature_by_slot('shape').remove()
    def nutrition_change(self, food_consumed):
        if food_consumed < self.food_demand():
            self.ration["overfeed"] -= 1
            chance = randint(-10, -1)
            if self.ration["overfeed"] <= chance:
                self.ration["overfeed"] = 0

        return


    def set_relations(self, person):
        if self.player_controlled:
            for relation in self._relations:
                if relation.owner == person:
                    return 
        else:
            for relation in self._relations:
                if relation.target == person:
                    return
        if self.player_controlled:
            rel = Relations(person, self)
            self._relations.append(rel)
            person._relations.append(rel)
        elif person.player_controlled:
            rel = Relations(self, person)
            self._relations.append(rel)
            person._relations.append(rel)
        else:
            # simple relations model needed for npc-npc relations
            return


    def relations(self, person):
        self.set_relations(person)
        for relation in self._relations:
            if self.player_controlled:
                if relation.target == self:
                    return relation
            else:
                if relation.target == person:
                    return relation
        

    def relations_tokens(self, person):
        if self.player_controlled:
            for rel in self._relations:
                if rel.target == self:
                    return rel._tokens
        else:
            for rel in self._relations:
                if isinstance(rel, Relations):
                    return rel.target.relations(person)._tokens

    def relations_player(self):
        if self.player_controlled:
            return None
        else:
            for rel in self._relations:
                if rel.target.player_controlled:
                    return rel



    def add_reward(self, name, need):
        self.rewards.append((name, need))

    def bribe_threshold(self):
        dif = self.relations(self.master).tokens_difficulty['dependence'] if self.master else 0
        threshold = 3 + self.spirit - self.sensitivity + dif
        return threshold

    def bribe(self):
        tensed_needs = []
        for need in self.needs:
            status = need.status
            if status == 'tense':
                tensed_needs.append(need.name)
        tensed_num = len(tensed_needs)
        if tensed_num < self.bribe_threshold():
            self.rewards = []
            return 
        needed_rewards = []
        needs = []
        for reward in self.rewards:
            need = reward[1]
            if need in tensed_needs and need not in needs:
                needed_rewards.append(reward)
                needs.append(need)
        if len(needed_rewards) < 1:
            self.rewards = []
            return
        if tensed_num - len(needed_rewards) <= self.bribe_threshold():
            for reward in needed_rewards:
                if reward not in self.used_rewards:
                    self.used_rewards += self.rewards
                    for reward in self.rewards:
                        getattr(self, reward[1]).set_shift(100)
                    self.rewards = []
                    self.add_token('dependence')
                    return
        else:
            self.rewards = []
            return

    def training_resistance(self):
        dif = self.relations(self.master).tokens_difficulty['discipline'] if self.master else 0
        return self.insurgensy() + self.mind - 1 + dif
    



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
        if self.relations_player():
            if self.relations_player().has_token(token):
                return True
        return False



    def moral_action(self, *args, **kwargs):
        result = self.check_moral(*args, **kwargs)
        self.selfesteem += result
        return result
        

    def check_moral(self, *args, **kwargs):
        result = 0
        act = {'ardent': 1, 'reasonable': 0, 'timid': -1}
        moral = {'good': 1, 'selfish': 0, 'evil': -1}
        order = {'lawful': 1, 'conformal': 0, 'chaotic': -1}
        activity = None
        morality = None
        orderliness = None
        target = None
        if 'target' in kwargs:
            target = kwargs['target']
        for arg in args:
            if arg in act.keys():
                activity = arg
            if arg in moral.keys():
                morality = arg
            if arg in order.keys():
                orderliness = arg
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
                    if self.relations(target).fervor == 'intense':
                        result += 1
                    elif self.relations(target).fervor == 'delicate':
                        result -= 1
                elif valact == -1:
                    if self.relations(target).fervor == 'delicate':
                        result -= 1
                    elif self.relations(target).fervor == 'intense':
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
                    if self.relations(target).congruence == 'supporter':
                        result += 1
                    elif self.relations(target).congruence == 'contradictor':
                        result -= 1
                elif valact == -1:
                    if self.relations(target).congruence == 'contradictor':
                        result -= 1
                    elif self.relations(target).congruence == 'supporter':
                        result += 1
        return result

    def reduce_esteem(self):
        if self.selfesteem == 0:
            return
        val = 5-self.sensitivity
        if self.selfesteem > 0:
            self.selfesteem -= val
            if val < 0:
                val = 0
        elif self.selfesteem < 0:
            self.selfesteem += val
            if val > 0:
                val = 0
    

    def add_condition(self, name):
        if not name in self.conditions:
            self.conditions.append(name)
        return


    def enslave(self, target):
        target.is_slave = True
        target.master = self
        self.slaves.append(target)
        self.relations(target)


    def master_stance(self):
        if self.player_controlled:
            raise Exception('master_stance is only for npc')
        stance = self.relations_player().master_stance
        l = ['cruel', 'opressive', 'rightful', 'benevolent']
        ind = l.index(stance)
        return ind

    def desirable_relations(self):
        d = {'lawful': 'formal', 'chaotic': 'intimate',
            'timid': 'delicate', 'ardent': 'intense',
            'good': 'supporter', 'evil': 'contradictor'}

        return [d.get(x) for x in self.alignment.values()]

    def willing_available(self, target):
        if not target in self.slaves:
            return False
        rel_check = False
        for rel in self.relations(target).description():
            if rel in target.desirable_relations():
                rel_check = True
                break
        return target.obedience()>target.spirit and target.relations(self).has_token('accordance') and rel_check
