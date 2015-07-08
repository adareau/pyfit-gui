# -*- coding: utf-8 -*-
#-------------------------------------#
# file        : pyfit_classes
# author      : A. Dareau
# version     : 11/2014
# description : secondary classes for pyfit objects
#-------------------------------------#

import numpy as np
import re

# Secondary objects
    
class Camera():
    
    def __init__(self):
        
        self.name = 'cam_name'
        self.magnification = 1
        self.rotate = 0
        self.pixel_size_x = 4.0
        self.pixel_size_y = 4.0
        self.OD_conversion = 'pickled_lambda'
        self.OD_conversion_formula = '(5.0+0.5)*x-0.5'
        self.image_size = (1392,1040)
        self.image_ext = '_cam.png'

    def update_OD_conversion(self):
        self.OD_conversion = eval('lambda x:'+self.OD_conversion_formula,
                                  {"__builtins__":None},{})        
        
class Atom():
    def __init__(self):
        
        self.name = 'ytterbium'
        self.fluo = False
        self.lbda = 399e-9
        self.sigma0 = 3*self.lbda**2/2/np.pi
        
        
class Picture():
    
    def __init__(self):
        
        self.filename = '*.jpg'
        self.path = ''
        self.variables = []
        
        self.ROI = []
        self.background = []
        
    def parseVariables(self):
        
        var_dic = {}
        
        # 1 - timestamp
        
        timestamp_pattern = "^([0-9]{6})" # search for 6 numbers at the beginning of the file name
        tmstp = re.findall(timestamp_pattern,self.filename)
        
        if tmstp:
            tmstp = int(tmstp[0])
        else:
            tmstp = 0
        
        var_dic['timestamp']=tmstp
        
        # 2 - variables
        
        pattern = "([A-Za-z]\w*) = (-*[0-9]*[,.]?[0-9]*)"
        var_list = re.findall(pattern,self.filename)
        
        
        for v in var_list:
            var_dic[v[0]] = np.float(v[1].replace(',','.'))
        self.variables = var_dic
        
class Fit():
    
    def __init__(self,**kwargs):
        
        self.name = kwargs.get('name','fit')
        self.formula = kwargs.get('formula','lambda(x,y),*p:0')
        
        self.parameters = kwargs.get('parameters',{}) #fixed fit parameters
        self.formula_parameters = kwargs.get('formula_parameters','lambda(x,y),*p:0')
        
        
        self.guess = kwargs.get('guess',[])
        
        self.results = []
        self.values = []
        
        self.options = kwargs.get('options',FitOptions())
        
    
    def updateFormulaFromParameters1D(self):
        self.formula = lambda x,*p:self.formula_parameters(self.parameters,x,*p)
        
    
    def updateFormulaFromParameters2D(self):
        self.formula = lambda (x,y),*p:self.formula_parameters(self.parameters,(x,y),*p)
        
        
class DoubleFit(Fit):
    
    def __init__(self):
        
        self.name = 'dblefit'
        self.fit_in = Fit()
        self.fit_out = Fit()
        self.guess = []
        self.results = []
        self.values = []
        
        self.combine = 'add'
        self.formula = 'lambda(x,y),*p:0'
        
        self.options = FitOptions()
        
        
class FitOptions():
    
    def __init__(self, **kwargs):
        
        # Binning
        
        self.do_binning = kwargs.get('do_binning',False)
        self.binning = kwargs.get('binning',4)
        self.auto_binning = kwargs.get('auto_binning',False)
        self.binning_maxpoints = kwargs.get('binning_maxpoints',200)
        
        self.askROI = kwargs.get('askROI',False)        
        
        # For double fit
        
        self.fit_hole_first = kwargs.get('fit_hole_first',True) 
        self.askHole = kwargs.get('askHole',False) 
        
        # Optimization options
        self.max_func_eval = 3000
        
class Value():

    def __init__(self, **kwargs):
        
        f = lambda pf:0
        
        self.formula = kwargs.get('formula',f)
        self.name = kwargs.get('name','val')
        self.unit = kwargs.get('unit','')
        self.format = kwargs.get('format','%.1f')     