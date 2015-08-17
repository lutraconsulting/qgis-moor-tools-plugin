# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_templateselector.ui'
#
# Created: Mon Aug 17 14:18:02 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TemplateSelector(object):
    def setupUi(self, TemplateSelector):
        TemplateSelector.setObjectName(_fromUtf8("TemplateSelector"))
        TemplateSelector.setWindowModality(QtCore.Qt.ApplicationModal)
        TemplateSelector.resize(297, 218)
        TemplateSelector.setModal(True)
        self.gridLayout = QtGui.QGridLayout(TemplateSelector)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(TemplateSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 5)
        self.copyrightComboBox = QtGui.QComboBox(TemplateSelector)
        self.copyrightComboBox.setObjectName(_fromUtf8("copyrightComboBox"))
        self.gridLayout.addWidget(self.copyrightComboBox, 5, 1, 1, 4)
        self.mapScalesGroupBox = QtGui.QGroupBox(TemplateSelector)
        self.mapScalesGroupBox.setObjectName(_fromUtf8("mapScalesGroupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.mapScalesGroupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scalesGridLayout = QtGui.QGridLayout()
        self.scalesGridLayout.setObjectName(_fromUtf8("scalesGridLayout"))
        self.gridLayout_2.addLayout(self.scalesGridLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.mapScalesGroupBox, 3, 0, 1, 5)
        self.suitableForLabel = QtGui.QLabel(TemplateSelector)
        self.suitableForLabel.setObjectName(_fromUtf8("suitableForLabel"))
        self.gridLayout.addWidget(self.suitableForLabel, 4, 0, 1, 1)
        self.copyrightLabel = QtGui.QLabel(TemplateSelector)
        self.copyrightLabel.setObjectName(_fromUtf8("copyrightLabel"))
        self.gridLayout.addWidget(self.copyrightLabel, 5, 0, 1, 1)
        self.suitableForComboBox = QtGui.QComboBox(TemplateSelector)
        self.suitableForComboBox.setObjectName(_fromUtf8("suitableForComboBox"))
        self.suitableForComboBox.addItem(_fromUtf8(""))
        self.suitableForComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.suitableForComboBox, 4, 1, 1, 4)
        self.templateTypeComboBox = QtGui.QComboBox(TemplateSelector)
        self.templateTypeComboBox.setObjectName(_fromUtf8("templateTypeComboBox"))
        self.gridLayout.addWidget(self.templateTypeComboBox, 0, 1, 1, 4)
        self.titleLabel = QtGui.QLabel(TemplateSelector)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 1, 0, 1, 1)
        self.titleLineEdit = QtGui.QLineEdit(TemplateSelector)
        self.titleLineEdit.setObjectName(_fromUtf8("titleLineEdit"))
        self.gridLayout.addWidget(self.titleLineEdit, 1, 1, 1, 4)
        self.templateTypeLabel = QtGui.QLabel(TemplateSelector)
        self.templateTypeLabel.setObjectName(_fromUtf8("templateTypeLabel"))
        self.gridLayout.addWidget(self.templateTypeLabel, 0, 0, 1, 1)
        self.sizeLabel = QtGui.QLabel(TemplateSelector)
        self.sizeLabel.setObjectName(_fromUtf8("sizeLabel"))
        self.gridLayout.addWidget(self.sizeLabel, 2, 0, 1, 1)
        self.sizeComboBox = QtGui.QComboBox(TemplateSelector)
        self.sizeComboBox.setObjectName(_fromUtf8("sizeComboBox"))
        self.gridLayout.addWidget(self.sizeComboBox, 2, 1, 1, 2)
        self.orientationLabel = QtGui.QLabel(TemplateSelector)
        self.orientationLabel.setObjectName(_fromUtf8("orientationLabel"))
        self.gridLayout.addWidget(self.orientationLabel, 2, 3, 1, 1)
        self.orientationComboBox = QtGui.QComboBox(TemplateSelector)
        self.orientationComboBox.setObjectName(_fromUtf8("orientationComboBox"))
        self.gridLayout.addWidget(self.orientationComboBox, 2, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)

        self.retranslateUi(TemplateSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TemplateSelector.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TemplateSelector.openTemplate)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("helpRequested()")), TemplateSelector.loadHelpPage)
        QtCore.QObject.connect(self.templateTypeComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), TemplateSelector.onTemplateTypeChanged)
        QtCore.QObject.connect(self.sizeComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), TemplateSelector.onPaperSizeChanged)
        QtCore.QObject.connect(self.orientationComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), TemplateSelector.onPaperOrientationChanged)
        QtCore.QMetaObject.connectSlotsByName(TemplateSelector)
        TemplateSelector.setTabOrder(self.titleLineEdit, self.sizeComboBox)
        TemplateSelector.setTabOrder(self.sizeComboBox, self.orientationComboBox)
        TemplateSelector.setTabOrder(self.orientationComboBox, self.suitableForComboBox)
        TemplateSelector.setTabOrder(self.suitableForComboBox, self.copyrightComboBox)
        TemplateSelector.setTabOrder(self.copyrightComboBox, self.buttonBox)

    def retranslateUi(self, TemplateSelector):
        TemplateSelector.setWindowTitle(_translate("TemplateSelector", "Open Template", None))
        self.mapScalesGroupBox.setTitle(_translate("TemplateSelector", "Composer Map Scale(s)", None))
        self.suitableForLabel.setText(_translate("TemplateSelector", "Suitable for", None))
        self.copyrightLabel.setText(_translate("TemplateSelector", "Copyright", None))
        self.suitableForComboBox.setItemText(0, _translate("TemplateSelector", "Paper (High res, 300 dpi)", None))
        self.suitableForComboBox.setItemText(1, _translate("TemplateSelector", "Electronic (Low res, 96 dpi)", None))
        self.titleLabel.setText(_translate("TemplateSelector", "Title", None))
        self.templateTypeLabel.setText(_translate("TemplateSelector", "Template Type", None))
        self.sizeLabel.setText(_translate("TemplateSelector", "Size", None))
        self.orientationLabel.setText(_translate("TemplateSelector", "Orientation", None))

