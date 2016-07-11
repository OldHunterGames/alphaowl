# -*- coding: UTF-8 -*-
from random import *
import renpy.store as store
import renpy.exports as renpy
from features import Feature, Phobia, person_features
from skills import Skill, skills_data
from needs import init_needs
from copy import copy
from copy import deepcopy
from food import *
from schedule import *
from taboos import init_taboos
from relations import Relations
from stance import Stance
accommodation_types = {'makeshift bad': {'comfort': -3},
                       'campfire': {'comfort': -1},
                       'chained': {'comfort': -4, 'activity': -4, 'wellness': -3},
                       'jailed': {'comfort': -3, 'activity': -3, 'wellness': -2},
                       'confined': {'comfort': -5, 'activity': -5, 'wellness': -4},
                       'rough mat': {'comfort': -2, 'prosperity': -1, 'wellness': -1},
                       'cot and blanket': {},
                       'appartament': {'comfort': 3},
                       'love nest': {'comfort': 5, 'prosperity': 2, 'communication': 2, 'eros': 2}
                       }
class Modifiers(object):
    def __init__(self):
        self._names = []
        self._attributes = []
        self._times = []
    

    def tick_time(self):
        for i in range(len(self._times)):
            try:
                self._times[i] -= 1
                if self._times[i] < 1:
                    self.del_item(i)
            except TypeError:
                pass

   
    def del_item(self, index):
        if isinstance(index, str):
            for name in self._names:
                if name == index:
                    index = self._names.index(name)
        self._names.pop(index)
        self._attributes.pop(index)
        self._times.pop(index)


    def add_item(self, name, attributes, time=None):
        if not name in self._names:
            self._names.append(name)
            self._attributes.append(attributes)
            self._times.append(time)
        else:
            index = self._names.index(name)
            self._names[index] = name
            self._attributes[index] = attributes
            self._times[index] = time


    def get_modified_attribute(self, attribute):
        mod = 0
        for d in self._attributes:
            for k, v in d.items():
                if k == attribute:
                    mod += v
        return mod


    def get_all(self):
        last_name = self._names[-1]
        txt = ''
        for name in self._names:
            index = self._names.index(name)
            attr_txt = ''
            d = self._attributes[index]
            for k, v in d.items():
                attr_txt += "{0}({1})".format(k, v)
            time_txt = self._times[index]
            txt += "{0}: attributes: {1}, time: {2}".format(name, attr_txt, time_txt)
            if name != last_name:
                txt += '\n'
        return txt

    def get_modifier(self, name):
        index = None
        for n in self._names:
            if n == name:
                index = self._names.index(name)
        try:
            return name, self._attributes[index], self._times[index]
        except TypeError:
            return None


    def get_modifier_separate(self, attribute):
        l = []
        for d in self._attributes:
            for k, v in d.items():
                if k == attribute:
                    l.append(v)
        return l
class Alignment(object):
    _needs = {'orderliness': {-1: 'independence', 1:'stability'},
            'activity': {-1: 'approval', 1: 'trill'},
            'morality': {-1: 'power', 1: 'altruism'}
            }

    _orderliness = {-1: "chaotic", 0: "conformal", 1: "lawful"}
    _activity = {-1: "timid", 0: "reasonable", 1: "ardent"}
    _morality = {-1: "evil", 0: "selfish", 1: "good"}
    _relation_binding = {'activity': 'fervor', 'morality': 'congruence', 'orderliness': 'distance'}
    def __init__(self):
        self._orderliness = 0
        self._activity = 0
        self._morality = 0
    
    @property
    def orderliness(self):
        return self._orderliness
    @orderliness.setter
    def orderliness(self, value):
        if isinstance(value, str):
            for k, v in Alignment._orderliness.items():
                if v == value:
                    self._orderliness = k
                    return
            raise Exception("Orderliness set with string value, but %s is not valid for this axis"%(value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._orderliness = value

    
    @property
    def activity(self):
        return self._activity
    @activity.setter
    def activity(self, value):
        if isinstance(value, str):
            for k, v in Alignment._activity.items():
                if v == value:
                    self._activity = k
                    return
            raise Exception("Activity set with string value, but %s is not valid for this axis"%(value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._activity = value
    

    @property
    def morality(self):
        return self._morality
    @morality.setter
    def morality(self, value):
        if isinstance(value, str):
            for k, v in Alignment._morality.items():
                if v == value:
                    self._morality = k
                    return
            raise Exception("Morality set with string value, but %s is not valid for this axis"%(value))
        if value < -1:
            value = -1
        elif value > 1:
            value = 1
        self._morality = value


    def show_orderliness(self):
        return Alignment._orderliness[self.orderliness]
    def show_activity(self):
        return Alignment._activity[self.activity]
    def show_morality(self):
        return Alignment._morality[self.morality]

    def description(self):
        return self.show_orderliness(), self.show_activity(), self.show_morality()


    def special_needs(self):
        n = Alignment._needs
        needs = []
        zero_needs = []
        for k in n.keys():
            try:
                val = getattr(self, k)
                needs.append(n[k][val])
                zero_needs.append(n[k][val - val*2])
            except KeyError:
                pass
        return needs, zero_needs




class Person(object):

    def __init__(self, age='adolescent', gender='male'):
        self.player_controlled = False
        self.firstname = u"Антон"
        self.surname = u"Сычов"
        self.nickname = u"Сычуля"
        self.alignment = Alignment()
        self.features = []          # gets Feature() objects and their child's. Add new Feature only with self.add_feature()
        self.tokens = []             # Special resources to activate various events
        self.relations_tendency = {'convention': 0, 'conquest': 0, 'contribution': 0}

        #obedience, dependecy and respect stats
        self._stance = []

        self.master = None          # If this person is a slave, the master will be set
        self.supervisor = None
        self.slaves = []
        self.subordinates = []
        self.ap = 1
        self.schedule = Schedule(self)
        self.modifiers = Modifiers()
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
        self.skills = []
        self.specialized_skill = None
        self.focused_skill = None
        self.focus = 0
        self.skills_used = []
        self.factors = []
        self.restrictions = []
        self._needs = init_needs(self)


        self.attributes = {
            'physique': 3,
            'mind': 3,
            'spirit': 3,
            'agility': 3,
            'sensitivity':3
        }
        self.university = {'name': 'study', 'effort': 'bad', 'auto': False}
        self.mood = 0
        self.fatigue = 0
        self._vitality = 0
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
        self.known_characters = []
        self.selfesteem = 0
        self.conditions = []
    

    def add_modifier(self, name, attributes, time=None):
        self.modifiers.add_item(name, attributes, time)
    

    def count_modifiers(self, key):
        val = self.__dict__['modifiers'].get_modified_attribute(key)
        return val
    

    @property
    def job(self):
        job = self.schedule.find_by_slot('job')
        if not job:
            return 'idle'
        else:
            return job.name


    def show_job(self):
        job = self.schedule.find_by_slot('job')
        if not job:
            return 'idle'
        else:
            values = []
            s = ''
            for k, v in job.special_values.items():
                s += '%s: '%(k)
                try:
                    l = [i for i in v]
                    try:
                        for i in l:
                            s += '%s, '%(i.name())
                    except KeyError:
                        for i in l:
                            s += '%s, '%(i)
                except TypeError:
                    try:
                        s += '%s, '%(v.name())
                    except KeyError:
                        s += '%s, '%(v)
                if k not in job.special_values.items()[-1]:
                    s += '\n'
            return '%s, %s'%(job.name, s)


    def job_object(self):
        job = self.schedule.find_by_slot('job')
        if not job:
            return None
        else:
            return job


    def __getattr__(self, key):
        if key in self.attributes:
            value = self.attributes[key]
            value += self.count_modifiers(key)
            if value < 1:
                value = 1
            if value > 5:
                value = 5
            return value
        n = self.get_all_needs()
        if key in n.keys():
            return n[key]
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


    def modifiers_separate(self, modifier):
        return self.modifiers.get_modifier_separate(modifier)
    @property
    def vitality(self):
        l = [self.physique, self.count_modifiers('shape'), self.count_modifiers('fitness'), self.mood,
            self.count_modifiers('therapy')]
        l += self.modifiers_separate('vitality')
        max_slot = 5
        val = 1
        ll = [i for i in l if i > -1]
        bad = len(l) - len(ll)
        ll = list(set(ll))
        ll.sort()
        for i in range(bad):
            ll.pop(0)
        for i in range(1, max_slot+1):
            if len(ll) < 1:
                break
            if not i < min(ll):
                val += 1
                ll.remove(min(ll))
        val += self._vitality
        if val > 5:
            val = 5
        return val


    @property
    def gender(self):
        return self.feature_by_slot('gender').name
    @property
    def age(self):
        return self.feature_by_slot('age').name

    def phobias(self):
        l = []
        for feature in self.features:
            if isinstance(feature, Phobia):
                l.append(feature.object_of_fear)
        return l
    def get_needs(self):
        d = {}
        for need in self._needs:
            if need.level > 0:
                d[need.name] = need
        return d

    def get_all_needs(self):
        d = {}
        for need in self._needs:
            d[need.name] = need
        return d
    def show_taboos(self):
        s = ""
        for taboo in self.taboos:
            if taboo.value != 0:
                s += "{taboo.name}({taboo.value}), ".format(taboo=taboo)
        return s


    def show_needs(self):
        s = ""
        for need in self.get_needs().values():
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
            s += "{name}({skill.level}, {skill.attribute}({value}))".format(name=skill.name, skill=skill, value=skill.attribute_value())
            if skill != self.skills[len(self.skills)-1]:
                s += ', '
        return s

    def show_mood(self):
        m = {-1: 'gloomy', 0: 'content', 1: 'happy'}
        mood = self.mood()
        return "{mood}({val})".format(mood=m[mood[0]], val=mood[1])


    def show_attributes(self):
        s = ""
        for key in self.attributes.keys():
            s += "{0}({1})".format(key, getattr(self, key))
        return s


    def show_tokens_difficulty(self):
        s = ""
        for key, value in self.tokens_difficulty.items():
            s += "{0}({1}), ".format(key, value)
        return s

    def name(self):
        s = self.firstname + " " + self.surname
        return s


    def taboo(self, name):
        for t in self.taboos:
            if t.name == name:
                return t
        return "No taboo named %s"%(name)
  

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


    def tick_features(self):
        for feature in self.features:
            feature.tick_time()
    

    def calc_focus(self):
        if self.focused_skill:
            if self.focused_skill in self.skills_used:
                self.focused_skill.focus += 1
                self.skills_used = []
                return
        try:
            self.focused_skill.focus = 0
        except AttributeError:
            pass

        if len(self.skills_used) > 0:
            from collections import Counter
            counted = Counter()
            for s.name in self.skills_used:
                counted[s]+=1
            maximum = max(counted.values())
            result = []
            for skill in counted:
                if counted[skill] == maximum:
                    result.append(self.skill(skill))
            self.skill(choice(result)).set_focus()
            self.focus = 1
        else:
            self.focused_skill = None
        
        self.skills_used = []

    def recalculate_mood(self):
        mood = 0
        happines = []
        dissapointment = []
        for need in self.get_needs().values():
            if need.tension and need.level > 0:
                dissapointment.append(need.level)
            if need.satisfaction > 0:
                happines.append(need.satisfaction)
                if need.level == 3:
                    happines.append(need.satisfaction)
            need.satisfaction = 0
            need.tension = False
        for i in range(self.determination):
            happines.append(1)
        for i in range(self.anxiety):
            dissapointment.append(1)

        hlen = len(happines)
        dlen = len(dissapointment)
        happines.sort()
        dissapointment.sort()
        
        if hlen > dlen:
            dissapointment = []
            for i in range(dlen):
                happines.pop(0)
            threshold = happines.count(5)
            sens = 5-self.sensitivity
            if threshold > sens:
                mood = 5
            elif threshold+happines.count(4) > sens:
                mood = 4
            elif threshold+happines.count(4)+happines.count(3) > sens:
                mood = 3
            elif threshold+happines.count(4)+happines.count(3)+happines.count(2) > sens:
                mood = 2
            elif threshold+happines.count(4)+happines.count(3)+happines.count(2)+happines.count(1) > sens:
                mood = 1

        elif hlen < dlen:
            happines = []
            for i in range(hlen):
                dissapointment.pop(0)
            dissapointment = [i for i in dissapointment if i > 1]
            despair = 6-setnsitivity-dissapointment.count(2)-dissapointment.count(3)*3
            if despair < 0:
                mood = -1
            else:
                mood = 0
            return
        
        else:
            mood = 0
        self.mood = mood



    def motivation(self, skill=None, tense_needs=[], satisfy_needs=[], beneficiar = None, morality=0, special=[]):# needs should be a list of tuples[(need, shift)]
        motiv = 0
        motiv += morality
        for i in special:
            motiv += i
        if skill:
            if self.skill(skill).talent:
                motiv += 1
            elif self.skill(skill).inability:
                motiv -= 1

        intense = []
        self_needs = self.get_needs()
        for need in tense_needs:
            if need in self_needs.keys():
                motiv -= 1
        for need in satisfy_needs:
            if need in self_needs.keys():
                intense.append(need.level)
        try:
            maximum = max(intense)
        except ValueError:
            maximum = 0
        motiv += maximum

        if beneficiar:
            if beneficiar == self:
                motiv += 2
            else:
                motiv += self.stance(beneficiar).value
                if self.stance(beneficiar) < 0:
                    motiv = 0
                if beneficiar == self.master or beneficiar == self.supervisor:
                    if self.stance(beneficiar).value == 0:
                        motiv = min(beneficiar.mind, beneficiar.spirit)
                    elif self.stance(beneficiar).value == 2:
                        motiv = 5
        if motiv < 0:
            motiv = 0
        if motiv > 5:
            motiv = 5

        return motiv

    

    def add_feature(self, name):    # adds features to person, if mutually exclusive removes old feature
        Feature(self, name)
    def add_phobia(self, name):
        Phobia(self, name)
    def feature_by_slot(self, slot):        # finds feature which hold needed slot
        for f in self.features:
            if f.slot == slot:
                return f
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
    def reset_needs(self):
        for need in self.get_all_needs().values():
            need.reset()
    def rest(self):
        self.tick_conditions()
        self.modifiers.tick_time()
        self.tick_features()
        self.schedule.use_actions()
        self.fatness_change()
        self.recalculate_mood()
        self.reset_needs()
        self.calc_focus()
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
        desire += self.nutrition.level
        desire += self.count_modifiers("food_desire")

        if desire < 1:
            desire = 1

        return desire

    def get_food_consumption(self):
        types = {'sperm': 0, 'forage': 0, 'dry': 1, 'canned': 2, 'cousine': 2}
        value = self.consume_food()
        multiplier = types[self.ration['food_type']]
        return value * multiplier
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
        if calorie_difference < self.food_desire():
            self.nutrition.set_tension()
        if self.ration['amount'] != 'starvation':
            d = {'sperm': -4, 'forage': -1, 'dry': -2, 'canned': 0, 'cousine': 3}
            self.nutrition.satisfaction = d[self.ration['food_type']]
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
                if self.feature('dyspnoea'):
                    self.remove_feature('dyspnoea')
                if ind < 0:
                    ind = 0
                if self.feature('starving'):
                    self.add_feature('dead')
                else:
                    self.add_feature('starving')
                f = flist[ind]
                if f:
                    self.add_feature(f)
                else:
                    self.feature_by_slot('shape').remove()
                self.calorie_storage = 0
                return
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
                self.calorie_storage = 0
    def nutrition_change(self, food_consumed):
        if food_consumed < self.food_demand():
            self.ration["overfeed"] -= 1
            chance = randint(-10, -1)
            if self.ration["overfeed"] <= chance:
                self.ration["overfeed"] = 0

        return

    def know_person(self, person):
        if person in self.known_characters:
            return True
        return False
    def _set_relations(self, person):
        relations = Relations(self, person)
        person._relations.append(relations)
        self._relations.append(relations)
        if not person.know_person(self):
            person.known_characters.append(self)
        if not self.know_person(person):
            self.known_characters.append(person)
        return relations


    def relations(self, person):
        if person==self:
            raise Exception("relations: target and caller is same person")
        if not self.know_person(person):
            relations = self._set_relations(person)
            self._set_stance(person)
            return relations
        for rel in self._relations:
            if self in rel.persons and person in rel.persons:
                return rel
    

    def _set_stance(self, person):
        stance = Stance(self, person)
        self._stance.append(stance)
        person._stance.append(stance)
        if not person.know_person(self):
            person.known_characters.append(self)
        if not self.know_person(person):
            self.known_characters.append(person)
        return stance

    
    def stance(self, person):
        if person==self:
            raise Exception("stance: target and caller is same person")
        elif not self.know_person(person):
            self._set_relations(person)
            stance = self._set_stance(person)
        else:
            for s in self._stance:
                if self in s.persons and person in s.persons:
                    stance = s
        return stance


    def add_reward(self, name, need):
        self.rewards.append((name, need))
    

    def use_token(self, token):
        if self.has_token(token):
            self.tokens.remove(token)
        else:
            return "%s has no token named %s"%(self.name(), token)


    def has_token(self, token):
        if token in self.tokens:
            return True
        return False


    def has_any_token(self):
        if len(self.tokens) > 0:
            return True
        return False

    
    def add_token(self, token):
        if not self.has_token(token):
            self.tokens.append(token)
            self.player_relations().stability += 1
            if token not in ('accordance', 'antagonism'):
                self.relations_tendency[token] += 1
            renpy.call_in_new_context('lbl_notify', self, token)


    def player_relations(self):
        for rel in self._relations:
            if rel.is_player_relations():
                return rel
        return None

    
    def moral_action(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, int):
                self.selfesteem += arg
                return 
        result = self.check_moral(*args, **kwargs)
        self.selfesteem += result
        return result
        

    def check_moral(self, *args, **kwargs):
        result = 0
        act = {'ardent': 1, 'reasonable': 0, 'timid': -1}
        moral = {'good': 1, 'selfish': 0, 'evil': -1}
        order = {'lawful': 1, 'conformal': 0, 'chaotic': -1}
        action_tones = {'activity': None, 'morality': None, 'orderliness': None}
        activity = None
        morality = None
        orderliness = None
        target = None
        
        if 'target' in kwargs:
            if isinstance(kwargs['target'], Person):
                target = kwargs['target']
        
        else:
            for arg in args:
                if isinstance(arg, Person):
                    target=arg
        
        for arg in args:
            if arg in act.keys():
                activity = arg
            if arg in moral.keys():
                morality = arg
            if arg in order.keys():
                orderliness = arg
        for k, v in action_tones.items():
            if v:
                valself = getattr(self.alignment, k)
                valact = v
                if valself != 0:
                    if valself + valact == 0:
                        result -= 1
                    elif abs(valself + valact) == 2:
                        result += 1
                elif target:
                    if valact != 0:
                        if getattr(self.relations(target), Alignment.relation_binding[k]) != valact:
                            result -= 1
                        else:
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
    

    def add_condition(self, name, time=1):
        if not name in self.conditions:
            self.conditions.append((name, time))
        return

    def has_condition(self, name):
        for cond in self.conditions:
            if name in cond:
                return True
        return False


    def tick_conditions(self):
        for cond in self.conditions:
            try:
                cond[1] -= 1
                if cond[1] < 1:
                    self.conditions.remove(cond)
            except TypeError:
                pass

    def enslave(self, target):
        if target.player_controlled:
            target.stance(self).change_stance('master')
        else:
            target.stance(self).change_stance('slave')
        target.master = self
        target.supervisor = self
        self.slaves.append(target)
        self.relations(target)

    def set_supervisor(self, supervisor):
        self.supervisor = supervisor

    def master_stance(self, target):
        if self.player_controlled:
            raise Exception('master_stance is only for npc')
        stance = self.stance(target).level
        l = ['cruel', 'opressive', 'rightful', 'benevolent']
        ind = l.index(stance)
        return ind

    def desirable_relations(self):
        d = {'lawful': ('formal', 'loyality'), 'chaotic': ('intimate', 'scum-slave'),
            'timid': ('delicate', 'worship'), 'ardent': ('intense', 'disciple'),
            'good': ('supporter', 'dedication'), 'evil': ('contradictor', 'henchman')}

        return [d.get(x) for x in self.alignment.description()]

    def willing_available(self):
        if not self.master:
            return []
        rel_check = False
        rel = self.desirable_relations()
        types = [x[1] for x in rel if isinstance(x, tuple)]
        check = [x[0] for x in rel if isinstance(x, tuple)]
        for rel in self.relations(self.master).description():
            if rel in check:
                rel_check = True
                break
        if self.stance(self.master).respect() < self.spirit:
            rel_check = False
        if not self.has_token('accordance'):
            rel_check = False
        if rel_check:
            return types
        else:
            return []


    def attitude_tendency(self):
        n = 0
        token = None
        for k, v in self.relations_tendency.items():
            if v > n:
                n = v
                token = k
        if self.relations_tendency.values().count(n) > 1:
            return None
        return token