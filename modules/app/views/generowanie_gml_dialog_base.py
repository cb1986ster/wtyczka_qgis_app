# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generowanie_gml_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(666, 331)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_lbl = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title_lbl.setFont(font)
        self.title_lbl.setObjectName("title_lbl")
        self.verticalLayout.addWidget(self.title_lbl)
        self.instruction_scrollArea = QtWidgets.QScrollArea(Dialog)
        self.instruction_scrollArea.setWidgetResizable(True)
        self.instruction_scrollArea.setObjectName("instruction_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 627, 210))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.instruction_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.instruction_lbl.setFont(font)
        self.instruction_lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.instruction_lbl.setWordWrap(True)
        self.instruction_lbl.setObjectName("instruction_lbl")
        self.gridLayout_2.addWidget(self.instruction_lbl, 0, 0, 1, 1)
        self.instruction_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.instruction_scrollArea)
        self.empty1_lbl = QtWidgets.QLabel(Dialog)
        self.empty1_lbl.setText("")
        self.empty1_lbl.setObjectName("empty1_lbl")
        self.verticalLayout.addWidget(self.empty1_lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addFile_lbl = QtWidgets.QLabel(Dialog)
        self.addFile_lbl.setObjectName("addFile_lbl")
        self.horizontalLayout.addWidget(self.addFile_lbl)
        self.addElement_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.addElement_btn.setFont(font)
        self.addElement_btn.setAutoDefault(False)
        self.addElement_btn.setObjectName("addElement_btn")
        self.horizontalLayout.addWidget(self.addElement_btn)
        self.deleteElement_btn = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.deleteElement_btn.setFont(font)
        self.deleteElement_btn.setAutoDefault(False)
        self.deleteElement_btn.setObjectName("deleteElement_btn")
        self.horizontalLayout.addWidget(self.deleteElement_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.filesTable_widget = QtWidgets.QTableWidget(Dialog)
        self.filesTable_widget.setObjectName("filesTable_widget")
        self.filesTable_widget.setColumnCount(4)
        self.filesTable_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.filesTable_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.filesTable_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.filesTable_widget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.filesTable_widget.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.filesTable_widget)
        self.empty3_lbl = QtWidgets.QLabel(Dialog)
        self.empty3_lbl.setText("")
        self.empty3_lbl.setObjectName("empty3_lbl")
        self.verticalLayout.addWidget(self.empty3_lbl)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.prev_btn = QtWidgets.QPushButton(Dialog)
        self.prev_btn.setEnabled(True)
        self.prev_btn.setAutoDefault(False)
        self.prev_btn.setObjectName("prev_btn")
        self.horizontalLayout_4.addWidget(self.prev_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.generate_btn = QtWidgets.QPushButton(Dialog)
        self.generate_btn.setAutoDefault(False)
        self.generate_btn.setObjectName("generate_btn")
        self.horizontalLayout_4.addWidget(self.generate_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.title_lbl.setText(_translate("Dialog", "Generowanie GML dla APP"))
        self.instruction_lbl.setText(_translate("Dialog", "<html><head/><body><p>W tym oknie zostanie wygenerowany końcowy plik GML dla pojedynczego APP. Składa się on ze wszystkich formularzy wygenerowanych w poprzednich krokach, to znaczy:<br/>-z co najmniej jednego formularza dla rysunku APP; <br/>- dokładnie jednego formularza dla APP;<br/>- co najmniej jednego formularza dla dokumentów formalnych. </p><p>W tabeli poniżej muszą znaleźć się wszystkie ww. formularze składające się na dany APP, aby został wygenerowany poprawny plik GML. Dla każdego pliku odczytanego jako <span style=\" text-decoration: underline;\">Dokument formalny</span>, użytkownik musi wybrać odpowiednią relację jaka wiąże ten dokument z APP. </p><p>Następnie można wybrać przycisk <span style=\" text-decoration: underline;\">Generuj</span>, który zwaliduje i zapisze plik GML dla APP na dysku. Po poprawnym wygenerowaniu użytkownik może zdecydować czy będzie tworzył kolejne APP, czy przejdzie do tworzenia zbioru. </p><p><span style=\" font-weight:600;\">Wskazówka</span>: Należy pamiętać, że po wczytywania pliku GML do programu QGIS należy użyć narzędzia <span style=\" text-decoration: underline;\">Zamień współrzędne X i Y</span>, aby dane przestrzenne wyświetliły się poprawnie. <br/></p></body></html>"))
        self.addFile_lbl.setText(_translate("Dialog", "Lista plików na podstawie, których zostanie wygenerowany plik GML"))
        self.addElement_btn.setText(_translate("Dialog", "+"))
        self.deleteElement_btn.setText(_translate("Dialog", "-"))
        item = self.filesTable_widget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Plik XML / GML"))
        item = self.filesTable_widget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Rodzaj dokumentu"))
        item = self.filesTable_widget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Data modyfikacji"))
        item = self.filesTable_widget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Relacja względem APP"))
        self.prev_btn.setText(_translate("Dialog", "Wstecz"))
        self.generate_btn.setText(_translate("Dialog", "Generuj"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
