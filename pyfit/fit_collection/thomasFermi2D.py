# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:36:45 2014

@author: Alexandre DAREAU
"""

import numpy as np
from pyfit.pyfit_classes import Fit, Value


def pos(x):
    return (0.5 * (np.sign(x) + 1.0))*x
    
def TF(x,y,A,sx,sy,cx,cy):
    return A*pos(1.0-((x-cx)/sx)**2-((y-cy)/sy)**2)**(1.5)
    

# p = [offset, Ampl,sx,sy,cx,cy ]

def ThomasFermi2D((x,y),*p):
    return p[0] + TF(x,y,p[1],p[2],p[3],p[4],p[5])

    
def gen():
        
    fit = Fit()
    fit.formula = ThomasFermi2D
    fit.name = 'ThomasFermi'
    fit.guess = guess
    
    # Values
    Rx = Value(name='Rx',unit='px',formula=Rx_func)
    Ry = Value(name='Ry',unit='px',formula=Ry_func)
    cx = Value(name='cx',unit='px',formula=cx_func)
    cy = Value(name='cy',unit='px',formula=cy_func)
    
    fit.values=(Rx,Ry,cx,cy)
    
    
    return fit

#----------------------------------------------------------------------------
# Values functions

def cy_func(p):
    return p.fit.results[5]
    
def cx_func(p):
    return p.fit.results[4]
    
def Rx_func(p):
    return p.fit.results[1]
    
def Ry_func(p):
    return p.fit.results[2]
    
    
#----------------------------------------------------------------------------
# Guess functions

    
def guess(pf): #takes a pyfit object as input
    
    d = pf.data
    frac = (3.0/4)**(1.5)
    M = d.max()
    m = d.min()
    
    i_cx,i_cy = np.unravel_index(d.argmax(),d.shape)
   
    cx = pf.xm[i_cx,i_cy]
    cy = pf.ym[i_cx,i_cy]
    

    A = M-m
    offset = m
    
    cutX = d[0:i_cx,i_cy]
    cutX = cutX[cutX<(m+M*frac)]
    ix = np.min([cutX.size,pf.xm[0,:].size-1])
    cutx = pf.xm[0,ix]
    sx = 2*np.abs(cx-cutx)
    
    cutY = d[i_cx,0:i_cy]
    cutY = cutY[cutY<(m+M*frac)]
    iy = np.min([cutY.size,pf.ym[:,0].size-1])
    cuty = pf.ym[iy,0]
    sy = 2*np.abs(cy-cuty)
    
    p = [offset, A, sx, sy, cx, cy]
    

    return p

