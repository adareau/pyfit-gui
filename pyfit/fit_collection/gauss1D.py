# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:36:45 2014

@author: Alexandre DAREAU
"""

import numpy as np
from pyfit.pyfit_classes import Fit, Value



def Gauss(x,A,sigma,c):
    return A*np.exp(-(x-c)**2/2/sigma**2)
    
'''
def Gauss2D((x,y),A,sx,sy,cx,cy):
    return A*Gauss(x,1,sx,cx)*Gauss(y,1,sy,cy)
'''
# p = [offset, Ampl,s,c]


def Gauss1D(x,*p):
    return p[0] + p[1]*Gauss(x,1,p[2],p[3])

    
def gen():
        
    fit = Fit()
    fit.formula = Gauss1D
    fit.name = 'Gauss'
    fit.guess = guess
    
    # Values
    sigma = Value(name = 'sigma',formula = lambda p:p.fit.results[2])
    center = Value(name = 'center',formula = lambda p:p.fit.results[3])
    amp = Value(name = 'amplitude',formula = lambda p:p.fit.results[1])
    offset = Value(name = 'offset',formula = lambda p:p.fit.results[0] )

    
    fit.values=(sigma,center,amp,offset)
    
    
    return fit
    
def guess(pf): #takes a pyfit1D object as input
    
    x = pf.x
    y = pf.y
    
    e = np.exp(1.0)
    M = y.max()
    m = y.min()
    
    i_c = y.argmax()
    c = x[i_c]
    

    

    A = M-m
    offset = m
    
    outside = y[0:i_c]
    outside = outside[outside<(m+M/e)]
    
    cut = x[outside.size]
    s = np.abs(c-cut)/np.sqrt(2.0)
    
    if s == 0:
        s = (x.max()-x.min())/10 # This is really (REALLY) ugly fix..
        
    p = [offset, A, s, c]
    

    return p

