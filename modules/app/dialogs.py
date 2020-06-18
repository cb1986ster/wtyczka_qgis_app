# -*- coding: utf-8 -*-
"""
/***************************************************************************
Okna dialogowe modułu APP
 ***************************************************************************/
"""

import os, sys

import PyQt5
from PyQt5.QtWidgets import *
from qgis.PyQt.QtCore import Qt
from qgis.PyQt import uic, QtGui
from PyQt5.QtXmlPatterns import *
from .. import QDialogOverride
from ..models import FormElement
from .. import utils

title_question ='Praca z APP / zbiorem APP'
title_app = 'Praca z APP'
icon_path = ':/plugins/wtyczka_app/img/praca_z_app.png'

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'pytanie_dialog_base.ui'))
FORM_CLASS1, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'zbior_przygotowanie_dialog_base.ui'))
FORM_CLASS2, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'views', 'ui', 'raster_instrukcja_dialog_base.ui'))
FORM_CLASS3, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_raster_dialog_base.ui'))
FORM_CLASS4, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_dokumenty_dialog_base.ui'))
FORM_CLASS5, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'formularz_wektor_dialog_base.ui'))
FORM_CLASS6, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'generowanie_gml_dialog_base.ui'))
FORM_CLASS7, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__),'views', 'ui', 'wektor_instrukcja_dialog_base.ui'))


class PytanieAppDialog(QDialogOverride, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(PytanieAppDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-views-with-auto-connect
        self.setupUi(self)
        self.setWindowTitle(title_question)
        self.setWindowIcon(QtGui.QIcon(':/plugins/wtyczka_app/img/logo.png'))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        # self.zbior_btn.clicked.connect(self.close)
        # self.app_btn.clicked.connect(self.close)


class ZbiorPrzygotowanieDialog(QDialogOverride, FORM_CLASS1):
    def __init__(self, parent=None):
        """Constructor."""
        super(ZbiorPrzygotowanieDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Tworzenie zbioru APP')
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)


class RasterInstrukcjaDialog(QDialogOverride, FORM_CLASS2):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 1 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)


class RasterFormularzDialog(QDialogOverride, FORM_CLASS3):
    def __init__(self, parent=None):
        """Constructor."""
        super(RasterFormularzDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 2 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.clearForm()
        # self.createForm(formElements = [
        #     FormElement('test1'),
        #     FormElement('test2'),
        #     FormElement('test3'),
        #     FormElement('test4'),
        #     FormElement('test5'),
        #     FormElement('test6'),
        #     FormElement('test7'),
        #     FormElement('test8'),
        #     FormElement('test9'),
        #     FormElement('test10'),
        #     FormElement('test11'),
        #     FormElement('test12'),
        # ])
        self.createForm(utils.createFormElementsRysunekAPP())

    def clearForm(self):
        self.form_scrollArea.takeWidget()

    def createForm(self, formElements):

        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
        for formElement in formElements:
            hbox = QHBoxLayout()
            lbl = QLabel(text=formElement.name)
            lbl.setObjectName(formElement.name + '_lbl')
            led = QLineEdit()
            led.setObjectName(formElement.name + '_lineEdit')
            btn = QPushButton(text='?')
            btn.setObjectName(formElement.name + 'Help_btn')
            hbox.addWidget(lbl)
            hbox.addWidget(led)
            hbox.addWidget(btn)
            vbox.addLayout(hbox)
        self.form_scrollArea.setWidget(wgtMain)



class WektorInstrukcjaDialog(QDialogOverride, FORM_CLASS7):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorInstrukcjaDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 3 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)
        self.layers_comboBox.setAllowEmptyLayer(True)

class WektorFormularzDialog(QDialogOverride, FORM_CLASS5):
    def __init__(self, parent=None):
        """Constructor."""
        super(WektorFormularzDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 4 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)


class DokumentyFormularzDialog(QDialogOverride, FORM_CLASS4):
    def __init__(self, parent=None):
        """Constructor."""
        super(DokumentyFormularzDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 5 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)


class GenerowanieGMLDialog(QDialogOverride, FORM_CLASS6):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerowanieGMLDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('%s (krok 6 z 6)' % title_app)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint, True)


