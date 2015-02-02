# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 17:02:46 2015

@author: Alexandre DAREAU
"""

from guidata.qt.QtGui import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                              QMainWindow)
from guidata.qt.QtCore import SIGNAL

#---Import plot widget base class
from guiqwt.curve import CurvePlot
from guiqwt.plot import PlotManager
from guiqwt.builder import make
from guidata.configtools import get_icon
#---

class FilterTestWidget(QWidget):
    """
    Filter testing widget
    parent: parent widget (QWidget)
    x, y: NumPy arrays
    func: function object (the signal filter to be tested)
    """
    def __init__(self, parent, x, y, func):
        QWidget.__init__(self, parent)
        self.setMinimumSize(320, 200)
        self.x = x
        self.y = y
        self.func = func
        #---guiqwt related attributes:
        self.plot = None
        self.curve_item = None
        #---
        
    def setup_widget(self, title):
        #---Create the plot widget:
        self.plot = CurvePlot(self)
        self.curve_item = make.curve([], [], color='b')
        self.plot.add_item(self.curve_item)
        self.plot.set_antialiasing(True)
        #---
        
        button = QPushButton(u"Test filter: %s" % title)
        self.connect(button, SIGNAL('clicked()'), self.process_data)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.plot)
        vlayout.addWidget(button)
        self.setLayout(vlayout)
        
        self.update_curve()
        
    def process_data(self):
        self.y = self.func(self.y)
        self.update_curve()
        
    def update_curve(self):
        #---Update curve
        self.curve_item.set_data(self.x, self.y)
        self.plot.replot()
        #---
    
    
class TestWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Signal filtering 2 (guiqwt)")
        self.setWindowIcon(get_icon('guiqwt.png'))
        
        hlayout = QHBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(hlayout)
        self.setCentralWidget(central_widget)
        #---guiqwt plot manager
        self.manager = PlotManager(self)
        #---
        
    def add_plot(self, x, y, func, title):
        widget = FilterTestWidget(self, x, y, func)
        widget.setup_widget(title)
        self.centralWidget().layout().addWidget(widget)
        #---Register plot to manager
        self.manager.add_plot(widget.plot)
        #---
        
    def setup_window(self):
        #---Add toolbar and register manager tools
        toolbar = self.addToolBar("tools")
        self.manager.add_toolbar(toolbar, id(toolbar))
        self.manager.register_all_curve_tools()
        #---
        

def test():
    """Testing this simple Qt/guiqwt example"""
    from guidata.qt.QtGui import QApplication
    import numpy as np
    import scipy.signal as sps, scipy.ndimage as spi
    
    app = QApplication([])
    win = TestWindow()
    
    x = np.linspace(-10, 10, 500)
    y = np.random.rand(len(x))+5*np.sin(2*x**2)/x
    win.add_plot(x, y, lambda x: spi.gaussian_filter1d(x, 1.), "Gaussian")
    win.add_plot(x, y, sps.wiener, "Wiener")
    #---Setup window
    win.setup_window()
    #---
    
    win.show()
    app.exec_()
        
        
if __name__ == '__main__':
    test()