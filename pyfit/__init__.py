# -*- coding: utf-8 -*-
#-------------------------------------#
# PyFit Package
# author      : A. Dareau
# version     : 11/2014
# description : camera collection for pyfit
#-------------------------------------##

# Objects

from pyfit2D import PyFit2D
from pyfit1D import PyFit1D
from pydoublefit2D import PyDoubleFit2D

# Modules

import pyfit_classes
import pyfit_functions


#from EditableRectangle import EditableRectangle

# Collections

import cam_collection
import fit_collection

# Create a dictionnary with fits (easier to access)

fit2D_dic = {fit_collection.gauss2D.gen().name:fit_collection.gauss2D.gen(),
             fit_collection.gaussTilted.gen().name:fit_collection.gaussTilted.gen(),
             fit_collection.thomasFermi2D.gen().name:fit_collection.thomasFermi2D.gen(),
             fit_collection.gaussTF2D.gen().name:fit_collection.gaussTF2D.gen()}


fit1D_dic = {fit_collection.gauss1D.gen().name:fit_collection.gauss1D.gen(),
             fit_collection.gaussDeriv1D.gen().name:fit_collection.gaussDeriv1D.gen(),
             fit_collection.gaussWaist.gen().name:fit_collection.gaussWaist.gen()}

camera_dic = {cam_collection.lumenera.gen().name:cam_collection.lumenera.gen()}
