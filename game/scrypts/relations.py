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


    def add_token(self, token):
        self.owner.relations_tokens(self.target).append(token)
 
    def has_token(self, token):
        if token in self.owner.relations_tokens(self.target):
            return True
        return False

    def use_token(self, token):
        if has_token(token):
            self.owner.relations_tokens(self.target).remove(token)
        else:
            return "%s has no token named %s"%(self.owner.description, token)
    def change(self, axis, direction):
        z = '_%s'%(axis)
        ax = getattr(Relation, z)
        rel = getattr(self, axis)
        ind = ax.index(rel)
        if direction == "+":
            ind += 1
            if ind > 2:
                ind = 2
        elif direction == '-':
            ind -= 1
            if ind < 0:
                ind = 0
        rel = ax[ind]
        self.__dict__[axis] = rel

