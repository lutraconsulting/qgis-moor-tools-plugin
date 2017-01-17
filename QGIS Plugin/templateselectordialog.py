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
import re
import locale
from xml.etree import ElementTree as ET
from xy_to_osgb import xy_to_osgb


class TemplateSelectorException(Exception):
    pass
        
        
class TemplateSelectorDialog(QtGui.QDialog):
    
    def __init__(self, iface):

        self.supportedPaperSizes = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'] # ISO A series
        self.paperSizesPresent = []
        self.presetScales = ['200', '500', '1,000', '1,250', '2,500', '5,000', '10,000', '25,000', '50,000', '100,000']

        self.iface = iface
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_TemplateSelector()
        self.ui.setupUi(self)
        
        # Set up the list of templates
        s = QtCore.QSettings()
        self.templateFileRoot = s.value("MoorTools/TemplateSelector/templateRoot", '', type=str)
        if len(self.templateFileRoot) == 0 or not os.path.isdir(self.templateFileRoot):
            raise TemplateSelectorException('\'%s\' is not a valid template file root folder.' % self.templateFileRoot)
        self.populateTemplateTypes()
        self.populatePoiLayers()
        self.onPoiLayerChanged()
        
        self.onTemplateTypeChanged()
        self.plugin_dir = os.path.dirname(__file__)
        
        # Replacement map
        self.replaceMap = { 'username' : os.environ['username'] }

    
    def onPoiLayerChanged(self):
        # Populate the list of available attribute names
        self.ui.poiFieldComboBox.blockSignals(True)
        self.ui.poiFieldComboBox.clear()
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == self.ui.poiLayerComboBox.currentText():
                for field in layer.dataProvider().fields().toList():
                    self.ui.poiFieldComboBox.addItem( field.name() )
        self.ui.poiFieldComboBox.blockSignals(False)


    def populatePoiLayers(self):
        # Called once on init
        for layer in self.iface.mapCanvas().layers():
            if layer.type() != QgsMapLayer.VectorLayer:
                continue
            if layer.geometryType() != QGis.Point:
                continue
            self.ui.poiLayerComboBox.addItem(layer.name())


    def populateTemplateTypes(self):
        self.ui.templateTypeComboBox.blockSignals(True)
        self.ui.templateTypeComboBox.clear()
        for entry in os.listdir(self.templateFileRoot):
            if os.path.isdir( os.path.join(self.templateFileRoot, entry) ):
                for subentry in os.listdir(os.path.join(self.templateFileRoot, entry)):
                    filePath = os.path.join(self.templateFileRoot, entry, subentry)
                    dummy, fileName = os.path.split(filePath)
                    if os.path.isfile(filePath) and \
                       fileName.lower().endswith('.qpt') and \
                       fileName[:2] in self.supportedPaperSizes:
                        self.ui.templateTypeComboBox.addItem(entry)
                        break
        self.ui.templateTypeComboBox.blockSignals(False)
    
    def onTemplateTypeChanged(self, newIdx=None):
        # Determine what paper sizes are available
        self.ui.sizeComboBox.blockSignals(True)
        self.ui.sizeComboBox.clear()
        if self.ui.templateTypeComboBox.count() > 0:
            self.getPaperSizes()
            for paperSize in self.paperSizesPresent:
                self.ui.sizeComboBox.addItem(paperSize)
            self.loadCopyrights()
        self.ui.sizeComboBox.blockSignals(False)
        self.onPaperSizeChanged()

    def getPaperSizes(self):
        # Maintain a list of paper sizes available for the given template
        self.paperSizesPresent = []
        templateFolder = os.path.join(self.templateFileRoot, self.ui.templateTypeComboBox.currentText())
        for entry in os.listdir(templateFolder):
            if not os.path.isfile(os.path.join(templateFolder, entry)) or not entry.lower().endswith('.qpt'):
                continue
            paperSize = entry[:2]
            if paperSize in self.supportedPaperSizes and not paperSize in self.paperSizesPresent:
                self.paperSizesPresent.append(paperSize)
    
    def onPaperSizeChanged(self, newIdx=None):
        # Determine what orientations are available
        self.ui.orientationComboBox.blockSignals(True)
        self.ui.orientationComboBox.clear()
        if self.ui.templateTypeComboBox.count() > 0:
            templateFolder = os.path.join(self.templateFileRoot, self.ui.templateTypeComboBox.currentText())
            for entry in os.listdir(templateFolder):
                if entry.lower().endswith('.qpt') and entry.startswith(self.ui.sizeComboBox.currentText()):
                    if entry[2] == 'P' and self.ui.orientationComboBox.findText('Portrait') == -1:
                        self.ui.orientationComboBox.addItem('Portrait')
                    elif entry[2] == 'L' and self.ui.orientationComboBox.findText('Landscape') == -1:
                        self.ui.orientationComboBox.addItem('Landscape')
        self.ui.orientationComboBox.blockSignals(False)
        self.onPaperOrientationChanged()
    
    def onPaperOrientationChanged(self, newIdx=None):
        self.populateScaleChoices()
        poiEnabled = False
        if self.ui.orientationComboBox.count() > 0:
            poiEnabled = self.hasGridRefs()
        self.ui.poiLayerLabel.setEnabled( poiEnabled )
        self.ui.poiLayerComboBox.setEnabled( poiEnabled )
        self.ui.poiFieldLabel.setEnabled( poiEnabled )
        self.ui.poiFieldComboBox.setEnabled( poiEnabled )
        # At this point we should know what the path to the .qpt file would be if the user was to hit OK
        # Check it exists and update the OK button appropriately
        qptFilePath = self.getQptFilePath()
        if qptFilePath is None or not os.path.isfile(qptFilePath):
            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)

    def populateScaleChoices(self):
        
        """ When the template type combo is initialised or changes, update the 
        layout of scales for the various Composer Maps """

        # Clear previous
        for i in reversed(range(self.ui.scalesGridLayout.count())):
            item = self.ui.scalesGridLayout.itemAt(i)
            if type(item) == QtGui.QSpacerItem:
                self.ui.scalesGridLayout.removeItem(item)
            else:
                item.widget().setParent(None)

        composerMapNames = self.fetchComposerMapNames()
        i = 0
        for composerMapName in composerMapNames:

            label_1 = QtGui.QLabel(composerMapName)
            self.ui.scalesGridLayout.addWidget(label_1, i, 0)

            spacer = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.ui.scalesGridLayout.addItem(spacer, i, 1)

            label_2 = QtGui.QLabel('1:')
            self.ui.scalesGridLayout.addWidget(label_2, i, 2)

            comboBox = QtGui.QComboBox()
            comboBox.setEditable(True)
            # Add current canvas scale
            locale.setlocale(locale.LC_ALL, '')
            currentMapCanvasScale = self.iface.mapCanvas().scale()
            scaleString = locale.format('%d', currentMapCanvasScale, grouping=True)
            comboBox.addItem('%s (Current map canvas)' % scaleString)
            for scale in self.presetScales:
                comboBox.addItem(str(scale))
            self.ui.scalesGridLayout.addWidget(comboBox, i, 3)

            i += 1

        if len(composerMapNames) == 0:
            label = QtGui.QLabel('(No Composer Maps Found)')
            self.ui.scalesGridLayout.addWidget(label, 0, 0)

    def fetchComposerMapNames(self):
        # Return a list of the names of Composer Maps in the current .qpt file
        composerNames = []
        if self.ui.templateTypeComboBox.count() == 0:
            return composerNames

        root = ET.parse(self.getQptFilePath())
        
        i = 1
        for composerMapElement in root.findall("./Composition/ComposerMap"):
            try:
                name = composerMapElement.find('ComposerItem').attrib['id']
            except ValueError:
                name = 'Map %d' % i
            if len(name) == 0:
                name = 'Map %d' % i
            composerNames.append(name)
            i += 1
        return composerNames

    def getQptFilePath(self):
        try:
            qptFilePath = os.path.join( self.templateFileRoot,
                                        self.ui.templateTypeComboBox.currentText(),
                                        self.ui.sizeComboBox.currentText() + self.ui.orientationComboBox.currentText()[0] +
                                        '.qpt' )
        except IndexError:
            qptFilePath = None
        return qptFilePath

    def hasGridRefs(self):
        # Returns true if the template has a label element with the ID 'gridref'

        root = ET.parse(self.getQptFilePath())
        return len(root.findall("//ComposerLabel/ComposerItem[@id='gridref']")) > 0

    def loadCopyrights(self):
        self.ui.copyrightComboBox.clear()
        templateFolder = os.path.join(self.templateFileRoot, self.ui.templateTypeComboBox.currentText())
        copyrightFolder = os.path.join(templateFolder, 'Copyrights')
        if not os.path.isdir(copyrightFolder):
            return
        for entry in os.listdir(copyrightFolder):
            if entry.lower().endswith('.txt'):
                entry = entry[:-4]
                if entry.lower() == 'default':
                    continue
                self.ui.copyrightComboBox.addItem(entry)
        
        defaultFilePath = os.path.join(copyrightFolder, 'default.txt')
        if os.path.isfile( defaultFilePath ):
            with open(defaultFilePath, 'r') as defaultFile:
                defautlCopyright = defaultFile.read().strip()
                if defautlCopyright.lower().endswith('.txt'):
                    defautlCopyright = defautlCopyright[:-4]
                self.ui.copyrightComboBox.setCurrentIndex( self.ui.copyrightComboBox.findText(defautlCopyright) )
    
    
    def getTemplateFilePath(self):
        orientationLetter = self.ui.orientationComboBox.currentText()
        try:
            orientationLetter = orientationLetter[0]
        except IndexError:
            pass
        qptFilePath = os.path.join( self.templateFileRoot,
                                    self.ui.templateTypeComboBox.currentText(), 
                                    self.ui.sizeComboBox.currentText() + orientationLetter + '.qpt' )
        return qptFilePath
        
    def getCopyrightText(self):
        copyrightFilePath = os.path.join( self.templateFileRoot, 
                                          self.ui.templateTypeComboBox.currentText(), 'Copyrights', 
                                          self.ui.copyrightComboBox.currentText() + '.txt' )
        try:
            with open(copyrightFilePath, 'r') as copyrightFile:
                copyrightText = copyrightFile.read().strip()
        except IOError:
            return ''
        return copyrightText
    
    def openTemplate(self):
        
        templateFilePath = self.getTemplateFilePath()
        
        if not os.path.isfile(templateFilePath):
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Template Not Found', \
                'The requested template (%s) is not currently available.' \
                % templateFilePath)
            return
        
        # Load replaceable text
        projectTitle = self.ui.titleLineEdit.text()
        projectSubTitle = self.ui.subtitleLineEdit.text()
        
        # Set copyright
    
        copyrightIndex = self.ui.copyrightComboBox.currentIndex()
        self.replaceMap['copyright'] = self.getCopyrightText()
        self.replaceMap['title'] = projectTitle
        self.replaceMap['subtitle'] = projectSubTitle
        
        # Create a new Composer View with name equal to the project 
        # title
        composerView = self.iface.createNewComposer(projectTitle)
        
        
        # Load the template file, replacing any text we find in 
        # '[' and ']'
        try:
            tree = ET.parse(templateFilePath)
            if self.hasGridRefs():
                # Replace the content of the 'gridref' element based on the selected POI layer
                composerLabelElem = tree.find("//ComposerLabel/ComposerItem[@id='gridref']/..")
                composerLabelElem.attrib['labelText'] = self.getPoiText()
            doc = QtXml.QDomDocument()
            doc.setContent( ET.tostring(tree.getroot()) )
        except IOError:
            # problem reading xml template
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Failed to Read Template', \
                'The requested template (%s) could not be read.' \
                % templateFilePath)
            return
        except:
            # Unexpected problem
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Failed to Read Template', \
                'An unexpected error occured while reading (%s):\n\n%s' \
                % (templateFilePath, traceback.format_exc()))
            return
        
        # Loaded the XML, replacing any replacables
        if not composerView.composition().loadFromTemplate(doc, self.replaceMap, True):
            QtGui.QMessageBox.critical(self.iface.mainWindow(), \
                'Failed to Read Template', \
                'loadFromTemplate returned False.')
            return
            
        # Update the ComposerMap cached images of all ComposerMaps
        
        i = 0
        compMap = composerView.composition().getComposerMapById(i)
        while(compMap):
            # Get the scale denominator (as a floating point)
            scaleCombo = self.ui.scalesGridLayout.itemAtPosition(i, 3).widget()
            assert scaleCombo != 0
            try:
                scaleDenom = float(scaleCombo.currentText().replace(',', ''))
            except ValueError:
                cleanedScaleString = scaleCombo.currentText().split(' (')[0]
                cleanedScaleString = cleanedScaleString.replace(')', '')
                scaleDenom = float(cleanedScaleString.replace(',', ''))
            # Set the scale
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
        
        
    def getPoiText(self):
        # Return grid references of POIs
        poiLayer = None
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == self.ui.poiLayerComboBox.currentText():
                poiLayer = layer
                break
        if poiLayer == None:
            return 'Failed to find POI layer %s' % self.ui.poiLayerComboBox.currentText()
        poiString = 'Grid References\n\n'
        f = QgsFeature()
        fit = poiLayer.getFeatures()
        while fit.nextFeature(f):
            gridRef = xy_to_osgb(f.geometry().centroid().asPoint()[0], f.geometry().centroid().asPoint()[1], 10)
            coordText = '%s\t%s\n' % ( f.attribute(self.ui.poiFieldComboBox.currentText()), gridRef )
            poiString += coordText
        return poiString


    def updateScaleText(self, newText):
        strippedtext = newText[4:]
        self.ui.scaleLineEdit.setText( strippedtext )
    
    def loadHelpPage(self):
        helpUrl = 'https://github.com/lutraconsulting/qgis-moor-tools-plugin/blob/master/README.md'
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(helpUrl))
        
