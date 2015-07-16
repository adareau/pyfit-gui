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


from scipy.io import loadmat


def import_MATLAB(filename):
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
    
    
    
    
    
    
    return res




# test

root = 'D:\\Alexandre DAREAU\\Documents\\Programmation\\Python\\pyfit-gui'
file = os.path.join(root,'fit examples','saved_fits','110046_Transport TOF = 3_evap_final_frac = 0,18_f_MOT_offset = -0,3_Verdi_cross_alpha = 10_a_cross_transfert = 7_lumenerb.fit')

test = import_MATLAB(file)
