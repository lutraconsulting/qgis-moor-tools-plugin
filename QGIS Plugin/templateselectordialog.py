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

from PyQt4 import QtCore, QtGui, QtXml
from qgis.core import *
from qgis.gui import *
from ui_templateselector import Ui_TemplateSelector
# create the dialog for zoom to point

import os
import traceback


class TemplateSelectorDialog(QtGui.QDialog):
    
    
    def __init__(self, iface):
        
        ##import pydevd; pydevd.settrace(suspend=False)
        
        self.iface = iface
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_TemplateSelector()
        self.ui.setupUi(self)
        self.plugin_dir = os.path.dirname(__file__)
        
        # Set accordingly to your environment
        self.templateFileRoot = os.path.join(self.plugin_dir, 'Templates')
        # self.templateFileRoot = r'C:\tmp\QGIS\Templates'
        
        # Replacement map
        self.replaceMap = { 'username' : os.environ['username'] }
        self.copyrightTexts = []
        self.loadCopyrights()
        
    
    def loadCopyrights(self):
        copyrightConfigFileName = os.path.join(self.templateFileRoot, 'copyright_selector_config.txt')
        copyrightConfigFile = open(copyrightConfigFileName, 'r')
        i = 0
        defaultIndex = 0
        for line in copyrightConfigFile:
            prettyName = line.split('|')[0]
            copyrightText = line.split('|')[1]
            self.copyrightTexts.append(copyrightText)
            if line.split('|')[2] == '1':
                defaultIndex = i
            self.ui.copyrightComboBox.addItem(prettyName)
            i += 1
        copyrightConfigFile.close()
        self.ui.copyrightComboBox.setCurrentIndex(defaultIndex)
    
    
    def openTemplate(self):
        
        # Determine the filename of the template by concention
        sizeText = self.ui.sizeComboBox.currentText()
        orientationText = self.ui.orientationComboBox.currentText()
        
        templateFileName = sizeText + orientationText[0] + '.qpt'
        #templateFileName = 'A4Ltest.qpt' # FIXME
        templateFilePath = os.path.join(self.templateFileRoot, templateFileName)
        prettyName = '%s %s' % (sizeText, orientationText)
        
        if not os.path.isfile(templateFilePath):
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Template Not Found', \
                'The requested template (%s) is not currently available.' \
                % templateFileName)
            return
        
        # Load replaceable text
        projectTitle = self.ui.titleLineEdit.text()
        
        # Set copyright
    
        copyrightIndex = self.ui.copyrightComboBox.currentIndex()
        self.replaceMap['copyright'] = self.copyrightTexts[copyrightIndex]
        self.replaceMap['title'] = projectTitle
        
        # Create a new Composer View with name equal to the project 
        # title
        composerView = self.iface.createNewComposer(projectTitle)
        
        
        # Load the template file, replacing any text we find in 
        # '[' and ']'
        try:
            templateFile = open(templateFilePath, 'r')
            fileContent = templateFile.read()
            templateFile.close()
            doc = QtXml.QDomDocument()
            doc.setContent(fileContent)
        except IOError:
            # problem reading xml template
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Failed to Read Template', \
                'The requested template (%s) could not be read.' \
                % templateFileName)
            return
        except:
            # Unexpected problem
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Failed to Read Template', \
                'An unexpected error occured while reading (%s):\n\n%s' \
                % (templateFileName, traceback.format_exc()))
            return
        
        # Loaded the XML, replacing any replacables
        if not composerView.composition().loadFromTemplate(doc, self.replaceMap, True):
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Failed to Read Template', \
                'loadFromTemplate returned False.')
            return
            
        # Get the scale denominator (as a floating point)
        scaleDenom = float(self.ui.scaleLineEdit.text().replace(',', ''))
        
        # Update the ComposerMap cached images of all ComposerMaps
        
        i = 0
        compMap = composerView.composition().getComposerMapById(i)
        while(compMap):
            if i == 0:
                # This is the first Composer Map, set the scale
                cme = compMap.extent()
                canvasEx = self.iface.mapCanvas().extent()
                p1 = QgsPoint( canvasEx.center().x()-(cme.width()/2.0),
                               canvasEx.center().y()-(cme.height()/2.0) )
                p2 = QgsPoint( canvasEx.center().x()+(cme.width()/2.0),
                               canvasEx.center().y()+(cme.height()/2.0) )
                newCme = QgsRectangle(p1, p2)
                compMap.setNewExtent( newCme )
                compMap.setNewScale(scaleDenom)
            compMap.updateCachedImage()
            i += 1
            compMap = composerView.composition().getComposerMapById(i)
        
        # Set scale
        resText = self.ui.suitableForComboBox.currentText()
        dpi = 0
        if resText.startswith('Paper'):
            dpi = 300
        else:
            # Electronic
            dpi = 96
        composerView.composition().setPrintResolution(dpi)
        
        # All done
        self.accept()
        
        
    def test(self):
        i = 1
        pass
        
    
    def updateScaleText(self, newText):
        strippedtext = newText[4:]
        self.ui.scaleLineEdit.setText( strippedtext )
    
    def loadHelpPage(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://intranet.dartmoor-npa.gov.uk/useful_i/gis-mapping-guidance'))
        
