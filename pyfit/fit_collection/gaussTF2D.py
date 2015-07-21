# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:36:45 2014

@author: Alexandre DAREAU
"""

import numpy as np
from pyfit.pyfit_classes import DoubleFit, Value

import gauss2D as g
import thomasFermi2D as tf


# TF,Gauss = [offset, Ampl,sx,sy,cx,cy ]
# Combined => [offset, A_gauss, sx_gauss, sy_gauss, cx, cy, A_tf, Rx_tf, Ry_tf]
def GaussTF2D((x,y),*p):
    gauss = g.Gauss2D((x,y),p[0],p[1],p[2],p[3],p[4],p[5])
    thom_fer = tf.ThomasFermi2D((x,y),0,p[6],p[7],p[8],p[4],p[5])
    return gauss+thom_fer
    
def gen():
        
    fit = DoubleFit()
    fit.fit_in = tf.gen()
    fit.fit_out = g.gen()
    fit.name = 'GaussTF'
    fit.formula = GaussTF2D
    fit.guess = guess
    fit.combine = 'add'
    # Values

    cx = Value(name='cx',unit='px',formula=cx_func)
    cy = Value(name='cy',unit='px',formula=cy_func)
    
    fit.values=(cx,cy)
    
    
    return fit

   
#----------------------------------------------------------------------------
# Values functions

def cy_func(p):
    return p.fit.results[5]
    
def cx_func(p):
    return p.fit.results[4]
    
    
#----------------------------------------------------------------------------
# Guess functions

def guess(p1,p2): 
    # combine guesses from first round fit p1 : gauss, p2 : TF
    #return (p1[0],p1[1],p1[2],p1[3],p1[4],p1[5],p2[1],p2[3],p2[4])#old (error ?)
    return (p1[0],p1[1],p1[2],p1[3],p1[4],p1[5],p2[1],p2[2],p2[3])