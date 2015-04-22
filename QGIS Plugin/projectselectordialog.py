# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProjectSelectorDialog
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
import collections
import os

from PyQt4 import QtCore, QtGui
from ui_projectselector import Ui_ProjectSelector
# create the dialog for zoom to point


class ProjectSelectorDialog(QtGui.QDialog):
    
    def __init__(self, iface):
        
        # import pydevd; pydevd.settrace(suspend=False)
        
        self.iface = iface
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ProjectSelector()
        self.ui.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)
        
        # Disable OK button until we are sure we have at least one project
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        
        # Loads the projects data structure
        # Replace the path below with the path to your config file
        #configFilePath = os.path.join(self.plugin_dir, 'examples', 'project_selector_config.txt')
        configFilePath = r'Q:\QGIS\plugins\project_selector_config\project_selector_config.txt'
        configFile = open(configFilePath, 'r')
        self.projects = collections.OrderedDict()
        for line in configFile:
            try:
                prettyName = line.split('|')[0]
                path = line.split('|')[1]
                enabled = line.split('|')[2].strip() == '1'
                self.projects[prettyName] = path, enabled
            except:
                pass
        configFile.close()

        self.radioButtons = []
        
        if len(self.projects) > 0:
            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        haveSelectedRadioButton = False
        for name, pathEnabledPair in self.projects.iteritems():
            path, enabled = pathEnabledPair
            rb = QtGui.QRadioButton(name, self.ui.groupBox)
            if enabled:
                rb.setChecked(True)
                haveSelectedRadioButton = True
            self.ui.groupBox.layout().addWidget(rb)
            self.radioButtons.append(rb)
            
        if not haveSelectedRadioButton:
            self.radioButtons[0].setChecked(True)
            
    def loadProject(self):
        
        """
            1 Determine which radio button is pressed
            2 Determine the associated project path
            3 Open the project
        """
        
        # Determine which radio button is pressed
        # projectPath = None
        for rb in self.radioButtons:
            if rb.isChecked():
                prettyName = rb.text()
                projectPath, dummy = self.projects[prettyName]
                break
        
        self.iface.addProject(projectPath)
        self.accept()
