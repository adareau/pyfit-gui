# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'screen.ui'
#
# Created: Mon Jan 26 18:26:10 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_screen(object):
    def setupUi(self, screen):
        screen.setObjectName(_fromUtf8("screen"))
        screen.resize(671, 500)
        self.widget = QtGui.QWidget(screen)
        self.widget.setGeometry(QtCore.QRect(0, 0, 671, 501))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cutX = CutScreen(self.widget)
        self.cutX.setObjectName(_fromUtf8("cutX"))
        self.gridLayout.addWidget(self.cutX, 0, 0, 1, 1)
        self.imageScreen = ImageScreen(self.widget)
        self.imageScreen.setObjectName(_fromUtf8("imageScreen"))
        self.gridLayout.addWidget(self.imageScreen, 1, 0, 1, 1)
        self.cutY = CutScreen(self.widget)
        self.cutY.setObjectName(_fromUtf8("cutY"))
        self.gridLayout.addWidget(self.cutY, 1, 1, 1, 1)
        self.mini = QtGui.QWidget(self.widget)
        self.mini.setObjectName(_fromUtf8("mini"))
        self.gridLayout.addWidget(self.mini, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 3)

        self.retranslateUi(screen)
        QtCore.QMetaObject.connectSlotsByName(screen)

    def retranslateUi(self, screen):
        screen.setWindowTitle(_translate("screen", "Form", None))

from GuiqwtScreen_v2 import ImageScreen, CutScreen
