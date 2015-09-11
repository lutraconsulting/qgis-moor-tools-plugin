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

class ProjectSelectorException(Exception):
    pass


class ProjectSelectorDialog(QtGui.QDialog):
    
    def __init__(self, iface):
        
        self.iface = iface
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ProjectSelector()
        self.ui.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)
        
        # Disable OK button until we are sure we have at least one project
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

        # Set up the list of templates
        s = QtCore.QSettings()
        projectFileRoot = s.value("MoorTools/ProjectSelector/projectRoot", '', type=str)
        if len(projectFileRoot) == 0 or not os.path.isdir(projectFileRoot):
            raise ProjectSelectorException('\'%s\' is not a valid project file root folder.' % projectFileRoot)

        # Loads the projects data structure
        self.projects = collections.OrderedDict()
        
        # TODO: Adapt this to work with projects in subfolders (to facilitate aggregation)

        for entry in os.listdir(projectFileRoot):
            projectFilePath = os.path.join(projectFileRoot, entry)
            if os.path.isdir(projectFilePath):
                continue
            if entry.lower().endswith('.qgs'):
                prettyName, dummy = os.path.splitext(entry)
                self.projects[prettyName] = projectFilePath, False
        defaultFilePath = os.path.join(projectFileRoot, 'default.txt')
        try:
            with open(defaultFilePath, 'r') as defaultFile:
                defaultProject = defaultFile.read().strip()
                if defaultProject.lower().endswith('.qgs'):
                    defaultProject = defaultProject[:-4]
        except IOError:
            pass
        try:
            path, dummy = self.projects[defaultProject]
            self.projects[defaultProject] = path, True
        except KeyError:
            pass
        except UnboundLocalError:
            pass

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
