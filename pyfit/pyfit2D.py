# -*- coding: utf-8 -*-
#-------------------------------------#
# file        : pyfit.py
# author      : A. Dareau
# version     : 11/2014
# description : Implements the PyFit class
#-------------------------------------#

import numpy as np
import matplotlib.pyplot as plt
import os 
import pylab as pl
import scipy.optimize as opt
import copy

from cPickle import dump

from matplotlib.patches import Rectangle

from pyfit_classes import *
from pyfit_functions import *
from EditableRectangle import EditableRectangle

# Main fit Object : PyFit

class PyFit2D():
    
    def __init__(self):
        
        self.camera = Camera()
        self.picture = Picture()
        self.fit = Fit()
        self.atom = Atom()
        
        self.data = []
        self.xm = []
        self.ym = []
        
        self.data_fit = []
        self.xm_fit = []
        self.ym_fit = []
        
        self.values = {}
        
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
        
        
        
        # Guesses
        pf_guess = copy.deepcopy(self)
        pf_guess.data = data_fit
        pf_guess.xm = xm
        pf_guess.ym = ym
        
        guess = self.fit.guess(pf_guess)
        
        
        
        data_fit_rav = data_fit.ravel()    
        fit_func = lambda (x,y),*p:self.fit.formula((x,y),*p).ravel()
        
        
        popt, pcov = opt.curve_fit(fit_func, (xm, ym), data_fit_rav, p0=guess, maxfev=self.fit.options.max_func_eval)
        
        self.data_fit = data_fit
        self.xm_fit = xm
        self.ym_fit = ym
        
        self.fit.results=popt
        
        
        return 0
     
    def print_values(self):
        
        for v in self.fit.values:
            c = v.formula(self)
            s = '-- '+v.name+' = '+v.format+' '+v.unit
            print(s%c)
    
    def values_to_str(self):
        if not self.values:
            self.compute_values()
            
        out = ''        
        for v in self.fit.values:
            c = self.values[v.name]
            s = '-- '+v.name+' = '+v.format+' '+v.unit
            s = s%c
            out = out+s+'\n'
        
        return out
            
    def compute_values(self):
        for v in self.fit.values:
            c = v.formula(self)
            self.values[v.name] = c
            
    def ask_ROI(self):
        
        if self.data == []:return
        
        plt.figure()
        r = self.picture.ROI
        
        ROI = Rectangle((r[0],r[2]), r[1]-r[0],r[3]-r[2] ,alpha=1,fc='none',ec='green',linewidth=5)
        plt.imshow(self.data,extent=(self.xm.min(), self.xm.max(), self.ym.max(), self.ym.min()))
        plt.gca().add_patch(ROI)
        
        ed_ROI = EditableRectangle(ROI,fixed_aspect_ratio=False)
        ed_ROI.connect()
        
        plt.show()
        
        self.picture.ROI = (ROI.xy[0],ROI.xy[0]+ROI.get_width(),ROI.xy[1],ROI.xy[1]+ROI.get_height())
        

    def generate_xy_fit_mesh(self):

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
        
        
        
        self.data_fit = data_fit
        self.xm_fit = xm
        self.ym_fit = ym
        

        
        
        return 0
        
    ''' Data related methods ''' 
    
    def load_data(self,f=None):
        """
        if no f argument is given, we use the filename stored in .picture
        else f must be path to file, and we update .picture accordingly
        """
        if f==None:
            f = os.path.join(self.picture.path,self.picture.filename)
        else:
            self.picture.path = os.path.split(f)[0]
            self.picture.filename = os.path.split(f)[1]
            
        if not os.path.isfile(f): return 0
        data = pl.imread(f)
        
        # HINT : some pictures are saved in RGB, then we only take one layer
        if len(data.shape)>2: data = data[:,:,0]
        
        if self.camera.OD_conversion=='pickled_lambda':
            self.camera.update_OD_conversion()
            
        data = self.camera.OD_conversion(data)
        
        
        nx = np.size(data,1)
        ny = np.size(data,0)
        
        x = np.arange(0,nx)
        y = np.arange(0,ny)
        
        xm, ym = np.meshgrid(x,y)
        
        if self.picture.ROI == []:
            self.picture.ROI = (xm.min(),xm.max(),ym.min(),ym.max())
        
        self.xm = xm
        self.ym = ym
        self.data = data
        
        self.picture.parseVariables()
    
        return 1
    
    ''' Saving '''
    
    def save_fit(self):
        f = os.path.join(self.picture.path,'.fits')
        if not os.path.isdir(f):
            os.mkdir(f)
        
        fname = self.picture.filename
        fname = fname[0:len(fname)-4]+'.fit'
        
        f=os.path.join(f,fname)
        fit = copy.deepcopy(self)
        
        fit.data = []
        fit.xm = []
        fit.ym = []
        fit.data_fit = []
        fit.xm_fit = []
        fit.ym_fit = []
        fit.camera.OD_conversion='pickled_lambda'
        
        with open(f, 'wb') as output:
            dump(fit, output)

        
        return

    
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