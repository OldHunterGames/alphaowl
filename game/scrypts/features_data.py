# -*- coding: UTF-8 -*-
from features import *
person_features = {
    'slim': {'slot': 'shape', 'modifiers': {'nutrition': 1}, 'value': 1},
    'emaciated': {'slot': 'shape', 'modifiers': {'nutrition': 2}, 'value': -2},
    'chubby': {'slot': 'shape', 'modifiers': {'nutrition': -1}, 'value': 1},
    'obese': {'slot': 'shape', 'modifiers': {'nutrition': -1}, 'value': 2},
    'starving': {'slot': None, 'modifiers': {'physique': -1}, 'value': 0},
    'dyspnoea': {},
    'diabetes': {},
    'dead': {}
}
