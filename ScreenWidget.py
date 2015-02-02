from PyQt4 import QtGui
import matplotlib
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import csv

class ScreenWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        
        # canvas
        font = self.font()
        windowColor = str(self.palette().window().color().name())
        matplotlib.rc('font', size=.9*font.pointSize(), weight="normal")
        matplotlib.rc('figure', facecolor=windowColor, edgecolor=windowColor)
        self.fig = Figure(dpi=self.logicalDpiX())
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)

        # navigation
        self.navigation = NavigationToolbar(self.canvas, self, coordinates=False)
        '''
        self.actionAutoscale = self.navigation.addAction("AutoScale", self.toggleAutoscale)
        self.saveData = self.navigation.addAction("Save data to file", self.saveDataToFile)
        self.actionAutoscale.setCheckable(True)
        self.actionAutoscale.setChecked(True)
        '''
        # layout
        layout = QtGui.QVBoxLayout(self)
        #layout.addWidget(self.navigation)
        layout.addWidget(self.canvas)
        
        self.xlabel = 'x (px)'
        self.ylabel = 'y (px)'
        
        # init other stuff
        gs = gridspec.GridSpec(5, 5)
        self.main_axes = self.fig.add_subplot(gs[1:,:-1])
        self.cutx_axes = self.fig.add_subplot(gs[0,:-1])
        self.cuty_axes = self.fig.add_subplot(gs[1:,-1])
        self.small_axes = self.fig.add_subplot(gs[0,-1])
        '''
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')
        '''
        self.refreshLabelsAndTicks()
        
        self.lineDict = {}
    
    
    def refreshLabelsAndTicks(self):
        
        self.main_axes.set_xlabel(self.xlabel)
        self.main_axes.set_ylabel(self.ylabel)
        
        
        self.cutx_axes.xaxis.tick_top()
        self.cuty_axes.yaxis.tick_right()
        self.small_axes.set_xticklabels([])
        self.small_axes.set_yticklabels([])
        
        self.cutx_axes.set_xlabel(self.xlabel)
        self.cutx_axes.xaxis.set_label_position('top')
        
        self.cuty_axes.set_ylabel(self.ylabel)
        self.cuty_axes.yaxis.set_label_position('right')
        
        
    def toggleAutoscale(self):
        self.draw()
        
    def addLine(self, name, color = "r", marker = None):
        x = [0]
        y = [0]  
        self.lineDict[name] = matplotlib.lines.Line2D(x, y, label = name, color = color, marker = marker, markeredgewidth = 0)
        
    def removeLine(self, name):
        if name in self.lineDict.keys():
            del self.lineDict[name]
            self.plot()
        else:
            print "name not in list"
    
    def getVisibleNames(self):
        pass
    
    def getLineNames(self):
        return self.lineDict.keys()
            
    def setLineVisible(self, name, vis):
        if name in self.lineDict.keys():
            self.lineDict[name].set_visible(vis)
            self.draw()
        else:
            print "name not in list"
        
    def plot(self):
        self.main_axes.cla()
        for key in self.lineDict.keys():
            self.main_axes.add_line(self.lineDict[key])
            self.lineDict[key].set
        self.draw()
        #self.background = self.canvas.copy_from_bbox(self.main_axes.bbox)
    
    def draw(self):
        '''
        if self.actionAutoscale.isChecked(): 
            self.main_axes.relim()
            self.main_axes.autoscale()
            '''
        #self.main_axes.legend(loc=0) # legend seems to slow down the drawing noticeably
        self.canvas.draw()
    
    def updateLine(self, name, x, y):        # needs draw command afterwards
        #self.background = self.canvas.copy_from_bbox(self.main_axes.bbox) 
        if name in self.lineDict.keys():
            #self.canvas.restore_region(self.background)
            self.lineDict[name].set_xdata(x)
            self.lineDict[name].set_ydata(y)
            #self.main_axes.draw_artist(self.lineDict[name])
            #self.canvas.blit(self.main_axes.bbox)
        else:
            print "name not in list"
            
    def updateLineX(self, name, x):
        if name in self.lineDict.keys():
            #self.canvas.restore_region(self.background)
            self.lineDict[name].set_xdata(x)
            #self.main_axes.draw_artist(self.lineDict[name])
            #self.canvas.blit(self.main_axes.bbox)
        else:
            print "name not in list"
            
    def updateLineY(self, name, y):
        if name in self.lineDict.keys():
            #self.canvas.restore_region(self.background)
            self.lineDict[name].set_ydata(y)
            #self.main_axes.draw_artist(self.lineDict[name])
            #self.canvas.blit(self.main_axes.bbox)
        else:
            print "name not in list"
            
    def saveDataToFile(self):
        try:
            fname = QtGui.QFileDialog.getSaveFileName(self, "Save As", "./motionControllerData.dat", "*.dat")
            wr = csv.writer(open(fname,"w"), delimiter=',')
            for name in self.lineDict.keys():
                wr.writerow(np.int32(self.lineDict[name].get_ydata()))
                print np.int32(self.lineDict[name].get_ydata())
        except:
            print "Error while saving data"
            
         
            
########################################################
            
def testMatplotlibWidget():
    app = QtGui.QApplication([])
    
    win = ScreenWidget()
    win.show()

    win.addLine("test1", "b")
    win.plot()
    """win.setLineVisible("test1", True)
    x = np.linspace(0, 1000, 1000)
    y = np.linspace(0, 1000, 1000)
    win.updateLine("test1", x, y)
    #win.removeLine("test1")
    win.addLine("test2", "r")
    print win.lineDict
    
    win.plot()
    win.setLineVisible("test2", False)
    win.setLineVisible("test2", True)
    win.updateLine("test2", x , 2*y)
    win.updateLine("test1", x , 3*y)
    print win.lineDict
    win.setXLabel("pups / mol")"""

    app.exec_()   

if __name__ == "__main__":
    testMatplotlibWidget()  

    
    
    