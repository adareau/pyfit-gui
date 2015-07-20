# -*- coding: utf-8 -*-
"""
Starts pyfit GUI

"""
import sys
from PyQt4 import QtCore, QtGui
import os


class StartQT4(QtGui.QMainWindow): #TODO : rename
    """
    Our pyfit gui object
    """
    def __init__(self, parent=None):

        ''' Initialize GUI '''
        # Link to ui
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_PyFit()
        self.ui.setupUi(self)
        self.setWindowTitle('PyF!T')

        # Scroll ?
        scroll_widget = QtGui.QScrollArea()
        scroll_widget.setWidget(self.ui.centralwidget)
        scroll_widget.setWidgetResizable(True)
        self.setCentralWidget(scroll_widget)

        # GUI data and settings
        self.settings = GuiSettings()
        self.load_settings()

        self.data = GuiData(self)
        self.data.gui_root = QtCore.QDir.currentPath()

        self.data.current_file_path = str(self.settings.current_folder)


        ''' GUI Components '''
        # Toolbar

        # Setting up the toolbar (we use the navigation toolbar from MPLWidget)
        # first let's add it to the top frame
        #XXX screen
        '''
        toolbar_layout = QtGui.QVBoxLayout(self.ui.toolbar)
        toolbar_layout.addWidget(self.ui.plotWindow.navigation)

        # then add all the extra toolbar buttons
        toolbar = self.ui.plotWindow.navigation


        toolbar.addSeparator()
        toolbar.addWidget(self.ui.toolbar_ROI)
        toolbar.addWidget(self.ui.toolbar_zoom2ROI)
        toolbar.addWidget(self.ui.toolbar_background)
        toolbar.addWidget(self.ui.toolbar_zoom2BKGND)

        self.ui.toolbar_ROI.clicked.connect(self.set_ROI)
        self.ui.toolbar_zoom2ROI.clicked.connect(self.zoom_to_ROI)
        self.ui.toolbar_background.clicked.connect(self.set_background)
        self.ui.toolbar_zoom2BKGND.clicked.connect(self.zoom_to_BKGND)
        '''
        '''
        a = 600
        self.ui.plotWindow.resize(int(a),int(a/1.338))

        self.ui.plotWindow.setLayout(QtGui.QHBoxLayout())
        self.ui.plotWindow.layout().addWidget(GuiqwtScreen(self))
        self.ui.plotWindow.updateGeometry()
        '''
        toolbar = self.ui.toolBar

        self.ui.plotWindow.manager.add_toolbar(toolbar, id(toolbar))

        for tool in self.ui.plotWindow.tools:
            self.ui.plotWindow.manager.add_tool(tool)

        # ROI management
        self.ui.plotWindow.manager.add_tool(ROISelectTool)
        roi_action = toolbar.actions()[-1]
        roi_action.setText("ROI")
        roi_action.setToolTip("Select ROI")
        roi_action.setStatusTip("click and draw new region of interest")
        icon = QtGui.QIcon.fromTheme("edit-cut")
        roi_action.setIcon(icon)
        #TODO : trouver icones dans
        # http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html#names
        self.roi_tool = self.ui.plotWindow.manager.get_tool(ROISelectTool)
        self.ui.plotWindow.screen.plot.add_item(self.roi_tool.rect)
        self.data.rectROI = self.roi_tool.rect
        
        # Background management
        self.ui.plotWindow.manager.add_tool(BKGNDSelectTool)
        bkgnd_action = toolbar.actions()[-1]
        bkgnd_action.setText("BKGND")
        bkgnd_action.setToolTip("Select BACKGROUND")
        bkgnd_action.setStatusTip("click and draw new background region")
        icon = QtGui.QIcon.fromTheme("edit-cut")
        bkgnd_action.setIcon(icon)
        self.bkgnd_tool = self.ui.plotWindow.manager.get_tool(BKGNDSelectTool)
        self.ui.plotWindow.screen.plot.add_item(self.bkgnd_tool.rect)
        self.data.rectBackground = self.bkgnd_tool.rect
        
        # Hole management
        self.ui.plotWindow.manager.add_tool(HOLESelectTool)
        hole_action = toolbar.actions()[-1]
        hole_action.setText("HOLE")
        hole_action.setToolTip("Select HOLE")
        hole_action.setStatusTip("click and draw new hole region")
        icon = QtGui.QIcon.fromTheme("edit-cut")
        hole_action.setIcon(icon)
        self.hole_tool = self.ui.plotWindow.manager.get_tool(HOLESelectTool)
        self.ui.plotWindow.screen.plot.add_item(self.hole_tool.rect)
        self.data.rectHOLE = self.hole_tool.rect
        
        if not self.settings.display_hole:
            self.data.rectHOLE.hide()
        #self.ui.plotWindow.manager.register_all_curve_tools()

        toolbar.addSeparator()
        '''
        # HINT : old toolbar version
        # I only keep it to have an example on toolbar button integration
        
        toolbar.addWidget(self.ui.toolbar_ROI)
        toolbar.addWidget(self.ui.toolbar_zoom2ROI)
        toolbar.addWidget(self.ui.toolbar_background)
        toolbar.addWidget(self.ui.toolbar_zoom2BKGND)

        self.ui.toolbar_ROI.clicked.connect(self.set_ROI)
        self.ui.toolbar_zoom2ROI.clicked.connect(self.zoom_to_ROI)
        self.ui.toolbar_background.clicked.connect(self.set_background)
        self.ui.toolbar_zoom2BKGND.clicked.connect(self.zoom_to_BKGND)
        '''
        # file tree browser

        self.folder_tree_model = QtGui.QFileSystemModel()
        root = self.settings.path_root
        self.folder_tree_model.setRootPath(root)
        qdir = QtCore.QDir
        self.folder_tree_model.setFilter(qdir.Dirs | qdir.Drives \
                                         | qdir.NoDotAndDotDot | qdir.AllDirs)
        self.ui.folder_tree.setModel(self.folder_tree_model)
        idx = self.folder_tree_model.index(self.settings.path_root)
        self.ui.folder_tree.setRootIndex(idx)

        for i in [1, 2, 3]:
            self.ui.folder_tree.hideColumn(i)

        self.ui.folder_tree.header().hide()
        self.ui.folder_tree.setExpandsOnDoubleClick(False)
        self.ui.folder_tree.doubleClicked.connect(self.folder_tree_dblclicked)
        self.ui.folder_tree.clicked.connect(self.folder_tree_clicked)

        self.ui.folder_tree_back.clicked.connect(self.folder_tree_back_clicked)
        self.ui.tree_root_button.clicked.connect(self.tree_root_button_clicked)
        self.ui.tree_root_button.setToolTip("change root for ''tree'' browsing")
        
        # calendar
        current_date = datetime.datetime.now()
        today = QtCore.QDate(current_date.year, current_date.month, current_date.day)
        
        self.ui.calendar.setDate(today)
        self.ui.calendar.dateChanged.connect(self.calendar_date_changed)
        self.ui.calendar_root_button.clicked.connect(self.calendar_root_button_clicked)
        self.ui.calendar_root_button.setToolTip("change root for calendar browsing")
        popup_calendar = self.ui.calendar.calendarWidget()
        popup_calendar.currentPageChanged.connect(self.calendar_page_changed)
        self.calendar_page_changed(current_date.year, current_date.month)
        
        # file list

        self.file_list_model = None
        #self.ui.file_list.clicked.connect(self.file_list_clicked)
        self.ui.refresh_file_list.clicked.connect(self.update_file_list)
        self.ui.hide_variables_button.clicked.connect(self.choose_variables_to_hide)
        
        # plot Window
        #XXX screen
        '''
        image_size_x = self.data.current_fit.camera.image_size[0]
        image_size_y = self.data.current_fit.camera.image_size[1]

        start_image = np.zeros([image_size_x,image_size_y])

        self.ui.plotWindow.main_axes.subplot2grid((2,2),(0,0))
        self.ui.plotWindow.canvas.ax.subplot2grid((2,2),(0,0))

        self.ui.plotWindow.main_axes.imshow(start_image,extent=(0,
                                                image_size_x, 0, image_size_x),
                                     cmap=plt.get_cmap(self.settings.colormap))

        self.ui.plotWindow.main_axes.set_xlim([0,image_size_x])
        self.ui.plotWindow.main_axes.set_ylim([0,image_size_y])
        '''
        # Fit settings Tab

        self.ui.fit_binning_box.clicked.connect(self.refresh_fit_settings)
        self.ui.fit_exclude_hole_box.clicked.connect(self.refresh_fit_settings)
        self.ui.fit_autobin_box.clicked.connect(self.refresh_fit_settings)

        self.ui.fit_binning_maxpoints_txt.textEdited.connect(\
                                                     self.refresh_fit_settings)

        int_validator = QtGui.QIntValidator(1, 2000)
        self.ui.fit_binning_maxpoints_txt.setValidator(int_validator)
        self.ui.fit_binning_txt.textEdited.connect(self.refresh_fit_settings)
        int_validator = QtGui.QIntValidator(1, 1000)
        self.ui.fit_binning_txt.setValidator(int_validator)

        for fit in self.data.fit2D_dic:
            self.ui.fit_type.addItem(fit)

        self.ui.fit_type.currentIndexChanged.connect(self.refresh_fit_settings)
        
        self.ui.fit_order.addItems(['hole first','out first','best of two'])
        self.ui.fit_order.currentIndexChanged.connect(self.refresh_fit_settings)
        
        # Cam settings tab

        self.refresh_cam_list()
        self.display_cam_settings(0)

        self.ui.update_cam_button.clicked.connect(self.update_cam_settings)
        self.ui.cam_type.currentIndexChanged.connect(self.refresh_selected_camera)
        self.ui.add_cam_button.clicked.connect(self.add_new_cam)
        self.ui.remove_cam_button.clicked.connect(self.delete_cam)

        self.ui.cam_mag.textEdited.connect(self.cam_settings_changed)
        self.ui.cam_image_ext.textEdited.connect(self.cam_settings_changed)
        self.ui.cam_img_sizex.textEdited.connect(self.cam_settings_changed)
        self.ui.cam_img_sizey.textEdited.connect(self.cam_settings_changed)
        self.ui.cam_od_calc.textEdited.connect(self.cam_settings_changed)
        self.ui.cam_px_sizex.textEdited.connect(self.cam_settings_changed)
        self.ui.cam_px_sizey.textEdited.connect(self.cam_settings_changed)

        # Display settings tab

        self.ui.disp_fit_contour_box.clicked.connect(self.refresh_gui_settings)
        self.ui.colormap_max.textEdited.connect(self.refresh_gui_settings)
        self.ui.colormap_min.textEdited.connect(self.refresh_gui_settings)
        self.ui.display_hole_box.clicked.connect(self.refresh_gui_settings)
        
        # a bit cumbersome, but we have to do that to set
        # load_fit=True to display_data
        callback_func = lambda: self.display_file(True)
        self.ui.refresh_display_button.clicked.connect(callback_func)

        self.ui.colormap_type.addItems(self.data.colormaps)
        self.ui.colormap_type.currentIndexChanged.connect(self.colormap_type_clicked)

        self.ui.display_interpolation.addItems(self.data.interpolations)
        self.ui.display_interpolation.currentIndexChanged.connect(\
                                            self.display_interpolation_clicked)

        
        # Comment editing/displaying zone
        
        self.ui.fit_comment_text.textChanged.connect(self.comment_text_changed)
        self.ui.fit_comment_text.setEnabled(False)
        self.ui.disable_comment_box.clicked.connect(self.refresh_gui_settings)
        
        # Quick list Tab

        self.ui.quickPlotButton.clicked.connect(self.plot_list)
        self.ui.quickStatsButton.clicked.connect(self.stat_list)
        self.ui.send_to_console_button.clicked.connect(self.send_to_console)
        self.ui.fit_list_box.clicked.connect(self.refresh_gui_settings)
        self.ui.save_quicklist_button.clicked.connect(self.save_quicklist)
        
        for fit in self.data.fit1D_dic:
            self.ui.list_fit_type.addItem(fit)

        # Fit button

        self.ui.fitButton.clicked.connect(self.fit_button_clicked)

        # Other buttons

        self.ui.flush_result_button.clicked.connect(self.flush_results)

        # Final
        self.refresh_fit_settings(None)
        self.refresh_gui_settings(None)

        self.update_file_list()

        # Dock console
        # XXX remove for debug

        name_space = {'gui': self, 'plt':plt, 'np':np, 'fit':self.fit()}
        self.pythonshell = internalshell.InternalShell(self.ui.console_dock,
                                                       namespace=name_space,
                                                       commands=['gui.init_shell()'],
                                                       multithreaded=False)

        self.pythonshell.set_codecompletion_auto(True)
        self.pythonshell.interpreter.namespace['res'] = {}
        self.ui.console_dock.setWidget(self.pythonshell)


    ##### GUI General functions

    ### File management and display

    def update_file_list(self):
        """
        updates file list
        """
        path = self.settings.current_folder
        
        self.ui.current_dir_txt.setText(self.trunc_path(str(path),30))
        self.ui.current_dir_txt.setToolTip(str(path)) # full path is displayed as toolTip
        
        file_name_filter = self.settings.file_name_filter.split(',')
        file_name_filter = ['*'+f for f in file_name_filter]

        qdir = QtCore.QDir
        current_dir = qdir(path)
        files_list = current_dir.entryList(file_name_filter,
                                           qdir.Files | qdir.NoSymLinks,
                                           QtCore.QDir.Time)
        
        # we keep the file list in here, so that we can change the names
        # displayed in the QListView 
        self.data.current_file_list = [f for f in files_list]
                                   
        # Check if saved fit exists and hide variables

        save_dir = os.path.join(str(path), '.fits')
        i = 0
        is_a_var_hidden = 0
        variable_list = []
        
        self.file_list_model = QtGui.QStandardItemModel()
        
        # Populate file list :
        
        for file_name in files_list:
            
            fname = str(file_name)
            fname = fname[:-4]+'.hdf5'
            fit_path = os.path.join(str(save_dir), fname)
            
            # Compatibility with old fitting program WnM
            old_fname = fname[:-5]+'.fit'
            fit_path_old =  os.path.join(str(path),'saved_fits',old_fname)
            #-----------------------------------
            
            if os.path.isfile(fit_path):
                name = self.settings.isfit_str+str(file_name)
                font_foreground_color = QtCore.Qt.darkBlue    
            elif os.path.isfile(fit_path_old): # WnM compatibility
                name = self.settings.isfit_wnm_str+str(file_name)
                font_foreground_color = QtCore.Qt.darkCyan
            else:
                name = self.settings.isnofit_str+str(file_name)
                font_foreground_color = QtCore.Qt.black
            
            variable_list += self.parseVariables(name).keys()
            
            for var_name in self.settings.variables_to_hide:
                name, modif = self.hide_variable(name,var_name)
                is_a_var_hidden |= modif
            files_list[i] = name
            i += 1
            
            item = QtGui.QStandardItem(name)
            font_weight = QtGui.QFont.Light
            font = QtGui.QFont('Monospace', 9, font_weight)
            item.setFont(font)
            item.setForeground(QtGui.QBrush(font_foreground_color))
            item.setToolTip(name)
            
            self.file_list_model.appendRow(item)
            
            
        if is_a_var_hidden:
            self.ui.hide_variable_txt.setText('some variables are hidden')
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,
                             QtCore.Qt.red)
            self.ui.hide_variable_txt.setPalette(palette)
            
        else:
            self.ui.hide_variable_txt.setText('no variable hidden')
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,
                             QtCore.Qt.black)
            self.ui.hide_variable_txt.setPalette(palette)
            
        self.data.all_available_variables = list(set(variable_list))
        
        self.ui.file_list.setModel(self.file_list_model)
        # callback has to be set after model is set for file_list
        self.ui.file_list.selectionModel().selectionChanged.connect(self.file_list_clicked)

    def hide_variable(self,file_name, var_name):
        pattern = "(_?)"+var_name+" = (-*[0-9]*[,.]?[0-9]*)"
        return re.sub(pattern,'',file_name), file_name==re.sub(pattern,'',file_name)
        
    def parseVariables(self,file_name):
        
        var_dic = {}
            
        # 2 - variables
        
        pattern = "([A-Za-z]\w*) = (-*[0-9]*[,.]?[0-9]*)"
        var_list = re.findall(pattern,file_name)
        
        
        for v in var_list:
            var_dic[v[0]] = np.float(v[1].replace(',','.'))
        return var_dic
        
    def choose_variables_to_hide(self):
        
        check_window = CheckListWindow(title = "hide variables",
                                       variables=self.data.all_available_variables,
                                       selected = self.settings.variables_to_hide)
        result = check_window.exec_()        
        
        if result:
            self.settings.variables_to_hide = check_window.selected
            self.update_file_list()
            
            
    def display_file(self, load_fit=True):
        """
        displays file + ROI + Background & fit results
        """
        self.get_ROI() # first we save ROI
        self.get_background()
        self.get_HOLE()

        # giving current file information to our fit object
        self.data.current_fit.picture.filename = self.data.current_file_name
        self.data.current_fit.picture.path = self.data.current_file_path


        # loading data
        res = self.data.current_fit.load_data()
        if not res: return

        xm = self.data.current_fit.xm
        ym = self.data.current_fit.ym
        data = self.data.current_fit.data

        #XXX display
        '''
        # plotting
        xlim = self.ui.plotWindow.main_axes.get_xlim()
        ylim = self.ui.plotWindow.main_axes.get_ylim()

        ax = self.ui.plotWindow.main_axes
        ax.cla()
        self.ui.plotWindow.small_axes.cla()
        self.ui.plotWindow.cutx_axes.cla()
        self.ui.plotWindow.cuty_axes.cla()

        self.ui.plotWindow.refreshLabelsAndTicks()

        cmap = str(self.ui.colormap_type.currentText())
        interp = str(self.ui.display_interpolation.currentText())


        img = ax.imshow(data,extent=(xm.min(), xm.max(), ym.max(), ym.min()),
                        cmap=plt.get_cmap(cmap),
                        interpolation =interp)

        img.set_clim(self.settings.colormap_min,self.settings.colormap_max)


        self.ui.plotWindow.main_axes.set_xlim(xlim)
        self.ui.plotWindow.main_axes.set_ylim(ylim)


        if load_fit:self.load_fit(draw=False)


        self.draw_ROI(draw=False)
        self.draw_background(draw=False)

        self.ui.plotWindow.draw()
        '''
        #self.draw_ROI(draw=False)
        #self.draw_HOLE()
        
        screen = self.ui.plotWindow.screen
        screen.x = xm[0, :]*1.0
        screen.y = ym[:, 0]*1.0
        screen.data = data
        
        colormap_scale = (self.settings.colormap_min*1.0,
                          self.settings.colormap_max*1.0)
        screen.image.set_lut_range(colormap_scale)
        
        interpolation_type = str(self.ui.display_interpolation.currentText())
        interp = self.data.interpolations_dic[interpolation_type]
        screen.image.set_interpolation(interp)
        
        screen.update_image()
        
        screen.plot.update_colormap_axis(screen.image)
        
        if load_fit: self.load_fit(draw=False)
        if load_fit and not self.settings.disable_comment: self.load_comment()
        
        if self.settings.display_hole:
            self.data.rectHOLE.show()
        else:
            self.data.rectHOLE.hide()
                
        self.draw_ROI()
        self.draw_HOLE()
        self.draw_background()

    ### ROI and background
    # ROI ----------------------------------
    

    
    def draw_ROI(self):

        r = self.data.current_fit.picture.ROI
        ROI_rect = self.data.rectROI
        ROI_rect.set_rect(r[0], r[2], r[1], r[3])
        self.ui.plotWindow.screen.plot.replot()


    def get_ROI(self):

        ROI_rect = self.data.rectROI
        r = ROI_rect.get_rect()

        self.data.current_fit.picture.ROI = (r[0], r[2], r[1], r[3])

    def draw_HOLE(self):

        r = self.data.current_fit.picture.hole
        HOLE_rect = self.data.rectHOLE
        HOLE_rect.set_rect(r[0], r[2], r[1], r[3])
        self.ui.plotWindow.screen.plot.replot()


    def get_HOLE(self):

        HOLE_rect = self.data.rectHOLE
        r = HOLE_rect.get_rect()

        self.data.current_fit.picture.hole = (r[0], r[2], r[1], r[3])

    def zoom_to_ROI(self):

        xlim = self.ui.plotWindow.main_axes.get_xlim()
        ylim = self.ui.plotWindow.main_axes.get_ylim()

        r = (xlim[0], xlim[1], ylim[0], ylim[1])
        self.data.current_fit.picture.ROI = r
        self.draw_ROI()

    # Background  ----------------------------------

    
    def draw_background(self):
        r = self.data.current_fit.picture.background
        BCKGND_rect = self.data.rectBackground
        BCKGND_rect.set_rect(r[0], r[2], r[1], r[3])
        self.ui.plotWindow.screen.plot.replot()

    def get_background(self):

        BCKGND_rect = self.data.rectBackground
        r = BCKGND_rect.get_rect()

        self.data.current_fit.picture.background = (r[0], r[2], r[1], r[3])


    def zoom_to_BKGND(self):

        xlim = self.ui.plotWindow.main_axes.get_xlim()
        ylim = self.ui.plotWindow.main_axes.get_ylim()

        r = (xlim[0], xlim[1], ylim[0], ylim[1])
        self.data.current_fit.picture.background = r
        self.draw_background()

    ### FITS


    def fit(self, index=None):

        if index == None: index = self.ui.file_list.currentIndex()
        if self.data.current_fit.data == []: return

        self.data.current_fit.values = {}

        self.get_ROI()
        self.get_background()
        self.get_HOLE()
        # printing image name before fit

        # TODO changer affichage résultats fit
        self.print_result(self.settings.results_delim)
        self.print_result("<b>     Starting FIT</b>")
        self.print_result("")
        self.print_settings()

        #### FIT---------------
        
        self.data.current_fit = self.data.current_fit.adapt_type_from_fit()
        self.data.current_fit.fit.options = self.settings.current_fit_options
        
        is_double = self.data.current_fit.fit.__class__.__name__ == 'DoubleFit'
        
        # if fit order is 2 (best of two) and fit is a double fit
        # then we do the fit twice (with different fit order) 
        # and keep best result !
        if self.settings.current_fit_order == 2 and is_double:
            
            # fit hole first
            self.print_result("round 1 : hole first")
            
            fit_hole_first = copy.deepcopy(self.data.current_fit)
            fit_hole_first.fit.options.fit_hole_first = True
            fit_hole_first.do_fit()
            
            xm = fit_hole_first.xm_fit
            ym = fit_hole_first.ym_fit
            fit_params = fit_hole_first.fit.results
            fit_res = fit_hole_first.fit.formula((xm, ym), *fit_params)
            fit_data = fit_hole_first.data_fit
            
            err_hole_first = np.sqrt((fit_res-fit_data)**2)
            err_hole_first = np.sum(np.sum(err_hole_first))
            
            # fit out first
            self.print_result("round 2 : out first")
            
            fit_out_first = copy.deepcopy(self.data.current_fit)
            fit_out_first.fit.options.fit_hole_first = False
            fit_out_first.do_fit()
            
            xm = fit_out_first.xm_fit
            ym = fit_out_first.ym_fit
            fit_params = fit_out_first.fit.results
            fit_res = fit_out_first.fit.formula((xm, ym), *fit_params)
            fit_data = fit_out_first.data_fit
            
            err_out_first = np.sqrt((fit_res-fit_data)**2)
            err_out_first = np.sum(np.sum(err_out_first))
            
            # choose the good one
            
            if err_out_first > err_hole_first:
                self.print_result(">>> HOLE first wins")
                self.data.current_fit = fit_hole_first
            else:
                self.print_result(">>> OUT first wins")
                self.data.current_fit = fit_out_first
            
        else: # else we fit only once
            self.data.current_fit.do_fit()
        
        ###---------------
        self.data.current_fit.compute_values()
        results_string = self.data.current_fit.values_to_str()

        self.print_result(results_string)

        self.data.current_fit.save_fit()

        # update diplayed name

        name = index.data().toString()
        name = name.replace(self.settings.isnofit_str, self.settings.isfit_str)
        self.file_list_model.setData(index, name)

        self.plot_fit_results()
        #self.ui.plotWindow.draw()


    def plot_fit_results(self, fitObj=None):

        if fitObj is None: fitObj = self.data.current_fit

        # display fit contour
        screen = self.ui.plotWindow.screen
        
        if self.settings.display_fit_contour:

            xm = fitObj.xm
            ym = fitObj.ym
            fit_params = fitObj.fit.results
            fit_res = fitObj.fit.formula((xm, ym), *fit_params)

            #self.display_file(load_fit=False) # to clear everything
            cs = plt.contour(xm, ym, fit_res, 8, colors='w')
            screen.level_xy = [ [[0,0],[0,0]] for i in range(8) ]
            for i in range(min(len(cs.collections),8)):
                p = cs.collections[i].get_paths()[0]
                v = p.vertices
                x = v[:,0]
                y = v[:,1]
                screen.level_xy[i][0] = x
                screen.level_xy[i][1] = y
            screen.update_contour()
            #self.ui.plotWindow.draw()
        else:
            screen.reset_contour()
        # display cuts
        
        if fitObj.fit.options.remove_background:
            fitObj.compute_background_value()
            offset = fitObj.picture.background_value
        else:
            offset = 0
            
        if fitObj.values.has_key('cx') and fitObj.values.has_key('cy'):

            cx = int(fitObj.values['cx'])
            cy = int(fitObj.values['cy'])

            if fitObj.ym_fit == []: fitObj.generate_xy_fit_mesh()

            y = fitObj.ym_fit[:, 0]
            x = fitObj.xm_fit[0, :]
            fit_params = fitObj.fit.results

            xfit = np.linspace(x.min(), x.max(), 1e3)
            yfit = np.linspace(y.min(), x.max(), 1e3)

            index_cx = ((x-cx)**2).argmin()
            index_cy = ((y-cy)**2).argmin()

            data_cuty = fitObj.data_fit[:, index_cx]-offset
            data_cutx = fitObj.data_fit[index_cy, :]-offset


            cut_x = self.ui.plotWindow.cutX
            cut_x.xdata = x
            cut_x.ydata = data_cutx
            cut_x.xfit = xfit
            cut_x.yfit = fitObj.fit.formula((xfit,cy),*fit_params)
            cut_x.update_plot()
            
            cut_y = self.ui.plotWindow.cutY
            cut_y.xdata = data_cuty
            cut_y.ydata = y
            cut_y.xfit = fitObj.fit.formula((cx,yfit),*fit_params)
            cut_y.yfit = yfit
            cut_y.update_plot()

        
    def load_fit(self, draw=True):

        save_dir = os.path.join(self.data.current_file_path, '.fits')
        fname = self.data.current_file_name
        fname = fname[0:len(fname)-4]+'.hdf5'
        fit_path = os.path.join(save_dir, fname)
        
        # Compatibility with old fitting program WnM
        old_fname = fname[:-5]+'.fit'
        fit_path_old =  os.path.join(self.data.current_file_path,'saved_fits',old_fname)
        #---------------------------------------
            
        if os.path.isfile(fit_path):
            old_fit = False
            self.print_result(self.settings.results_delim)
            self.print_result("<b> Loading FIT</b>")
            saved_fit = self.data.current_fit.hdf5_to_fit(fit_path)
        elif os.path.isfile(fit_path_old):
            #-----------------------------------------------------
            # Compatibility with old fitting program WnM
            old_fit = True
            self.print_result(self.settings.results_delim)
            self.print_result("<b> Loading FIT</b>")
            loaded_fit = import_WNM_fit(fit_path_old)
            if isinstance(loaded_fit,basestring):
                self.print_result('conversion from WnM not implemented for fit type "'+loaded_fit+'"')
                return
            # initialize fit object
            saved_fit = pf.PyFit2D()
            # get properties from current fit (which are not stored in saved fit)
            saved_fit.picture = copy.deepcopy(self.data.current_fit.picture)
            saved_fit.atom = copy.deepcopy(self.data.current_fit.atom)
            saved_fit.camera = copy.deepcopy(self.data.current_fit.camera)
            # loaded properties
            saved_fit.fit = loaded_fit.fit
            saved_fit.picture.ROI = loaded_fit.picture.ROI
            saved_fit.picture.background = loaded_fit.picture.background
            saved_fit.camera.magnification = loaded_fit.camera.magnification
            if loaded_fit.fit.options.do_binning:
                saved_fit.fit.options.do_binning = loaded_fit.fit.options.do_binning
                saved_fit.fit.options.binning = loaded_fit.fit.options.binning
                saved_fit.fit.options.auto_binning = loaded_fit.fit.options.auto_binning
            
            
            self.data.debug = saved_fit
            #-----------------------------------------------------
        else:
            return # if no fit available, stop and return nothing
        
        # import lambdas from fit generator 
        if saved_fit.fit.name in pf.fit2D_dic.keys():
            buffer_fit = pf.fit2D_dic[saved_fit.fit.name]
            saved_fit.fit.formula = buffer_fit.formula
            saved_fit.fit.formula_parameters = buffer_fit.formula_parameters
            if not isinstance(saved_fit.fit.formula_parameters,str):
                saved_fit.fit.updateFormulaFromParameters2D()
            saved_fit.fit.values = buffer_fit.values
            #if old_fit:saved_fit.compute_values()
        else:
            self.print_result('Saved fit name not found in known fit list - abort')
            return
        
        self.print_settings(saved_fit)


        # load ROI
        self.data.current_fit.picture.ROI = saved_fit.picture.ROI
        if draw: self.draw_ROI()
        
        # load HOLE
        self.data.current_fit.picture.hole = saved_fit.picture.hole
        if draw: self.draw_HOLE()
           
        # load background
        self.data.current_fit.picture.background = saved_fit.picture.background
        if draw: self.draw_background()
        
        # display results
        saved_fit.load_data()
        if old_fit:saved_fit.compute_values()
        self.plot_fit_results(fitObj=saved_fit)
        
        # print results
        results_str = saved_fit.values_to_str()
        self.print_result(results_str)
        
        

    ### GUI settings management

    def load_comment(self):
        self.ui.fit_comment_text.setEnabled(True)
        save_dir = os.path.join(self.data.current_file_path, '.fits')
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        fname = self.data.current_file_name
        fname = fname[0:len(fname)-4]+'.txt'
        comment_path = os.path.join(save_dir, fname)
        self.data.current_comment_file = comment_path
        if not os.path.isfile(comment_path):
            self.data.do_not_load_comment = True 
            self.ui.fit_comment_text.setPlainText('')
            self.data.do_not_load_comment = False 
            return
        
        text = ''
        with open(comment_path, "r") as text_file:
            text = text_file.read()
        self.data.do_not_load_comment = True 
        self.ui.fit_comment_text.setPlainText(text)
        self.data.do_not_load_comment = False 
        
        
    def refresh_fit_settings(self, event):
        if event is None:
            load = True

        else:
            load = False

        options = self.settings.current_fit_options

        bools = [['do_binning', self.ui.fit_binning_box],
                 ['exclude_hole', self.ui.fit_exclude_hole_box],
                 ['remove_background',self.ui.fit_remove_background_box],
                 ['auto_binning', self.ui.fit_autobin_box]]

        params = [['binning_maxpoints', self.ui.fit_binning_maxpoints_txt],
                  ['binning', self.ui.fit_binning_txt]]

        if load:
            for b in bools:
                box = b[1]
                name = b[0]

                box.setChecked(getattr(options, name))

            for p in params:
                txt = p[1]
                name = p[0]

                txt.setText(str(getattr(options, name)))


            self.ui.fit_order.setCurrentIndex(self.settings.current_fit_order)
            
            # change displayed fit type if it has changed
            if self.settings.current_fit_type != self.ui.fit_type.currentText():
                for i in range(self.ui.fit_type.count()):
                    if self.settings.current_fit_type == self.ui.fit_type.itemText(i):
                        self.ui.fit_type.setCurrentIndex(i)
                        break
                pass

        else:
            for b in bools:
                box = b[1]
                name = b[0]

                setattr(options, name, box.isChecked())

            for p in params:
                txt = p[1]
                name = p[0]
                setattr(options, name, int(float(txt.text())))
                txt.setText(str(getattr(options, name)))

            fit_order = self.ui.fit_order.currentIndex()
            self.settings.current_fit_order = fit_order
            if fit_order == 0:
                options.fit_hole_first = True
            elif fit_order == 1:
                options.fit_hole_first = False
                
            # change fit type if it has changed
            if self.settings.current_fit_type != self.ui.fit_type.currentText():
                fit_name_str = str(self.ui.fit_type.currentText())
                self.settings.current_fit_type = fit_name_str
                curr_fit = self.data.fit2D_dic[self.settings.current_fit_type]
                self.data.current_fit.fit = curr_fit
                opt = self.settings.current_fit_options
                self.data.current_fit.fit.options = opt


        self.settings.current_fit_options = options

        # enable / disable according to settings

        self.ui.fit_autobin_box.setEnabled(options.do_binning)
        self.ui.fit_binning_label1.setEnabled(options.do_binning)
        self.ui.fit_binning_label2.setEnabled(options.do_binning)
        self.ui.fit_binning_maxpoints_txt.setEnabled(options.do_binning)
        self.ui.fit_binning_txt.setEnabled(options.do_binning)

    def refresh_gui_settings(self, event):
        if event is None:
            load = True

        else:
            load = False

        settings = self.settings

        bools = [['display_fit_contour', self.ui.disp_fit_contour_box],
                 ['display_hole', self.ui.display_hole_box],
                 ['disable_comment', self.ui.disable_comment_box],
                 ['fit_list', self.ui.fit_list_box]]

        params = [['colormap_min', self.ui.colormap_min],
                  ['colormap_max', self.ui.colormap_max]]

        if load:
            for b in bools:
                box = b[1]
                name = b[0]

                box.setChecked(getattr(settings, name))

            for p in params:
                txt = p[1]
                name = p[0]

                txt.setText(str(getattr(settings, name)))



        else:
            for b in bools:
                box = b[1]
                name = b[0]

                setattr(settings, name, box.isChecked())

            for p in params:
                txt = p[1]
                name = p[0]
                setattr(settings, name, float(txt.text()))
                #txt.setText(str(getattr(settings,name)))


        if load:
            index = self.ui.colormap_type.findText(self.settings.colormap)
            if index > -1:
                self.ui.colormap_type.setCurrentIndex(index)

            inter_type = self.settings.display_interpolation
            index = self.ui.display_interpolation.findText(inter_type)
            if index > -1:
                self.ui.display_interpolation.setCurrentIndex(index)
                
            if self.settings.display_hole:
                self.data.rectHOLE.show()
            else:
                self.data.rectHOLE.hide()
                
            self.ui.plotWindow.screen.plot.replot()
        
        if settings.disable_comment:
            self.ui.fit_comment_text.setEnabled(False)
        else:
            self.ui.fit_comment_text.setEnabled(True)
            
        self.settings = settings
        

    def save_settings(self):

        root = str(self.data.gui_root)
        f = os.path.join(root, 'settings')
        if not os.path.isdir(f):
            os.mkdir(f)

        fname = 'current.set'
        f = os.path.join(f, fname)

        # remove lambda functions from settings (in cam list)
        # otherwise we can't pickle them

        settings_tosave = copy.deepcopy(self.settings)
        for cname in settings_tosave.cam_list:
            settings_tosave.cam_list[cname].OD_conversion = 'pickled_lambda'


        with open(f, 'wb') as output:
            dump(settings_tosave, output, -1)

    def load_settings(self):

        # current settings should be in gui_root/settings/current.set
        root = str(QtCore.QDir.currentPath())

        f = os.path.join(root, 'settings')
        if not os.path.isdir(f):
            os.mkdir(f)

        fname = 'current.set'
        f = os.path.join(f, fname)

        if os.path.isfile(f):
            with open(f, 'rb') as output:
                try:
                    settings = load(output)
                    for cname in settings.cam_list:
                        settings.cam_list[cname].update_OD_conversion()

                    self.settings.load_old_version(settings)
                except:
                    pass
                #self.settings = settings


    ### Console

    def init_shell(self):
        print "-----------------------"
        print "[[ Welcome to PyF!T ]]"
        print "access mainWindow with 'gui'"
        print "modules : numpy as 'np', matplotlip.pyplot as 'plt' "
        print "local functions : fit"
        print "exported list : res (dict)"

        

    def print_result(self, txt):
        self.ui.result_text.append(txt)

    def flush_results(self):
        self.ui.result_text.setText("")

    def print_settings(self, fit=None):

        if fit is None: fit = self.data.current_fit

        file_name = fit.picture.filename
        p = self.print_result
        p("<font color=blue><b>- Settings </b></font>")

        p("-- file : <font color=DarkGreen>"+file_name+"</font>")
        #TODO Finir affichage


    ### List management

    def refresh_available_parameters(self):

        #TODO : prendre les paramètres du fit chargé si il existe !

        # 1 - Get available parameters
        self.data.current_fit.picture.parseVariables()

        params = self.data.current_fit.picture.variables.keys()
        fit_params = self.data.current_fit.fit.values
        for v in fit_params:
            params.append(v.name)

        self.data.available_variables = params

        # 2 - update variable selection list

        x_current = self.ui.list_plot_x.currentText()
        y_current = self.ui.list_plot_y.currentText()

        self.ui.list_plot_x.clear()
        self.ui.list_plot_y.clear()

        for p in params:
            self.ui.list_plot_x.addItem(p)
            self.ui.list_plot_y.addItem(p)

        # 3 - if previous x,y variables still available, select them

        for i in range(self.ui.list_plot_x.count()):

            if self.ui.list_plot_x.itemText(i) == x_current:
                self.ui.list_plot_x.setCurrentIndex(i)

            if self.ui.list_plot_y.itemText(i) == y_current:
                self.ui.list_plot_y.setCurrentIndex(i)



    def plot_list(self):

        X = []
        Y = []
        x_name = str(self.ui.list_plot_x.currentText())
        y_name = str(self.ui.list_plot_y.currentText())

        for i in reversed(self.ui.file_list.selectedIndexes()):

            # 1 - Get file name

            #name = str(i.data().toString())
            name = str(self.data.current_file_list[i.row()])
            root = str(self.settings.current_folder)
            root = os.path.abspath(root)

            name = name.replace(self.settings.isfit_str, '')
            name = name.replace(self.settings.isnofit_str, '')


            # 2 - load fit data

            save_dir = os.path.join(root, '.fits')
            name = name[:-4]+'.hdf5'
            fit_path = os.path.join(save_dir, name)

            if not os.path.isfile(fit_path): continue

            fit = self.data.current_fit.hdf5_to_fit(fit_path)
        
            # import lambdas from fit generator 
            if fit.fit.name in pf.fit2D_dic.keys():
                buffer_fit = pf.fit2D_dic[fit.fit.name]
                fit.fit.formula = buffer_fit.formula
                fit.fit.formula_parameters = buffer_fit.formula_parameters
                if not isinstance(fit.fit.formula_parameters,str):
                    fit.fit.updateFormulaFromParameters2D()
                fit.fit.values = buffer_fit.values
                
            else:
                self.print_result('Saved fit name not found in known fit list - abort')
                return

            fit.picture.parseVariables()

            all_params = dict(fit.picture.variables.items()+fit.values.items())

            if all_params.has_key(x_name) and all_params.has_key(y_name):
                X.append(all_params[x_name])
                Y.append(all_params[y_name])


        if X and self.settings.fit_list:

            fit_name = str(self.ui.list_fit_type.currentText())
            fmodel = self.data.fit1D_dic[fit_name]

            self.print_result(self.settings.results_delim)
            self.print_result("<b>     Starting LIST FIT</b>")
            self.print_result("")

            fit = pf.PyFit1D(fit=fmodel, x=np.array(X), y=np.array(Y))
            fit.do_fit()

            res = fit.values_to_str()
            self.print_result(res)


        if X:
            plt.figure()
            plt.plot(X, Y, 'or')
            if self.settings.fit_list:
                x_fit = np.linspace(np.min(X), np.max(X), 1e3)
                y_fit = fit.fit.formula(x_fit, *fit.fit.results)

                plt.plot(x_fit, y_fit, 'b')

            plt.xlabel(x_name.replace('_', ' '))
            plt.ylabel(y_name.replace('_', ' '))
            plt.show()

    def stat_list(self):

        params = {}

        for i in reversed(self.ui.file_list.selectedIndexes()):

            # 1 - Get file name

            #name = str(i.data().toString())
            name = str(self.data.current_file_list[i.row()])
            root = str(self.settings.current_folder)
            root = os.path.abspath(root)

            name = name.replace(self.settings.isfit_str, '')
            name = name.replace(self.settings.isnofit_str, '')


            # 2 - load fit data and get parameters

            save_dir = os.path.join(root, '.fits')
            name = name[0:-4]+'.hdf5'
            fit_path = os.path.join(save_dir, name)

            if not os.path.isfile(fit_path): continue

            fit = self.data.current_fit.hdf5_to_fit(fit_path)
        
            # import lambdas from fit generator 
            if fit.fit.name in pf.fit2D_dic.keys():
                buffer_fit = pf.fit2D_dic[fit.fit.name]
                fit.fit.formula = buffer_fit.formula
                fit.fit.formula_parameters = buffer_fit.formula_parameters
                if not isinstance(fit.fit.formula_parameters,str):
                    fit.fit.updateFormulaFromParameters2D()
                fit.fit.values = buffer_fit.values
                
            else:
                self.print_result('Saved fit name not found in known fit list - abort')
                return
            
            fit.picture.parseVariables()

            all_params = dict(fit.picture.variables.items()+fit.values.items())

            for n, v in all_params.iteritems():
                if params.has_key(n):
                    params[n].append(v)
                else:
                    params[n] = [v]

        # Display results

        if params:
            params = OrderedDict(sorted(params.items()))

            self.print_result(self.settings.results_delim)
            self.print_result("<b>     Selection Statistics</b>")
            self.print_result("")
            for n, v in params.iteritems():
                out = ' - '+n+' = \t'
                out += '%1.2e'%np.mean(v)
                out += ' +/- '
                out += '%1.1e'%np.std(v)
                self.print_result(out)


    def send_to_console(self):
        
        params = {}

        for i in reversed(self.ui.file_list.selectedIndexes()):

            # 1 - Get file name

            #name = str(i.data().toString())
            name = str(self.data.current_file_list[i.row()])
            root = str(self.settings.current_folder)
            root = os.path.abspath(root)

            name = name.replace(self.settings.isfit_str, '')
            name = name.replace(self.settings.isnofit_str, '')


            # 2 - load fit data and get parameters

            save_dir = os.path.join(root, '.fits')
            name = name[0:-4]+'.hdf5'
            fit_path = os.path.join(save_dir, name)

            if not os.path.isfile(fit_path): continue

            fit = self.data.current_fit.hdf5_to_fit(fit_path)
        
            # import lambdas from fit generator 
            if fit.fit.name in pf.fit2D_dic.keys():
                buffer_fit = pf.fit2D_dic[fit.fit.name]
                fit.fit.formula = buffer_fit.formula
                fit.fit.formula_parameters = buffer_fit.formula_parameters
                if not isinstance(fit.fit.formula_parameters,str):
                    fit.fit.updateFormulaFromParameters2D()
                fit.fit.values = buffer_fit.values
                
            else:
                self.print_result('Saved fit name not found in known fit list - abort')
                return
            
            fit.picture.parseVariables()

            all_params = dict(fit.picture.variables.items()+fit.values.items())

            for n, v in all_params.iteritems():
                if params.has_key(n):
                    params[n].append(v)
                else:
                    params[n] = [v]
        
        to_send = AttrDict() # Matlab structure like dict
        for n,v in params.iteritems():
            to_send[n] = np.array(v)

                

        # send

        self.pythonshell.interpreter.namespace['res'] = to_send
    
    
    def save_quicklist(self):
        
        # 1) Get list of variables to save and save format
        
        check_window = CheckListWindow(title = "saving list variables to file",
                                       variables=self.data.available_variables,
                                       selected = self.settings.variables_to_save,
                                       msg = 'choose variables to save',
                                       droplist_choice=['txt','hdf5'],
                                       droplist_msg="save format")
        result = check_window.exec_()        
        
        if not result:
            return
        
        self.settings.variables_to_save = check_window.selected
        format = str(check_window.drop_list.currentText())
        
        # 2) Get file_name
        
        file_name = QtGui.QFileDialog.getSaveFileName(None, "save list to...", self.settings.path_root)
        if not file_name:
            return
        
        # 3) Gather all variables
        
        vars = {vname:[] for vname in self.settings.variables_to_save}

        for i in reversed(self.ui.file_list.selectedIndexes()):

            # 1 - Get file name

            #name = str(i.data().toString())
            name = str(self.data.current_file_list[i.row()])
            root = str(self.settings.current_folder)
            root = os.path.abspath(root)
            name = name.replace(self.settings.isfit_str, '')
            name = name.replace(self.settings.isnofit_str, '')


            # 2 - load fit data

            save_dir = os.path.join(root, '.fits')
            name = name[:-4]+'.hdf5' #TODO WnM compatibility
            fit_path = os.path.join(save_dir, name)

            if not os.path.isfile(fit_path): continue

            fit = self.data.current_fit.hdf5_to_fit(fit_path)
        
            # import lambdas from fit generator 
            if fit.fit.name in pf.fit2D_dic.keys():
                buffer_fit = pf.fit2D_dic[fit.fit.name]
                fit.fit.formula = buffer_fit.formula
                fit.fit.formula_parameters = buffer_fit.formula_parameters
                if not isinstance(fit.fit.formula_parameters,str):
                    fit.fit.updateFormulaFromParameters2D()
                fit.fit.values = buffer_fit.values
                
            else:
                self.print_result('Saved fit name not found in known fit list - abort')
                return

            fit.picture.parseVariables()

            all_params = dict(fit.picture.variables.items()+fit.values.items())
            
            for vname in self.settings.variables_to_save:
                if all_params.has_key(vname):
                    vars[vname].append(all_params[vname])
                else:
                    vars[vname].append(-1)
            

        
        self.data.debug=vars        
        
        # TEST
        if format=='txt':
            numpy_stack = np.transpose(np.vstack(vars.values()))
            header = vars.keys()                         
            delimiter = '\t'
            comments = 'Generated by PyFit on '+str(datetime.datetime.now())+'\n'
            fmt = "%.3e"
            np.savetxt(str(file_name), numpy_stack, delimiter=delimiter, fmt=fmt, 
                       header=delimiter.join(header), comments=comments)
    ### Cam management

    def refresh_cam_list(self):

        cam_list = self.settings.cam_list
        self.ui.cam_type.clear()
        self.ui.cam_type.addItems([c for c in sorted(cam_list)])

        #keep selected camera
        ind = self.ui.cam_type.findText(self.settings.current_cam)
        if ind > 0 and self.ui.cam_type.currentIndex != ind:
            self.ui.cam_type.setCurrentIndex(ind)


    def refresh_selected_camera(self, event):

        if event == -1: return
        selected_cam_name = str(self.ui.cam_type.currentText())
        self.settings.current_cam = selected_cam_name
        self.data.current_fit.camera = self.settings.cam_list[selected_cam_name]
        self.display_cam_settings(0)

        self.settings.file_name_filter = self.data.current_fit.camera.image_ext
        self.update_file_list()

    def display_cam_settings(self, event):

        if event == -1: return

        cam = self.data.current_fit.camera

        self.ui.cam_mag.setText(str(cam.magnification))
        self.ui.cam_px_sizex.setText(str(cam.pixel_size_x))
        self.ui.cam_px_sizey.setText(str(cam.pixel_size_y))
        self.ui.cam_image_ext.setText(cam.image_ext)
        self.ui.cam_img_sizex.setText(str(cam.image_size[0]))
        self.ui.cam_img_sizey.setText(str(cam.image_size[1]))
        self.ui.cam_od_calc.setText(cam.OD_conversion_formula)

        self.ui.update_cam_button.setDefault(False)

    def update_cam_settings(self):

        current_cam_name = self.ui.cam_type.currentText()
        cam = pf.pyfit_classes.Camera() # new instance..
        cam.name = current_cam_name

        cam.magnification = float(self.ui.cam_mag.text())
        cam.pixel_size_x = float(self.ui.cam_px_sizex.text())
        cam.pixel_size_y = float(self.ui.cam_px_sizey.text())
        cam.image_ext = str(self.ui.cam_image_ext.text())
        cam.image_size = (int(float(self.ui.cam_img_sizex.text())),
                          int(float(self.ui.cam_img_sizey.text())))
        cam.OD_conversion_formula = str(self.ui.cam_od_calc.text())

        cam.update_OD_conversion()

        self.data.current_fit.camera = cam
        self.settings.cam_list[str(current_cam_name)] = cam

        self.ui.update_cam_button.setDefault(False)

    def add_new_cam(self):

        camera_name, ok = QtGui.QInputDialog.getText(self,
                                                     'PyF!T wanna know...',
                                                     'Enter new camera name :')
        camera_name = str(camera_name)

        if ok:
            if self.settings.cam_list.has_key(camera_name):
                QtGui.QMessageBox.critical(self, 'PyF!T no happy...',
                                           'This name already exists... aborting !')
                return

            new_cam = pf.pyfit_classes.Camera()
            new_cam.name = camera_name
            self.settings.cam_list[camera_name] = new_cam
            self.refresh_cam_list()

    def delete_cam(self):

        reply = QtGui.QMessageBox.question(self, 'PyF!T wanna know...',
                                           'Delete this camera ?',
                                           QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)

        current_cam_name = str(self.ui.cam_type.currentText())

        if reply == QtGui.QMessageBox.Yes:
            self.settings.cam_list.pop(current_cam_name)
            self.refresh_cam_list()
            self.ui.cam_type.setCurrentIndex(0)
            self.refresh_selected_camera(0)

    def cam_settings_changed(self):
        self.ui.update_cam_button.setDefault(True)
    
    ##### GUI usefull functions
    
    def trunc_path(self,pathstr,max_len):
        p = self.splitPath(pathstr)
        shortpath = pathstr
        security = 1
        while len(shortpath)>max_len and security<100:
            p = p[1:]
            shortpath = '../'+'/'.join(p)
            security +=1
            
        return shortpath
        
    def splitPath(self,path):
        root, d = os.path.split(path)
        if d:
            return self.splitPath(root)+[d]
        else:
            return [root]
    
    ##### Usefull functions
    
    def gen_calendar_path(self,y,m,d):
        
        year_fmt = self.settings.calendar_yearfolder
        month_fmt = self.settings.calendar_monthfolder
        day_fmt = self.settings.calendar_dayfolder
        root = self.settings.calendar_root
        pic_folder = self.settings.calendar_picturefolder
        date = datetime.datetime(year=y, month=m, day=d)
        
        day_folder = date.strftime(day_fmt)
        month_folder = date.strftime(month_fmt)
        year_folder = date.strftime(year_fmt)
        
        calendar_path = os.path.join(root, year_folder, month_folder, day_folder,pic_folder)
        
        return calendar_path
    
    ##### GUI general callbacks

    def closeEvent(self, event):
        '''
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message',
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        '''
        self.save_settings()
        event.accept()

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_F1:
            print 'F1'

        if event.modifiers() & QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_F:
                self.fit()



    ##### GUI components callbacks
    
    def tree_root_button_clicked(self):
        msg = "Select folder (for tree browsing)"
        folder = QtGui.QFileDialog.getExistingDirectory(None, msg, self.settings.path_root)
        if folder:
            root = str(folder)
            self.settings.path_root = root
            self.folder_tree_model.setRootPath(root)
            idx = self.folder_tree_model.index(root)
            self.ui.folder_tree.setRootIndex(idx)
            self.settings.current_folder = root
            self.update_file_list()
                        
    def folder_tree_dblclicked(self, index):

        indexItem = self.folder_tree_model.index(index.row(), 0, index.parent())
        filePath = self.folder_tree_model.filePath(indexItem)
        self.ui.folder_tree.setRootIndex(indexItem)
        self.settings.path_root = filePath
        self.settings.current_folder = filePath
        self.update_file_list()

    def folder_tree_clicked(self, index):

        indexItem = self.folder_tree_model.index(index.row(), 0, index.parent())
        filePath = self.folder_tree_model.filePath(indexItem)
        self.settings.current_folder = filePath
        self.update_file_list()

    def folder_tree_back_clicked(self):

        root = self.settings.path_root
        index = self.folder_tree_model.index(root)
        self.ui.folder_tree.setRootIndex(index.parent())
        new_root = self.folder_tree_model.filePath(index.parent())
        self.settings.path_root = new_root
        self.settings.current_folder = new_root
        self.update_file_list()

    def calendar_date_changed(self,date):
        y = date.year()
        m = date.month()
        d = date.day()
        
        new_path = self.gen_calendar_path(y, m, d)
        if os.path.isdir(new_path):
            
            # update folder treeview accordingly
            root = self.settings.calendar_root
            self.settings.path_root = root
            self.folder_tree_model.setRootPath(root)
            idx = self.folder_tree_model.index(root)
            self.ui.folder_tree.setRootIndex(idx)
            
            
            self.settings.current_folder = new_path
            self.update_file_list()
            
        else:
            model = QtGui.QStandardItemModel()
            item = QtGui.QStandardItem("This folder does not exist...")
            model.appendRow(item)
            self.ui.file_list.setModel(model)
                       
    def calendar_page_changed(self,y,m):
        '''
        when calendar page is changed, we scan all folders for the current month,
        and we highlight (bold) the dates for which the folder exist and is not empty
        '''
        # QTFont bold format definition
        bold_fmt = QtGui.QTextCharFormat()
        bold_fmt.setFontWeight(QtGui.QFont.Bold)
        
        maxday = calendar.monthrange(y,m)[1]
        
        for d in range(maxday):
            path = self.gen_calendar_path(y, m, d+1)
            #for each day, check picture dir exists AND is NOT empty
            #TODO: make it faster than os.listdir ?
            if os.path.isdir(path) and os.listdir(path)!=[]:
                date = QtCore.QDate(y,m,d+1)
                self.ui.calendar.calendarWidget().setDateTextFormat(date,bold_fmt)
                        
    def calendar_root_button_clicked(self):
        msg = "Select root for calendar browsing"
        folder = QtGui.QFileDialog.getExistingDirectory(None, msg, self.settings.calendar_root)
        if folder:
            self.settings.calendar_root = str(folder)
            date = self.ui.calendar.date()
            self.calendar_date_changed(date)
    
                   
    def file_list_clicked(self, index):

        if len(self.ui.file_list.selectedIndexes()) > 1:
            return

        index = self.ui.file_list.selectedIndexes()[0]
        
        #name = index.data().toString()
        #name = str(name)
        #name = name.replace(self.settings.isfit_str, '')
        #name = name.replace(self.settings.isnofit_str, '')
        
        name = str(self.data.current_file_list[index.row()])
        root = str(self.settings.current_folder)


        root = os.path.abspath(root)



        self.data.current_file_name = name
        self.data.current_file_path = root


        self.display_file()
        self.refresh_available_parameters()
        
        
    def fit_button_clicked(self):

        # loop over all selected files


        N = len(self.ui.file_list.selectedIndexes())
        n = 0.0

        for i in reversed(self.ui.file_list.selectedIndexes()):

            # 0 - Progress Bar
            self.ui.progressBar.setValue(n*100.0/N)
            # 1 - Get file name

            #name = str(i.data().toString())
            name = str(self.data.current_file_list[i.row()])
            root = str(self.settings.current_folder)
            root = os.path.abspath(root)

            name = name.replace(self.settings.isfit_str, '')
            name = name.replace(self.settings.isnofit_str, '')

            self.data.current_file_name = name
            self.data.current_file_path = root

            # 2 - load data

            self.display_file(load_fit=False)

            # 3 - fit

            self.fit(i)
            n += 1.0

        #self.update_file_list()
        self.ui.progressBar.setValue(100)

    def colormap_type_clicked(self, e):
        if e == -1: return
        self.settings.colormap = str(self.ui.colormap_type.currentText())
        self.display_file(False)

    def display_interpolation_clicked(self, e):
        if e == -1: return
        self.settings.display_interpolation = str(self.ui.display_interpolation.currentText())
        self.display_file(False)


    ##### DEBUGGING

    def debug(self):
        
        check_window = CheckListWindow(title = "hide variables",
                                       variables=self.data.available_variables,
                                       selected = self.settings.variables_to_hide)
        result = check_window.exec_()        
        
        if result:
            self.settings.variables_to_hide =  check_window.selected


    def comment_text_changed(self):
        text = self.ui.fit_comment_text.toPlainText()
        filename = self.data.current_comment_file
        if self.data.do_not_load_comment: return
        if filename != '':
            with open(filename, "w") as text_file:
                text_file.write(text)
        
        
    def print_event(self, event):
        print event

    def tic(self, message="tic"):
        print message
        self.data.tictoc_start = time.time()

    def toc(self):
        print "Elapsed time = "+str(time.time()-self.data.tictoc_start)+" s"


class GuiSettings():

    def __init__(self):


        # Files browsing
        
        self.path_root = u'/home/alex/Thèse/Programmation/Python/'
        self.current_folder = ''
        self.file_name_filter = '.jpg,.png'
        
        # Calendar browsing
        
        self.calendar_root = u'Z:\\DATAMANIP\\' # root for calendar selection
        self.calendar_yearfolder = "%Y" # format for year folder, strftime style
        self.calendar_monthfolder = "%b%Y"
        self.calendar_dayfolder = "%d%b%Y"
        self.calendar_picturefolder = "Pictures"
        
        # Files list
        
        self.variables_to_hide = []
        self.variables_to_save = []
        # Camera

        self.current_cam = 'lumenera'
        self.cam_list = pf.camera_dic

        # Fit options

        self.current_fit_type = 'Gauss'
        self.current_fit_options = pf.pyfit_classes.FitOptions()
        self.current_fit_order = 0
        
        # Display

        self.display_fit_contour = True
        self.colormap_min = 0
        self.colormap_max = 1
        self.colormap = 'jet'
        self.display_interpolation = 'none'
        self.display_hole = False
        
        # Lists

        self.fit_list = False
        
        # Comments
        
        self.disable_comment = False
        
        # Other

        self.isfit_str = ''
        self.isfit_wnm_str = '' # Watch and MOT fit
        self.isnofit_str = ''
        self.results_delim = '<b>'+'-'*30+'</b>'

    def load_old_version(self, gs):
        # loads an old version of GuiSettings object (gs)
        for param, value in vars(gs).iteritems():
            setattr(self, param, value)



class GuiData():

    def __init__(self, gui):

        self.gui_root = ''

        self.current_file_name = ''
        self.current_file_path = ''
        self.current_file_list = []

        self.current_fit = pf.PyFit2D()
        self.current_fit.camera = gui.settings.cam_list[gui.settings.current_cam]
        self.current_fit.fit = pf.fit2D_dic[gui.settings.current_fit_type]
        
        self.available_variables = []
        self.all_available_variables = []
        
        self.fit2D_dic = pf.fit2D_dic
        self.fit1D_dic = pf.fit1D_dic

        self.rectROI = None
        self.ed_rectROI = None

        self.rectBackground = None
        self.ed_rectBackground = None
        
        self.rectHOLE = None

        self.colormaps = ['jet', 'binary', 'hot', 'gray', 'Blues', 'Greens',
                          'rainbow']
        self.interpolations = ['none', 'linear']
        self.interpolations_dic = {'none' : INTERP_NEAREST,
                                   'linear' : INTERP_LINEAR}

        self.tictoc_start = time.time()

        self.current_comment_file = ''
        self.do_not_load_comment = False

        self.debug = ''
        
class CheckListWindow(QtGui.QDialog):
 
    def __init__(self, parent=None, title='Window Title',
                 variables = ['var1', 'var2'],
                 selected = ['var1'], 
                 msg = 'check to hide variable',
                 droplist_choice=None,
                 droplist_msg="save as"):
        super(CheckListWindow, self).__init__(parent)
 
        #self.resize(260,160)

        
        layout = QtGui.QGridLayout()

        
        #self.buttons = []
        self.cboxes = []
        
        self.varlist = [v for v in variables]
        self.selected = selected
        
        text_1 = QtGui.QLabel(msg)
        layout.addWidget(text_1,0,0,1,2)
        
        i_row=2
        i_var=0
        for var in variables:
            self.cboxes.append(QtGui.QCheckBox(var))
            #self.buttons.append(QtGui.QPushButton('del'))
            #self.buttons[-1].setMaximumWidth(50)
            layout.addWidget(self.cboxes[-1],i_row+1,0)
            #layout.addWidget(buttons[-1],i,1)
            
            
            if var in selected:
                self.cboxes[-1].setChecked(True)
            
            self.cboxes[-1].stateChanged.connect(partial(self.checkbox_clicked,var,i_var))
            #self.buttons[-1].clicked.connect(partial(self.button_clicked,i))    
            i_row+=1
            i_var+=1
        
        
        if droplist_choice is not None:
            self.drop_list = QtGui.QComboBox()
            drop_label = QtGui.QLabel(droplist_msg)
            for choice in droplist_choice:
                self.drop_list.addItem(choice)
            layout.addWidget(drop_label,i_row+1,0)
            i_row+=1
            layout.addWidget(self.drop_list,i_row+1,0)
            i_row+=1
            
            
        button_OK = QtGui.QPushButton('OK')
        button_cancel = QtGui.QPushButton('Cancel')
        button_checkALL = QtGui.QPushButton('ALL')
        button_uncheckALL = QtGui.QPushButton('NO')
        
        button_OK.setMaximumWidth(70)
        button_cancel.setMaximumWidth(70)
        button_checkALL.setMaximumWidth(30)
        button_uncheckALL.setMaximumWidth(30)
        
        button_OK.clicked.connect(self.accept)
        button_cancel.clicked.connect(self.reject)
        button_checkALL.clicked.connect(self.check_all)
        button_uncheckALL.clicked.connect(self.uncheck_all)
        
        layout.addWidget(button_OK,i_row+1,0)
        layout.addWidget(button_cancel,i_row+1,1)
        
        layout.addWidget(button_checkALL,1,0)
        layout.addWidget(button_uncheckALL,1,1)
        
        
        self.setLayout(layout)
        self.setWindowTitle(title)
    
    def checkbox_clicked(self, var,i):
        if self.cboxes[i].isChecked():
            if var not in self.selected:
                self.selected.append(var)
        else:
            if var in self.selected:
                self.selected.remove(var)
    
    def button_clicked(self,index):
        print(index)
        
    def check_all(self):
        for c in self.cboxes:
            c.setChecked(True)
        self.selected = [v for v in self.varlist] 

    def uncheck_all(self):
        for c in self.cboxes:
            c.setChecked(False)
        self.selected = []
        
class AttrDict(dict): # Matlab like dictionnary
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


################################# START ##########################################
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    # splash screen
    splash_file = os.path.join('.','img','splash.png')
    splash_pix = QtGui.QPixmap(splash_file)
    splash = QtGui.QSplashScreen(splash_pix,QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    
    def update_message(msg):
        splash.showMessage(msg,4)
        QtCore.QCoreApplication.processEvents()
    
    
    # Heavy imports
    
    update_message("loading gui...")
    from pyfit_gui import Ui_PyFit
    update_message("loading pyplot...")
    import matplotlib.pyplot as plt
    update_message("loading numpy...")
    import numpy as np
    update_message("loading generic libraries...")
    import copy
    import time
    import datetime
    import calendar
    import re
    
    from functools import partial

    from guiqwt._scaler import INTERP_NEAREST, INTERP_LINEAR
    update_message("displaying quick message : Hello world ^(°0°)^")
    update_message("loading pyfit...")
    import pyfit as pf
    update_message("loading screen (guiqwt)...")
    from GuiqwtScreen import ROISelectTool, BKGNDSelectTool, HOLESelectTool
    from import_WNM_fit import import_WNM_fit
    update_message("loading internal shell (spyderlib)...")
    from spyderlib.widgets import internalshell
    
    update_message("Reticulating Splines...") # ^^
    from collections import OrderedDict
    
    from matplotlib.patches import Rectangle
    
    from cPickle import dump, load
    from sqlalchemy.sql.functions import current_date

    # start programm
    update_message("loading finished : starting app !")
    myapp = StartQT4()
    myapp.show()
    splash.finish(myapp)
    sys.exit(app.exec_())

