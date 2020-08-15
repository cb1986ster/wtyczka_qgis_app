# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from qgis.core import QgsMapLayerProxyModel
from qgis.gui import QgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox
from qgis.PyQt.QtCore import Qt, QRegExp, QVariant
from qgis.PyQt.QtGui import QRegExpValidator, QPixmap
from . import dictionaries, utils


class NoScrollQComboBox(QComboBox):
    """Combobox bez scrolla"""

    def wheelEvent(self, event):
        event.ignore()


class NoScrollQgsDateTimeEdit(QgsDateTimeEdit):
    """QgsDateTimeEdit bez scrolla"""

    def wheelEvent(self, event):
        event.ignore()


class Formularz:
    """Klasa reprezentująca formularz"""

    pomijane = ["dokumentPrzystepujacy",
                "dokumentUchwalajacy",
                "dokumentZmieniajacy",
                "dokumentUchylajacy",
                "dokumentUniewazniajacy",
                "przystapienie",
                "uchwala",
                "zmienia",
                "uchyla",
                "uniewaznia",
                "plan",
                "dokument",
                "rysunek",
                "zasiegPrzestrzenny",
                "zmiana"]

    def returnFormElements(self, formElements):
        for fe in formElements:
            print('\t'+fe.name)
            try:
                print(fe.refObject.objectName())
            except:
                print('W pominiętych')

    def removeForm(self, container):
        """usuwa zawartość kontenera(container), żeby zrobić miejsce na formularz"""
        container.takeWidget()

    def clearForm(self, container):
        """czyści pola formularza"""
        widgets = utils.getWidgets(
            layout=container,
            types=[QgsDateTimeEdit, NoScrollQgsDateTimeEdit, QgsFilterLineEdit, QgsMapLayerComboBox, QComboBox, NoScrollQComboBox, QCheckBox, QListWidget])
        for widget in widgets[QgsDateTimeEdit]:
            widget.clear()
        for widget in widgets[NoScrollQgsDateTimeEdit]:
            widget.clear()
        for widget in widgets[QgsFilterLineEdit]:
            widget.clear()
        for widget in widgets[QgsMapLayerComboBox]:
            widget.setCurrentIndex(0)
        for widget in widgets[QComboBox]:
            widget.setCurrentIndex(0)
        for widget in widgets[NoScrollQComboBox]:
            widget.setCurrentIndex(0)
        for widget in widgets[QCheckBox]:
            if widget.isChecked():
                widget.click()
        for widget in widgets[QListWidget]:
            widget.clear()

    def createForm(self, container, formElements):
        """tworzy formularz w miejscu kontenera (container), na podstawie listy obiektów klasy <FormElement>"""
        wgtMain = QWidget()
        vbox = QVBoxLayout(wgtMain)
        self.__loopFormElements(formElements, vbox)

        self.__preparePoziomHierarchii(vbox)
        container.setWidget(wgtMain)

    def __preparePoziomHierarchii(self, layout):
        """definiuje autouzupełnianie poziomHierarchii (INSPIRE)
        na podstawie typPlanu"""
        def typPlanu_cmbbx_currentTextChanged(currentText):
            if currentText.strip():
                poziomHierarchii_cmbbx.clear()
                wybor = dictionaries.typyPlanuPoziomyHierarchii[currentText]
                poziomHierarchii_cmbbx.addItems(wybor)

        # pobranie dynamicznie utworzonych obiektów UI
        poziomHierarchii_cmbbx = utils.layout_widget_by_name(
            layout, "poziomHierarchii_cmbbx")
        typPlanu_cmbbx = utils.layout_widget_by_name(layout, "typPlanu_cmbbx")
        if poziomHierarchii_cmbbx and typPlanu_cmbbx:   # jeżeli formularz zawiera te pola
            typPlanu_cmbbx.currentTextChanged.connect(
                typPlanu_cmbbx_currentTextChanged)

    def __loopFormElements(self, formElements, vbox, prefix=''):
        """Przerabia listę obiektów FormElements na GUI"""
        def createListWidget(name):
            """Tworzy listę dla pól wielokrotnej liczności"""
            def checkListFormValidity():
                if name == 'mapaPodkladowa':
                    if not referencja_lineEdit.text():
                        return False
                    if not data_dateTimeEdit.date():
                        return False
                    # if (not lacze_lineEdit.text() and
                    #         not lacze_lineEdit_nilReason_chkbx.isChecked()):
                    #     return False
                    # if (not lacze_lineEdit.text() and
                    #         lacze_lineEdit_nilReason_chkbx.isChecked() and
                    #         not lacze_lineEdit_nilReason_cmbbx.currentText()):
                    #     return False
                    return True
                else:
                    if formItems[0].text().strip():
                        return True
                    else:
                        return False

            def addItem():
                if checkListFormValidity():
                    newListWidgetItem = QListWidgetItem()
                    data = {}
                    textList = []
                    for formItem in formItems:
                        if isinstance(formItem, QLineEdit):
                            if formItem.text() == '':
                                data[formItem.objectName()] = '<brak wartości>'
                            else:
                                data[formItem.objectName()] = formItem.text()
                            textList.append(formItem.text())
                        elif isinstance(formItem, QDateTimeEdit):
                            data[formItem.objectName()] = formItem.dateTime()
                            textList.append(formItem.dateTime().toString())
                        elif isinstance(formItem, QCheckBox):
                            data[formItem.objectName()] = formItem.isChecked()
                        elif isinstance(formItem, QComboBox):
                            data[formItem.objectName()] = formItem.currentIndex()

                    newListWidgetItem.setData(
                        Qt.UserRole,
                        QVariant(data)
                    )
                    newListWidgetItem.setText(" - ".join(textList))
                    listWidget.addItem(newListWidgetItem)
                    clearDataFromListWidget()   # czyszczenie
                else:
                    if name == 'mapaPodkladowa':
                        utils.showPopup("Wypełnij formularz mapy podkładowej",
                                        'Musisz zdefiniować wartości dla obowiązkowych pól:\n'
                                        '- referencja,\n'
                                        '- data')
                    else:
                        utils.showPopup("Wypełnij formularz",
                                        "Musisz wpisać wartość przed dodaniem")

            def removeItem():
                listWidget.takeItem(listWidget.currentRow())

            def clearDataFromListWidget():
                for formItem in formItems:
                    if isinstance(formItem, QCheckBox):
                        formItem.setChecked(False)
                    elif isinstance(formItem, QComboBox):
                        formItem.setCurrentIndex(0)
                    else:
                        formItem.clear()

            def setDataToListWidget(listItem):
                data = listItem.data(Qt.UserRole)
                for formItem in formItems:
                    if isinstance(formItem, QLineEdit):
                        formItem.setText(data[formItem.objectName()])
                    elif isinstance(formItem, QDateTimeEdit):
                        formItem.setDateTime(data[formItem.objectName()])
                    elif isinstance(formItem, QCheckBox):
                        formItem.setChecked(data[formItem.objectName()])
                    elif isinstance(formItem, QComboBox):
                        formItem.setCurrentIndex(data[formItem.objectName()])

            if name == 'mapaPodkladowa':
                referencja_lineEdit = utils.layout_widget_by_name(
                    vbox2, name="referencja_lineEdit")
                data_dateTimeEdit = utils.layout_widget_by_name(
                    vbox2, name="data_dateTimeEdit")
                lacze_lineEdit = utils.layout_widget_by_name(
                    vbox2, name="lacze_lineEdit")
                # lacze_lineEdit_nilReason_chkbx = utils.layout_widget_by_name(
                #     vbox2, name="lacze_lineEdit_nilReason_chkbx")
                # lacze_lineEdit_nilReason_cmbbx = utils.layout_widget_by_name(
                #     vbox2, name="lacze_lineEdit_nilReason_cmbbx")
                # lacze_lineEdit_nilReason_chkbx.stateChanged.connect(
                #     lambda: lacze_lineEdit.clear())
                formItems = [referencja_lineEdit,
                             data_dateTimeEdit,
                             lacze_lineEdit]  # , lacze_lineEdit_nilReason_chkbx, lacze_lineEdit_nilReason_cmbbx]
            elif formElement.name == 'lacze':
                lacze_lineEdit = utils.layout_widget_by_name(
                    vbox2, name="lacze_lineEdit")
                formItems = [lacze_lineEdit]

            elif formElement.name == 'tytulAlternatywny':
                tytulAlternatywny_lineEdit = utils.layout_widget_by_name(
                    vbox2, name="tytulAlternatywny_lineEdit")
                formItems = [tytulAlternatywny_lineEdit]

            # buttony
            btnHBox = QHBoxLayout()
            addBtn = QPushButton("Dodaj")
            addBtn.clicked.connect(addItem)
            remBtn = QPushButton("Usuń")
            remBtn.clicked.connect(removeItem)
            btnHBox.addWidget(addBtn)
            btnHBox.addWidget(remBtn)
            vbox2.addLayout(btnHBox)

            # QListWidget
            listWidget = QListWidget()
            listWidget.setObjectName(formElement.name + "_listWidget")
            listWidget.itemDoubleClicked.connect(setDataToListWidget)
            formElement.refObject = listWidget
            vbox2.addWidget(listWidget)

        for formElement in formElements:
            if (
                    formElement.type == 'gml:ReferenceType' or
                    formElement.type == "gml:AbstractFeatureMemberType" or
                    formElement.type == "gml:MultiSurfacePropertyType"
            ) and formElement.name in self.pomijane:
                continue  # pomiń element
            if formElement.name == 'zmiana':
                continue  # pomiń zmianę (dodana w postprodukcji 8-) )

            hbox = QHBoxLayout()  # wiersz formularza
            hbox.setObjectName(formElement.name + '_hbox')

            # label
            lbl = QLabel(text=prefix + formElement.name +
                         ('*' if formElement.minOccurs else ''))
            lbl.setObjectName(formElement.name + '_lbl')
            hbox.addWidget(lbl)

            input = self.__makeInput(formElement)
            formElement.refObject = input
            tooltipImg = self.__makeTooltip(formElement)

            if formElement.maxOccurs == "unbounded":

                groupbox = QGroupBox(formElement.name)
                vbox2 = QVBoxLayout()
                groupbox.setLayout(vbox2)
                vbox2.addLayout(hbox)

                hbox.addWidget(input)
                hbox.addWidget(tooltipImg)
                vbox.addWidget(groupbox)

                if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                    # input.setEnabled(False)
                    input.setVisible(False)
                    # rekurencja dla obiektów wewntrznych
                    self.__loopFormElements(
                        formElement.innerFormElements, vbox2, '  - ')

                createListWidget(formElement.name)

            else:
                hbox.addWidget(input)
                if formElement.type == 'gmd:CI_Date_PropertyType':
                    input2 = NoScrollQComboBox()
                    input2.setObjectName(formElement.name + '_cmbbx')
                    input2.addItems(dictionaries.cI_DateTypeCode.keys())
                    formElement.refObject = [input, input2]

                    hbox.addWidget(input2)

                hbox.addWidget(tooltipImg)
                vbox.addLayout(hbox)
                # if formElement.name == 'zmiana':
                #     input.setEnabled(False)
                #     input.setText('0')
                if formElement.isComplex():  # zawiera podrzędne elementy typu complex
                    input.setEnabled(False)
                    # rekurencja dla obiektów wewntrznych
                    self.__loopFormElements(
                        formElement.innerFormElements, vbox, '  - ')

            if formElement.isNillable:  # dodaj dodatkowo checkbox i powód
                nilHbox = self.__makeNilHbox(input)
                formElement.refNilObject = nilHbox
                vbox.addLayout(nilHbox)

    def __makeNilHbox(self, nillableWidget):
        """tworzy zestaw widgetów do obługi typu "nillable"""
        def changeState():
            currentState = chckBox.isChecked()
            if currentState:
                nilLbl2.setEnabled(True)
                nillableWidget.setEnabled(False)
                comboBox.setEnabled(True)
            else:
                nilLbl2.setEnabled(False)
                nillableWidget.setEnabled(True)
                comboBox.setEnabled(False)

        nilHbox = QHBoxLayout()
        nilLbl1 = QLabel(text='    ')
        nilLbl2 = QLabel(text='wskaż powód: ')
        nilLbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        nilLbl2.setObjectName(
            nillableWidget.objectName() + 'nilReason' + '_lbl')
        nilLbl2.setEnabled(False)
        chckBox = QCheckBox(text='brak wartości')
        chckBox.setObjectName(
            nillableWidget.objectName() + '_nilReason' + '_chkbx')
        chckBox.stateChanged.connect(lambda: changeState())
        comboBox = QComboBox()
        comboBox.setObjectName(
            nillableWidget.objectName() + '_nilReason' + '_cmbbx')
        comboBox.addItems(dictionaries.nilReasons.keys())
        comboBox.setEnabled(False)
        tooltipImg = QLabel()
        tooltipImg.setMaximumWidth(16)

        nilHbox.addWidget(nilLbl1)
        nilHbox.addWidget(chckBox)
        nilHbox.addWidget(nilLbl2)
        nilHbox.addWidget(comboBox)
        nilHbox.addWidget(tooltipImg)
        return nilHbox

    def __makeInput(self, formElement):
        # pole wprowadzania
        if formElement.name == "ukladOdniesieniaPrzestrzennego":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.ukladyOdniesieniaPrzestrzennego.keys())
        elif formElement.name == "typPlanu":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.typyPlanu.keys())
        elif formElement.name == "poziomHierarchii":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(
                reversed(list(dictionaries.poziomyHierarchii.keys())[1:]))
            # input.addItems(dictionaries.poziomyHierarchii.keys())
        elif formElement.name == "status":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            input.addItems(dictionaries.statusListaKodowa.keys())
        elif formElement.name == "dziennikUrzedowy":
            input = NoScrollQComboBox()
            input.setObjectName(formElement.name + '_cmbbx')
            dict1 = dictionaries.dziennikUrzedowyKod.keys()
            values = ['']
            values.extend(list(dict1))
            input.addItems(values)
        elif formElement.type == 'dateTime':
            input = NoScrollQgsDateTimeEdit()
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'date':
            input = NoScrollQgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'gmd:CI_Date_PropertyType':
            input = NoScrollQgsDateTimeEdit()
            input.setDisplayFormat('dd.MM.yyyy')
            input.setObjectName(formElement.name + '_dateTimeEdit')
            input.clear()
        elif formElement.type == 'integer':
            input = QgsFilterLineEdit()
            # tylko liczby calkowite
            input.setValidator(QRegExpValidator(QRegExp("[0-9]*")))
            input.setObjectName(formElement.name + '_lineEdit')
        elif formElement.type == 'anyURI':
            input = QgsFilterLineEdit()
            # tylko ciąg znaków
            input.setValidator(QRegExpValidator(QRegExp(r"\S*")))
            input.setObjectName(formElement.name + '_lineEdit')
        else:
            input = QgsFilterLineEdit()
            input.setObjectName(formElement.name + '_lineEdit')

        # ustawienie podpowiedzi inputa (typ)
        input.setToolTip((formElement.type + ' - nillable')
                         if formElement.isNillable else formElement.type)

        # ustawienie domyślnych wartości
        fullFormElementName = formElement.form + ":" + formElement.name
        # # print(fullFormElementName)

        # wartości domyślne - debug
        # if fullFormElementName in dictionaries.placeholders.keys():
        #     if isinstance(input, QLineEdit):  # dla pól tekstowych
        #         input.setText(
        #             dictionaries.placeholders[fullFormElementName])
        #     elif isinstance(input, QComboBox):  # QComboBox
        #         pass

        # ustawienie podpowiedzi
        if fullFormElementName in dictionaries.placeholders.keys():
            input.setPlaceholderText(
                'np.: ' + dictionaries.placeholders[fullFormElementName])  # dla pól tekstowych

        return input

    def __makeTooltip(self, formElement):
        tooltipImg = QLabel()
        p = QPixmap(':/plugins/wtyczka_app/img/info1.png')
        tooltipImg.setMaximumWidth(16)
        tooltipImg.setPixmap(p.scaled(16, 16, Qt.KeepAspectRatio))
        tooltipImg.setToolTip(
            "<FONT COLOR=black>%s</FONT>" % formElement.documentation)  # dodanie tooltip z documentation 'rich text' dla zawijania
        tooltipImg.setObjectName(formElement.name + '_tooltip')
        return tooltipImg
