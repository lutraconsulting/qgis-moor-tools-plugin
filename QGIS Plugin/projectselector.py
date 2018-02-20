# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSelector
                                 A QGIS plugin
 Tool for selecting pre-defined QGIS projects.
                              -------------------
        begin                : 2013-12-04
        copyright            : (C) 2013 by Dartmoor National Park Authority
        email                : gi@dartmoor.gov.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
import os.path
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Import the code for the dialog
from projectselectordialog import *
from templateselectordialog import *
from settingsdialog import *


class ProjectSelector(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'projectselector_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        # Create action that will start plugin configuration
        proj_icon_path = os.path.join(self.plugin_dir, 'icon.png')
        temp_icon_path = os.path.join(self.plugin_dir, 'template_selector_icon.png')
        self.projectSelectorAction = QAction(QIcon(proj_icon_path),
                                            u"Project Selector", self.iface.mainWindow())
        self.templateSelectorAction = QAction(QIcon(temp_icon_path),
                                              u"Template Selector", self.iface.mainWindow())
        self.configureAction = QAction(u"Configure Moor Tools", self.iface.mainWindow())
        # connect the action to the run method
        self.projectSelectorAction.triggered.connect(self.selectProject)
        self.templateSelectorAction.triggered.connect(self.selectTemplate)
        self.configureAction.triggered.connect(self.configure)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.projectSelectorAction)
        self.iface.addToolBarIcon(self.templateSelectorAction)
        self.iface.addPluginToMenu(u"&Moor Tools", self.projectSelectorAction)
        self.iface.addPluginToMenu(u"&Moor Tools", self.templateSelectorAction)
        self.iface.addPluginToMenu(u"&Moor Tools", self.configureAction)
        
        # Connect the dialog to QGIS' initializationCompleted() signal
        self.iface.initializationCompleted.connect(self.onInitializationCompleted)

    def unload(self):
        # Disconnect the dialog to QGIS' initializationCompleted() signal
        self.iface.initializationCompleted.disconnect(self.onInitializationCompleted)
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Moor Tools", self.configureAction)
        self.iface.removePluginMenu(u"&Moor Tools", self.projectSelectorAction)
        self.iface.removePluginMenu(u"&Moor Tools", self.templateSelectorAction)
        self.iface.removeToolBarIcon(self.projectSelectorAction)
        self.iface.removeToolBarIcon(self.templateSelectorAction)
        
    def onInitializationCompleted(self):
        project_selector_enabled = QSettings().value("MoorTools/ProjectSelector/isEnabled", True, type=bool)
        if len(QgsProject.instance().fileName()) == 0 and project_selector_enabled:
            # The project file name will only be populated after the initializationCompleted() signal is emitted if QGIS has
            # been invoked on a .qgs (project) file.  So only show the selector if we've not been opened on an existing .qgs
            # file
            self.selectProject()

    # run method that performs all the real work
    def selectProject(self):
        try:
            projectSelectorDlg = ProjectSelectorDialog(self.iface)
        except ProjectSelectorException:
            reply = QtGui.QMessageBox.question(self.iface.mainWindow(),
                'Moor Tools (Project Selector): No Projects Folder Specified',
                'It looks like you haven\'t yet specified the folder containing your QGIS start-up projects. Would you like to do that now?',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
            if reply == QtGui.QMessageBox.No:
                return
            self.configure()
            return # The user will need to invoke the action again
        # show the dialog
        projectSelectorDlg.show()
        # Run the dialog event loop
        result = projectSelectorDlg.exec_()

    def configure(self):
        settingsDialog = SettingsDialog()
        settingsDialog.show()
        settingsDialog.exec_()
            
    # run method that performs all the real work
    def selectTemplate(self):
        try:
            templateSelectorDlg = TemplateSelectorDialog(self.iface)
        except TemplateSelectorException:
            reply = QtGui.QMessageBox.question(self.iface.mainWindow(), 'Moor Tools (Template Selector): No Template Folder Specified', 'It looks like you haven\'t yet specified the folder containing your templates. Would you like to do that now?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
            if reply == QtGui.QMessageBox.No:
                return
            self.configure()
            return # The user will need to invoke the action again
        # show the dialog
        templateSelectorDlg.show()
        # Run the dialog event loop
        result = templateSelectorDlg.exec_()
