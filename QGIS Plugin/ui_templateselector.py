# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_templateselector.ui'
#
# Created: Fri Jan 31 16:47:03 2014
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
        TemplateSelector.resize(323, 262)
        TemplateSelector.setModal(True)
        self.gridLayout = QtGui.QGridLayout(TemplateSelector)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.titleLabel = QtGui.QLabel(TemplateSelector)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.titleLineEdit = QtGui.QLineEdit(TemplateSelector)
        self.titleLineEdit.setObjectName(_fromUtf8("titleLineEdit"))
        self.gridLayout.addWidget(self.titleLineEdit, 0, 1, 1, 2)
        self.sizeLabel = QtGui.QLabel(TemplateSelector)
        self.sizeLabel.setObjectName(_fromUtf8("sizeLabel"))
        self.gridLayout.addWidget(self.sizeLabel, 1, 0, 1, 1)
        self.sizeComboBox = QtGui.QComboBox(TemplateSelector)
        self.sizeComboBox.setObjectName(_fromUtf8("sizeComboBox"))
        self.sizeComboBox.addItem(_fromUtf8(""))
        self.sizeComboBox.addItem(_fromUtf8(""))
        self.sizeComboBox.addItem(_fromUtf8(""))
        self.sizeComboBox.addItem(_fromUtf8(""))
        self.sizeComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.sizeComboBox, 1, 1, 1, 2)
        self.orientationLabel = QtGui.QLabel(TemplateSelector)
        self.orientationLabel.setObjectName(_fromUtf8("orientationLabel"))
        self.gridLayout.addWidget(self.orientationLabel, 2, 0, 1, 1)
        self.orientationComboBox = QtGui.QComboBox(TemplateSelector)
        self.orientationComboBox.setObjectName(_fromUtf8("orientationComboBox"))
        self.orientationComboBox.addItem(_fromUtf8(""))
        self.orientationComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.orientationComboBox, 2, 1, 1, 2)
        self.scaleLabel = QtGui.QLabel(TemplateSelector)
        self.scaleLabel.setObjectName(_fromUtf8("scaleLabel"))
        self.gridLayout.addWidget(self.scaleLabel, 3, 0, 1, 1)
        self.scaleLineEdit = QtGui.QLineEdit(TemplateSelector)
        self.scaleLineEdit.setObjectName(_fromUtf8("scaleLineEdit"))
        self.gridLayout.addWidget(self.scaleLineEdit, 3, 1, 1, 1)
        self.scaleComboBox = QtGui.QComboBox(TemplateSelector)
        self.scaleComboBox.setObjectName(_fromUtf8("scaleComboBox"))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.scaleComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.scaleComboBox, 3, 2, 1, 1)
        self.suitableForLabel = QtGui.QLabel(TemplateSelector)
        self.suitableForLabel.setObjectName(_fromUtf8("suitableForLabel"))
        self.gridLayout.addWidget(self.suitableForLabel, 4, 0, 1, 1)
        self.suitableForComboBox = QtGui.QComboBox(TemplateSelector)
        self.suitableForComboBox.setObjectName(_fromUtf8("suitableForComboBox"))
        self.suitableForComboBox.addItem(_fromUtf8(""))
        self.suitableForComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.suitableForComboBox, 4, 1, 1, 2)
        self.copyrightLabel = QtGui.QLabel(TemplateSelector)
        self.copyrightLabel.setObjectName(_fromUtf8("copyrightLabel"))
        self.gridLayout.addWidget(self.copyrightLabel, 5, 0, 1, 1)
        self.copyrightComboBox = QtGui.QComboBox(TemplateSelector)
        self.copyrightComboBox.setObjectName(_fromUtf8("copyrightComboBox"))
        self.gridLayout.addWidget(self.copyrightComboBox, 5, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(TemplateSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Help|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)

        self.retranslateUi(TemplateSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TemplateSelector.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TemplateSelector.openTemplate)
        QtCore.QObject.connect(self.scaleComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), TemplateSelector.updateScaleText)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("helpRequested()")), TemplateSelector.loadHelpPage)
        QtCore.QMetaObject.connectSlotsByName(TemplateSelector)
        TemplateSelector.setTabOrder(self.titleLineEdit, self.sizeComboBox)
        TemplateSelector.setTabOrder(self.sizeComboBox, self.orientationComboBox)
        TemplateSelector.setTabOrder(self.orientationComboBox, self.scaleLineEdit)
        TemplateSelector.setTabOrder(self.scaleLineEdit, self.scaleComboBox)
        TemplateSelector.setTabOrder(self.scaleComboBox, self.suitableForComboBox)
        TemplateSelector.setTabOrder(self.suitableForComboBox, self.copyrightComboBox)
        TemplateSelector.setTabOrder(self.copyrightComboBox, self.buttonBox)

    def retranslateUi(self, TemplateSelector):
        TemplateSelector.setWindowTitle(_translate("TemplateSelector", "Open Template", None))
        self.titleLabel.setText(_translate("TemplateSelector", "Title", None))
        self.sizeLabel.setText(_translate("TemplateSelector", "Size", None))
        self.sizeComboBox.setItemText(0, _translate("TemplateSelector", "A4", None))
        self.sizeComboBox.setItemText(1, _translate("TemplateSelector", "A3", None))
        self.sizeComboBox.setItemText(2, _translate("TemplateSelector", "A2", None))
        self.sizeComboBox.setItemText(3, _translate("TemplateSelector", "A1", None))
        self.sizeComboBox.setItemText(4, _translate("TemplateSelector", "A0", None))
        self.orientationLabel.setText(_translate("TemplateSelector", "Orientation", None))
        self.orientationComboBox.setItemText(0, _translate("TemplateSelector", "Portrait", None))
        self.orientationComboBox.setItemText(1, _translate("TemplateSelector", "Landscape", None))
        self.scaleLabel.setText(_translate("TemplateSelector", "Scale 1 : ", None))
        self.scaleLineEdit.setText(_translate("TemplateSelector", "200", None))
        self.scaleComboBox.setItemText(0, _translate("TemplateSelector", "1 : 200", None))
        self.scaleComboBox.setItemText(1, _translate("TemplateSelector", "1 : 500", None))
        self.scaleComboBox.setItemText(2, _translate("TemplateSelector", "1 : 1,000", None))
        self.scaleComboBox.setItemText(3, _translate("TemplateSelector", "1 : 1,250", None))
        self.scaleComboBox.setItemText(4, _translate("TemplateSelector", "1 : 2,500", None))
        self.scaleComboBox.setItemText(5, _translate("TemplateSelector", "1 : 5,000", None))
        self.scaleComboBox.setItemText(6, _translate("TemplateSelector", "1 : 10,000", None))
        self.scaleComboBox.setItemText(7, _translate("TemplateSelector", "1 : 25,000", None))
        self.scaleComboBox.setItemText(8, _translate("TemplateSelector", "1 : 50,000", None))
        self.scaleComboBox.setItemText(9, _translate("TemplateSelector", "1 : 100,000", None))
        self.suitableForLabel.setText(_translate("TemplateSelector", "Suitable for", None))
        self.suitableForComboBox.setItemText(0, _translate("TemplateSelector", "Paper (High res, 300 dpi)", None))
        self.suitableForComboBox.setItemText(1, _translate("TemplateSelector", "Electronic (Low res, 96 dpi)", None))
        self.copyrightLabel.setText(_translate("TemplateSelector", "Copyright", None))

