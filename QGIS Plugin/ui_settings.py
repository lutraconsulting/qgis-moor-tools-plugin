# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settings.ui'
#
# Created: Tue Dec 12 09:20:31 2017
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(428, 156)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.projectsFolderLabel = QtGui.QLabel(Dialog)
        self.projectsFolderLabel.setObjectName(_fromUtf8("projectsFolderLabel"))
        self.gridLayout.addWidget(self.projectsFolderLabel, 0, 0, 1, 1)
        self.projectsFolderLineEdit = QtGui.QLineEdit(Dialog)
        self.projectsFolderLineEdit.setObjectName(_fromUtf8("projectsFolderLineEdit"))
        self.gridLayout.addWidget(self.projectsFolderLineEdit, 0, 1, 1, 1)
        self.templateRootPushButton = QtGui.QPushButton(Dialog)
        self.templateRootPushButton.setObjectName(_fromUtf8("templateRootPushButton"))
        self.gridLayout.addWidget(self.templateRootPushButton, 1, 2, 1, 1)
        self.projectsFolderPushButton = QtGui.QPushButton(Dialog)
        self.projectsFolderPushButton.setObjectName(_fromUtf8("projectsFolderPushButton"))
        self.gridLayout.addWidget(self.projectsFolderPushButton, 0, 2, 1, 1)
        self.templateRootLineEdit = QtGui.QLineEdit(Dialog)
        self.templateRootLineEdit.setObjectName(_fromUtf8("templateRootLineEdit"))
        self.gridLayout.addWidget(self.templateRootLineEdit, 1, 1, 1, 1)
        self.templateRootLabel = QtGui.QLabel(Dialog)
        self.templateRootLabel.setObjectName(_fromUtf8("templateRootLabel"))
        self.gridLayout.addWidget(self.templateRootLabel, 1, 0, 1, 1)
        self.projectSelectorEnabledCheckBox = QtGui.QCheckBox(Dialog)
        self.projectSelectorEnabledCheckBox.setChecked(True)
        self.projectSelectorEnabledCheckBox.setTristate(False)
        self.projectSelectorEnabledCheckBox.setObjectName(_fromUtf8("projectSelectorEnabledCheckBox"))
        self.gridLayout.addWidget(self.projectSelectorEnabledCheckBox, 2, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.templateRootPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.browseForTemplateRoot)
        QtCore.QObject.connect(self.projectsFolderPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.browseForProjectRoot)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Moor Tools Settings", None))
        self.projectsFolderLabel.setText(_translate("Dialog", "Projects Folder", None))
        self.templateRootPushButton.setText(_translate("Dialog", "Browse", None))
        self.projectsFolderPushButton.setText(_translate("Dialog", "Browse", None))
        self.templateRootLabel.setText(_translate("Dialog", "Folder Containing Templates", None))
        self.projectSelectorEnabledCheckBox.setText(_translate("Dialog", "Show project selector on QGIS startup", None))

