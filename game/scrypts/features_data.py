# -*- coding: UTF-8 -*-
from features import *
person_features = {
    'slim': Feature(name='slim', slot='shape', modifiers={'nutrition': 1}, value=-1),
    'emaciated': Feature(name='emaciated', slot='shape', modifiers={'nutrition': 2}, value=-2),
    'chubby': Feature(name='chubby', slot='shape', modifiers={'nutrition': -1}, value=1),
    'obese': Feature(name='obese', slot='shape', modifiers={'nutrition': -1}, value=2),
    'starving': Feature(name='starving', slot=None, modifiers={'physique': -1}),
    'dyspnoea': Feature(name='dyspnoea', slot=None),
    'diabets': Feature(name='diabets', slot=None),
    'dead': Feature(name='dead', slot=None)
}
