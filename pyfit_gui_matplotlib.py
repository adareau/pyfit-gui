# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyfit.ui'
#
# Created: Thu Jan 22 11:50:51 2015
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

class Ui_PyFit(object):
    def setupUi(self, PyFit):
        PyFit.setObjectName(_fromUtf8("PyFit"))
        PyFit.resize(1036, 886)
        self.centralwidget = QtGui.QWidget(PyFit)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.folder_tree = QtGui.QTreeView(self.centralwidget)
        self.folder_tree.setGeometry(QtCore.QRect(600, 70, 191, 192))
        self.folder_tree.setObjectName(_fromUtf8("folder_tree"))
        self.fitButton = QtGui.QPushButton(self.centralwidget)
        self.fitButton.setGeometry(QtCore.QRect(880, 350, 75, 41))
        self.fitButton.setDefault(False)
        self.fitButton.setFlat(False)
        self.fitButton.setObjectName(_fromUtf8("fitButton"))
        self.plotWindow = ScreenWidget(self.centralwidget)
        self.plotWindow.setGeometry(QtCore.QRect(10, 50, 571, 461))
        self.plotWindow.setObjectName(_fromUtf8("plotWindow"))
        self.file_list = QtGui.QListView(self.centralwidget)
        self.file_list.setGeometry(QtCore.QRect(810, 70, 201, 192))
        self.file_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.file_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.file_list.setObjectName(_fromUtf8("file_list"))
        self.folder_tree_back = QtGui.QPushButton(self.centralwidget)
        self.folder_tree_back.setGeometry(QtCore.QRect(600, 270, 31, 21))
        self.folder_tree_back.setObjectName(_fromUtf8("folder_tree_back"))
        self.toolbar = QtGui.QFrame(self.centralwidget)
        self.toolbar.setGeometry(QtCore.QRect(0, 0, 1021, 51))
        self.toolbar.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolbar.setFrameShadow(QtGui.QFrame.Raised)
        self.toolbar.setLineWidth(0)
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        self.toolbar_ROI = QtGui.QToolButton(self.toolbar)
        self.toolbar_ROI.setGeometry(QtCore.QRect(0, 10, 41, 41))
        self.toolbar_ROI.setCheckable(True)
        self.toolbar_ROI.setObjectName(_fromUtf8("toolbar_ROI"))
        self.toolbar_zoom2ROI = QtGui.QToolButton(self.toolbar)
        self.toolbar_zoom2ROI.setGeometry(QtCore.QRect(40, 10, 101, 41))
        self.toolbar_zoom2ROI.setCheckable(False)
        self.toolbar_zoom2ROI.setObjectName(_fromUtf8("toolbar_zoom2ROI"))
        self.toolbar_background = QtGui.QToolButton(self.toolbar)
        self.toolbar_background.setGeometry(QtCore.QRect(140, 10, 51, 41))
        self.toolbar_background.setCheckable(True)
        self.toolbar_background.setObjectName(_fromUtf8("toolbar_background"))
        self.toolbar_zoom2BKGND = QtGui.QToolButton(self.toolbar)
        self.toolbar_zoom2BKGND.setGeometry(QtCore.QRect(190, 10, 101, 41))
        self.toolbar_zoom2BKGND.setCheckable(False)
        self.toolbar_zoom2BKGND.setObjectName(_fromUtf8("toolbar_zoom2BKGND"))
        self.fitEditorTab = QtGui.QTabWidget(self.centralwidget)
        self.fitEditorTab.setGeometry(QtCore.QRect(600, 310, 271, 201))
        self.fitEditorTab.setObjectName(_fromUtf8("fitEditorTab"))
        self.fit_settings_tab = QtGui.QWidget()
        self.fit_settings_tab.setObjectName(_fromUtf8("fit_settings_tab"))
        self.fit_binning_box = QtGui.QCheckBox(self.fit_settings_tab)
        self.fit_binning_box.setGeometry(QtCore.QRect(10, 10, 97, 22))
        self.fit_binning_box.setObjectName(_fromUtf8("fit_binning_box"))
        self.fit_autobin_box = QtGui.QCheckBox(self.fit_settings_tab)
        self.fit_autobin_box.setGeometry(QtCore.QRect(30, 53, 151, 22))
        self.fit_autobin_box.setObjectName(_fromUtf8("fit_autobin_box"))
        self.fit_binning_txt = QtGui.QLineEdit(self.fit_settings_tab)
        self.fit_binning_txt.setGeometry(QtCore.QRect(60, 31, 41, 20))
        self.fit_binning_txt.setFrame(True)
        self.fit_binning_txt.setObjectName(_fromUtf8("fit_binning_txt"))
        self.fit_binning_maxpoints_txt = QtGui.QLineEdit(self.fit_settings_tab)
        self.fit_binning_maxpoints_txt.setGeometry(QtCore.QRect(90, 75, 41, 20))
        self.fit_binning_maxpoints_txt.setFrame(True)
        self.fit_binning_maxpoints_txt.setObjectName(_fromUtf8("fit_binning_maxpoints_txt"))
        self.fit_binning_label1 = QtGui.QLabel(self.fit_settings_tab)
        self.fit_binning_label1.setGeometry(QtCore.QRect(50, 75, 41, 16))
        self.fit_binning_label1.setObjectName(_fromUtf8("fit_binning_label1"))
        self.fit_binning_label2 = QtGui.QLabel(self.fit_settings_tab)
        self.fit_binning_label2.setGeometry(QtCore.QRect(30, 33, 31, 16))
        self.fit_binning_label2.setObjectName(_fromUtf8("fit_binning_label2"))
        self.fit_type = QtGui.QComboBox(self.fit_settings_tab)
        self.fit_type.setGeometry(QtCore.QRect(10, 140, 121, 22))
        self.fit_type.setObjectName(_fromUtf8("fit_type"))
        self.fitEditorTab.addTab(self.fit_settings_tab, _fromUtf8(""))
        self.cam_settings_tab = QtGui.QWidget()
        self.cam_settings_tab.setObjectName(_fromUtf8("cam_settings_tab"))
        self.cam_type = QtGui.QComboBox(self.cam_settings_tab)
        self.cam_type.setGeometry(QtCore.QRect(10, 10, 121, 22))
        self.cam_type.setObjectName(_fromUtf8("cam_type"))
        self.remove_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.remove_cam_button.setGeometry(QtCore.QRect(176, 10, 31, 23))
        self.remove_cam_button.setObjectName(_fromUtf8("remove_cam_button"))
        self.add_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.add_cam_button.setGeometry(QtCore.QRect(140, 10, 31, 23))
        self.add_cam_button.setObjectName(_fromUtf8("add_cam_button"))
        self.fit_binning_label2_2 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_2.setGeometry(QtCore.QRect(20, 44, 71, 16))
        self.fit_binning_label2_2.setObjectName(_fromUtf8("fit_binning_label2_2"))
        self.cam_mag = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_mag.setGeometry(QtCore.QRect(100, 41, 41, 20))
        self.cam_mag.setFrame(True)
        self.cam_mag.setObjectName(_fromUtf8("cam_mag"))
        self.cam_px_sizex = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_px_sizex.setGeometry(QtCore.QRect(100, 68, 41, 20))
        self.cam_px_sizex.setFrame(True)
        self.cam_px_sizex.setObjectName(_fromUtf8("cam_px_sizex"))
        self.fit_binning_label2_3 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_3.setGeometry(QtCore.QRect(20, 71, 71, 16))
        self.fit_binning_label2_3.setObjectName(_fromUtf8("fit_binning_label2_3"))
        self.cam_px_sizey = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_px_sizey.setGeometry(QtCore.QRect(160, 68, 41, 20))
        self.cam_px_sizey.setFrame(True)
        self.cam_px_sizey.setObjectName(_fromUtf8("cam_px_sizey"))
        self.fit_binning_label2_4 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_4.setGeometry(QtCore.QRect(150, 71, 16, 16))
        self.fit_binning_label2_4.setObjectName(_fromUtf8("fit_binning_label2_4"))
        self.fit_binning_label2_5 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_5.setGeometry(QtCore.QRect(15, 97, 71, 16))
        self.fit_binning_label2_5.setObjectName(_fromUtf8("fit_binning_label2_5"))
        self.cam_img_sizex = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_img_sizex.setGeometry(QtCore.QRect(100, 94, 41, 20))
        self.cam_img_sizex.setFrame(True)
        self.cam_img_sizex.setObjectName(_fromUtf8("cam_img_sizex"))
        self.cam_img_sizey = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_img_sizey.setGeometry(QtCore.QRect(160, 93, 41, 20))
        self.cam_img_sizey.setFrame(True)
        self.cam_img_sizey.setObjectName(_fromUtf8("cam_img_sizey"))
        self.fit_binning_label2_6 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_6.setGeometry(QtCore.QRect(150, 96, 16, 16))
        self.fit_binning_label2_6.setObjectName(_fromUtf8("fit_binning_label2_6"))
        self.cam_image_ext = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_image_ext.setGeometry(QtCore.QRect(101, 120, 81, 21))
        self.cam_image_ext.setFrame(True)
        self.cam_image_ext.setObjectName(_fromUtf8("cam_image_ext"))
        self.fit_binning_label2_7 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_7.setGeometry(QtCore.QRect(18, 124, 81, 16))
        self.fit_binning_label2_7.setObjectName(_fromUtf8("fit_binning_label2_7"))
        self.fit_binning_label2_8 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_8.setGeometry(QtCore.QRect(20, 150, 41, 16))
        self.fit_binning_label2_8.setObjectName(_fromUtf8("fit_binning_label2_8"))
        self.cam_od_calc = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_od_calc.setGeometry(QtCore.QRect(67, 148, 121, 21))
        self.cam_od_calc.setFrame(True)
        self.cam_od_calc.setObjectName(_fromUtf8("cam_od_calc"))
        self.rename_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.rename_cam_button.setGeometry(QtCore.QRect(211, 10, 51, 23))
        self.rename_cam_button.setObjectName(_fromUtf8("rename_cam_button"))
        self.update_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.update_cam_button.setGeometry(QtCore.QRect(210, 142, 51, 31))
        self.update_cam_button.setDefault(False)
        self.update_cam_button.setFlat(False)
        self.update_cam_button.setObjectName(_fromUtf8("update_cam_button"))
        self.fitEditorTab.addTab(self.cam_settings_tab, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.disp_fit_contour_box = QtGui.QCheckBox(self.tab)
        self.disp_fit_contour_box.setGeometry(QtCore.QRect(10, 60, 101, 17))
        self.disp_fit_contour_box.setObjectName(_fromUtf8("disp_fit_contour_box"))
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(140, 10, 111, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.colormap_min = QtGui.QLineEdit(self.groupBox)
        self.colormap_min.setGeometry(QtCore.QRect(10, 60, 31, 20))
        self.colormap_min.setFrame(True)
        self.colormap_min.setObjectName(_fromUtf8("colormap_min"))
        self.colormap_max = QtGui.QLineEdit(self.groupBox)
        self.colormap_max.setGeometry(QtCore.QRect(60, 60, 31, 20))
        self.colormap_max.setFrame(True)
        self.colormap_max.setObjectName(_fromUtf8("colormap_max"))
        self.colormap_type = QtGui.QComboBox(self.groupBox)
        self.colormap_type.setGeometry(QtCore.QRect(10, 20, 81, 22))
        self.colormap_type.setObjectName(_fromUtf8("colormap_type"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(12, 44, 21, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(61, 44, 21, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.refresh_display_button = QtGui.QPushButton(self.tab)
        self.refresh_display_button.setGeometry(QtCore.QRect(180, 140, 75, 23))
        self.refresh_display_button.setObjectName(_fromUtf8("refresh_display_button"))
        self.display_interpolation = QtGui.QComboBox(self.tab)
        self.display_interpolation.setGeometry(QtCore.QRect(10, 30, 81, 22))
        self.display_interpolation.setObjectName(_fromUtf8("display_interpolation"))
        self.fit_binning_label2_9 = QtGui.QLabel(self.tab)
        self.fit_binning_label2_9.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.fit_binning_label2_9.setObjectName(_fromUtf8("fit_binning_label2_9"))
        self.fitEditorTab.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.list_plot_x = QtGui.QComboBox(self.tab_2)
        self.list_plot_x.setGeometry(QtCore.QRect(40, 10, 111, 22))
        self.list_plot_x.setObjectName(_fromUtf8("list_plot_x"))
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 16, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.list_plot_y = QtGui.QComboBox(self.tab_2)
        self.list_plot_y.setGeometry(QtCore.QRect(40, 40, 111, 22))
        self.list_plot_y.setObjectName(_fromUtf8("list_plot_y"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 16, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.quickPlotButton = QtGui.QPushButton(self.tab_2)
        self.quickPlotButton.setGeometry(QtCore.QRect(160, 10, 51, 31))
        self.quickPlotButton.setObjectName(_fromUtf8("quickPlotButton"))
        self.quickStatsButton = QtGui.QPushButton(self.tab_2)
        self.quickStatsButton.setGeometry(QtCore.QRect(10, 140, 51, 31))
        self.quickStatsButton.setObjectName(_fromUtf8("quickStatsButton"))
        self.list_fit_type = QtGui.QComboBox(self.tab_2)
        self.list_fit_type.setGeometry(QtCore.QRect(60, 70, 151, 22))
        self.list_fit_type.setObjectName(_fromUtf8("list_fit_type"))
        self.fit_list_box = QtGui.QCheckBox(self.tab_2)
        self.fit_list_box.setGeometry(QtCore.QRect(20, 70, 61, 22))
        self.fit_list_box.setObjectName(_fromUtf8("fit_list_box"))
        self.fitEditorTab.addTab(self.tab_2, _fromUtf8(""))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(810, 270, 201, 16))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.current_dir_txt = QtGui.QLabel(self.centralwidget)
        self.current_dir_txt.setGeometry(QtCore.QRect(600, 50, 411, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.current_dir_txt.setFont(font)
        self.current_dir_txt.setTextFormat(QtCore.Qt.AutoText)
        self.current_dir_txt.setWordWrap(False)
        self.current_dir_txt.setObjectName(_fromUtf8("current_dir_txt"))
        PyFit.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PyFit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1036, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        PyFit.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(PyFit)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        PyFit.setStatusBar(self.statusbar)
        self.console_dock = QtGui.QDockWidget(PyFit)
        self.console_dock.setFloating(False)
        self.console_dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.console_dock.setObjectName(_fromUtf8("console_dock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.console_dock.setWidget(self.dockWidgetContents)
        PyFit.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.console_dock)
        self.result_dock = QtGui.QDockWidget(PyFit)
        self.result_dock.setMinimumSize(QtCore.QSize(307, 258))
        self.result_dock.setMaximumSize(QtCore.QSize(307, 500))
        self.result_dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.result_dock.setObjectName(_fromUtf8("result_dock"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.result_text = QtGui.QTextEdit(self.dockWidgetContents_2)
        self.result_text.setGeometry(QtCore.QRect(0, 0, 300, 211))
        self.result_text.setReadOnly(True)
        self.result_text.setObjectName(_fromUtf8("result_text"))
        self.flush_result_button = QtGui.QPushButton(self.dockWidgetContents_2)
        self.flush_result_button.setGeometry(QtCore.QRect(0, 211, 300, 20))
        self.flush_result_button.setObjectName(_fromUtf8("flush_result_button"))
        self.result_dock.setWidget(self.dockWidgetContents_2)
        PyFit.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.result_dock)

        self.retranslateUi(PyFit)
        self.fitEditorTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(PyFit)

    def retranslateUi(self, PyFit):
        PyFit.setWindowTitle(_translate("PyFit", "MainWindow", None))
        self.fitButton.setText(_translate("PyFit", "FIT", None))
        self.folder_tree_back.setText(_translate("PyFit", "<--", None))
        self.toolbar_ROI.setText(_translate("PyFit", "ROI", None))
        self.toolbar_zoom2ROI.setText(_translate("PyFit", "Zoom to ROI", None))
        self.toolbar_background.setText(_translate("PyFit", "BKGND", None))
        self.toolbar_zoom2BKGND.setText(_translate("PyFit", "Zoom to BKGND", None))
        self.fit_binning_box.setText(_translate("PyFit", "Binning", None))
        self.fit_autobin_box.setText(_translate("PyFit", "Auto binning ", None))
        self.fit_binning_label1.setText(_translate("PyFit", "Max :", None))
        self.fit_binning_label2.setText(_translate("PyFit", "N =", None))
        self.fitEditorTab.setTabText(self.fitEditorTab.indexOf(self.fit_settings_tab), _translate("PyFit", "Fit", None))
        self.remove_cam_button.setText(_translate("PyFit", "del", None))
        self.add_cam_button.setText(_translate("PyFit", "new", None))
        self.fit_binning_label2_2.setText(_translate("PyFit", "magnification :", None))
        self.fit_binning_label2_3.setText(_translate("PyFit", "pixel size :   X", None))
        self.fit_binning_label2_4.setText(_translate("PyFit", "Y", None))
        self.fit_binning_label2_5.setText(_translate("PyFit", "image size :  X", None))
        self.fit_binning_label2_6.setText(_translate("PyFit", "Y", None))
        self.fit_binning_label2_7.setText(_translate("PyFit", "image extension", None))
        self.fit_binning_label2_8.setText(_translate("PyFit", "OD calc", None))
        self.rename_cam_button.setText(_translate("PyFit", "rename", None))
        self.update_cam_button.setText(_translate("PyFit", "Update", None))
        self.fitEditorTab.setTabText(self.fitEditorTab.indexOf(self.cam_settings_tab), _translate("PyFit", "Cam", None))
        self.disp_fit_contour_box.setText(_translate("PyFit", "show fit contour", None))
        self.groupBox.setTitle(_translate("PyFit", "Colormap", None))
        self.colormap_min.setText(_translate("PyFit", "0", None))
        self.colormap_max.setText(_translate("PyFit", "1", None))
        self.label.setText(_translate("PyFit", "min", None))
        self.label_2.setText(_translate("PyFit", "max", None))
        self.refresh_display_button.setText(_translate("PyFit", "Refresh", None))
        self.fit_binning_label2_9.setText(_translate("PyFit", "interpolation", None))
        self.fitEditorTab.setTabText(self.fitEditorTab.indexOf(self.tab), _translate("PyFit", "Display", None))
        self.label_3.setText(_translate("PyFit", "X :", None))
        self.label_4.setText(_translate("PyFit", "Y :", None))
        self.quickPlotButton.setText(_translate("PyFit", "PLOT", None))
        self.quickStatsButton.setText(_translate("PyFit", "Stats", None))
        self.fit_list_box.setText(_translate("PyFit", "fit :", None))
        self.fitEditorTab.setTabText(self.fitEditorTab.indexOf(self.tab_2), _translate("PyFit", "Quick list", None))
        self.current_dir_txt.setText(_translate("PyFit", "c:/path/to/our/file", None))
        self.console_dock.setWindowTitle(_translate("PyFit", "console", None))
        self.result_dock.setWindowTitle(_translate("PyFit", "results", None))
        self.flush_result_button.setText(_translate("PyFit", "flush", None))

from ScreenWidget import ScreenWidget
