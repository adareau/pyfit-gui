# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:36:45 2014

@author: Alexandre DAREAU
"""

import numpy as np
from pyfit.pyfit_classes import Fit, Value
import gauss2D as g2D

#p = [offset, Ampl,sx,sy,cx,cy,theta]

def GaussTilted((x,y),*p):
    theta = np.mod(p[-1]*2.0*np.pi/360.0,2*np.pi)
    
    xr = (x-p[4])*np.cos(theta)+(y-p[5])*np.sin(theta)
    yr = (y-p[5])*np.cos(theta)-(x-p[4])*np.sin(theta)
    pnew = [p[0],p[1],p[2],p[3],0,0]
    
    return g2D.Gauss2D((xr,yr),*pnew)
    
    
   
def gen():
        
    fit = g2D.gen()
    fit.formula = lambda(x,y),*p:GaussTilted((x,y),*p)
    fit.name = 'GaussTilted'
    fit.guess = guess
    
    values = fit.values
    theta = Value(name='angle',unit='deg',formula=lambda p:np.mod(p.fit.results[6],180))
    
    fit.values = values+(theta,)
    
    return fit
    
def guess(pf): #takes a pyfit object as input
    
    p = g2D.guess(pf)
    p.append(0)
    

    return p

