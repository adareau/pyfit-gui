# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:36:45 2014

@author: Alexandre DAREAU
"""

import numpy as np
import pyfit as pyf
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
    Nint = Value(name = 'Nint',
                 unit = '',
                 format = '%.2e',
                 formula = Nint_func)
    Nfit = Value(name = 'Nfit',
                 unit = '',
                 format = '%.2e',
                 formula = Nfit_func)
    Ncalc = Value(name = 'Ncalc',
                 unit = '',
                 format = '%.2e',
                 formula = Ncalc_func)
    Rx = Value(name='Rx',unit='px',formula=Rx_func)
    Ry = Value(name='Ry',unit='px',formula=Ry_func)
    cx = Value(name='cx',unit='px',formula=cx_func)
    cy = Value(name='cy',unit='px',formula=cy_func)
    
    Rx_mic = Value(name = 'Rx_mic',
                    unit = 'microns',
                    format = '%.2e',
                    formula = Rx_mic_func)
    
    Ry_mic = Value(name = 'Ry_mic',
                    unit = 'microns',
                    format = '%.2e',
                    formula = Ry_mic_func)
    
    fit.values=(Ncalc,Nint,Nfit,Ncalc,Rx,Rx_mic,Ry,Ry_mic,cx,cy)
    
    
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
    
def Rx_mic_func(p):
    return p.fit.results[2]*p.camera.pixel_size_x/p.camera.magnification

def Ry_mic_func(p):
    return p.fit.results[1]*p.camera.pixel_size_y/p.camera.magnification

def Nint_func(pf):
    
    
    pf.compute_background_value()
    
    d = pf.data_fit-pf.picture.background_value #TODO : change fit offset to measured offset (from background)
    
    # V1
    
    x = pf.xm_fit[0,:]*pf.camera.pixel_size_x/pf.camera.magnification*1e-6 # in m
    y = pf.ym_fit[:,0]*pf.camera.pixel_size_y/pf.camera.magnification*1e-6 # in m
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


def Ncalc_func(pf):
    sx = pf.fit.results[2]*pf.camera.pixel_size_x/pf.camera.magnification*1e-6 # in m
    sy = pf.fit.results[3]*pf.camera.pixel_size_y/pf.camera.magnification*1e-6 # in m
    A = pf.fit.results[1]
    sigma0 = pf.atom.sigma0
    
    Ncalc = (2./5.)*np.pi*A*sx*sy/sigma0
    
    return Ncalc  
#----------------------------------------------------------------------------
# Guess functions

def guess(pf):
     
    d = pf.data
    x = pf.xm[0,:]
    y = pf.ym[:,0]
    
    fmodel = pyf.fit1D_dic['TF']
    
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
    A = d.max()-d.min()
    
    p = [offset, A, sx, sy, cx, cy]
    
    
    return p
    
def guess_old(pf): #takes a pyfit object as input
    
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

