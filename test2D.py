# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 09:54:08 2014

@author: Alexandre DAREAU
"""


import matplotlib.pyplot as plt
import inspect
import os
import numpy as np
import pickle
import pyfit as pf

path =  os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(path)
name = u'185214 Nom de sequence TOF = 3_Final_frac = -3.5_lumenerb.jpg'

#fit = pf.PyDoubleFit2D()
#fit.fit = pf.fit2D_dic['GaussTF']

fit = pf.PyFit2D()
fit.fit = pf.fit2D_dic['Gauss']

fit.camera = pf.cam_collection.lumenera.gen()



fit.fit.options.do_binning=True
fit.fit.options.auto_binning = True
fit.fit.options.binning = 5
fit.fit.options.askROI = False
fit.fit.options.askHole = False

fit.picture.filename = name
fit.picture.path = path
#fit.picture.ROI = (286.00403225806451, 626.38911290322574, 153.07258064516134, 339.88508064516128)
#fit.hole = (424.0645161290322, 496.53024193548384, 250.12500000000006, 274.27217741935482)

fit.load_data()
fit.do_fit()

fit.save_fit()

savename = name[0:len(name)-4]+'.fit'
file_save = os.path.join(path,'saved_fits',savename)
f = open(file_save,'rb')

fit = pickle.load(f)



fit.print_values()

plt.figure('pyfit test')

plt.clf()
xm = fit.xm_fit
ym = fit.ym_fit
d = fit.data_fit
p = fit.fit.results

fit_res = fit.fit.formula((xm,ym),*p)
plt.imshow(d,extent=(xm.min(), xm.max(), ym.max(), ym.min()))
plt.contour(xm,ym,fit_res,8,colors='w')
plt.show()



