# -*- coding: utf-8 -*-
#-------------------------------------#
# file        : pyfit.py
# author      : A. Dareau
# version     : 11/2014
# description : Implements the PyFit class
#----------------------------s---------#

import numpy as np
import matplotlib.pyplot as plt
import os 
import pylab as pl
import scipy.optimize as opt
import copy

from matplotlib.patches import Rectangle

from pyfit_classes import *
from pyfit_functions import *
from EditableRectangle import EditableRectangle

import pyfit2D as pf

# Main fit Object : PyDoubleFit

class PyDoubleFit2D(pf.PyFit2D):
    
    def __init__(self):
        
        self.camera = Camera()
        self.picture = Picture()
        self.atom = Atom()
        
        self.fit = DoubleFit()
        
        self.hole = []
        self.data = []
        self.xm = []
        self.ym = []
        
        self.data_fit = []
        self.xm_fit = []
        self.ym_fit = [] 
        
    ''' Fit related methods ''' 
    
            
        
    def do_fit(self):

        if self.data == []:
            self.load_data()
        
        
        xm = self.xm
        ym = self.ym
        data_fit = self.data
        
        # Region of Interest :
        
        if self.fit.options.askROI: self.ask_ROI()
        
        x = xm[1,:]
        y = ym[:,1]
        
        ix_start = x[x<=self.picture.ROI[0]].argmax()
        ix_stop = x[x<=self.picture.ROI[1]].argmax()
        iy_start = y[y<=self.picture.ROI[2]].argmax()
        iy_stop = y[y<=self.picture.ROI[3]].argmax()
        
        xm = xm[iy_start:iy_stop,ix_start:ix_stop]
        ym = ym[iy_start:iy_stop,ix_start:ix_stop]
        data_fit = data_fit[iy_start:iy_stop,ix_start:ix_stop]
        
        
        # Binning 
        
        if self.fit.options.do_binning:
            
            # ROI 
            
            nx = np.size(xm,0)
            ny = np.size(xm,1)
            
            if self.fit.options.auto_binning:
                bx = np.max([1,nx//self.fit.options.binning_maxpoints]) 
                by = np.max([1,ny//self.fit.options.binning_maxpoints])
            else:
                bx = self.fit.options.binning
                by = bx
                    
            
            ix = (nx//bx)*bx
            iy = (ny//by)*by

            xm = xm[0:ix,0:iy]
            ym = ym[0:ix,0:iy]
            data_fit = data_fit[0:ix,0:iy]
            xm = rebin(xm,(nx//bx,ny//by))
            ym = rebin(ym,(nx//bx,ny//by))
            data_fit = rebin(data_fit,(nx//bx,ny//by))
            
        
        # Hole
        
        if self.fit.options.askHole or self.hole==[]:self.ask_Hole()
        
        x = xm[1,:]
        y = ym[:,1]
        
        ix_start = x[x<=self.hole[0]].argmax()
        ix_stop = x[x<=self.hole[1]].argmax()
        iy_start = y[y<=self.hole[2]].argmax()
        iy_stop = y[y<=self.hole[3]].argmax()
        
        xhole = xm[iy_start:iy_stop,ix_start:ix_stop]
        yhole = ym[iy_start:iy_stop,ix_start:ix_stop]
        data_hole = data_fit[iy_start:iy_stop,ix_start:ix_stop]  
        
        # Guesses
        
        if self.fit.options.fit_hole_first:
            
            p_hole = pf.PyFit2D()
            p_hole.fit = self.fit.fit_in
            p_hole.data = data_hole-np.min(data_hole)
            p_hole.xm = xhole
            p_hole.ym = yhole
            p_hole.picture.ROI = [xhole.min(),xhole.max(),yhole.min(),yhole.max()]
            p_hole.do_fit()
            
            guess_in = p_hole.fit.results
            hole_fit = p_hole.fit.formula((xm,ym),*guess_in)
            
            if self.fit.combine == 'add':
                data_out = data_fit-hole_fit
            else:
                data_out = data_fit
            
            p_out = pf.PyFit2D()
            p_out.fit = self.fit.fit_out
            p_out.data = data_out
            p_out.xm = xm
            p_out.ym = ym
            p_out.picture.ROI = [xm.min(),xm.max(),ym.min(),ym.max()]
            p_out.do_fit()
            
            guess_out = p_out.fit.results
        

        
        guess = self.fit.guess(guess_out,guess_in)
        
        
        
        data_fit = data_fit.ravel()    
        fit_func = lambda (x,y),*p:self.fit.formula((x,y),*p).ravel()
        

        popt, pcov = opt.curve_fit(fit_func, (xm, ym), data_fit, p0=guess)
        
        self.data_fit = data_fit
        self.xm_fit = xm
        self.ym_fit = ym
        self.fit.results=popt
        
        
        return 0
     
    def ask_Hole(self):
        
        if self.data == []:return
        if self.picture.ROI ==[]:return
        
        if self.hole == []: self.hole=self.picture.ROI
        xm = self.xm
        ym = self.ym
        data_fit = self.data
        
        # Restrict to region of Interest :
        
        x = xm[1,:]
        y = ym[:,1]
        
        ix_start = x[x<=self.picture.ROI[0]].argmax()
        ix_stop = x[x<=self.picture.ROI[1]].argmax()
        iy_start = y[y<=self.picture.ROI[2]].argmax()
        iy_stop = y[y<=self.picture.ROI[3]].argmax()
        
        xm = xm[iy_start:iy_stop,ix_start:ix_stop]
        ym = ym[iy_start:iy_stop,ix_start:ix_stop]
        data_fit = data_fit[iy_start:iy_stop,ix_start:ix_stop]
           
        plt.figure('Hole')
        r = self.hole
        
        hole = Rectangle((r[0],r[2]), r[1]-r[0],r[3]-r[2] ,alpha=1,fc='none',ec='red',linewidth=2)
        plt.imshow(data_fit,extent=(xm.min(), xm.max(), ym.max(), ym.min()))
        plt.gca().add_patch(hole)
        
        ed_hole = EditableRectangle(hole,fixed_aspect_ratio=False)
        ed_hole.connect()
        
        plt.show()
        
        self.hole = (hole.xy[0],hole.xy[0]+hole.get_width(),hole.xy[1],hole.xy[1]+hole.get_height())

    
        
    


    
 # TEST
'''
path = '/home/alex/Thèse/Programmation/Python/Fits/'
name = '1.png'
pic = Picture()

pic.filename=name
pic.path=path
pic.load()

plt.figure()
plt.imshow(pic.data)
plt.show()
   '''     