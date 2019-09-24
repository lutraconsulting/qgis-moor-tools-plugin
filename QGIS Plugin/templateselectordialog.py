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
import traceback
import locale
from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtWidgets import (
    QAction,
    QDialog,
    QDialogButtonBox,
    QSpacerItem,
    QComboBox,
    QLabel,
    QSizePolicy,
    QMessageBox
)
from qgis.core import (
    QgsPrintLayout,
    QgsMapLayer,
    QgsProject,
    QgsLayerTree,
    QgsLayerTreeLayer,
    QgsLayoutItemLegend,
    QgsLayoutItemMap,
    QgsReadWriteContext,
    QgsFeature,
    QgsPointXY,
    QgsRectangle,
    QgsWkbTypes,
    QgsUnitTypes
)
from qgis.gui import QtCore
from math import ceil
from xml.etree import ElementTree as ET
from .xy_to_osgb import xy_to_osgb

ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui_templateselector.ui')


class TemplateSelectorException(Exception):
    pass


class TemplateSelectorDialog(QDialog):
    def __init__(self, iface):

        self.supportedPaperSizes = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']  # ISO A series
        self.paperSizesPresent = []
        self.presetScales = ['200', '500', '1 000', '1 250', '2 500', '5 000', '10 000', '25 000', '50 000', '100 000']

        self.iface = iface
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = uic.loadUi(ui_file, self)

        # Set up the list of templates
        s = QtCore.QSettings()
        self.identifiable_only = s.value("SelectorTools/ProjectSelector/identifiableOnly", True, type=bool)
        self.templateFileRoot = s.value("SelectorTools/TemplateSelector/templateRoot", '', type=str)
        if len(self.templateFileRoot) == 0 or not os.path.isdir(self.templateFileRoot):
            raise TemplateSelectorException('\'%s\' is not a valid template file root folder.' % self.templateFileRoot)
        self.populateTemplateTypes()
        self.populatePoiLayers()
        self.onPoiLayerChanged()

        self.onTemplateTypeChanged()
        self.plugin_dir = os.path.dirname(__file__)

        # Replacement map
        self.ui.suitableForComboBox.addItem('<custom>')
        self.user = os.environ.get('username', '[user]')
        self.replaceMap = {
            'author': "Compiled by {} on [%concat(day($now ),'/',month($now),'/',year($now))%]".format(self.user)
        }
        self.ui.autofit_btn.clicked.connect(self.autofit_map)
        self.ui.suitableForComboBox.currentIndexChanged.connect(self.specify_dpi)
        self.ui.suitableForComboBox.editTextChanged.connect(self.text_changed)
        self.ui.poiLayerComboBox.currentIndexChanged.connect(self.onPoiLayerChanged)

    def specify_dpi(self, idx):
        if idx == 2:
            self.ui.suitableForComboBox.setEditable(True)
        else:
            self.ui.suitableForComboBox.setEditable(False)

    def text_changed(self, txt):
        self.ui.suitableForComboBox.setItemText(self.ui.suitableForComboBox.currentIndex(), txt)

    def autofit_map(self):
        canvas = self.iface.mapCanvas()
        units = canvas.mapUnits()
        coef = 1 / 0.3048 if units == QgsUnitTypes.DistanceFeet else 1
        map_extent = canvas.extent()
        me_height = map_extent.height() * 1000 / coef
        me_width = map_extent.width() * 1000 / coef
        print_layout = self.get_print_layout()
        map_elements = [item for item in print_layout.items() if isinstance(item, QgsLayoutItemMap)]

        for idx, item in enumerate(map_elements):
            size = item.sizeWithUnits()
            h = size.height()
            w = size.width()
            hscale = me_height / h
            wscale = me_width / w
            scale = hscale if hscale > wscale else wscale
            scale_str = '{} (Autofit)'.format(ceil(scale))
            scaleCombo = self.ui.scalesGridLayout.itemAtPosition(idx, 3).widget()
            idx = scaleCombo.findText(scale_str)
            if idx == -1:
                scaleCombo.insertItem(0, scale_str)
                scaleCombo.setCurrentIndex(0)
            else:
                scaleCombo.setCurrentIndex(idx)

    def onPoiLayerChanged(self):
        # Populate the list of available attribute names
        self.ui.poiFieldComboBox.blockSignals(True)
        self.ui.poiFieldComboBox.clear()
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == self.ui.poiLayerComboBox.currentText():
                for field in layer.dataProvider().fields().toList():
                    self.ui.poiFieldComboBox.addItem(field.name())
        self.ui.poiFieldComboBox.blockSignals(False)

    def populatePoiLayers(self):
        # Called once on init
        for layer in self.iface.mapCanvas().layers():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QgsWkbTypes.PointGeometry:
                self.ui.poiLayerComboBox.addItem(layer.name())

    def populateTemplateTypes(self):
        self.ui.templateTypeComboBox.blockSignals(True)
        self.ui.templateTypeComboBox.clear()
        for entry in os.listdir(self.templateFileRoot):
            if os.path.isdir(os.path.join(self.templateFileRoot, entry)):
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
            if paperSize in self.supportedPaperSizes and paperSize not in self.paperSizesPresent:
                self.paperSizesPresent.append(paperSize)
        self.paperSizesPresent.sort(reverse=True)

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
            print_layout = self.get_print_layout()
            poiEnabled = True if print_layout.itemById('gridref') else False
        self.ui.poiLayerLabel.setEnabled(poiEnabled)
        self.ui.poiLayerComboBox.setEnabled(poiEnabled)
        self.ui.poiFieldLabel.setEnabled(poiEnabled)
        self.ui.poiFieldComboBox.setEnabled(poiEnabled)
        # At this point we should know what the path to the .qpt file would be if the user was to hit OK
        # Check it exists and update the OK button appropriately
        qptFilePath = self.getQptFilePath()
        if qptFilePath is None or not os.path.isfile(qptFilePath):
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def populateScaleChoices(self):
        """ When the template type combo is initialised or changes, update the
        layout of scales for the various map elements in layout. """

        # Clear previous
        for i in reversed(list(range(self.ui.scalesGridLayout.count()))):
            item = self.ui.scalesGridLayout.itemAt(i)
            if type(item) == QSpacerItem:
                self.ui.scalesGridLayout.removeItem(item)
            else:
                item.widget().setParent(None)

        print_layout = self.get_print_layout()
        map_elements = [item for item in print_layout.items() if isinstance(item, QgsLayoutItemMap)]
        i = 0
        for elem in map_elements:
            label_1 = QLabel(elem.displayName())
            self.ui.scalesGridLayout.addWidget(label_1, i, 0)

            spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.ui.scalesGridLayout.addItem(spacer, i, 1)

            label_2 = QLabel('1:')
            self.ui.scalesGridLayout.addWidget(label_2, i, 2)

            comboBox = QComboBox()
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

        if len(map_elements) == 0:
            label = QLabel('No layout map elements found. Limited usability.')
            self.ui.scalesGridLayout.addWidget(label, i, 1)

    def set_legend_compositions(self, print_layout):
        non_ident = QgsProject.instance().nonIdentifiableLayers()
        self.legend_tree_root = QgsLayerTree()
        layer_nodes = []

        for lyr in self.iface.mapCanvas().layers():
            if lyr.id() not in non_ident:
                layer_nodes.append(QgsLayerTreeLayer(lyr))

        self.legend_tree_root.insertChildNodes(-1, layer_nodes)
        # update the model
        for item in print_layout.items():
            if not isinstance(item, QgsLayoutItemLegend):
                continue
            legend_model = item.model()
            legend_model.setRootGroup(self.legend_tree_root)

    def getQptFilePath(self):
        try:
            qptFilePath = os.path.join(self.templateFileRoot,
                                       self.ui.templateTypeComboBox.currentText(),
                                       self.ui.sizeComboBox.currentText() + self.ui.orientationComboBox.currentText()[
                                           0] +
                                       '.qpt')
        except IndexError:
            qptFilePath = None
        return qptFilePath

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
        if os.path.isfile(defaultFilePath):
            with open(defaultFilePath, 'r') as defaultFile:
                defautlCopyright = defaultFile.read().strip()
                if defautlCopyright.lower().endswith('.txt'):
                    defautlCopyright = defautlCopyright[:-4]
                self.ui.copyrightComboBox.setCurrentIndex(self.ui.copyrightComboBox.findText(defautlCopyright))

    def getTemplateFilePath(self):
        orientationLetter = self.ui.orientationComboBox.currentText()
        try:
            orientationLetter = orientationLetter[0]
        except IndexError:
            pass
        qptFilePath = os.path.join(self.templateFileRoot,
                                   self.ui.templateTypeComboBox.currentText(),
                                   self.ui.sizeComboBox.currentText() + orientationLetter + '.qpt')
        return qptFilePath

    def getCopyrightText(self):
        copyrightFilePath = os.path.join(self.templateFileRoot,
                                         self.ui.templateTypeComboBox.currentText(), 'Copyrights',
                                         self.ui.copyrightComboBox.currentText() + '.txt')
        try:
            with open(copyrightFilePath, 'r') as copyrightFile:
                copyrightText = copyrightFile.read().strip()
        except IOError:
            return ''
        return copyrightText

    def openTemplate(self):
        print_layout = self.get_print_layout()
        # Load replaceable text
        self.replaceMap['copyright'] = self.getCopyrightText()
        self.replaceMap['title'] = self.ui.titleLineEdit.text()
        # not in examples, is it still supported?
        self.replaceMap['subtitle'] = self.ui.subtitleLineEdit.text()
        self.replaceMap['gridref'] = self.getPoiText()

        for k, v in self.replaceMap.items():
            item = print_layout.itemById(k)
            if item:
                item.setText(v)

        # Update images of all maps elements in layout
        if self.identifiable_only:
            try:
                self.set_legend_compositions(print_layout)
            except AttributeError:
                msg = 'Filtering by identifiable layers ignored.'
                self.iface.messageBar().pushMessage('Project and Template Selector: ', msg, level=0)

        # get map items only
        map_items = [item for item in print_layout.items() if isinstance(item, QgsLayoutItemMap)]
        for idx, layout_map in enumerate(map_items):
            # Get the scale denominator (as a floating point)
            scaleCombo = self.ui.scalesGridLayout.itemAtPosition(idx, 3).widget()
            assert scaleCombo != 0
            try:
                scaleDenom = float(scaleCombo.currentText().replace(',', ''))
            except ValueError:
                cleanedScaleString = scaleCombo.currentText().replace(',', '').split(' (')[0]
                cleanedScaleString = ''.join(cleanedScaleString.split())
                scaleDenom = float(cleanedScaleString)
            # Set the scale
            cme = layout_map.extent()
            canvasEx = self.iface.mapCanvas().extent()
            p1 = QgsPointXY(canvasEx.center().x() - (cme.width() / 2.0),
                          canvasEx.center().y() - (cme.height() / 2.0))
            p2 = QgsPointXY(canvasEx.center().x() + (cme.width() / 2.0),
                          canvasEx.center().y() + (cme.height() / 2.0))
            newCme = QgsRectangle(p1, p2)
            layout_map.setExtent(newCme)
            layout_map.setScale(scaleDenom)
            layout_map.refresh()

        # Set scale
        cur_idx = self.ui.suitableForComboBox.currentIndex()
        if cur_idx == 0:
            # Paper
            dpi = 300
        elif cur_idx == 1:
            # Electronic
            dpi = 96
        else:
            res_text = self.ui.suitableForComboBox.currentText()
            try:
                dpi = int(res_text)
            except (TypeError, ValueError):
                dpi = 96
        print_layout.renderContext().setDpi(dpi)
        layout_designer_interface = self.iface.openLayoutDesigner(print_layout)

        # Maximize layout window
        ldi_window = layout_designer_interface.window()
        ldi_window.showMaximized()

        # Zoom to 100%
        ldi_parent = layout_designer_interface.parent()
        zoom_action = ldi_parent.findChild(QAction, 'mActionZoomActual')
        zoom_action.trigger()

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
            coordText = '%s\t%s\n' % (f.attribute(self.ui.poiFieldComboBox.currentText()), gridRef)
            poiString += coordText
        return poiString

    def updateScaleText(self, newText):
        strippedtext = newText[4:]
        self.ui.scaleLineEdit.setText(strippedtext)

    def loadHelpPage(self):
        helpUrl = 'https://github.com/lutraconsulting/qgis-moor-tools-plugin/blob/master/README.md'
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(helpUrl))

    def get_print_layout(self):
        template_path = self.getTemplateFilePath()
        if not os.path.isfile(template_path):
            msg = 'The requested template {} is not currently available.'.format(template_path)
            QMessageBox.critical(self.iface.mainWindow(), 'Template Not Found', msg)
            return

        # Create a new print layout with name equal to the project title
        project = QgsProject.instance()
        layout_manager = project.layoutManager()
        existing_print_layout = layout_manager.layoutByName(self.ui.titleLineEdit.text())
        if existing_print_layout:
            layout_manager.removeLayout(existing_print_layout)
        print_layout = QgsPrintLayout(project)
        print_layout.setName(self.ui.titleLineEdit.text())
        layout_manager.addLayout(print_layout)

        # Load the template file
        try:
            tree = ET.parse(template_path)
            doc = QDomDocument()
            doc.setContent(ET.tostring(tree.getroot()))
        except IOError:
            # problem reading xml template
            msg = 'The requested template {} could not be read.'.format(template_path)
            QMessageBox.critical(self.iface.mainWindow(), 'Failed to Read Template', msg)
            return
        except:
            # Unexpected problem
            msg = 'An unexpected error occurred while reading {}:\n\n{}'.format(template_path, traceback.format_exc())
            QMessageBox.critical(self.iface.mainWindow(), 'Failed to Read Template', msg)
            return

        if not print_layout.loadFromTemplate(doc, QgsReadWriteContext(), True):
            msg = 'loadFromTemplate returned False.'
            QMessageBox.critical(self.iface.mainWindow(), 'Failed to Read Template', msg)
            return

        return print_layout
