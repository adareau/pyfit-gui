# -*- coding: utf-8 -*-

# draggable rectangle with the animation blit techniques; see
# http://www.scipy.org/Cookbook/Matplotlib/Animations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCursor

####################################################################################"


class EditableRectangle:
    """
    Modified from :
    
        Draggable and resizeable rectangle with the animation blit techniques.
        Based on example code at http://matplotlib.sourceforge.net/users/event_handling.html
        If *allow_resize* is *True* the recatngle can be resized by dragging its
        lines. *border_tol* specifies how close the pointer has to be to a line for
        the drag to be considered a resize operation. Dragging is still possible by
        clicking the interior of the rectangle. *fixed_aspect_ratio* determines if
        the recatngle keeps its aspect ratio during resize operations.
    """
    lock = None  # only one can be animated at a time
    def __init__(self, rect, border_tol=.15, allow_resize=True,
                 fixed_aspect_ratio=True):
        self.rect = rect
        self.border_tol = border_tol
        self.allow_resize = allow_resize
        self.fixed_aspect_ratio = fixed_aspect_ratio
        self.press = None
        self.background = None
        
    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):

        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        if EditableRectangle.lock is not None: return
        contains, attrd = self.rect.contains(event)
        if not contains: return
        #print 'event contains', self.rect.xy
        x0, y0 = self.rect.xy
        w0, h0 = self.rect.get_width(), self.rect.get_height()
        aspect_ratio = np.true_divide(w0, h0)
        self.press = x0, y0, w0, h0, aspect_ratio, event.xdata, event.ydata
        EditableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        self.rect.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.rect)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        self.update_cursor(event)
        if EditableRectangle.lock is not self:
            return
        if event.inaxes != self.rect.axes: return
        x0, y0, w0, h0, aspect_ratio, xpress, ypress = self.press
        self.dx = event.xdata - xpress
        self.dy = event.ydata - ypress
        #self.rect.set_x(x0+dx)
        #self.rect.set_y(y0+dy)
        
        self.update_rect(event)

        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.rect)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if EditableRectangle.lock is not self:
            return

        self.press = None
        EditableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.rect.set_animated(False)
        self.background = None

        # redraw the full figure
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

                
    def update_rect(self,event):
        x0, y0, w0, h0, aspect_ratio, xpress, ypress = self.press
        dx, dy = self.dx, self.dy
        fixed_ar = self.fixed_aspect_ratio
        bt = self.border_tol
        pos = self.mouse_position_fast(x0,y0,w0,h0,xpress,ypress,bt)
        
        if (not self.allow_resize or
            pos == 'In'):
                
            self.rect.set_x(x0+dx)
            self.rect.set_y(y0+dy)
            
        if 'Left' in pos:
            self.rect.set_x(x0+dx)
            self.rect.set_width(w0-dx)
            if fixed_ar:
                dy = np.true_divide(dx, aspect_ratio)
                self.rect.set_y(y0+dy)
                self.rect.set_height(h0-dy)
                
        elif 'Right' in pos:
            self.rect.set_width(w0+dx)
            if fixed_ar:
                dy = np.true_divide(dx, aspect_ratio)
                self.rect.set_height(h0+dy)
                
        if 'Bottom' in pos:
            self.rect.set_y(y0+dy)
            self.rect.set_height(h0-dy)
            if fixed_ar:
                dx = dy*aspect_ratio
                self.rect.set_x(x0+dx)
                self.rect.set_width(w0-dx)
                
        elif 'Top' in pos:
            self.rect.set_height(h0+dy)
            if fixed_ar:
                dx = dy*aspect_ratio
                self.rect.set_width(w0+dx)
                

            
                
    def update_cursor(self,event):
        
        pos = self.mouse_position(event)
        
        if pos == 'In':
            cursor = Qt.SizeAllCursor
            
        elif (pos == 'Top' or pos == 'Bottom'):
            cursor = Qt.SizeVerCursor
            
        elif (pos == 'Left' or pos == 'Right'):
            cursor = Qt.SizeHorCursor
            
        elif (pos == 'TopRight' or pos == 'BottomLeft'):
            cursor = Qt.SizeFDiagCursor
            
        elif (pos == 'TopLeft' or pos == 'BottomRight'):
            cursor = Qt.SizeBDiagCursor
            
        else:
            cursor = Qt.ArrowCursor
        
        QApplication.setOverrideCursor(QCursor(cursor))        

         
         

                   
    def mouse_position(self,event):
        if event.inaxes != self.rect.axes: return 'Out'
            
        contains = self.rect.contains(event)
        if not contains: return 'Out'
            
            
        x0, y0 = self.rect.xy
        w0, h0 = self.rect.get_width(), self.rect.get_height()
        xpress = event.xdata
        ypress = event.ydata
        bt = self.border_tol
        
        if (abs(x0+np.true_divide(w0,2)-xpress)<np.true_divide(w0,2) and
             abs(y0+np.true_divide(h0,2)-ypress)<np.true_divide(h0,2)):
            
            pos = ''
            
            # Top / Bottom
            
            if abs(y0-ypress)<bt*h0:
                pos = pos+'Bottom'
            elif abs(y0+h0-ypress)<bt*h0:
                pos = pos+'Top'
                
            # Right / Left
            
            if abs(x0-xpress)<bt*w0:
                pos = pos+'Left'
                
            elif abs(x0+w0-xpress)<bt*w0:
                pos = pos+'Right'
        
            if pos == '':pos = 'In'
        else:
            pos = 'Out'
        
        return pos
       
    def mouse_position_fast(self,x0,y0,w0,h0,xpress,ypress,bt):
        
        if (abs(x0+np.true_divide(w0,2)-xpress)<np.true_divide(w0,2) and
             abs(y0+np.true_divide(h0,2)-ypress)<np.true_divide(h0,2)):
            
            pos = ''
            
            # Top / Bottom
            
            if abs(y0-ypress)<bt*h0:
                pos = pos+'Bottom'
            elif abs(y0+h0-ypress)<bt*h0:
                pos = pos+'Top'
                
            # Right / Left
            
            if abs(x0-xpress)<bt*w0:
                pos = pos+'Left'
                
            elif abs(x0+w0-xpress)<bt*w0:
                pos = pos+'Right'
        
            if pos == '':pos = 'In'
        else:
            pos = 'Out'
            
            
        
                 
        return pos

        



