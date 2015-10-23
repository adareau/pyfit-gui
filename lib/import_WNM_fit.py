# -*- coding: utf-8 -*-
#-------------------------------------#
# import WNM Fit
# author      : A. Dareau
# version     : 07/2015
# description : imports "Watch_and_MOT" saved fits (MATLAB format)
#               and convert them to pyfit-gui compatible fits
#-------------------------------------##

import os
import numpy as np
import pyfit as pf

from scipy.io import loadmat


def import_WNM_fit(filename):
    '''
    input : filename (str) -> path to fit
    output : 0 if any error
             fit_name (str) if fit loaded, but conversion not implemented for the name
             pyfit Object otherwise
    '''
    #--- Load and extract data
    
    # check that fit file exists
    if not os.path.isfile(filename): return 0
    
    # load fit file and check it has a "tosave" key
    loaded_fit = loadmat(filename, squeeze_me=True, struct_as_record=False)
    if not loaded_fit.has_key('tosave'): return 0
    res = loaded_fit['tosave']
    
    # extract fit properties
    

    fit_type = res.fitType
    p = res.fittedParam
    
    ROI = res.ROI
    background = res.background
    magnification = res.magnification
    binning = res.Binning
    
    
    #--- Generate fit from data 
    
    # initialize fit object
    fit = pf.PyFit2D()
    
    # general
    
    fit.picture.ROI = ROI
    fit.picture.background = background
    fit.camera.magnification = magnification
    if binning>1:
        fit.fit.options.do_binning = True
        fit.fit.options.binning = binning
        fit.fit.options.auto_binning = False
    # convert according to fit name
    # /!\ pay attention to the index difference between MATLAB and python 
    # since MATLAB starts at 1, and python starts at 0, on has to remove 1
    # from all absolute positions measured in MATLAB !!
    
    if fit_type == 'Gaussian':
        # OLD : order of parameters: offset,ampl,sx,sy,cx,cy
        # NEW :p = [offset, Ampl,sx,sy,cx,cy ]
        # NB x and y inverted !
        
        fit.fit = pf.fit2D_dic['Gauss']
        # -2 due to index difference (-1 for fit center, -1 for ROI start)
        p_new = np.array([p[0],p[1],p[3],p[2],p[5]+ROI[0]-2,p[4]+ROI[2]-2])
        fit.fit.results = p_new
        fit_collection = [fit]
        roi_index = [0]
        
    elif fit_type == 'TF':
        # OLD : order of parameters: offset,ampl,sx,sy,cx,cy
        # NEW :  p = [offset, Ampl,sx,sy,cx,cy ]
        # NB x and y inverted !
        
        fit.fit = pf.fit2D_dic['ThomasFermi']
        # -2 due to index difference (-1 for fit center, -1 for ROI start)
        p_new = np.array([p[0],p[1],p[3],p[2],p[5]+ROI[0]-2,p[4]+ROI[2]-2])
        fit.fit.results = p_new
        fit_collection = [fit]
        roi_index = [0]
    
    elif fit_type == 'ConcentricBoseTF' or fit_type == 'ConcentricBoseTF2':  
        # OLD : order of parameters: offset,ampl1,sx1,sy1,cx,cy,ampl2,sx2,sy2 (Bose first, TF then)
        # NEW : [offset, A_bose, sx_bose, sy_bose,  cx , cy, A_tf, Rx_tf, Ry_tf]
        # NB x and y inverted !
        
        fit.fit = pf.fit2D_dic['BoseTF']
        p_new = np.array([p[0],p[1],p[3],p[2],p[5]+ROI[0]-2,p[4]+ROI[2]-2,p[6],p[8],p[7]])
        fit.fit.results = p_new
        fit_collection = [fit]
        roi_index = [0]
        
    else: # not known...
        return (fit_type,0)
        
    
    
    return (fit_collection, roi_index)




# test
'''
root = 'D:\\Alexandre DAREAU\\Documents\\Programmation\\Python\\pyfit-gui'
file = os.path.join(root,'fit examples','saved_fits','110046_Transport TOF = 3_evap_final_frac = 0,18_f_MOT_offset = -0,3_Verdi_cross_alpha = 10_a_cross_transfert = 7_lumenerb.fit')

test = import_WNM_fit(file)
'''