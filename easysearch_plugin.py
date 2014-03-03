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

import os.path
import unicodedata

from PyQt4.QtCore import QObject, QSettings, QTranslator, QCoreApplication, qVersion
from PyQt4.QtGui import QAction, QIcon, QLineEdit

from qgis.core import QgsMapLayerRegistry, QgsFeatureRequest, QgsFeature
from qgis.gui import QgsMessageBar

from easysearch.ui import resources_rc
from easysearch.widgets.settings_dialog import SettingsDialog


def remove_accents(data):
    # http://www.unicode.org/reports/tr44/#GC_Values_Table
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if unicodedata.category(x)[0] in ('L', 'N', 'P', 'Zs')).lower()

class EasySearch(QObject):

    name = ""
    actions = {}
    toolbar = None
    searchText = None
    layer = None

    def __init__(self, iface):
        """Constructor for the plugin.

        :param iface: A QGisAppInterface instance we use to access QGIS via.
        :type iface: QgsAppInterface
        """
        super(EasySearch, self).__init__()

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'easysearch_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.name = self.tr(u"Easy Search")

    def initGui(self):
        self.actions['showSettings'] = QAction(
            QIcon(":/plugins/easysearch/flaticon/gears2.svg"),
            self.tr(u"&Settings"),
            self.iface.mainWindow())
        self.actions['showSettings'].triggered.connect(self.showSettings)
        self.iface.addPluginToMenu(u"&{}".format(self.name), self.actions['showSettings'])

        #self.iface.addToolBarIcon(self.actions['show_settings'])

        self.toolbar_init()

    def unload(self):
        self.iface.removePluginMenu(u"&{}".format(self.name), self.actions['showSettings'])
        #self.iface.removeToolBarIcon(self.action)
        if self.toolbar:
            self.toolbar.deleteLater()
            self.toolbar = None

    def toolbar_init(self):
        """setup the plugin toolbar."""
        self.toolbar = self.iface.addToolBar(self.name)
        self.toolbar.setObjectName('mEasySearchToolBar')

        self.searchText = QLineEdit(self.toolbar)
        self.searchText.returnPressed.connect(self.search)
        self.actions['searchText'] = self.toolbar.addWidget(self.searchText)
        self.actions['searchText'].setVisible(True);

        self.actions['searchButton'] = QAction(
            QIcon(":/plugins/easysearch/flaticon/magnifier13.svg"),
            self.tr("Search"),
            self.toolbar)
        self.actions['searchButton'].triggered.connect(self.search)
        self.toolbar.addAction(self.actions['searchButton'])

        self.toolbar.setVisible(True)

    def search(self):
        settings = QSettings()
        layerId = settings.value('EasySearch/layerId')
        fieldName = settings.value('EasySearch/fieldName')
        pattern = self.searchText.text()

        self.layer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        if self.layer is None:
            self.iface.messageBar().pushMessage(self.name,
                self.tr("Choose a layer first in settings dialog."),
                QgsMessageBar.WARNING, 3)
            return

        if fieldName == "":
            self.iface.messageBar().pushMessage(self.name,
                self.tr("Choose a field first in settings dialog."),
                QgsMessageBar.WARNING, 3)
            return
        fields = self.layer.dataProvider().fields()
        fieldIndex = fields.indexFromName(fieldName)

        # create feature request
        featReq = QgsFeatureRequest()
        featReq.setFlags(QgsFeatureRequest.NoGeometry)
        featReq.setSubsetOfAttributes([fieldIndex])
        iterator = self.layer.getFeatures(featReq)

        # process
        f = QgsFeature()
        results = []
        self.continueSearch = True
        while iterator.nextFeature(f) and self.continueSearch:
            if self.evaluate(f[fieldName], pattern):
                results.append(f.id())
            QCoreApplication.processEvents()

        # process results
        if self.continueSearch:
            self.iface.messageBar().pushMessage(self.name,
                self.tr("{} features found").format(len(results)),
                QgsMessageBar.INFO, 2)

            self.processResults(results)

    def evaluate(self, v1, v2):
        try:
            remove_accents(unicode(v1)).index(remove_accents(v2))
            return True
        except ValueError:
            return False

    def processResults(self, results):
        if self.layer is None:
            return

        self.layer.setSelectedFeatures(results)
        if len(results) == 0:
            return

        canvas = self.iface.mapCanvas()
        rect = canvas.mapRenderer().layerExtentToOutputExtent(self.layer, self.layer.boundingBoxOfSelected())
        if rect is not None:
            rect.scale(1.5)
            canvas.setExtent(rect)

        canvas.refresh()

    def showSettings(self):
        dlg = SettingsDialog()
        dlg.exec_()
