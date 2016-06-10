# -*- coding: UTF-8 -*-


class Stance(object):
    _types = {'master': ['cruel', 'opressive', 'rightful', 'benevolent'],
            'slave': ['rebellious', 'forced', 'accustomed', 'willing'],
            'neutral': ['hostile', 'distrustful', 'favorable', 'friendly']}
    _ax = {0: ['dependence', 'craving', 'attraction'], 1: ['discipline', 'confidence', 'reliance'],
            2: ['dread', 'compassion', 'kindness']}
    _types_stats = {'master': ['dread', 'discipline', 'dependence'],
                    'slave': ['craving', 'confidence', 'compassion'],
                    'neutral': ['attraction', 'reliance', 'kindness']}
    def __init__(self, owner, target):
        self.owner = owner
        self.target = target
        self.characters = [self.owner, self.target]
        self._type = 'neutral'
        self._value = 0
        self._points = [0, 0, 0]
        self._special_value = None

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
        if not self.target.player_controlled:
            self.target.stance(self.owner)._value = value
        if self._value < -1:
            self._value = -1

        elif self._value > 1:
            self._value = 1

    def to_max(self, value=None):
        self._value = 2
        if self.target.player_controlled:
            self._special_value = value


    @property
    def type(self):
        return self._type

    @property
    def level(self):
        if self.value == 2 and self.target.player_controlled:
            return self._special_value
        return Stance._types[self._type][self.value+1]

    
    def set_level(self, value):
        wrong = True
        for key in Stance._types:
            if value in Stance._types[key]:
                if self._type == key:
                    self._value = Stance._types[key].index(value)-1
                    wrong = False
                    break
                else:
                    raise Exception("Wrong value(%s) for %s type of stance"%(value, self.type))
        if wrong:
            raise Exception("Unknown value %s"%(value))

    
    def add_point(self, axis, value=1):
        ind = None
        for key in Stance._types_stats:
            if axis in Stance._types_stats[key] and self._type!=key:
                raise Exception("Wrong axis for this type of relations: %s, %s"%(self.type, axis))
        for key in Stance._ax.keys():
            if axis in Stance._ax[key]:
                ind = key
                break
        if not ind:
            raise Exception("Wrong axis: %s"%(axis))
        self._points[ind] += value
    
    def points(self, axis):
        ind = None
        for key in Stance._types_stats:
            if axis in Stance._types_stats[key] and self._type!=key:
                raise Exception("Wrong axis for this type of relations: %s, %s"%(self.type, axis))
        for key in Stance._ax.keys():
            if axis in Stance._ax[key]:
                ind = key
                break
        return self._points[ind]

    def respect(self):
        alig_relations = {'lawful': self._points[1]*2, 'conformal': self._points[1], 'chaotic': self._points[1]/2,
                            'timid': self._points[0]*2, 'reasonable': self._points[0], 'ardent': self._points[0]/2,
                            'evil': self._points[2]*2, 'selfish': self._points[2], 'good': self._points[2]/2}
        alig = self.owner.alignment.values()
        val = 0
        for i in alig:
            val += alig_relations[i]
        if not self.target.player_controlled:
            values = {-1:0, 0:1, 1:5, 2:10}
            return values[self.value]   
        return val


    def change_stance(self, stance):
        if stance not in Stance._types.keys():
            raise Exception("Wrong stance: %s"%(t))
        else:
            self._type = stance
            self._points = [0, 0, 0]
            self._value = 0


