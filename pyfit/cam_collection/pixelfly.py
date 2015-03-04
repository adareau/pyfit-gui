# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:46:55 2014

@author: Alexandre DAREAU
"""

from pyfit.pyfit_classes import Camera

def gen():
    cam = Camera()
    cam.magnification = 1
    cam.name = "pixelfly"
    cam.pixel_size_x = 6.45
    cam.pixel_size_y = 6.45
    cam.OD_conversion_formula = '(5.0+0.5)*x/255.0-0.5'
    cam.OD_conversion = OD_conversion
    cam.image_ext = '_pixelfly.bmp'
    cam.image_size = (1392,1040)
    return cam
    
def OD_conversion(x):
    #return (5.0+0.5)*x/255.0-0.5
    return (5.0+0.5)*x/255.0-0.5