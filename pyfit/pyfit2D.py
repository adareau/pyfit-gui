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
import h5py

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
        
        self.type = 'pyfit2D'
        
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

        # TEST
        f = f[0:-4]+'.hdf5'
        self.fit_to_hdf5(f)
        
        return
        
        
    def fit_to_hdf5(self, fname):
        """
        converts the fit object (self) into a hdf5 format
        
        Structure :
        
        hdf5
        ├─ general
        |   └─ type (pyfit2D ? pydoublefit2D ?)
        |
        ├─ values
        |   └─ values (dic, stored in attributes)
        |
        ├─ fit
        |   ├─ name (str)
        |   ├─ parameters (dict)
        |   ├─ formula_parameters (lbda...)
        |   ├─ guess (lbda)
        |   ├─ results (array)
        |   └─ values (lbda)
        | 
        ├─ fit_options
        |   ├─ do_binning (bool)
        |   ├─ binning (int)
        |   ├─ auto_binning (bool)
        |   ├─ binning_maxpoint (int)
        |   ├─ askROI (bool)
        |   ├─ fit_hole_first (bool)
        |   ├─ askHole (bool)
        |   └─  max_func_eval (int)
        |
        ├─ camera 
        |   ├─ magnification (float)
        |   ├─ rotate (float)
        |   ├─ pixel_size_x (float)
        |   ├─ pixel_size_y (float)
        |   ├─ OD_conversion (str = 'pickled_lambda')
        |   ├─ OD_conversion_formula (str)
        |   ├─ image_size (tuple)
        |   └─ image_ext (str)
        |
        ├─ picture
        |   ├─ filename (str)
        |   ├─ path (str)
        |   ├─ variables (dict)
        |   ├─ ROI (tuple)
        |   └─ background (tuple)
        |
        └─ atom
            ├─ name (str)
            ├─ fluo (bool)
            ├─ lbda (float)
            └─ sigma0 (float)
         
        """
        
        with h5py.File(fname,"w") as f:
            
            # general data
            dset = f.create_dataset("general", (0,), dtype='i')
            dset.attrs['type'] = self.type
                    
            # pyfit2D self properties save
            dset = f.create_dataset("values", (0,), dtype='i')
            if self.values:
                for key, val in self.values.iteritems():
                    dset.attrs[key] = val
                    
            # fit
            dset = f.create_dataset("fit", (0,), dtype='i')
            dset.attrs['name'] = self.fit.name
            dset.attrs['results'] = self.fit.results
            
            # fit_options
            dset = f.create_dataset("fit_options", (0,), dtype='i')
            dset.attrs['do_binning'] = self.fit.options.do_binning
            dset.attrs['binning'] = self.fit.options.binning
            dset.attrs['auto_binning'] = self.fit.options.auto_binning
            dset.attrs['binning_maxpoints'] = self.fit.options.binning_maxpoints
            dset.attrs['askROI'] = self.fit.options.askROI
            dset.attrs['fit_hole_first'] = self.fit.options.fit_hole_first
            dset.attrs['askHole'] = self.fit.options.askHole
            dset.attrs['max_func_eval'] = self.fit.options.max_func_eval
            
            # camera
            dset = f.create_dataset("camera", (0,), dtype='i')
            dset.attrs['magnification'] = self.camera.magnification
            dset.attrs['rotate'] = self.camera.rotate
            dset.attrs['pixel_size_x'] = self.camera.pixel_size_x
            dset.attrs['pixel_size_y'] = self.camera.pixel_size_y
            dset.attrs['OD_conversion_formula'] = self.camera.OD_conversion_formula
            dset.attrs['OD_conversion'] = 'pickled_lambda'
            dset.attrs['image_size'] = self.camera.image_size
            dset.attrs['image_ext'] = self.camera.image_ext
            
            # picture
            dset = f.create_dataset("picture", (0,), dtype='i')
            dset.attrs['filename'] = self.picture.filename
            dset.attrs['path'] = self.picture.path
            dset.attrs['ROI'] = self.picture.ROI
            dset.attrs['background'] = self.picture.background
            
            # atom
            dset = f.create_dataset("atom", (0,), dtype='i')
            dset.attrs['name'] = self.atom.name
            dset.attrs['fluo'] = self.atom.fluo
            dset.attrs['lbda'] = self.atom.lbda
            dset.attrs['sigma0'] = self.atom.sigma0
        
        pass


    def hdf5_to_fit(self,fname):
        """
        reads hdf5 format to generate fit object
        """
        loaded_fit = PyFit2D()
        
        with h5py.File(fname,"r") as f:
            
            # general data
            dset = f['general']
            loaded_fit.type = dset.attrs['type']
            
            # pyfit2D self properties save
            dset = f['values']
            values = {}
            for key in dset.attrs.keys():
                values[key] = dset.attrs[key]
            
            loaded_fit.values = values
            
            # fit
            dset = f["fit"]
            loaded_fit.fit.name = dset.attrs['name']
            loaded_fit.fit.results = dset.attrs['results'] 
            
            # fit_options
            dset = f["fit_options"]
            loaded_fit.fit.options.do_binning = dset.attrs['do_binning']
            loaded_fit.fit.options.binning = dset.attrs['binning']
            loaded_fit.fit.options.auto_binning = dset.attrs['auto_binning']
            loaded_fit.fit.options.binning_maxpoints = dset.attrs['binning_maxpoints']
            loaded_fit.fit.options.askROI = dset.attrs['askROI']
            loaded_fit.fit.options.fit_hole_first = dset.attrs['fit_hole_first']
            loaded_fit.fit.options.askHole = dset.attrs['askHole']
            loaded_fit.fit.options.max_func_eval = dset.attrs['max_func_eval']
            
            # camera
            dset = f["camera"]
            loaded_fit.camera.magnification = dset.attrs['magnification']
            loaded_fit.camera.rotate = dset.attrs['rotate']
            loaded_fit.camera.pixel_size_x = dset.attrs['pixel_size_x']
            loaded_fit.camera.pixel_size_y = dset.attrs['pixel_size_y']
            loaded_fit.camera.OD_conversion_formula = dset.attrs['OD_conversion_formula']
            loaded_fit.camera.OD_conversion = dset.attrs['OD_conversion']
            loaded_fit.camera.image_size = dset.attrs['image_size']
            loaded_fit.camera.image_ext = dset.attrs['image_ext']
            
            # picture
            dset = f["picture"]
            loaded_fit.picture.filename = dset.attrs['filename']
            loaded_fit.picture.path = dset.attrs['path']
            loaded_fit.picture.ROI = dset.attrs['ROI']
            loaded_fit.picture.background = dset.attrs['background']
            
            # atom
            dset = f["atom"]
            loaded_fit.atom.name = dset.attrs['name']
            loaded_fit.atom.fluo = dset.attrs['fluo']
            loaded_fit.atom.lbda = dset.attrs['lbda']
            loaded_fit.atom.sigma0 = dset.attrs['sigma0']
            
           
        return loaded_fit
        
        
        ''' Conversions to/from doublefit '''
        
    def adapt_type_from_fit(self):
        choosen_fit_type = self.fit.__class__.__name__
        current_fit_type = self.type
        
        if choosen_fit_type == 'Fit' and current_fit_type != 'pyfit2D':
            new_fit = PyFit2D()
            new_fit.atom = self.atom
            new_fit.picture = self.picture
            new_fit.camera = self.camera
            new_fit.fit = self.fit
            new_fit.data = self.data
            new_fit.xm = self.xm
            new_fit.ym = self.ym
            new_fit.data_fit = self.data_fit
            new_fit.xm_fit = self.xm_fit
            new_fit.ym_fit = self.ym_fit
            new_fit.values = self.values
            
        elif choosen_fit_type == 'DoubleFit' and current_fit_type != 'pydoublefit2D':
            new_fit = PyDoubleFit2D()
            new_fit.atom = self.atom
            new_fit.picture = self.picture
            new_fit.camera = self.camera
            new_fit.fit = self.fit
            new_fit.data = self.data
            new_fit.xm = self.xm
            new_fit.ym = self.ym
            new_fit.data_fit = self.data_fit
            new_fit.xm_fit = self.xm_fit
            new_fit.ym_fit = self.ym_fit
            new_fit.values = self.values
        else:
            new_fit = self
            
        return new_fit
    
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

#---------------------------------------------------------------------------#

class PyDoubleFit2D(PyFit2D):
    
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
        
        self.type = 'pydoublefit2D'
        
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
            
            p_hole = PyFit2D()
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
            
            p_out = PyFit2D()
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