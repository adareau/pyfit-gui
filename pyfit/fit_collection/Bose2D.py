# -*- coding: utf-8 -*-
"""
Created on 16/07/2015

@author: Alexandre DAREAU
"""

import numpy as np

import pyfit as pyf
from pyfit.pyfit_classes import Fit, Value



def Gauss(x,A,sigma,c):
    return A*np.exp(-(x-c)**2/2/sigma**2)
    

# p = [offset, Ampl,sx,sy,cx,cy,z ] (z=fugacity)

def Bose2D((x,y),*p):
    g2_argument =  Gauss(x,1,p[2],p[4])*Gauss(y,1,p[3],p[5])*np.exp(p[6])
    
    return p[0] + p[1]*g2(g2_argument)

    
def gen():
        
    fit = Fit()
    #fit.formula = lambda(x,y),*p:Gauss2D((x,y),*p)
    fit.formula = Bose2D
    fit.name = 'Bose'
    fit.guess = guess
    
    # Values
    
    Ncalc = Value(name = 'Ncalc',
                 unit = '',
                 format = '%.2e',
                 formula = Ncalc_func)
    
    Nint = Value(name = 'Nint',
                 unit = '',
                 format = '%.2e',
                 formula = Nint_func)
    Nfit = Value(name = 'Nfit',
                 unit = '',
                 format = '%.2e',
                 formula = Nfit_func)
                 
    sigma_x = Value(name = 'sx',
                    unit = 'px',
                    format = '%.1f',
                    formula = sx_func)
    
    sigma_x_mic = Value(name = 'sx_mic',
                    unit = 'microns',
                    format = '%.1f',
                    formula = sx_mic_func)
    
    sigma_y = Value(name = 'sy',
                    unit = 'px',
                    format = '%.1f',
                    formula = sy_func)
                    
    sigma_y_mic = Value(name = 'sy_mic',
                    unit = 'microns',
                    format = '%.1f',
                    formula = sy_mic_func)
     
    cx = Value(name='cx',unit='px',formula=cx_func)
    cy = Value(name='cy',unit='px',formula=cy_func)
    z = Value(name='z (fugacity)',unit='',formula=z_func)
    
    fit.values=(Ncalc,Nint,Nfit,sigma_x,sigma_x_mic,sigma_y,sigma_y_mic,cx,cy,z)
    
    
    return fit
  
#----------------------------------------------------------------------------
# Values functions

def z_func(p):
    return p.fit.results[6]

def sx_func(p):
    return p.fit.results[2]

def sx_mic_func(p):
    return p.fit.results[2]*p.camera.pixel_size_x/p.camera.magnification

def sy_func(p):
    return p.fit.results[3]
    
def cy_func(p):
    return p.fit.results[5]
    
def cx_func(p):
    return p.fit.results[4]

def sy_mic_func(p):
    return p.fit.results[3]*p.camera.pixel_size_y/p.camera.magnification
   
def Ncalc_func(pf):
    sx = pf.fit.results[2]*pf.camera.pixel_size_x/pf.camera.magnification*1e-6 # in m
    sy = pf.fit.results[3]*pf.camera.pixel_size_y/pf.camera.magnification*1e-6 # in m
    A = pf.fit.results[1]
    sigma0 = pf.atom.sigma0
    
    Ncalc = 2*np.pi*sx*sy*A/sigma0
    
    return Ncalc

def Nint_func(pf):
    
    d = pf.data-pf.fit.results[0] #TODO : change fit offset to measured offset (from background)
    
    # V1
    
    x = pf.xm[0,:]*pf.camera.pixel_size_x/pf.camera.magnification*1e-6 # in m
    y = pf.ym[:,0]*pf.camera.pixel_size_y/pf.camera.magnification*1e-6 # in m
    sigma0 = pf.atom.sigma0
    
    d_int = abs(np.trapz(np.trapz(d,x=x,axis=1),x=y.T))
    
    # V2
    '''
    x = pf.xm[0,:]
    y = pf.ym[:,0]
    
    xbin = abs(x[1]-x[0])
    ybin = abs(y[1]-y[0])
    
    d_int2 = np.sum(np.sum(d))*xbin*ybin*pf.camera.pixel_size_x*pf.camera.pixel_size_y/pf.camera.magnification**2*1e-12
    '''
    
    Nint = d_int/sigma0
    
    return Nint

def Nfit_func(pf):
    
    x = pf.xm
    y = pf.ym
    p = np.append([0],pf.fit.results[1:])
    d = pf.fit.formula((x,y),*p)
    
    # V1
    
    x = x[0,:]*pf.camera.pixel_size_x/pf.camera.magnification*1e-6 # in m
    y = y[:,0]*pf.camera.pixel_size_y/pf.camera.magnification*1e-6 # in m
    sigma0 = pf.atom.sigma0
    
    d_int = abs(np.trapz(np.trapz(d,x=x,axis=1),x=y.T))
    
    Nfit = d_int/sigma0
    
    return Nfit
        
#----------------------------------------------------------------------------
# Guess function :
    
def guess(pf):
     
    d = pf.data
    x = pf.xm[0,:]
    y = pf.ym[:,0]
    
    fmodel = pyf.fit1D_dic['Gauss']
    
    fitx = pyf.PyFit1D(fit=fmodel,x=x,y=d.sum(0))
    fitx.do_fit()
    px = fitx.fit.results
    
    sx = px[2]
    cx = px[3]
    Ax = px[1]*np.diff(x).mean()/np.sqrt(2*np.pi)/sx
        
    
    fity = pyf.PyFit1D(fit=fmodel,x=y,y=d.sum(1))
    fity.do_fit()
    py = fity.fit.results
    
    sy = py[2]
    cy = py[3]
    Ay = py[1]*np.diff(y).mean()/np.sqrt(2*np.pi)/sy
    
    offset = d.min()
    A = (Ay+Ax)/2.0
    
    z = 0.01 # wa assume low fugacity
    p = [offset, A, sx, sy, cx, cy, z]
    
    
    return p

def g2(z):
    clip = 1e-10
    z=np.clip(z,-np.inf,1-clip)
    return np.real((1-z)*np.log(1-z)+1.98*z-0.16*z**2-0.17*z**3)
