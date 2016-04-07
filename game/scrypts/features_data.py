# -*- coding: UTF-8 -*-
person_features = {
    # base
    'junior': {'slot': 'age', 'modifiers': {'physique': -1, 'spirit': -1, 'mind': -1, 'sensitivity': +1}, 'visible': True},
    'adolescent': {'slot': 'age', 'modifiers': {}, 'visible': True},
    'mature': {'slot': 'age', 'modifiers': {'spirit': +1}, 'visible': True},
    'elder': {'slot': 'age', 'modifiers': {'agility': -1, 'mind': +1}, 'visible': True},

    'sexless': {'slot': 'gender', 'modifiers': {}, 'visible': True},
    'male': {'slot': 'gender', 'modifiers': {'physique': +1, 'sensitivity': -1}, 'visible': True},
    'female': {'slot': 'gender', 'modifiers': {'physique': -1, 'sensitivity': +1}, 'visible': True},
    'shemale': {'slot': 'gender', 'modifiers': {}, 'visible': True},

    # nutrition
    'slim': {'slot': 'shape', 'modifiers': {'nutrition': 1}, 'visible': True},
    'emaciated': {'slot': 'shape', 'modifiers': {'nutrition': 2}, 'visible': True},
    'chubby': {'slot': 'shape', 'modifiers': {'nutrition': -1}, 'visible': True},
    'obese': {'slot': 'shape', 'modifiers': {'nutrition': -1}, 'visible': True},
    'starving': {'slot': None, 'modifiers': {'physique': -1}, 'visible': True},
    'dyspnoea': {'visible': True},
    'diabetes': {'visible': False},

    'dead': {'visible': True},
}


