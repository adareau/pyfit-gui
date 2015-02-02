# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 11:20:55 2015

@author: Alexandre DAREAU
"""

import os
import glob
import time
import pylab as pl

from guiqwt.plot import ImageDialog
from guiqwt.builder import make
from guiqwt.config import _


if os.name == 'posix':
    root ='/home/alex/Thèse/'
else:
    root = 'D:\\Alexandre DAREAU\\Documents\\'
    
path = os.path.join(root,'Programmation','Python',
                    'Fits','fit examples','fringe removal test','RAW')
                    
parent_path = os.path.join(root,'Programmation','Python',
                    'Fits','fit examples','fringe removal test')
                    

pics = glob.glob(parent_path+os.sep+'*.png')


os.path



pics = pics[:9]
data = []

p = pl.imread(pics[0])
p = p[:,:,0]
'''
for p in pics:
    data.append(pl.imread(p))


f = plt.figure()
i=0
for p in data:
    plt.subplot(3,3,i)
    plt.imshow(p)
    i+=1
'''

### guiqwt

#win = ImageDialog(edit=True,toolbar=True,wintitle="hum")
win = ImageDialog(edit=False, toolbar=True, wintitle="Cross sections test",
                      options=dict(show_xsection=True, show_ysection=True))
image = make.image(p)
plot = win.get_plot()

plot.add_item(image)

win.exec_()





