# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 21:39:47 2014

@author: alex
"""

import numpy as np
from pyfit.pyfit_classes import Fit, Value



def GaussDer(x,A,sigma,c):
    return -A*(x-c)/sigma*np.exp(-(x-c)**2/2/sigma**2)
    
'''
def Gauss2D((x,y),A,sx,sy,cx,cy):
    return A*Gauss(x,1,sx,cx)*Gauss(y,1,sy,cy)
'''
# p = [offset, Ampl,s,c]


def Gauss1D(x,*p):
    return p[0] + p[1]*GaussDer(x,1,p[2],p[3])

    
def gen():
        
    fit = Fit()
    fit.formula = Gauss1D
    fit.name = 'GaussDeriv'
    fit.guess = guess
    
    # Values
    sigma = Value(name = 'sigma',formula = lambda p:np.abs(p.fit.results[2]))
    center = Value(name = 'center',formula = lambda p:p.fit.results[3])
    amp = Value(name = 'amplitude',formula = lambda p:p.fit.results[1])
    offset = Value(name = 'offset',formula = lambda p:p.fit.results[0] )

    
    fit.values=(sigma,center,amp,offset)
    
    
    return fit
    
def guess(pf): #takes a pyfit1D object as input
    
    x = pf.x
    y = pf.y
    
    e = np.exp(1)
    M = y.max()
    m = y.min()
    
    i_M = y.argmax()
    i_m = y.argmin()
    c = (x[i_M]+x[i_m])/2.0
    s = (x[i_m]-x[i_M])/2.0
    

    

    A = (M-m)*e**0.5/2
    offset = (M+m)/2.0
    

    
    
    p = [offset, A, s, c]
    

    return p

