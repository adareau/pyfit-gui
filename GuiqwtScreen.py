# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:05:06 2015

@author: Alexandre DAREAU
"""

from guidata.qt.QtGui import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QMainWindow, QGridLayout,QSizePolicy)
from guidata.qt.QtCore import QRect
import numpy as np

import weakref

#---Import plot widget base class
import guiqwt.tools as tools
from guiqwt.config import _
from guiqwt.curve import CurvePlot
from guiqwt.image import ImagePlot
from guiqwt.plot import PlotManager
from guiqwt.builder import make
from guiqwt.shapes import RectangleShape
from guiqwt.annotations import AnnotatedRectangle
from guiqwt.styles import LineStyleParam

from guiqwt.styles import ShapeParam

from guidata.configtools import get_icon

class DefaultToolbarID:
    pass


#---

class ImageScreen(QWidget):
    """
    Hum hum hum
    """
    def __init__(self, parent, x, y, data):
        QWidget.__init__(self, parent)
        
        #self.setMinimumSize(sizex, sizey)
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
        
        self.plot.adjustSize()
        
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
        #self.setMinimumSize(self.sizex,self.sizey)
        
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
        

# New class : LabelledRectangle = same as AnnotatedRectangle but with fixed text label

class LabelledRectangle(AnnotatedRectangle):
    
    def __init__(self, label_txt=''):
        
        super(AnnotatedRectangle,self).__init__()
        self.label_txt = label_txt
    
    # Override get_text to return always the same text
    def get_text(self):
        return self.label_txt

    
class RegionSelectTool(tools.RectangleTool):
    def __init__(self, *args, **kwargs):
        super(RegionSelectTool,self).__init__(*args, **kwargs)
        
        self.name = "test"
        
        self.rect = LabelledRectangle(label_txt=self.name)
        self.set_shape_style(self.rect)
        self.p0=(0,0)
        self.p1=(0,0)
        

    
    def add_shape_to_plot(self, plot, p0, p1):
        """
        Method called when shape's rectangular area
        has just been drawn on screen.
        Adding the final shape to plot and returning it.
        """
        self.p0 = p0
        self.p1 = p1
        self.rect.move_local_point_to(0,p0)
        self.rect.move_local_point_to(2,p1)
        #self.set_shape_style(self.rect)
        
        plot.replot()
        
 
   
class ROISelectTool(RegionSelectTool):
    def __init__(self, *args, **kwargs):
        super(ROISelectTool,self).__init__(*args, **kwargs)
        
        self.name = "ROI"
        self.rect.label_txt = self.name
        
        '''
        line = LineStyleParam()
        line.set_style_from_matlab(':')
        line.color="#ff0000"
        
        self.rect.shape.shapeparam.line.update_param(line.build_pen())
        '''
        
         
        
        
        
    

            
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
        
                
        sx = 600
        sy = int(sx/1.338)
        stretch_x = 3
        stretch_y = 3
        
        #self.setGeometry(QRect(0,0,sx,sy))
        layout = QGridLayout(self)
        layout.setMargin(0)
        
        self.screen = ImageScreen(self,x,y,data)       
        self.cutX = CutScreen(self)       
        self.cutY = CutScreen(self)
        
        
        layout.addWidget(self.screen,1,0)
        layout.addWidget(self.cutX,0,0)
        layout.addWidget(self.cutY,1,1)
        
        layout.setColumnStretch(0, stretch_x)
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, stretch_y)
        
        self.setLayout(layout)
        
        self.updateGeometry()
        
        self.manager = PlotManager(self) 
        self.manager.add_plot(self.screen.plot)
        self.manager.add_plot(self.cutX.plot)
        self.manager.add_plot(self.cutY.plot)
        
        roi = ROISelectTool
        self.tools=[tools.SelectTool,tools.RectZoomTool,
                    tools.ColormapTool, roi]
                    
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
    