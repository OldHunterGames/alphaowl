# -*- coding: UTF-8 -*-


class Relations(object):
    _consideration = ['miserable', 'respectful', 'significant']
    _distance = ['formal', 'close', 'intimate']
    _affection = ['foe', 'associate', 'friend']
    def __init__(self, owner, target):
        self.owner = owner
        self.target = target
        self.consideration = 'respectful'
        self.distance = 'close'
        self.affection = 'associate'
        self._tokens = []

    @property
    def tokens(self):
        return self.owner.relations_tokens(self.target)
    def add_token(self, token):
        if not token in self._tokens:
            self.owner.relations_tokens(self.target).append(token)
 
    def has_token(self, token):
        if token in self.owner.relations_tokens(self.target):
            return True
        return False

    def use_token(self, token):
        if has_token(token):
            self.owner.relations_tokens(self.target).remove(token)
        else:
            return "%s has no token named %s"%(self.owner.name(), token)
    def change(self, axis, direction):
        z = '_%s'%(axis)
        ax = getattr(Relations, z)
        rel = getattr(self, axis)
        ind = ax.index(rel)
        if direction == "+":
            ind += 1
            if ind > 2:
                if axis == 'distance':
                    if self.owner.alignment['orderliness'] == 'chaotic':
                        self.add_token('accordance')
                    elif self.owner.alignment['orderliness'] == 'lawful':
                        self.add_token('antagonism')
                if axis == 'consideration':
                    if self.owner.alignment['activity'] == 'timid':
                        self.add_token('accordance')
                    elif self.owner.alignment['activity'] == 'ardent':
                        self.add_token('antagonism')
                if axis == 'affection':
                    if self.owner.alignment['morality'] == 'good':
                        self.add_token('accordance')
                    elif self.owner.alignment['morality'] == 'evil':
                        self.add_token('antagonism')
                ind = 2
        elif direction == '-':
            ind -= 1
            if ind < 0:
                if axis == 'distance':
                    if self.owner.alignment['orderliness'] == 'chaotic':
                        self.add_token('antagonism')
                    elif self.owner.alignment['orderliness'] == 'lawful':
                        self.add_token('accordance')
                if axis == 'consideration':
                    if self.owner.alignment['activity'] == 'timid':
                        self.add_token('antagonism')
                    elif self.owner.alignment['activity'] == 'ardent':
                        self.add_token('accordance')
                if axis == 'affection':
                    if self.owner.alignment['morality'] == 'good':
                        self.add_token('antagonism')
                    elif self.owner.alignment['morality'] == 'evil':
                        self.add_token('accordance')
                ind = 0
        rel = ax[ind]
        self.__dict__[axis] = rel

    def description(self):
        return (self.consideration, self.distance, self.affection)

