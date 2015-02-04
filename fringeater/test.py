# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 17:53:38 2015

@author: Alexandre DAREAU
"""

import os
import glob
import time

import fringeater as fr
import matplotlib.pyplot as plt
import numpy as np

if os.name == 'posix':
    root ='/home/alex/Thèse/'
else:
    root = 'D:\\Alexandre DAREAU\\Documents\\'
    
path = os.path.join(root,'Programmation','Python',
                    'Fits','fit examples','fringe removal test','RAW')
                    
parent_path = os.path.join(root,'Programmation','Python',
                    'Fits','fit examples','fringe removal test')
                    

pics = glob.glob(parent_path+os.sep+'*.png')

pics = [os.path.split(p)[-1] for p in pics]
pics = [os.path.join(path,p) for p in pics]





pic_set_1 = pics[:30]
#pic_set_1 = pics[:3]
pic_set_2 = pics[31:]

roi_1_x = [610,835]
roi_1_y = [190,396]

background_1_x = [819,1157]
background_1_y = [243,567]


background1 = np.zeros((1040, 1392),dtype=bool)
roi1 = np.zeros((1040, 1392),dtype=bool)


background1[background_1_y[0]:background_1_y[1],background_1_x[0]:background_1_x[1]] = True
roi1[roi_1_y[0]:roi_1_y[1],roi_1_x[0]:roi_1_x[1]] = True

file_list_1 = [(p.replace('.png','_1.png'),p.replace('.png','_2.png')) for p in pic_set_1]
file_list_2 = [(p.replace('.png','_1.png'),p.replace('.png','_2.png')) for p in pic_set_2]

background = []

t_list = []
data = []
REF = []

t0 = time.time()
for i in np.arange(1):
    del data
    del REF
    
    data,REF = fr.LoadRefImages(file_list_1,background1,0)

print(time.time()-t0)
    


od_list = []
od_list_corr = []

'''
i = 10

at = np.array(data[0][i])
noat = np.array(data[1][i])
'''

for at,noat in zip(data[0],data[1]):

    c = fr.ComputeBestRef(at,REF)
    ref = fr.GenRefPic(c,data[1])
    
    od = -np.log(at/noat)
    od_corr = -np.log(at/ref)

    img_roi = od[roi_1_y[0]:roi_1_y[1],roi_1_x[0]:roi_1_x[1]]
    img_roi_corr = od_corr[roi_1_y[0]:roi_1_y[1],roi_1_x[0]:roi_1_x[1]]
    
    
    img_background = od[background_1_y[0]:background_1_y[1],background_1_x[0]:background_1_x[1]]
    img_background_corr = od_corr[background_1_y[0]:background_1_y[1],background_1_x[0]:background_1_x[1]]
    
    od_list.append(od)
    od_list_corr.append(od_corr)
    
cmin = 0
cmax = 1

plt.figure('1')
plt.subplot(221)
img = plt.imshow(img_roi)
img.set_clim(cmin,cmax)

plt.subplot(222)
img = plt.imshow(img_background)
img.set_clim(cmin,cmax)

plt.subplot(223)
img = plt.imshow(img_roi_corr)
img.set_clim(cmin,cmax)

plt.subplot(224)
img = plt.imshow(img_background_corr)
img.set_clim(cmin,cmax)


plt.figure('2')
plt.subplot(211)
img = plt.imshow(od)
img.set_clim(cmin,cmax)

plt.subplot(212)
img = plt.imshow(od_corr)
img.set_clim(cmin,cmax)

plt.show()


del data
del od
del od_corr