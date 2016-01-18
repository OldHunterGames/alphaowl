# -*- coding: UTF-8 -*-
from features import *
person_features = {
    'slim': Feature(
    name='slim', slot='shape', modifiers={
    'nutrinion': 1}),
    'emaciated': Feature(
    name='emaciated', slot='shape', modifiers={
    'nutrinion': 2
    }),
    'chubby': Feature(
    name='chubby', slot='shape', modifiers={
    'nutrinion': -1
    }),
    'obese': Feature(
    name='obese', slot='shape', modifiers={
    'nutrinion': -1
    }),

}
