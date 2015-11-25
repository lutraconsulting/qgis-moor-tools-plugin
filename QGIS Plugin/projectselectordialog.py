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
        
        # import pydevd; pydevd.settrace()
        
        # Disable OK button until we are sure we have at least one project
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

        # Set up the list of templates
        self.settings = QtCore.QSettings()
        self.projectFileRoot = self.settings.value('MoorTools/ProjectSelector/projectRoot', '', type=str)
        if len(self.projectFileRoot) == 0 or not os.path.isdir(self.projectFileRoot):
            raise ProjectSelectorException('\'%s\' is not a valid project file root folder.' % self.projectFileRoot)

        # Populate the list of project types
        self.ui.projectGroupComboBox.blockSignals(True)
        for entry in os.listdir(self.projectFileRoot):
            entryPath = os.path.join(self.projectFileRoot, entry)
            if not os.path.isdir(entryPath):
                continue
            # Check there's a .qgs file in this path
            for subEntry in os.listdir(entryPath):
                if subEntry.lower().endswith('.qgs') and os.path.isfile(os.path.join(entryPath, subEntry)):
                    # The folder contains at least one project, add it
                    self.ui.projectGroupComboBox.addItem(entry)
                    break
        self.ui.projectGroupComboBox.blockSignals(False)
        defaultGroup = self.settings.value('MoorTools/ProjectSelector/defaultProjectGroup', '', type=str)
        if len(defaultGroup) > 0:
            self.ui.projectGroupComboBox.setCurrentIndex( self.ui.projectGroupComboBox.findText(defaultGroup) )
        if self.ui.projectGroupComboBox.count() == 1:
            self.ui.projectGroupComboBox.setCurrentIndex(0)
            self.ui.projectGroupComboBox.setEnabled(False)
        self.onProjectGroupChanged()
        
    def getDefaultProject(self, location):
        
        defaultProject = None
        defaultFilePath = os.path.join(location, 'default.txt')
        try:
            with open(defaultFilePath, 'r') as defaultFile:
                defaultProject = defaultFile.read().strip()
                if defaultProject.lower().endswith('.qgs'):
                    defaultProject = defaultProject[:-4]
        except IOError:
            pass
        return defaultProject
        
    def onProjectGroupChanged(self, projectGroupId=-1):
        
        # Called when the project group changes
        # Used to update the list of projects within this group

        projectGroupname = self.ui.projectGroupComboBox.currentText()
        if projectGroupname == '':
            return
        self.ui.selectedProjectListWidget.clear()
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        groupFolderPath = os.path.join(self.projectFileRoot, projectGroupname)
        for entry in os.listdir(groupFolderPath):
            projectFilePath = os.path.join(groupFolderPath, entry)
            if os.path.isdir(projectFilePath):
                continue
            if entry.lower().endswith('.qgs'):
                prettyName, dummy = os.path.splitext(entry)
                self.ui.selectedProjectListWidget.addItem(prettyName)
                self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        
        # Set the default project (if exists)
        defP = self.getDefaultProject(groupFolderPath)
        if defP != None:
            for i in range(self.ui.selectedProjectListWidget.count()):
                if self.ui.selectedProjectListWidget.item(i).text() == defP:
                    self.ui.selectedProjectListWidget.setCurrentRow(i)
                    break
        else:
            self.ui.selectedProjectListWidget.setCurrentRow(0)
                    
    def loadProject(self):
        
        groupName = self.ui.projectGroupComboBox.currentText()
        projectName = self.ui.selectedProjectListWidget.selectedItems()[0].text()
        projectPath = os.path.join( self.projectFileRoot, groupName, projectName + '.qgs' )
        
        self.iface.addProject(projectPath)
        # Store last used project group
        self.settings.setValue('MoorTools/ProjectSelector/defaultProjectGroup', self.ui.projectGroupComboBox.currentText())
        self.accept()
