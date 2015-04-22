# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_projectselector.ui'
#
# Created: Wed Dec 04 14:18:29 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ProjectSelector(object):
    def setupUi(self, ProjectSelector):
        ProjectSelector.setObjectName(_fromUtf8("ProjectSelector"))
        ProjectSelector.setWindowModality(QtCore.Qt.ApplicationModal)
        ProjectSelector.resize(178, 84)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProjectSelector.sizePolicy().hasHeightForWidth())
        ProjectSelector.setSizePolicy(sizePolicy)
        ProjectSelector.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ProjectSelector)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(ProjectSelector)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProjectSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ProjectSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProjectSelector.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProjectSelector.loadProject)
        QtCore.QMetaObject.connectSlotsByName(ProjectSelector)

    def retranslateUi(self, ProjectSelector):
        ProjectSelector.setWindowTitle(QtGui.QApplication.translate("ProjectSelector", "Select Project", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ProjectSelector", "Available Projects", None, QtGui.QApplication.UnicodeUTF8))

