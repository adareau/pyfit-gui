# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 15:18:25 2014

@author: alex
"""

import pyfit as pf

a = pf.pyfit_classes.Value(name = 'a', formula = lambda x:0)
b = pf.pyfit_classes.Value(name = 'b', formula = lambda x:1)

ls = (a,b)

for v in ls:
    if v.name == 'a':
        v.formula = lambda x:3


