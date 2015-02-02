# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:54:08 2014

@author: Alexandre DAREAU
"""


import matplotlib.pyplot as plt
import inspect
import os
import numpy as np

import pyfit as pf

path =  os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#

fmodel = pf.fit1D_dic['GaussDeriv']

x = np.linspace(-10,10,1e3)
p = [0.5,2,-1.4,2.6]

y = fmodel.formula(x,*p)
y = y + 0.1*np.random.normal(size=y.shape)


fit = pf.PyFit1D(fit=fmodel,x=x,y=y)


fit.fit.options.do_binning=False
fit.fit.options.auto_binning = True
fit.fit.options.binning = 5

guess = fmodel.guess(fit)

fit.do_fit()
fit.print_values()

fit_res = fit.fit.formula(x,*fit.fit.results)
fit_guess = fit.fit.formula(x,*guess)

plt.figure('pyfit test')
plt.clf()
plt.plot(x,y,'r')
plt.plot(x,fit_res,'b',dashes=[1,1])
plt.plot(x,fit_guess,'k')
plt.show()