# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:05:06 2015

@author: Alexandre DAREAU
"""

from guidata.qt.QtGui import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QMainWindow, QGridLayout,QSizePolicy)
from guidata.qt.QtCore import SIGNAL
import numpy as np

#---Import plot widget base class
import guiqwt.tools as tools
from guiqwt.curve import CurvePlot
from guiqwt.image import ImagePlot
from guiqwt.plot import PlotManager
from guiqwt.builder import make

from guidata.configtools import get_icon
#---

class ImageScreen(QWidget):
    """
    Hum hum hum
    """
    def __init__(self, parent, x, y, data, sizex, sizey):
        QWidget.__init__(self, parent)
        
        self.setMinimumSize(sizex, sizey)
        self.x = x
        self.y = y
        self.data = data
        #---guiqwt related attributes:
        self.plot = None
        self.image = None
        self.ROI = None
        self.background = None
        #---
        self.setup_widget()
        
    def setup_widget(self):
        
        self.plot = ImagePlot(self)
        self.image = make.xyimage(self.x,self.y,self.data,colormap='jet')
        self.plot.add_item(self.image)
        self.plot.set_antialiasing(True)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.plot)
        self.setLayout(vlayout)
        
        #self.plot.adjustSize()
        
    def update_image(self):
        self.image.x = self.x
        self.image.y = self.y
        self.image.data = self.data
        
        self.plot.replot()
        
        pass
        
class CutScreen(QWidget):

    def __init__(self, parent, xdata=[], ydata=[], xfit=[], yfit=[],
                 sizex=100, sizey=100):
                     
        QWidget.__init__(self,parent)
        
        self.sizex = sizex
        self.sizey = sizey
        self.setMinimumSize(self.sizex,self.sizey)
        
        self.xdata = xdata
        self.ydata = ydata
        self.xfit = xfit
        self.yfit = yfit
        
        self.plot = None
        self.data_cut = None
        self.fit_cut = None
        
        self.setup_widget()
        
    def setup_widget(self):
        
        self.plot = CurvePlot(self)
        self.data_cut = make.curve(self.xdata,self.ydata)
        self.data_fit = make.curve(self.xfit, self.yfit)
        
        self.plot.add_item(self.data_cut)
        self.plot.add_item(self.data_fit)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.plot)
        self.setLayout(vlayout)
        
    
class RegionSelectTool(tools.RectangleTool):
    pass
        
        
class GuiqwtScreen(QWidget):
    """
    Hum hum hum
    """
    def __init__(self, parent=None, x=[], y=[], data=[]):
        QWidget.__init__(self, parent)
        
        if len(x)<2:
            x = np.linspace(0,1392,1392)
            y = np.linspace(0,1040,1040)
            data = np.zeros((1040,1392))
            
        self.x = x
        self.y = y
        self.data = data
        

        layout = QGridLayout(self)
        
        '''
        self.screen = ImageScreen(self,x,y,data,int(self.sizex*5.0/6.0),int(self.sizey*5.0/6.0))       
        self.cutX = CutScreen(self,sizex=int(self.sizex*5.0/6.0),sizey=int(self.sizey*1.0/6.0))       
        self.cutY = CutScreen(self,sizex=int(self.sizex*1.0/6.0),sizey=int(self.sizey*5.0/6.0))
        '''
        
        sx = 500
        sy = int(sx/1.338)
        a = 0.2
        
        self.screen = ImageScreen(self,x,y,data,sizex=sx,sizey=sy)       
        self.cutX = CutScreen(self,sizex=sx,sizey=int(a*sy))       
        self.cutY = CutScreen(self,sizex=int(a*sx),sizey=sy)
        
        
        layout.addWidget(self.screen,1,0)
        layout.addWidget(self.cutX,0,0)
        layout.addWidget(self.cutY,1,1)
        
        self.setLayout(layout)
        
        self.updateGeometry()
        
        self.manager = PlotManager(self) 
        self.manager.add_plot(self.screen.plot)
        self.manager.add_plot(self.cutX.plot)
        self.manager.add_plot(self.cutY.plot)
        
        roi = RegionSelectTool
        self.tools=[tools.SelectTool,tools.RectZoomTool,roi,
                    tools.ColormapTool]
        self.manager.register_all_curve_tools()

### Test function

class TestWindow(QMainWindow):
    
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Test")
        a = 600
        self.resize(int(a),int(a/1.338))
        
        hlayout = QHBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(hlayout)
        self.setCentralWidget(central_widget)


    def setup_window(self):
        x = np.linspace(0,1392,1392)
        y = np.linspace(0,1040,1040)
        xm,ym = np.meshgrid(x,y)
        
        data = np.exp(-(xm-700.)**2/50.0-(ym-500.)**2/100.0)
        x=[]
        
        wid = GuiqwtScreen(self,x,y,data)
        self.centralWidget().layout().addWidget(wid)
        
       
def test():
    from guidata.qt.QtGui import QApplication

    

    
    app = QApplication([])
    win = TestWindow()
    win.setup_window()
    
    
    
    win.show()
    app.exec_()
    
if __name__ == '__main__':
    test()
    