# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyfit.ui'
#
# Created: Thu Jul 16 10:10:40 2015
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
        PyFit.resize(1195, 894)
        PyFit.setMaximumSize(QtCore.QSize(1196, 894))
        self.centralwidget = QtGui.QWidget(PyFit)
        self.centralwidget.setMinimumSize(QtCore.QSize(1150, 560))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.toolbar = QtGui.QFrame(self.centralwidget)
        self.toolbar.setGeometry(QtCore.QRect(720, 520, 41, 31))
        self.toolbar.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolbar.setFrameShadow(QtGui.QFrame.Raised)
        self.toolbar.setLineWidth(0)
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1201, 581))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_2.setGeometry(QtCore.QRect(710, 0, 221, 181))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.folder_tree = QtGui.QTreeView(self.groupBox_2)
        self.folder_tree.setGeometry(QtCore.QRect(10, 40, 191, 91))
        self.folder_tree.setObjectName(_fromUtf8("folder_tree"))
        self.current_dir_txt = QtGui.QLabel(self.groupBox_2)
        self.current_dir_txt.setGeometry(QtCore.QRect(10, 20, 191, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.current_dir_txt.setFont(font)
        self.current_dir_txt.setTextFormat(QtCore.Qt.AutoText)
        self.current_dir_txt.setWordWrap(False)
        self.current_dir_txt.setObjectName(_fromUtf8("current_dir_txt"))
        self.folder_tree_back = QtGui.QPushButton(self.groupBox_2)
        self.folder_tree_back.setGeometry(QtCore.QRect(10, 140, 31, 21))
        self.folder_tree_back.setObjectName(_fromUtf8("folder_tree_back"))
        self.calendar = QtGui.QDateEdit(self.groupBox_2)
        self.calendar.setGeometry(QtCore.QRect(50, 140, 91, 22))
        self.calendar.setCalendarPopup(True)
        self.calendar.setObjectName(_fromUtf8("calendar"))
        self.calendar_root_button = QtGui.QPushButton(self.groupBox_2)
        self.calendar_root_button.setGeometry(QtCore.QRect(150, 140, 31, 21))
        self.calendar_root_button.setToolTip(_fromUtf8(""))
        self.calendar_root_button.setObjectName(_fromUtf8("calendar_root_button"))
        self.tree_root_button = QtGui.QPushButton(self.groupBox_2)
        self.tree_root_button.setGeometry(QtCore.QRect(202, 17, 16, 21))
        self.tree_root_button.setToolTip(_fromUtf8(""))
        self.tree_root_button.setObjectName(_fromUtf8("tree_root_button"))
        self.plotWindow = GuiqwtScreen(self.tab_3)
        self.plotWindow.setGeometry(QtCore.QRect(0, 7, 711, 491))
        self.plotWindow.setObjectName(_fromUtf8("plotWindow"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab_3)
        self.groupBox_3.setGeometry(QtCore.QRect(710, 190, 221, 261))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.fitEditorTab = QtGui.QTabWidget(self.groupBox_3)
        self.fitEditorTab.setGeometry(QtCore.QRect(7, 20, 211, 231))
        self.fitEditorTab.setObjectName(_fromUtf8("fitEditorTab"))
        self.fit_settings_tab = QtGui.QWidget()
        self.fit_settings_tab.setObjectName(_fromUtf8("fit_settings_tab"))
        self.fit_binning_box = QtGui.QCheckBox(self.fit_settings_tab)
        self.fit_binning_box.setGeometry(QtCore.QRect(10, 35, 97, 22))
        self.fit_binning_box.setObjectName(_fromUtf8("fit_binning_box"))
        self.fit_autobin_box = QtGui.QCheckBox(self.fit_settings_tab)
        self.fit_autobin_box.setGeometry(QtCore.QRect(30, 78, 151, 22))
        self.fit_autobin_box.setObjectName(_fromUtf8("fit_autobin_box"))
        self.fit_binning_txt = QtGui.QLineEdit(self.fit_settings_tab)
        self.fit_binning_txt.setGeometry(QtCore.QRect(60, 56, 41, 20))
        self.fit_binning_txt.setFrame(True)
        self.fit_binning_txt.setObjectName(_fromUtf8("fit_binning_txt"))
        self.fit_binning_maxpoints_txt = QtGui.QLineEdit(self.fit_settings_tab)
        self.fit_binning_maxpoints_txt.setGeometry(QtCore.QRect(90, 100, 41, 20))
        self.fit_binning_maxpoints_txt.setFrame(True)
        self.fit_binning_maxpoints_txt.setObjectName(_fromUtf8("fit_binning_maxpoints_txt"))
        self.fit_binning_label1 = QtGui.QLabel(self.fit_settings_tab)
        self.fit_binning_label1.setGeometry(QtCore.QRect(50, 100, 41, 16))
        self.fit_binning_label1.setObjectName(_fromUtf8("fit_binning_label1"))
        self.fit_binning_label2 = QtGui.QLabel(self.fit_settings_tab)
        self.fit_binning_label2.setGeometry(QtCore.QRect(30, 58, 31, 16))
        self.fit_binning_label2.setObjectName(_fromUtf8("fit_binning_label2"))
        self.fit_type = QtGui.QComboBox(self.fit_settings_tab)
        self.fit_type.setGeometry(QtCore.QRect(8, 7, 121, 22))
        self.fit_type.setObjectName(_fromUtf8("fit_type"))
        self.fit_exclude_hole_box = QtGui.QCheckBox(self.fit_settings_tab)
        self.fit_exclude_hole_box.setGeometry(QtCore.QRect(10, 124, 141, 22))
        self.fit_exclude_hole_box.setObjectName(_fromUtf8("fit_exclude_hole_box"))
        self.fit_order = QtGui.QComboBox(self.fit_settings_tab)
        self.fit_order.setGeometry(QtCore.QRect(11, 175, 101, 22))
        self.fit_order.setObjectName(_fromUtf8("fit_order"))
        self.hide_variable_txt_3 = QtGui.QLabel(self.fit_settings_tab)
        self.hide_variable_txt_3.setGeometry(QtCore.QRect(13, 155, 101, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.hide_variable_txt_3.setFont(font)
        self.hide_variable_txt_3.setTextFormat(QtCore.Qt.AutoText)
        self.hide_variable_txt_3.setWordWrap(False)
        self.hide_variable_txt_3.setObjectName(_fromUtf8("hide_variable_txt_3"))
        self.fitEditorTab.addTab(self.fit_settings_tab, _fromUtf8(""))
        self.cam_settings_tab = QtGui.QWidget()
        self.cam_settings_tab.setObjectName(_fromUtf8("cam_settings_tab"))
        self.cam_type = QtGui.QComboBox(self.cam_settings_tab)
        self.cam_type.setGeometry(QtCore.QRect(0, 10, 121, 22))
        self.cam_type.setObjectName(_fromUtf8("cam_type"))
        self.remove_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.remove_cam_button.setGeometry(QtCore.QRect(166, 10, 31, 23))
        self.remove_cam_button.setObjectName(_fromUtf8("remove_cam_button"))
        self.add_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.add_cam_button.setGeometry(QtCore.QRect(130, 10, 31, 23))
        self.add_cam_button.setObjectName(_fromUtf8("add_cam_button"))
        self.fit_binning_label2_2 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_2.setGeometry(QtCore.QRect(10, 44, 71, 16))
        self.fit_binning_label2_2.setObjectName(_fromUtf8("fit_binning_label2_2"))
        self.cam_mag = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_mag.setGeometry(QtCore.QRect(90, 41, 41, 20))
        self.cam_mag.setFrame(True)
        self.cam_mag.setObjectName(_fromUtf8("cam_mag"))
        self.cam_px_sizex = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_px_sizex.setGeometry(QtCore.QRect(90, 68, 41, 20))
        self.cam_px_sizex.setFrame(True)
        self.cam_px_sizex.setObjectName(_fromUtf8("cam_px_sizex"))
        self.fit_binning_label2_3 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_3.setGeometry(QtCore.QRect(10, 71, 71, 16))
        self.fit_binning_label2_3.setObjectName(_fromUtf8("fit_binning_label2_3"))
        self.cam_px_sizey = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_px_sizey.setGeometry(QtCore.QRect(150, 68, 41, 20))
        self.cam_px_sizey.setFrame(True)
        self.cam_px_sizey.setObjectName(_fromUtf8("cam_px_sizey"))
        self.fit_binning_label2_4 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_4.setGeometry(QtCore.QRect(140, 71, 16, 16))
        self.fit_binning_label2_4.setObjectName(_fromUtf8("fit_binning_label2_4"))
        self.fit_binning_label2_5 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_5.setGeometry(QtCore.QRect(5, 97, 71, 16))
        self.fit_binning_label2_5.setObjectName(_fromUtf8("fit_binning_label2_5"))
        self.cam_img_sizex = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_img_sizex.setGeometry(QtCore.QRect(90, 94, 41, 20))
        self.cam_img_sizex.setFrame(True)
        self.cam_img_sizex.setObjectName(_fromUtf8("cam_img_sizex"))
        self.cam_img_sizey = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_img_sizey.setGeometry(QtCore.QRect(150, 93, 41, 20))
        self.cam_img_sizey.setFrame(True)
        self.cam_img_sizey.setObjectName(_fromUtf8("cam_img_sizey"))
        self.fit_binning_label2_6 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_6.setGeometry(QtCore.QRect(140, 96, 16, 16))
        self.fit_binning_label2_6.setObjectName(_fromUtf8("fit_binning_label2_6"))
        self.cam_image_ext = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_image_ext.setGeometry(QtCore.QRect(91, 120, 81, 21))
        self.cam_image_ext.setFrame(True)
        self.cam_image_ext.setObjectName(_fromUtf8("cam_image_ext"))
        self.fit_binning_label2_7 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_7.setGeometry(QtCore.QRect(8, 124, 81, 16))
        self.fit_binning_label2_7.setObjectName(_fromUtf8("fit_binning_label2_7"))
        self.fit_binning_label2_8 = QtGui.QLabel(self.cam_settings_tab)
        self.fit_binning_label2_8.setGeometry(QtCore.QRect(10, 150, 41, 16))
        self.fit_binning_label2_8.setObjectName(_fromUtf8("fit_binning_label2_8"))
        self.cam_od_calc = QtGui.QLineEdit(self.cam_settings_tab)
        self.cam_od_calc.setGeometry(QtCore.QRect(57, 148, 121, 21))
        self.cam_od_calc.setFrame(True)
        self.cam_od_calc.setObjectName(_fromUtf8("cam_od_calc"))
        self.rename_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.rename_cam_button.setGeometry(QtCore.QRect(140, 40, 51, 23))
        self.rename_cam_button.setObjectName(_fromUtf8("rename_cam_button"))
        self.update_cam_button = QtGui.QPushButton(self.cam_settings_tab)
        self.update_cam_button.setGeometry(QtCore.QRect(0, 170, 51, 31))
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
        self.groupBox.setGeometry(QtCore.QRect(110, 10, 101, 91))
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
        self.refresh_display_button.setGeometry(QtCore.QRect(120, 140, 75, 23))
        self.refresh_display_button.setObjectName(_fromUtf8("refresh_display_button"))
        self.display_interpolation = QtGui.QComboBox(self.tab)
        self.display_interpolation.setGeometry(QtCore.QRect(10, 30, 81, 22))
        self.display_interpolation.setObjectName(_fromUtf8("display_interpolation"))
        self.fit_binning_label2_9 = QtGui.QLabel(self.tab)
        self.fit_binning_label2_9.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.fit_binning_label2_9.setObjectName(_fromUtf8("fit_binning_label2_9"))
        self.display_hole_box = QtGui.QCheckBox(self.tab)
        self.display_hole_box.setGeometry(QtCore.QRect(10, 140, 101, 17))
        self.display_hole_box.setObjectName(_fromUtf8("display_hole_box"))
        self.fitEditorTab.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.list_plot_x = QtGui.QComboBox(self.tab_2)
        self.list_plot_x.setGeometry(QtCore.QRect(30, 10, 111, 22))
        self.list_plot_x.setObjectName(_fromUtf8("list_plot_x"))
        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 16, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.list_plot_y = QtGui.QComboBox(self.tab_2)
        self.list_plot_y.setGeometry(QtCore.QRect(30, 40, 111, 22))
        self.list_plot_y.setObjectName(_fromUtf8("list_plot_y"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(10, 40, 16, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.quickPlotButton = QtGui.QPushButton(self.tab_2)
        self.quickPlotButton.setGeometry(QtCore.QRect(150, 10, 41, 41))
        self.quickPlotButton.setObjectName(_fromUtf8("quickPlotButton"))
        self.quickStatsButton = QtGui.QPushButton(self.tab_2)
        self.quickStatsButton.setGeometry(QtCore.QRect(10, 141, 51, 31))
        self.quickStatsButton.setObjectName(_fromUtf8("quickStatsButton"))
        self.list_fit_type = QtGui.QComboBox(self.tab_2)
        self.list_fit_type.setGeometry(QtCore.QRect(47, 70, 151, 22))
        self.list_fit_type.setObjectName(_fromUtf8("list_fit_type"))
        self.fit_list_box = QtGui.QCheckBox(self.tab_2)
        self.fit_list_box.setGeometry(QtCore.QRect(7, 70, 61, 22))
        self.fit_list_box.setObjectName(_fromUtf8("fit_list_box"))
        self.send_to_console_button = QtGui.QPushButton(self.tab_2)
        self.send_to_console_button.setGeometry(QtCore.QRect(70, 141, 61, 31))
        self.send_to_console_button.setObjectName(_fromUtf8("send_to_console_button"))
        self.hide_variable_txt_2 = QtGui.QLabel(self.tab_2)
        self.hide_variable_txt_2.setGeometry(QtCore.QRect(72, 127, 61, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.hide_variable_txt_2.setFont(font)
        self.hide_variable_txt_2.setTextFormat(QtCore.Qt.AutoText)
        self.hide_variable_txt_2.setWordWrap(False)
        self.hide_variable_txt_2.setObjectName(_fromUtf8("hide_variable_txt_2"))
        self.fitEditorTab.addTab(self.tab_2, _fromUtf8(""))
        self.hide_variables_button = QtGui.QPushButton(self.tab_3)
        self.hide_variables_button.setGeometry(QtCore.QRect(1110, 520, 51, 21))
        self.hide_variables_button.setObjectName(_fromUtf8("hide_variables_button"))
        self.hide_variable_txt = QtGui.QLabel(self.tab_3)
        self.hide_variable_txt.setGeometry(QtCore.QRect(972, 521, 131, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.hide_variable_txt.setFont(font)
        self.hide_variable_txt.setTextFormat(QtCore.Qt.AutoText)
        self.hide_variable_txt.setWordWrap(False)
        self.hide_variable_txt.setObjectName(_fromUtf8("hide_variable_txt"))
        self.refresh_file_list = QtGui.QPushButton(self.tab_3)
        self.refresh_file_list.setGeometry(QtCore.QRect(970, 498, 51, 21))
        self.refresh_file_list.setObjectName(_fromUtf8("refresh_file_list"))
        self.file_list = QtGui.QListView(self.tab_3)
        self.file_list.setGeometry(QtCore.QRect(940, 0, 251, 491))
        self.file_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.file_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.file_list.setObjectName(_fromUtf8("file_list"))
        self.progressBar = QtGui.QProgressBar(self.tab_3)
        self.progressBar.setGeometry(QtCore.QRect(1030, 500, 141, 16))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.fitButton = QtGui.QPushButton(self.tab_3)
        self.fitButton.setGeometry(QtCore.QRect(710, 450, 75, 41))
        self.fitButton.setDefault(False)
        self.fitButton.setFlat(False)
        self.fitButton.setObjectName(_fromUtf8("fitButton"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        PyFit.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(PyFit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1195, 21))
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
        self.result_dock.setMinimumSize(QtCore.QSize(320, 258))
        self.result_dock.setMaximumSize(QtCore.QSize(320, 500))
        self.result_dock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.result_dock.setObjectName(_fromUtf8("result_dock"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.result_text = QtGui.QTextEdit(self.dockWidgetContents_2)
        self.result_text.setGeometry(QtCore.QRect(0, 0, 321, 211))
        self.result_text.setReadOnly(True)
        self.result_text.setObjectName(_fromUtf8("result_text"))
        self.flush_result_button = QtGui.QPushButton(self.dockWidgetContents_2)
        self.flush_result_button.setGeometry(QtCore.QRect(0, 211, 321, 20))
        self.flush_result_button.setObjectName(_fromUtf8("flush_result_button"))
        self.result_dock.setWidget(self.dockWidgetContents_2)
        PyFit.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.result_dock)
        self.toolBar = QtGui.QToolBar(PyFit)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        PyFit.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.comment_dock = QtGui.QDockWidget(PyFit)
        self.comment_dock.setMinimumSize(QtCore.QSize(300, 258))
        self.comment_dock.setMaximumSize(QtCore.QSize(300, 258))
        self.comment_dock.setObjectName(_fromUtf8("comment_dock"))
        self.dockWidgetContents_4 = QtGui.QWidget()
        self.dockWidgetContents_4.setObjectName(_fromUtf8("dockWidgetContents_4"))
        self.fit_comment_text = QtGui.QTextEdit(self.dockWidgetContents_4)
        self.fit_comment_text.setGeometry(QtCore.QRect(5, 0, 291, 221))
        self.fit_comment_text.setFrameShape(QtGui.QFrame.Box)
        self.fit_comment_text.setFrameShadow(QtGui.QFrame.Plain)
        self.fit_comment_text.setReadOnly(False)
        self.fit_comment_text.setObjectName(_fromUtf8("fit_comment_text"))
        self.comment_dock.setWidget(self.dockWidgetContents_4)
        PyFit.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.comment_dock)

        self.retranslateUi(PyFit)
        self.tabWidget.setCurrentIndex(0)
        self.fitEditorTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PyFit)

    def retranslateUi(self, PyFit):
        PyFit.setWindowTitle(_translate("PyFit", "MainWindow", None))
        self.groupBox_2.setTitle(_translate("PyFit", "Browsing", None))
        self.current_dir_txt.setText(_translate("PyFit", "c:/path/to/our/file", None))
        self.folder_tree_back.setText(_translate("PyFit", "<--", None))
        self.calendar_root_button.setText(_translate("PyFit", "...", None))
        self.tree_root_button.setText(_translate("PyFit", "....", None))
        self.groupBox_3.setTitle(_translate("PyFit", "Fit options", None))
        self.fit_binning_box.setText(_translate("PyFit", "Binning", None))
        self.fit_autobin_box.setText(_translate("PyFit", "Auto binning ", None))
        self.fit_binning_label1.setText(_translate("PyFit", "Max :", None))
        self.fit_binning_label2.setText(_translate("PyFit", "N =", None))
        self.fit_exclude_hole_box.setText(_translate("PyFit", "exclude hole (simple fit)", None))
        self.hide_variable_txt_3.setText(_translate("PyFit", "fit order (double fit)", None))
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
        self.display_hole_box.setText(_translate("PyFit", "show hole rect.", None))
        self.fitEditorTab.setTabText(self.fitEditorTab.indexOf(self.tab), _translate("PyFit", "Disp", None))
        self.label_3.setText(_translate("PyFit", "X :", None))
        self.label_4.setText(_translate("PyFit", "Y :", None))
        self.quickPlotButton.setText(_translate("PyFit", "PLOT", None))
        self.quickStatsButton.setText(_translate("PyFit", "Stats", None))
        self.fit_list_box.setText(_translate("PyFit", "fit :", None))
        self.send_to_console_button.setText(_translate("PyFit", "to console", None))
        self.hide_variable_txt_2.setText(_translate("PyFit", "--> res", None))
        self.fitEditorTab.setTabText(self.fitEditorTab.indexOf(self.tab_2), _translate("PyFit", "List", None))
        self.hide_variables_button.setText(_translate("PyFit", "choose", None))
        self.hide_variable_txt.setText(_translate("PyFit", "some variables are hidden", None))
        self.refresh_file_list.setText(_translate("PyFit", "refresh", None))
        self.fitButton.setText(_translate("PyFit", "FIT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("PyFit", "Display and Fit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("PyFit", "...", None))
        self.console_dock.setWindowTitle(_translate("PyFit", "console", None))
        self.result_dock.setWindowTitle(_translate("PyFit", "results", None))
        self.flush_result_button.setText(_translate("PyFit", "flush", None))
        self.toolBar.setWindowTitle(_translate("PyFit", "toolBar", None))
        self.comment_dock.setWindowTitle(_translate("PyFit", "comments", None))

from GuiqwtScreen import GuiqwtScreen
