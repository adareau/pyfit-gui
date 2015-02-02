# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:36:45 2014

@author: Alexandre DAREAU

Fit name        : gaussWaist
Description     : gaussian beam waist propagation (1D)
Fit parameters  : w0 -> 1/e**2 radius (m)
                  z0 -> waist position (m)
    
Fixed param.    : lbda -> laser wavelength (m)
"""

import numpy as np
from pyfit.pyfit_classes import Fit, Value





# Parameters p = [w0,z0]
def GaussWaist(z,w0,z0,lbda):
    zr = np.pi*w0**2/lbda
    return w0*np.sqrt(1+((z-z0)/zr)**2)

def GaussWaistGenerator(params,z,*p):
    lbda = params['lambda']
    #return GaussWaist(z,p[0],p[1],lbda)
    return GaussWaist(z,p[0],p[1],lbda)
    
def gen():
        
    fit = Fit()
    fit.name = 'GaussWaist'
    fit.parameters = {'lambda':760.0e-9}
    fit.formula_parameters = GaussWaistGenerator
    fit.updateFormulaFromParameters1D()
    fit.guess = guess
    
    
    # Values
    w0 = Value(name = 'w0',
               formula = lambda p:p.fit.results[0],
               unit='m',
               format = '%0.3e')
    z0 = Value(name = 'z0',formula = lambda p:p.fit.results[1],
               unit='m',
               format = '%0.3e')
    zr = Value(name = 'zr',formula = lambda p:p.fit.results[0]**2*np.pi/p.fit.parameters['lambda'],
               unit='m',
               format = '%0.3e')


    
    fit.values=(w0,z0,zr)
    
    
    return fit
    
def guess(pf): #takes a pyfit1D object as input
    
    x = pf.x
    y = pf.y
    
    w0 = y.min()
    
    i_c = y.argmin()
    z0 = x[i_c]
    

    p = [w0,z0]
    

    return p

