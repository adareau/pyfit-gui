# -*- coding: utf-8 -*-

import os




f_in = 'pyfit.ui'
f_out = 'pyfit_gui.py'

res = os.system('pyuic4 '+f_in+' > '+f_out)

'''
f_in = 'screen.ui'
f_out = 'screen_gui.py'

os.system('pyuic4 '+f_in+' > '+f_out)
'''

print('build ended')
print(res)