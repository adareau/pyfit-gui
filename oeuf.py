# -*- coding: utf-8 -*-
'''----------------------------------------------------------
  file        : D:/Alexandre DAREAU/Documents/Programmation/Python/pyfit-gui/oeuf.py
  author      : A.  Dareau
  created     : 2015-07-23 10:17
  modified    : 2015-07-23 10:17
  description : Easter eggs, all over the place
----------------------------------------------------------'''


def keylog_reader(gui):
    
    action_triggered = False
    
    keylog = gui.data.keylog
    # KONAMI 
    if keylog.find('upupdowndownleftrightleftrightbareturn')>-1:
        gui.print_result('KONAMI !!!!!!!!!!')
        action_triggered = True
        
    return action_triggered