# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_projectselector.ui'
#
# Created: Wed Nov 25 15:28:52 2015
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

class Ui_ProjectSelector(object):
    def setupUi(self, ProjectSelector):
        ProjectSelector.setObjectName(_fromUtf8("ProjectSelector"))
        ProjectSelector.setWindowModality(QtCore.Qt.ApplicationModal)
        ProjectSelector.resize(470, 285)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProjectSelector.sizePolicy().hasHeightForWidth())
        ProjectSelector.setSizePolicy(sizePolicy)
        ProjectSelector.setModal(True)
        self.gridLayout = QtGui.QGridLayout(ProjectSelector)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(ProjectSelector)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.projectGroupComboBox = QtGui.QComboBox(ProjectSelector)
        self.projectGroupComboBox.setObjectName(_fromUtf8("projectGroupComboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.projectGroupComboBox)
        self.label_2 = QtGui.QLabel(ProjectSelector)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.selectedProjectListWidget = QtGui.QListWidget(ProjectSelector)
        self.selectedProjectListWidget.setObjectName(_fromUtf8("selectedProjectListWidget"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.selectedProjectListWidget)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProjectSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ProjectSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProjectSelector.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProjectSelector.loadProject)
        QtCore.QObject.connect(self.projectGroupComboBox, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), ProjectSelector.onProjectGroupChanged)
        QtCore.QMetaObject.connectSlotsByName(ProjectSelector)
        ProjectSelector.setTabOrder(self.projectGroupComboBox, self.buttonBox)

    def retranslateUi(self, ProjectSelector):
        ProjectSelector.setWindowTitle(_translate("ProjectSelector", "Select Project", None))
        self.label.setText(_translate("ProjectSelector", "Project Groups", None))
        self.label_2.setText(_translate("ProjectSelector", "Selected Project", None))

