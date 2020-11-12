# -*- coding: utf-8 -*-
from . import (MetadaneDialog, SmtpDialog, CswDialog)
from . import (xmlToMetadataElementDict,
               formToMetadataElementDict,
               metadataElementDictToXml,
               appGmlToMetadataElementDict,
               metadataElementDictToForm)
from .metadata_form_validator import validateMetadataForm

from .. import BaseModule
from ..utils import showPopup
from .. import utils
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from qgis.core import QgsSettings



class MetadataModule(BaseModule):
    walidacjaDialog = None

    def __init__(self, iface):
        self.iface = iface
        self.dataValidator = None
        self.saved = False
        # plik metadanych do wysłania

        self.s = QgsSettings()
        # self.metadataXmlPath = os.path.join(os.path.dirname(__file__), '../validator', 'test_metadata.xml')
        self.metadataXmlPath = None
        # region okno moduł metadata
        self.metadaneDialog = MetadaneDialog()



        # endregion
        self.smtpDialog = SmtpDialog(iface=self.iface)
        self.cswDialog = CswDialog(iface=self.iface)

        # region eventy moduł metadata
        self.metadaneDialog.prev_btn.clicked.connect(self.metadaneDialog_prev_btn_clicked)
        self.metadaneDialog.validateAndSave_btn.clicked.connect(self.showPopupValidateAndSave)
        self.metadaneDialog.close_btn.clicked.connect(self.metadaneDialog.close)

        self.metadaneDialog.email_btn.clicked.connect(self.metadaneDialog_email_btn_clicked)
        self.metadaneDialog.server_btn.clicked.connect(self.metadaneDialog_server_btn_clicked)

        # self.metadaneDialog.newFile_widget.clicked.connect(self.saveMetaFile)
        self.metadaneDialog.chooseFile_widget.setFilter(filter="pliki XML (*.xml)")
        self.metadaneDialog.chooseFile_widget.setDefaultRoot(self.s.value("qgis_app/settings/defaultPath", ""))
        self.metadaneDialog.chooseFile_widget.fileChanged.connect(self.chooseFile_widget_fileChanged)

        self.metadaneDialog.chooseSet_widget.setFilter(filter="pliki XML/GML (*.xml *.gml)")
        self.metadaneDialog.chooseSet_widget.setDefaultRoot(self.s.value("qgis_app/settings/defaultPath", ""))
        self.metadaneDialog.chooseSet_widget.fileChanged.connect(self.chooseSet_widget_fileChanged)
        # endregion

    """Event handlers"""
    def chooseSet_widget_fileChanged(self, path):
        if path:
            # utworzenie słownika na podstawie pliku zbioru APP
            metadataElementDict = appGmlToMetadataElementDict(path)
            # print(metadataElementDict)

            if metadataElementDict:
                # zapisanie słownika do formularza
                metadataElementDictToForm(metadataElementDict, self.metadaneDialog)
                self.iface.messageBar().pushSuccess("Aktualizacja formularza metadanych:",
                                                    "Zaktualizowano formularz metadanych w oparciu o plik zbioru APP.")

    def chooseFile_widget_fileChanged(self, path):
        if path:
            # utworzenie słownika na podstawie pliku metadanych
            metadataElementDict = xmlToMetadataElementDict(path)
            # print(metadataElementDict)

            # zapisanie słownika do formularza
            metadataElementDictToForm(metadataElementDict, self.metadaneDialog)
            self.iface.messageBar().pushSuccess("Aktualizacja formularza metadanych:",
                                                "Zaktualizowano formularz metadanych w oparciu o plik XML metadanych.")


    # region metadaneDialog
    def metadaneDialog_prev_btn_clicked(self):
        self.openNewDialog(self.listaOkienek.pop())
        self.metadaneDialog.server_btn.setEnabled(False)
        self.metadaneDialog.email_btn.setEnabled(False)

    def metadaneDialog_next_btn_clicked(self):
        self.openNewDialog(self.walidacjaDialog)
        self.listaOkienek.append(self.metadaneDialog)
        self.walidacjaDialog.prev_btn.setEnabled(True)

    def metadaneDialog_email_btn_clicked(self):
        self.smtpDialog.setXmlPath(self.metadataXmlPath)
        self.smtpDialog.show()

    def metadaneDialog_server_btn_clicked(self):
        self.cswDialog.setXmlPath(self.metadataXmlPath)
        self.cswDialog.show()

    def server_checkBoxChangedAction(self, state):
        if Qt.Checked == state:
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.email_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)

    def email_checkBoxChangedAction(self, state):
        if Qt.Checked == state:
            self.metadaneDialog.send_btn.setEnabled(True)
        else:
            if self.metadaneDialog.server_checkBox.isChecked():
                self.metadaneDialog.send_btn.setEnabled(True)
            else:
                self.metadaneDialog.send_btn.setEnabled(False)
    # endregion

    """Helper methods"""
    def saveMetaFile(self, xmlString):

        defaultPath = self.s.value("qgis_app/settings/defaultPath", "")
        self.metadataXmlPath = QFileDialog.getSaveFileName(directory=defaultPath, filter="*.xml")[0]
        if self.metadataXmlPath:
            try:
                with open(self.metadataXmlPath, 'w') as file:
                    file.write(xmlString)
                    return True
            except IOError:
                showPopup("Błąd zapisu",
                          "Nie udało się zapisać pliku na dysku.")
                return False
        return False


    """Popup windows"""
    def showPopupValidateAndSave(self):
        validationResult = validateMetadataForm(dlg=self.metadaneDialog)
        # if True: # do testów w celu ominięcia walidacji formularza
        if validationResult[0]:
            # odczyt fromularza
            metadataElementDict = formToMetadataElementDict(self.metadaneDialog)
            # wygnerowanie XML
            xml = metadataElementDictToXml(metadataElementDict)
            showPopup("Zwaliduj plik XML",
                      "Poprawnie zwalidowano formularz. Możesz teraz zapisać plik XML z metadanymi.")
            if self.saveMetaFile(xmlString=xml):
                self.iface.messageBar().pushSuccess("Generowanie pliku metadanych:",
                                                    "Pomyślnie zapisano plik metadanych.")
                self.metadaneDialog.server_btn.setEnabled(True)
                self.metadaneDialog.email_btn.setEnabled(True)
        else:
            msg = validationResult[1]
            utils.showPopup("Błąd walidacji formularza", msg, QMessageBox.Warning)