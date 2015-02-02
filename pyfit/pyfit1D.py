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

from pyfit_classes import *
from pyfit_functions import *

# Main fit Object : PyFit

class PyFit1D():
    
    def __init__(self,**kwargs):
        
        #self.camera = Camera()
        #self.picture = Picture()
        #self.atom = Atom()
        self.fit = kwargs.get('fit',Fit())
        self.x = kwargs.get('x',[])
        self.y = kwargs.get('y',[])
        
        self.values = {}
        
    def do_fit(self):

        
        
        x = self.x
        y = self.y
        
        if self.fit.options.do_binning:
            
            n = np.size(x)
            
            if self.fit.options.auto_binning:
                b = np.max([1,n//self.fit.options.binning_maxpoints]) 
            else:
                b = self.fit.options.binning
                   
            i = (n//b)*b


            x = x[0:i]
            y = y[0:i]

            x = rebin(x,(n//b,1))
            y = rebin(y,(n//b,1))

        
        # guesses
        pf_guess = copy.deepcopy(self)
        pf_guess.x = x
        pf_guess.y = y
        
        guess = self.fit.guess(pf_guess)
        
        fit_func = self.fit.formula
        popt, pcov = opt.curve_fit(fit_func, x, y, p0=guess, maxfev=self.fit.options.max_func_eval)
        '''
        try:
            popt, pcov = opt.curve_fit(fit_func, x, y, p0=guess, maxfev=self.fit.options.max_func_eval)
        
        except RuntimeError:
            print("Error - curve_fit failed")
            popt=guess
        '''
        self.fit.results=popt
        
        
        
    
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
            
    def print_values(self):
        
        for v in self.fit.values:
            c = v.formula(self)
            s = '-- '+v.name+' = '+v.format+' '+v.unit
            print(s%c)
            
    def plot(self):
        
        x = self.x
        y = self.y
        
        x_fit = np.linspace(x.min(),x.max(),1e3)
        y_fit = self.fit.formula(x_fit,*self.fit.results)
        
        plt.figure()
        plt.plot(x,y,'or')
        plt.plot(x_fit,y_fit,'b')
        plt.show()
       
       
    def run(self):
        
        self.do_fit()
        self.print_values()
        self.plot()
        
        



    
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