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

import os
from qgis.PyQt import QtCore, uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QMessageBox
# create the dialog for zoom to point

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = os.path.join(PARENT_DIR, 'defaults.txt')

ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui_settings.ui')


class SettingsDialog(QDialog):

    def __init__(self):
        
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = uic.loadUi(ui_file, self)

        self.settings = QtCore.QSettings()

        # Populate the values
        with open(DEFAULTS) as paths:
            projects = paths.readline().strip().split(':', 1)[-1]
            templates = paths.readline().strip().split(':', 1)[-1]
            self.ui.projectsFolderLineEdit.setText(projects)
            self.ui.templateRootLineEdit.setText(templates)
        project_selector_enabled = self.settings.value("SelectorTools/ProjectSelector/isEnabled", True, type=bool)
        identifiable_only = self.settings.value("SelectorTools/ProjectSelector/identifiableOnly", True, type=bool)
        self.ui.projectSelectorEnabledCheckBox.setChecked(project_selector_enabled)
        self.ui.identifiableOnly.setChecked(identifiable_only)

    def browseForProjectRoot(self):
        startingDir = str(self.settings.value("SelectorTools/ProjectSelector/projectRoot", os.path.expanduser("~"), type=str))
        d = str(QFileDialog.getExistingDirectory(None, 'Select Projects Folder', startingDir))
        if d != os.sep and d.lower() != 'c:\\' and d != '':
            self.ui.projectsFolderLineEdit.setText(d)

    def browseForTemplateRoot(self):
        startingDir = str(self.settings.value("SelectorTools/TemplateSelector/templateRoot", os.path.expanduser("~"), type=str))
        d = str(QFileDialog.getExistingDirectory(None, 'Select Root of Template Folder Structure', startingDir))
        if d != os.sep and d.lower() != 'c:\\' and d != '':
            self.ui.templateRootLineEdit.setText(d)

    def accept(self):
        projects = self.ui.projectsFolderLineEdit.text()
        self.settings.setValue("SelectorTools/ProjectSelector/projectRoot", projects)
        templates = self.ui.templateRootLineEdit.text()
        self.settings.setValue("SelectorTools/TemplateSelector/templateRoot", templates)
        try:
            with open(DEFAULTS, 'w') as paths:
                paths.write('projects:{}\n'.format(projects))
                paths.write('templates:{}\n'.format(templates))
        except IOError:
            QMessageBox.warning(None, \
                                      'Could not save folders', \
                                      '%s could not be opened for writing, please ensure you have permission to edit this file.' \
                                      % DEFAULTS )
        project_selector_enabled = self.ui.projectSelectorEnabledCheckBox.isChecked()
        self.settings.setValue("SelectorTools/ProjectSelector/isEnabled", project_selector_enabled)
        identifiable_only = self.ui.identifiableOnly.isChecked()
        self.settings.setValue("SelectorTools/ProjectSelector/identifiableOnly", identifiable_only)
        QDialog.accept(self)
