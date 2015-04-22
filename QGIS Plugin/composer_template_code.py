""" myComposition = QgsComposition(CANVAS.mapRenderer())
mySubstitutionMap = {'replace-me': myText }
myFile = os.path.join(TEST_DATA_DIR, 'template-for-substitution.qpt')
myTemplateFile = file(myFile, 'rt')
myTemplateContent = myTemplateFile.read()
myTemplateFile.close()
myDocument = QDomDocument()
myDocument.setContent(myTemplateContent)
myComposition.loadFromTemplate(myDocument, mySubstitutionMap) """

import os
from PyQt4 import QtXml

testComposer = iface.createNewComposer("test Comp")
comp = QgsComposition(iface.mapCanvas().mapRenderer())

replaceMap = { 'title' : 'Fancy title',
               'username' : os.environ['username'] }
templateFilePath = r'Q:\QGIS\Templates\A4Ltest.qpt'
templateFile = open(templateFilePath, 'r')
fileContent = templateFile.read()
templateFile.close()
doc = QtXml.QDomDocument()
doc.setContent(fileContent)

comp.loadFromTemplate(doc, replaceMap, True)
testComposer.setComposition(comp)

testComposer.composition().getComposerMapById(0).updateCachedImage()
