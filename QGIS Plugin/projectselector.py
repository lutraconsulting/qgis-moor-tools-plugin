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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from projectselectordialog import ProjectSelectorDialog
from templateselectordialog import TemplateSelectorDialog
import os.path


class ProjectSelector:

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

        # Create the dialog (after translation) and keep reference
        self.projectSelectorDlg = ProjectSelectorDialog(self.iface)
        self.templateSelectorDlg = TemplateSelectorDialog(self.iface)

    def initGui(self):
        # Create action that will start plugin configuration
        self.projectSelectorAction = QAction(
            QIcon(":/plugins/projectselector/icon.png"),
            u"Project Selector", self.iface.mainWindow())
        self.templateSelectorAction = QAction(
            QIcon(":/plugins/projectselector/template_selector_icon.png"),
            u"Template Selector", self.iface.mainWindow())
        # connect the action to the run method
        self.projectSelectorAction.triggered.connect(self.selectProject)
        self.templateSelectorAction.triggered.connect(self.selectTemplate)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.projectSelectorAction)
        self.iface.addToolBarIcon(self.templateSelectorAction)
        self.iface.addPluginToMenu(u"&Moor Tools", self.projectSelectorAction)
        self.iface.addPluginToMenu(u"&Moor Tools", self.templateSelectorAction)
        
        # Connect the dialog to QGIS' initializationCompleted() signal
        QObject.connect( self.iface, SIGNAL("initializationCompleted()"), self.selectProject )

    def unload(self):
        # Disconnect the dialog to QGIS' initializationCompleted() signal
        QObject.disconnect( self.iface, SIGNAL("initializationCompleted()"), self.selectProject )
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Moor Tools", self.projectSelectorAction)
        self.iface.removePluginMenu(u"&Moor Tools", self.templateSelectorAction)
        self.iface.removeToolBarIcon(self.projectSelectorAction)
        self.iface.removeToolBarIcon(self.templateSelectorAction)
        

    # run method that performs all the real work
    def selectProject(self):
        # show the dialog
        self.projectSelectorDlg.show()
        # Run the dialog event loop
        result = self.projectSelectorDlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
            
    # run method that performs all the real work
    def selectTemplate(self):
        # show the dialog
        self.templateSelectorDlg.show()
        # Run the dialog event loop
        result = self.templateSelectorDlg.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            pass
