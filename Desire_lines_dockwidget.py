# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DesirelinesDockWidget
                                 A QGIS plugin
 Create the desire lines from a space Syntax accessibility analysis
                             -------------------
        begin                : 2018-02-28
        git sha              : $Format:%H$
        copyright            : (C) 2018 by AA/Space Syntax Limited
        email                : a.acharya@spacesyntax.com
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

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from . import utility_functions as uf
from qgis.core import *
import processing



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Desire_lines_dockwidget_base.ui'))


class DesirelinesDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(DesirelinesDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.legend = self.iface.legendInterface()
        self.plugin_path = os.path.dirname(__file__)


        self.selectextent = self.pushButton_5
        self.create = self.pushButton_2
        self.selectLayer = self.comboBox
        self.firstMeasure = self.comboBox_2
        self.firstCheck = self.checkBox
        self.firstSpinBox = self.doubleSpinBox
        self.secondMeasure = self.comboBox_3
        self.secondCheck = self.checkBox_2
        self.secondSpinBox = self.doubleSpinBox_2
        self.applyThreshold = self.pushButton
        self.savelocationText = self.lineEdit
        self.saveLocation = self.pushButton_3
        self.rdbuttonAND = self.radioButtonAND
        self.rdbuttonOR = self.radioButtonOR
        self.selectedExtentLayer = self.comboBox_4
        self.createDesireLines = self.pushButton_4
        self.firstperc = self.radioButtonPer1
        self.firstabs = self.radioButtonAbs1
        self.secondperc = self.radioButtonPer2
        self.secondabs = self.radioButtonAbs2

        self.updateLayer()
        self.updateFilterLayer()
        self.initialisations()
        self.firstButtonsActivate()

        QgsMapLayerRegistry.instance().legendLayersAdded.connect(self.updateLayer)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.updateLayer)
        QgsMapLayerRegistry.instance().legendLayersAdded.connect(self.updateFilterLayer)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.updateFilterLayer)
        QgsMapLayerRegistry.instance().legendLayersAdded.connect(self.initialisations)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.initialisations)
        QgsMapLayerRegistry.instance().legendLayersAdded.connect(self.firstButtonsActivate)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.firstButtonsActivate)

        self.selectextent.clicked.connect(self.selectByRadius)
        self.firstCheck.stateChanged.connect(self.updateChoiceColumn1)
        self.secondCheck.stateChanged.connect(self.updateChoiceColumn2)
        self.selectLayer.currentIndexChanged.connect(self.refreshfirstCheck1)
        self.selectLayer.currentIndexChanged.connect(self.refreshfirstCheck2)
        self.create.clicked.connect(self.layerCreate)
        self.applyThreshold.clicked.connect(self.layerFilter)
        self.rdbuttonAND.toggled.connect(self.activateSecondMeasure)
        self.rdbuttonOR.toggled.connect(self.activateSecondMeasure)
        self.firstCheck.stateChanged.connect(self.otherButtonsActivate)
        self.createDesireLines.clicked.connect(self.saveSelectedFeatures)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
        QgsMapLayerRegistry.instance().legendLayersAdded.disconnect(self.updateLayer)
        QgsMapLayerRegistry.instance().layersRemoved.disconnect(self.updateLayer)
        QgsMapLayerRegistry.instance().legendLayersAdded.disconnect(self.updateFilterLayer)
        QgsMapLayerRegistry.instance().layersRemoved.disconnect(self.updateFilterLayer)
        QgsMapLayerRegistry.instance().legendLayersAdded.disconnect(self.initialisations)
        QgsMapLayerRegistry.instance().layersRemoved.disconnect(self.initialisations)
        self.firstCheck.stateChanged.disconnect(self.updateChoiceColumn1)
        self.secondCheck.stateChanged.disconnect(self.updateChoiceColumn2)
        self.selectLayer.currentIndexChanged.disconnect(self.refreshfirstCheck1)
        self.selectLayer.currentIndexChanged.disconnect(self.refreshfirstCheck2)
        self.firstCheck.stateChanged.disconnect(self.otherButtonsActivate)

    def initialisations(self):
        self.selectLayer.setEnabled(False)
        self.firstMeasure.setEnabled(False)
        self.firstCheck.setEnabled(False)
        self.firstSpinBox.setEnabled(False)
        self.secondMeasure.setEnabled(False)
        self.secondCheck.setEnabled(False)
        self.secondSpinBox.setEnabled(False)
        self.applyThreshold.setEnabled(False)
        self.savelocationText.setEnabled(True)
        self.saveLocation.setEnabled(True)
        self.selectedExtentLayer.setEnabled(True)
        self.rdbuttonAND.setEnabled(False)
        self.rdbuttonOR.setEnabled(False)
        self.selectextent.setEnabled(True)
        self.create.setEnabled(True)
        self.selectLayer.setEnabled(True)
        self.firstperc.setEnabled(False)
        self.firstabs.setEnabled(False)
        self.secondperc.setEnabled(False)
        self.secondabs.setEnabled(False)

    def firstButtonsActivate(self):
        if self.selectedExtentLayer.count() > 0:
            self.firstCheck.setEnabled(True)

    def otherButtonsActivate(self):
        if self.firstCheck.isChecked():
            self.firstSpinBox.setEnabled(True)
            self.firstMeasure.setEnabled(True)
            self.rdbuttonAND.setEnabled(True)
            self.rdbuttonOR.setEnabled(True)
            self.applyThreshold.setEnabled(True)
            self.firstperc.setEnabled(True)
            self.firstabs.setEnabled(True)

        else:
            self.firstSpinBox.setEnabled(False)
            self.firstMeasure.setEnabled(False)
            self.rdbuttonAND.setEnabled(False)
            self.rdbuttonOR.setEnabled(False)
            self.applyThreshold.setEnabled(False)
            self.firstperc.setEnabled(False)
            self.firstabs.setEnabled(False)


    def activateSecondMeasure(self):
        if self.rdbuttonAND.isChecked() or self.rdbuttonOR.isChecked():
            self.secondMeasure.setEnabled(True)
            self.secondCheck.setEnabled(True)
            self.secondSpinBox.setEnabled(True)
            self.secondperc.setEnabled(True)
            self.secondabs.setEnabled(True)

        else:
            self.secondMeasure.setEnabled(False)
            self.secondCheck.setEnabled(False)
            self.secondSpinBox.setEnabled(False)
            self.secondperc.setEnabled(False)
            self.secondabs.setEnabled(False)


    def setLayer(self):
        # get the new layer
        index = self.selectLayer.currentIndex()
        self.selectedLayer = self.selectLayer.itemData(index)
        return self.selectedLayer

    def setFilterLayer(self):
        # get the new layer
        index = self.selectedExtentLayer.currentIndex()
        self.selectedFilterLayer = self.selectLayer.itemData(index)
        return self.selectedFilterLayer


    # Add  layer to combobox if conditions are satisfied
    def updateLayer(self):
        self.selectLayer.clear()
        self.selectLayer.setEnabled(False)
        layers = self.legend.layers()
        type=1
        for lyr in layers:
            if uf.isRequiredLayer(self.iface, lyr, type):
                self.selectLayer.addItem(lyr.name(), lyr)

        if self.selectLayer.count() > 0:
            self.selectLayer.setEnabled(True)
            self.layer = self.setLayer()

            # Add  layer to combobox if conditions are satisfied

    def updateFilterLayer(self):
        self.selectedExtentLayer.clear()
        self.selectedExtentLayer.setEnabled(False)
        layers = self.legend.layers()
        type = 1
        for lyr in layers:
            if uf.isRequiredLayer(self.iface, lyr, type):
                self.selectedExtentLayer.addItem(lyr.name(), lyr)

        if self.selectedExtentLayer.count() > 0:
            self.selectedExtentLayer.setEnabled(True)
            self.layer = self.setFilterLayer()


    def selectByRadius(self):
        if self.selectLayer.count() > 0:
            self.selectextent.setEnabled(True)
            self.iface.actionSelectRadius().trigger()

    def updateChoiceColumn1(self):
        layer = self.setFilterLayer()
        fields = layer.pendingFields()

        if self.firstCheck.isChecked():
            self.firstMeasure.setEnabled(True)
            for field in fields:
                self.firstMeasure.addItem(field.name(), field)

    def updateChoiceColumn2(self):
        layer = self.setFilterLayer()
        fields = layer.pendingFields()

        if self.secondCheck.isChecked():
            self.secondMeasure.setEnabled(True)
            for field in fields:
                self.secondMeasure.addItem(field.name(), field)

    def refreshfirstCheck1(self):
        self.firstCheck.setChecked(0)

    def refreshfirstCheck2(self):
        self.secondMeasure.clear()
        self.secondCheck.setChecked(0)


    def layerCreate(self):
        layer = self.setLayer()
        selectedLines = processing.runalg('qgis:saveselectedfeatures', layer, None)
        filename = os.path.basename(selectedLines['OUTPUT_LAYER'])
        location = os.path.abspath(selectedLines['OUTPUT_LAYER'])
        resultLayer = self.iface.addVectorLayer(location, filename, "ogr")
        resultLayer.setLayerName("memory:Selected Extent")
        qml_path = self.plugin_path + "/styles/Extent.qml"
        resultLayer.loadNamedStyle(qml_path)
        layer.removeSelection()
        self.canvas.refresh()



    def layerFilter(self):
        firstfieldname = self.firstMeasure.currentText()
        secondfieldname = self.secondMeasure.currentText()

        filterlayer = self.setFilterLayer()

        idx1 = filterlayer.fieldNameIndex(firstfieldname)
        self.maxFieldValue1 = filterlayer.maximumValue(idx1)


        idx2 = filterlayer.fieldNameIndex(secondfieldname)
        maxFieldValue2 = filterlayer.maximumValue(idx2)


        if self.firstperc.isChecked():
            self.firstfieldvalue = (self.firstSpinBox.value()/100.00)*self.maxFieldValue1

        if self.firstabs.isChecked():
            self.firstfieldvalue = self.firstSpinBox.value()

        if self.secondperc.isChecked():
            secondfieldvalue = (self.secondSpinBox.value()/100.00)*maxFieldValue2

        if self.secondabs.isChecked():
            secondfieldvalue = self.secondSpinBox.value()


        if self.firstCheck.checkState() == 2 and self.secondCheck.checkState() == 2:
            if self.rdbuttonAND.isChecked():
                expr = QgsExpression("\"{}\">{} AND \"{}\">{}".format(firstfieldname, self.firstfieldvalue, secondfieldname, secondfieldvalue))
                selection = filterlayer.getFeatures(QgsFeatureRequest(expr))
                ids = [s.id() for s in selection]
                filterlayer.setSelectedFeatures(ids)
                print expr.dump()

            if self.rdbuttonOR.isChecked():
                expr = QgsExpression("\"{}\">{} OR \"{}\">{}".format(firstfieldname, self.firstfieldvalue, secondfieldname, secondfieldvalue))
                selection = filterlayer.getFeatures(QgsFeatureRequest(expr))
                ids = [s.id() for s in selection]
                filterlayer.setSelectedFeatures(ids)
                print expr.dump()


        if self.firstCheck.checkState() == 2 and self.secondCheck.checkState() == 0:
            expr = QgsExpression("\"{}\">{}".format(firstfieldname, self.firstfieldvalue))
            selection = filterlayer.getFeatures(QgsFeatureRequest(expr))
            ids = [s.id() for s in selection]
            filterlayer.setSelectedFeatures(ids)
            print expr.dump()



    def saveSelectedFeatures(self):
        filterlayer = self.setFilterLayer()
        firstfieldname = self.firstMeasure.currentText()


        selectedLines = processing.runalg('qgis:saveselectedfeatures', filterlayer, None)
        filename = os.path.basename(selectedLines['OUTPUT_LAYER'])
        location = os.path.abspath(selectedLines['OUTPUT_LAYER'])
        resultLayer = self.iface.addVectorLayer(location, filename, "ogr")
        resultLayer.setLayerName("memory:Desire Lines")
        #qml_path = self.plugin_path + "/styles/Legends.qml"
        #resultLayer.loadNamedStyle(qml_path)

        uf.applySymbologyFixedDivisions(resultLayer,firstfieldname,self.firstfieldvalue,self.maxFieldValue1)































