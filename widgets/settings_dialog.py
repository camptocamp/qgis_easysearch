# -*- coding: utf-8 -*-
#/***************************************************************************
# Easy Search
#
# Easy search features base on predefined layer and attribute
#
#                             -------------------
#        begin                : 2014-03-03
#        copyright            : (C) 2014 by Camptocamp SA
#        email                : info@camptocamp.com
# ***************************************************************************/
#
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

from easysearch.ui.ui_settings_dialog import Ui_settingsDialog

from PyQt4.QtCore import QSettings, QVariant
from PyQt4.QtGui import QDialog
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer


class SettingsDialog(QDialog, Ui_settingsDialog):

    settings = None
    layerId = None
    fieldName = None

    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.settings = QSettings()
        self.layerId = self.settings.value('EasySearch/layerId')
        self.fieldName = self.settings.value('EasySearch/fieldName')

        self.layerCombo_init()

    def layerCombo_init(self):

        self.layerCombo.clear()

        layers = QgsMapLayerRegistry.instance().mapLayers()
        for layerId, layer in layers.iteritems():
            if isinstance(layer, QgsVectorLayer):
                self.layerCombo.addItem(layer.name(), layer)
                if layerId == self.layerId:
                    self.layerCombo.setCurrentIndex(self.layerCombo.count() - 1)
                    self.fieldCombo_init()

        if not self.layerId:
            self.layerCombo.setCurrentIndex(-1)
            self.fieldCombo_init()

        self.layerCombo.currentIndexChanged.connect(
                self.layerCombo_currentIndexChanged)

    def layerCombo_currentIndexChanged(self, index):
        self.fieldCombo_init()

    def layerCombo_layer(self):
        if (self.layerCombo.currentIndex()) == -1:
            return None
        return self.layerCombo.itemData(self.layerCombo.currentIndex())

    def layerCombo_layerId(self):
        layer = self.layerCombo_layer()
        if not layer:
            return None
        return layer.id()

    def fieldCombo_init(self):

        self.fieldCombo.clear()

        layer = self.layerCombo_layer()
        if not layer:
            return

        fieldIndex = None
        fields = layer.dataProvider().fields()
        for field in fields:
            if field.type() in [QVariant.String]:
                fieldName = field.name()
                self.fieldCombo.addItem(fieldName, field)
                if fieldName == self.fieldName:
                    self.fieldCombo.setCurrentIndex(self.fieldCombo.count() - 1)
                    fieldIndex = fields.indexFromName(fieldName)

        if fieldIndex is None:
            self.fieldCombo.setCurrentIndex(-1)

        self.fieldCombo.currentIndexChanged.connect(
            self.fieldCombo_currentIndexChanged)

    def fieldCombo_currentIndexChanged(self, index):
        self.fieldName = self.fieldCombo_fieldName()

    def fieldCombo_field(self):
        if (self.fieldCombo.currentIndex()) == -1:
            return None
        return self.fieldCombo.itemData(self.fieldCombo.currentIndex())

    def fieldCombo_fieldName(self):
        field = self.fieldCombo_field()
        if not field:
            return None
        return field.name()

    def accept(self, *args, **kwargs):
        self.settings.setValue('EasySearch/layerId',
                               self.layerCombo_layerId())
        self.settings.setValue('EasySearch/fieldName',
                               self.fieldCombo_fieldName())
        self.settings.sync()

        return QDialog.accept(self, *args, **kwargs)
