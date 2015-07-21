# -*- coding: utf-8 -*-
'''----------------------------------------------------------
  file        : pyfit/fit_collection/boseTF2D.py
  author      : A.  Dareau
  created     : 2015-07-21 09:53
  modified    : 2015-07-21 09:53
  description : 
----------------------------------------------------------'''

import numpy as np
from pyfit.pyfit_classes import DoubleFit, Value

import Bose2D_condensed as b
import thomasFermi2D as tf


# TF = [offset, Ampl,sx,sy,cx,cy ]
#         0      1    2  3  4  5
# Bose_condensed = [offset, Ampl,sx,sy,cx,cy] --> here z=1 !! (BEC)
#                     0      1    2  3  4  5
#
# Combined => [offset, A_bose, sx_bose, sy_bose,  cx , cy, A_tf, Rx_tf, Ry_tf]
#                0       1        2        3       4    5   6      7      8     

def BoseTF2D((x,y),*p):
    bose = b.Bose2D((x,y),p[0],p[1],p[2],p[3],p[4],p[5]) # z=1
    thom_fer = tf.ThomasFermi2D((x,y),0,p[6],p[7],p[8],p[4],p[5])
    return bose+thom_fer
    
def gen():
        
    fit = DoubleFit()
    fit.fit_in = tf.gen()
    fit.fit_out = b.gen()
    fit.name = 'BoseTF'
    fit.formula = BoseTF2D
    fit.guess = guess
    fit.combine = 'add'
    
    fit.params_in = params_in
    fit.params_out = params_out
    
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

# TF = [offset, Ampl,sx,sy,cx,cy ]
#         0      1    2  3  4  5
# Bose = [offset, Ampl,sx,sy,cx,cy, z ]
#           0      1    2  3  4  5  6
#
# Combined => [offset, A_bose, sx_bose, sy_bose,  cx , cy, A_tf, Rx_tf, Ry_tf]
#                0       1        2        3       4    5   6      7      8    
def guess(p1,p2): 
    # combine guesses from first round fit p1 : bose, p2 : TF

    return (p1[0],p1[1],p1[2],p1[3],p1[4],p1[5],p2[1],p2[2],p2[3])

def params_in(p):
    '''
    takes fit results as entry (p), and returns results for inside fit
    '''
    p_in = [0,p[6],p[7],p[8],p[4],p[5]]
    return p_in

def params_out(p):
    '''
    takes fit results as entry (p), and returns results for inside fit
    '''
    p_out = [p[0],p[1],p[2],p[3],p[4],p[5]]
    return p_out