# -*- coding: UTF-8 -*-
from features import *
person_features = {
    'slim': Feature(name='slim', slot='shape', modifiers={'nutrition': 1}),
    'emaciated': Feature(name='emaciated', slot='shape', modifiers={'nutrition': 2}),
    'chubby': Feature(name='chubby', slot='shape', modifiers={'nutrition': -1}),
    'obese': Feature(name='obese', slot='shape', modifiers={'nutrition': -1}),
}
