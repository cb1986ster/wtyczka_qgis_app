# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WtyczkaAPP
                                 A QGIS plugin
 Wtyczka QGIS wspomagająca przygotowanie aktów planowania przestrzennego zgodnych z rozporządzeniem Ministra Rozwoju.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-05-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by EnviroSolutions Sp. z o.o.
        email                : office@envirosolutions.pl
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
import atexit

from PyQt5.QtWidgets import QDialog, QFileDialog

from qgis.PyQt import QtGui
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QToolButton, QMenu, QMessageBox, QTableWidgetItem
#from qgis.core import QgsVectorLayer
from qgis.PyQt import QtWidgets
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .modules.app import PytanieAppDialog, ZbiorPrzygotowanieDialog, RasterInstrukcjaDialog, RasterFormularzDialog, WektorFormularzDialog, DokumentyFormularzDialog, WektorInstrukcjaDialog, GenerowanieGMLDialog
from .modules.metadata import MetadaneDialog
from .modules.validator import WalidacjaDialog

import os

PLUGIN_NAME = 'Wtyczka APP'
PLUGIN_VERSION = '0.1'
title_question ='Praca z APP / zbiorem APP'
title_app = 'Praca z APP'
title_set = 'Tworzenie zbioru APP'
title_metadata = 'Tworzenie / aktualizacja metadanych'
title_validator = 'Walidacja GML / XML'
title_settings = 'Ustawienia'


class WtyczkaAPP:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.activeDlg = None
        self.prevDlg = None
        # Declare instance attributes
        self.actions = []
        self.listaOkienek = []
        icon_path = ':/plugins/wtyczka_app/img/'
        icon_app = 'praca_z_app.png'
        icon_metadata = 'tworzenie.png'
        icon_validator = 'walidacja.png'
        icon_setting = 'ustawienia.png'
        self.listaPlikow = []


        # region okna moduł app
        self.pytanieAppDialog = PytanieAppDialog()
        self.pytanieAppDialog.setWindowTitle('%s' % (title_question))
        self.pytanieAppDialog.setWindowIcon(QtGui.QIcon(':/plugins/wtyczka_app/img/logo.png'))
        self.pytanieAppDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.zbiorPrzygotowanieDialog = ZbiorPrzygotowanieDialog()
        self.zbiorPrzygotowanieDialog.setWindowTitle('%s' % (title_set))
        self.zbiorPrzygotowanieDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.zbiorPrzygotowanieDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.rasterInstrukcjaDialog = RasterInstrukcjaDialog()
        self.rasterInstrukcjaDialog.setWindowTitle('%s (krok 1 z 6)' % (title_app))
        self.rasterInstrukcjaDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.rasterInstrukcjaDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.rasterFormularzDialog = RasterFormularzDialog()
        self.rasterFormularzDialog.setWindowTitle('%s (krok 2 z 6)' % (title_app))
        self.rasterFormularzDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.rasterFormularzDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.wektorInstrukcjaDialog = WektorInstrukcjaDialog()
        self.wektorInstrukcjaDialog.setWindowTitle('%s (krok 3 z 6)' % (title_app))
        self.wektorInstrukcjaDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.wektorInstrukcjaDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.wektorFormularzDialog = WektorFormularzDialog()
        self.wektorFormularzDialog.setWindowTitle('%s (krok 4 z 6)' % (title_app))
        self.wektorFormularzDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.wektorFormularzDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.dokumentyFormularzDialog = DokumentyFormularzDialog()
        self.dokumentyFormularzDialog.setWindowTitle('%s (krok 5 z 6)' % (title_app))
        self.dokumentyFormularzDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.dokumentyFormularzDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)

        self.generowanieGMLDialog = GenerowanieGMLDialog()
        self.generowanieGMLDialog.setWindowTitle('%s (krok 6 z 6)' % (title_app))
        self.generowanieGMLDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_app)))
        self.generowanieGMLDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        # endregion

        # region eventy moduł app
        self.pytanieAppDialog.zbior_btn.clicked.connect(self.pytanieAppDialog_zbior_btn_clicked)
        self.pytanieAppDialog.app_btn.clicked.connect(self.pytanieAppDialog_app_btn_clicked)

        self.rasterInstrukcjaDialog.next_btn.clicked.connect(self.rasterInstrukcjaDialog_next_btn_clicked)
        self.rasterInstrukcjaDialog.prev_btn.clicked.connect(self.rasterInstrukcjaDialog_prev_btn_clicked)

        self.rasterFormularzDialog.prev_btn.clicked.connect(self.rasterFormularzDialog_prev_btn_clicked)
        self.rasterFormularzDialog.next_btn.clicked.connect(self.rasterFormularzDialog_next_btn_clicked)
        self.rasterFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.wektorInstrukcjaDialog.next_btn.clicked.connect(self.wektorInstrukcjaDialog_next_btn_clicked)
        self.wektorInstrukcjaDialog.prev_btn.clicked.connect(self.wektorInstrukcjaDialog_prev_btn_clicked)
        self.wektorInstrukcjaDialog.generateTemporaryLayer_btn.clicked.connect(self.showPopupGenerateLayer)
        self.wektorInstrukcjaDialog.chooseFile_btn.clicked.connect(self.openFile)
        self.wektorInstrukcjaDialog.layers_comboBox.setAllowEmptyLayer(True)

        self.wektorFormularzDialog.prev_btn.clicked.connect(self.wektorFormularzDialog_prev_btn_clicked)
        self.wektorFormularzDialog.next_btn.clicked.connect(self.wektorFormularzDialog_next_btn_clicked)
        self.wektorFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.dokumentyFormularzDialog.prev_btn.clicked.connect(self.dokumentyFormularzDialog_prev_btn_clicked)
        self.dokumentyFormularzDialog.next_btn.clicked.connect(self.dokumentyFormularzDialog_next_btn_clicked)
        self.dokumentyFormularzDialog.saveForm_btn.clicked.connect(self.showPopupSaveForm)

        self.generowanieGMLDialog.prev_btn.clicked.connect(self.generowanieGMLDialog_prev_btn_clicked)
        self.generowanieGMLDialog.next_btn.clicked.connect(self.generowanieGMLDialog_next_btn_clicked)
        self.generowanieGMLDialog.generate_btn.clicked.connect(self.showPopupGenerate)
        self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.toggled.connect(self.makeAnotherApp_radioBtn_toggled)
        self.generowanieGMLDialog.yesMakeSet_radioBtn.toggled.connect(self.makeSet_radioBtn_toggled)
        self.generowanieGMLDialog.addElement_btn.clicked.connect(self.addTableContentGML)
        self.generowanieGMLDialog.deleteElement_btn.clicked.connect(self.deleteTableContentGML)
        header_gml = self.generowanieGMLDialog.filesTable_widget.horizontalHeader()
        header_gml.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.zbiorPrzygotowanieDialog.prev_btn.clicked.connect(self.zbiorPrzygotowanieDialog_prev_btn_clicked)
        self.zbiorPrzygotowanieDialog.next_btn.clicked.connect(self.zbiorPrzygotowanieDialog_next_btn_clicked)
        self.zbiorPrzygotowanieDialog.validateAndGenerate_btn.clicked.connect(self.showPopupGenerate2)
        self.zbiorPrzygotowanieDialog.addElement_btn.clicked.connect(self.addTableContentSet)
        self.zbiorPrzygotowanieDialog.deleteElement_btn.clicked.connect(self.deleteTableContentSet)
        header_zbior = self.zbiorPrzygotowanieDialog.appTable_widget.horizontalHeader() #auto resize kolumn
        header_zbior.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.zbiorPrzygotowanieDialog.addFile_widget.setFilter("*.gml")
        # endregion

        # region okno moduł metadata
        self.metadaneDialog = MetadaneDialog()
        self.metadaneDialog.setWindowTitle('%s' % (title_metadata))
        self.metadaneDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_metadata)))
        self.metadaneDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        # endregion

        # region eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.next_btn.clicked.connect(self.metadaneDialog_next_btn_clicked)

        self.metadaneDialog.send_btn.clicked.connect(self.showPopupSend)
        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)

        self.metadaneDialog.newMetadata_radioButton.toggled.connect(self.newMetadataRadioButton_toggled)
        self.metadaneDialog.existingMetadata_radioButton.toggled.connect(self.existingMetadataRadioButton_toggled)

        self.metadaneDialog.server_checkBox.stateChanged.connect(self.server_checkBoxChangedAction)
        self.metadaneDialog.email_checkBox.stateChanged.connect(self.email_checkBoxChangedAction)

        self.metadaneDialog.newFile_widget.clicked.connect(self.saveMetaFile)
        self.metadaneDialog.chooseFile_widget.clicked.connect(self.openMetaFile)

        #self.metadaneDialog.chooseFile_widget.setFilter("*.xml")
        #self.metadaneDialog.chooseSet_widget.setFilter("*.gml")
        #self.metadaneDialog.newFile_widget.clicked.connect(self.getSaveFileName(filter="*.xml")[0])
        # endregion

        # region okno moduł validator
        self.walidacjaDialog = WalidacjaDialog()
        self.walidacjaDialog.setWindowTitle('%s' % (title_validator))
        self.walidacjaDialog.setWindowIcon(QtGui.QIcon('%s%s' % (icon_path, icon_validator)))
        self.walidacjaDialog.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        # endregion

        # region eventy moduł validator
        self.walidacjaDialog.prev_btn.clicked.connect(self.walidacjaDialog_prev_btn_clicked)

        self.walidacjaDialog.close_btn.setEnabled(False)
        self.walidacjaDialog.export_btn.clicked.connect(self.showPopupExport)
        self.walidacjaDialog.validate_btn.clicked.connect(self.walidacjaDialog_validate_btn_clicked)
        self.walidacjaDialog.validateGML_checkBox.stateChanged.connect(self.gml_checkBoxChangedAction)
        self.walidacjaDialog.validateXML_checkBox.stateChanged.connect(self.xml_checkBoxChangedAction)
        self.walidacjaDialog.close_btn.clicked.connect(self.walidacjaDialog.close)

        self.walidacjaDialog.chooseXML_widget.setFilter("*.xml")
        self.walidacjaDialog.chooseGML_widget.setFilter("*.gml")
        # endregion

    def addAction(self, icon_path, text, callback):
        m = self.toolButton.menu()
        action = QAction(
            icon=QIcon(icon_path),
            text=text,
            parent=self.iface.mainWindow()
        )
        action.triggered.connect(callback)
        self.actions.append(action)
        m.addAction(action)
        self.iface.addPluginToMenu(u'&' + PLUGIN_NAME, action)
        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.toolButton = QToolButton()
        self.toolButton.setDefaultAction(QAction(
            icon=QIcon(':/plugins/wtyczka_app/img/logo.png'),
            text=u'&' + PLUGIN_NAME,
            parent=self.iface.mainWindow()
        ))
        self.toolButton.clicked.connect(self.run_app)

        self.toolButton.setMenu(QMenu())
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.toolBtnAction = self.iface.addToolBarWidget(self.toolButton)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/praca_z_app.png',
                       text=u'Praca z APP / zbiorem APP',
                       callback=self.run_app)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/tworzenie.png',
                       text=u'Tworzenie / aktualizacja metadanych',
                       callback=self.run_metadata)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/walidacja.png',
                       text=u'Walidacja GML / XML',
                       callback=self.run_validator)

        self.addAction(icon_path=':/plugins/wtyczka_app/img/ustawienia.png',
                       text=u'Ustawienia',
                       callback=self.run_settings)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(u'&' + PLUGIN_NAME, action)
            self.iface.removeToolBarIcon(action)

        self.iface.removeToolBarIcon(self.toolBtnAction)

    """Action handlers"""
    # region action handlers
    def run_app(self):
        self.openNewDialog(self.pytanieAppDialog)

    def run_metadata(self):
        self.openNewDialog(self.metadaneDialog)
        self.metadaneDialog.prev_btn.setEnabled(False)

    def run_settings(self):
        pass

    def run_validator(self):
        self.openNewDialog(self.walidacjaDialog)
        self.walidacjaDialog.prev_btn.setEnabled(False)
    # endregion

    """Event handlers"""

    # region pytanieAppDialog

    def pytanieAppDialog_app_btn_clicked(self):
        self.openNewDialog(self.rasterInstrukcjaDialog)
        self.listaOkienek.append(self.pytanieAppDialog)

    def pytanieAppDialog_zbior_btn_clicked(self):
        self.openNewDialog(self.zbiorPrzygotowanieDialog)
        self.listaOkienek.append(self.pytanieAppDialog)
    # endregion

    # region rasterInstrukcjaDialog
    def rasterInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.rasterFormularzDialog)
        self.listaOkienek.append(self.rasterInstrukcjaDialog)

    def rasterInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())
    # endregion

    # region rasterFormularzDialog
    def rasterFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def rasterFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorInstrukcjaDialog)
        self.listaOkienek.append(self.rasterFormularzDialog)
    # endregion

    # region wektorInstrukcjaDialog
    def wektorInstrukcjaDialog_next_btn_clicked(self):
        self.openNewDialog(self.wektorFormularzDialog)
        self.listaOkienek.append(self.wektorInstrukcjaDialog)

    def wektorInstrukcjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())
    # endregion

    # region wektorFormularzDialog
    def wektorFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def wektorFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.dokumentyFormularzDialog)
        self.listaOkienek.append(self.wektorFormularzDialog)
    # endregion

    # region dokumentyFormularzDialog
    def dokumentyFormularzDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def dokumentyFormularzDialog_next_btn_clicked(self):
        self.openNewDialog(self.generowanieGMLDialog)
        self.listaOkienek.append(self.dokumentyFormularzDialog)
    # endregion

    # region generowanieGMLDialog
    def generowanieGMLDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def generowanieGMLDialog_next_btn_clicked(self):
        if self.generowanieGMLDialog.yesMakeAnotherApp_radioBtn.isChecked():
            self.openNewDialog(self.rasterInstrukcjaDialog)
            self.listaOkienek.append(self.generowanieGMLDialog)
        if self.generowanieGMLDialog.noMakeAnotherApp_radioBtn.isChecked():
            if self.generowanieGMLDialog.yesMakeSet_radioBtn.isChecked():
                self.openNewDialog(self.zbiorPrzygotowanieDialog)
                self.listaOkienek.append(self.generowanieGMLDialog)
            if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
                self.generowanieGMLDialog.close()

    def makeAnotherApp_radioBtn_toggled(self, setYes):
        if setYes:  # tak - utworzenie kolejnego APP
            self.generowanieGMLDialog.next_btn.setText("Dalej")
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setChecked(False)
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(False)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(False)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(False)
        else:  # nie
            self.generowanieGMLDialog.questionMakeSet_lbl.setEnabled(True)
            self.generowanieGMLDialog.yesMakeSet_radioBtn.setEnabled(True)
            self.generowanieGMLDialog.noMakeSet_radioBtn.setEnabled(True)
            if self.generowanieGMLDialog.noMakeSet_radioBtn.isChecked():
                self.generowanieGMLDialog.next_btn.setText("Zakończ")

    def makeSet_radioBtn_toggled(self, setYes):
        if setYes:  # finalne tworzenie zbioru app
            self.generowanieGMLDialog.next_btn.setText("Dalej")
        else:  # zakończ działanie wtyczki
            self.generowanieGMLDialog.next_btn.setText("Zakończ")

    # endregion

    # region zbiorPrzygotowanieDialog
    def zbiorPrzygotowanieDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def zbiorPrzygotowanieDialog_next_btn_clicked(self):
        self.openNewDialog(self.metadaneDialog)
        self.listaOkienek.append(self.zbiorPrzygotowanieDialog)
        self.metadaneDialog.prev_btn.setEnabled(True)
    # endregion

    # region metadaneDialog
    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)
        self.listaOkienek.append(self.metadaneDialog)
        self.walidacjaDialog.prev_btn.setEnabled(True)

    def newMetadataRadioButton_toggled(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(True)
            self.metadaneDialog.chooseFile_widget.setEnabled(False)
            self.metadaneDialog.file_lbl.setText("...")

    def existingMetadataRadioButton_toggled(self, enabled):
        if enabled:
            self.metadaneDialog.newFile_widget.setEnabled(False)
            self.metadaneDialog.chooseFile_widget.setEnabled(True)
            self.metadaneDialog.file_lbl.setText("...")

    def server_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.email_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)

    def email_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.server_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)
    # endregion

    # region walidacjaDialog
    def walidacjaDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())

    def walidacjaDialog_validate_btn_clicked(self):
        self.showPopupValidate()
        self.walidacjaDialog.close_btn.setEnabled(True)

    def xml_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.walidacjaDialog.chooseXML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseXML_widget.setEnabled(False)

    def gml_checkBoxChangedAction(self, state):
        if (QtCore.Qt.Checked == state):
            self.walidacjaDialog.chooseGML_widget.setEnabled(True)
        else:
            self.walidacjaDialog.chooseGML_widget.setEnabled(False)
    # endregion

    """Helper methods"""
    # region Helper methods
    def openNewDialog(self, dlg):
        self.prevDlg = self.activeDlg
        self.activeDlg = dlg
        if self.prevDlg:
            self.prevDlg.close()
        self.activeDlg.show()

    #działa, ale trzeba dodać również inne rozszerzenia
    def openShpFile(self):
        shpFile = str(QFileDialog.getOpenFileName(filter=("Shapefiles (*.shp)"))[0])
        self.wektorInstrukcjaDialog.label.setText(shpFile)
        if shpFile is not None:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    def saveMetaFile(self):
        self.outputPlik = QFileDialog.getSaveFileName(filter="*.xml")[0]
        if self.outputPlik != '':
            self.metadaneDialog.file_lbl.setText(self.outputPlik)

    def openMetaFile(self):
        self.plik = QFileDialog.getOpenFileName(filter="*.xml")[0]
        if self.plik != '':
            self.metadaneDialog.file_lbl.setText(self.plik)

    #setAdditionalItems nie działa, niepoprawny argument
    #dodać inne rozszerzenia
    def openFile(self):
        shpFile = str(QFileDialog.getOpenFileName(filter=("Shapefiles (*.shp)"))[0])
        #self.listaPlikow.append(shpFile)
        #self.wektorInstrukcjaDialog.layers_comboBox.setAdditionalItems(self.listaPlikow)
        if shpFile:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    #niepotrzebne, było używane do QgsFileWidget - obecnie jest PushButton
    def openQgsFile(self):
        shpFile = self.wektorInstrukcjaDialog.chooseFile_btn.filePath()
        self.wektorInstrukcjaDialog.label.setText(shpFile)
        if shpFile is not None:
            self.iface.addVectorLayer(shpFile, str.split(os.path.basename(shpFile), ".")[0], "ogr")

    #wybór warstwy z QgsMapLayerComboBox
    def selectQgsLayer(self):
        # co jak użytkownik usunie wszystkie warstwy??
        aktywna_warstwa = self.wektorInstrukcjaDialog.layers_comboBox.currentLayer()
        if aktywna_warstwa:
            self.wektorInstrukcjaDialog.label.setText(aktywna_warstwa.name())
        else:
            self.wektorInstrukcjaDialog.label.setText("...")

    def addTableContentGML(self):
        plik = str(QFileDialog.getOpenFileName(filter=("XML/GML files (*.xml *.gml)"))[0])
        if plik:
            rows = self.generowanieGMLDialog.filesTable_widget.rowCount()
            self.generowanieGMLDialog.filesTable_widget.setRowCount(rows+1)
            self.generowanieGMLDialog.filesTable_widget.setItem(rows, 0, QTableWidgetItem(plik))

    def deleteTableContentGML(self):
        row_num = self.generowanieGMLDialog.filesTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.generowanieGMLDialog.filesTable_widget.currentRow()
            self.generowanieGMLDialog.filesTable_widget.removeRow(do_usuniecia)
        else:
            pass

    def addTableContentSet(self):
        plik = str(QFileDialog.getOpenFileName(filter=("GML file (*.gml)"))[0])
        if plik:
            rows = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
            self.zbiorPrzygotowanieDialog.appTable_widget.setRowCount(rows+1)
            self.zbiorPrzygotowanieDialog.appTable_widget.setItem(rows, 0, QTableWidgetItem(plik))

    def deleteTableContentSet(self):
        row_num = self.zbiorPrzygotowanieDialog.appTable_widget.rowCount()
        if row_num > 0:
            do_usuniecia = self.zbiorPrzygotowanieDialog.appTable_widget.currentRow()
            self.zbiorPrzygotowanieDialog.appTable_widget.removeRow(do_usuniecia)
        else:
            pass


    # endregion

    """Popup windows"""
    # region Popup windows
    def showPopup(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec_()

    def showPopupSaveForm(self):
        self.showPopup("Zapisz aktualny formularz", "Poprawnie zapisano formularz.")

    def showPopupSaveLayer(self):
        self.showPopup("Zapisz warstwę", "Poprawnie zapisano warstwę.")

    def showPopupGenerateLayer(self):
        self.showPopup("Wygeneruj warstwę", "Poprawnie utworzono pustą warstwę. Uzupełnij ją danymi wektorowymi oraz wypełnij atrybuty.")

    def showPopupGenerate(self):
        self.showPopup("Wygeneruj plik GML dla APP", "Poprawnie wygenerowano plik GML.")

    def showPopupGenerate2(self):
        self.showPopup("Wygeneruj plik GML dla zbioru APP", "Poprawnie wygenerowano plik GML.")

    def showPopupExport(self):
        self.showPopup("Wyeksportuj plik z błędami", "Poprawnie wyeksportowano plik z błędami.")

    def showPopupValidateAndSave(self):
        self.showPopup("Zwaliduj i zapisz plik XML", "Poprawnie zwalidowano oraz zapisano plik XML.")

    def showPopupSend(self):
        self.showPopup("Wyśli plik", "Wysłano plik XML zawierający metadane.")

    def showPopupValidate(self):
        self.showPopup("Waliduj pliki", "Poprawnie zwalidowano wszystkie wgrane pliki.")
    # endregion