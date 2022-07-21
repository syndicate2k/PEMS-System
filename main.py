import sys
import emissions
from datetime import datetime, date
from random import random, randint
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import *
import pandas as pd
import numpy as np

current_method = 1

name = "data"
NO2 = True
SO2 = True
CO2 = True


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.setFixedSize(QSize(200, 200))
        #self.setGeometry(100, 100, 200, 100)
        self.setWindowTitle("Settings")
        self.setStyleSheet("QDialog{background-color:rgb(39, 44, 54)}")

        label_title = QLabel("Настройки")

        font = label_title.font();
        font.setFamily('Arial Black')
        font.setPointSize(15)

        label_title.setFont(font)
        label_title.setStyleSheet("color: rgb(85, 170, 255);")
        label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(label_title)
        self.create_checkbox()
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.setText("Сохранить и выйти")
        self.pushButton.setStyleSheet(
            "QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 5px;}"
            "QPushButton:pressed {background-color:rgb(31,101,163) ; }")

    def create_checkbox(self):
        # hbox = QHBoxLayout()

        #global SO2
        #global NO2
        #global CO2

        #SO2 = False
        #NO2 = False
        #CO2 = False

        # these are checkboxes
        self.check1 = QCheckBox("SO2")
        self.check1.setFont(QFont("Arial Black", 13))
        self.check1.setStyleSheet("color: rgb(85, 170, 255);")
        self.check1.toggled.connect(self.item_selected)
        #self.check1.setChecked(True)
        self.verticalLayout.addWidget(self.check1)

        self.check2 = QCheckBox("NO2")
        self.check2.setFont(QFont("Arial Black", 13))
        self.check2.setStyleSheet("color: rgb(85, 170, 255);")
        self.check2.toggled.connect(self.item_selected)
        #self.check2.setChecked(True)
        self.verticalLayout.addWidget(self.check2)

        self.check3 = QCheckBox("CO2")
        self.check3.setFont(QFont("Arial Black", 13))
        self.check3.setStyleSheet("color: rgb(85, 170, 255);")
        self.check3.toggled.connect(self.item_selected)
        #self.check3.setChecked(True)
        self.verticalLayout.addWidget(self.check3)

    def item_selected(self):
        global SO2
        global NO2
        global CO2

        if self.check1.isChecked():
            SO2 = True
        else:
            SO2 = False

        if self.check2.isChecked():
            NO2 = True
        else:
            NO2 = False

        if self.check3.isChecked():
            CO2 = True
        else:
            CO2 = False

    def btnClosed(self):
        self.w2 = MainWindow()
        self.w2.setStyleSheet("MainWindow{background-color:rgb(39, 44, 54)}")

        self.close()
        self.w2.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        global SO2
        global NO2
        global CO2

        self.w2 = SettingsWindow()
        self.setWindowTitle("PEMS-System SUSU")
        # self.setGeometry(100, 100, 800, 400)
        layout = QVBoxLayout()

        self.setFixedSize(QSize(1200, 700))

        label_title = QLabel("Мониторинг выбросов")

        font = label_title.font();
        font.setFamily('Arial Black')
        font.setPointSize(20);

        label_title.setFont(font)
        label_title.setStyleSheet("color: rgb(85, 170, 255);")
        label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(label_title)

        label_namePipe = "Дымовая труба №1"

        label_namePipe = QLabel("Название источника: " + label_namePipe)

        font = label_namePipe.font();
        font.setFamily('Lucida Sans Unicode')
        font.setPointSize(20);

        label_namePipe.setFont(font)

        label_namePipe.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_namePipe.setStyleSheet("color: rgb(85, 170, 255);")
        layout.addWidget(label_namePipe)

        current_datetime = date.today()

        label_Date = QLabel("Дата: " + str(current_datetime))

        font = label_Date.font()
        font.setPointSize(20)
        font.setFamily('Lucida Sans Unicode')

        label_Date.setFont(font)
        label_Date.setStyleSheet("color: rgb(85, 170, 255);")
        label_Date.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(label_Date)

        cbMethod = QComboBox()
        font = cbMethod.font()
        cbMethod.addItems(["Способ №1 (Классический)", "Способ №2 (Маш. обучение)", "Способ №3 (Нейронная сеть)"])
        cbMethod.setStyleSheet("QComboBox::drop-down{width: 0px;height: 0px;border: 0px;}"
                               "QComboBox QAbstractItemView { color: rgb(85, 170, 255);	background-color: "
                               "#373e4e;padding: 10px; selection-background-color: rgb(39, 44, 54);} "
                               )

        cbMethod.currentIndexChanged.connect(self.index_changed)
        cbMethod.editTextChanged.connect(self.text_changed)
        cbMethod.setFixedSize(210, 30)

        a = emissions.Calculate().emissions_calculation(name, NO2, SO2, CO2)

        pic = QLabel("Дата: " + str(current_datetime))
        pic.setPixmap(QPixmap('temp.png'))
        pic.setPixmap(QPixmap('images.png'))

        groupbox1 = QGroupBox()
        groupbox1.setCheckable(False)

        vbox = QVBoxLayout()
        groupbox1.setLayout(vbox)

        vbox.addWidget(pic)

        bLoad = QPushButton("Загрузить")
        bLoad.setCheckable(True)
        bLoad.setStyleSheet("QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 5px;}"
                            "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        bLoad.clicked.connect(self.the_button_was_clicked)
        bLoad.setFixedSize(170, 30)

        bSettings = QPushButton("Настройки")
        bSettings.setCheckable(True)
        bSettings.setStyleSheet("QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 5px;}"
                                "QPushButton:pressed {background-color:rgb(31,101,163) ; }")
        bSettings.clicked.connect(self.the_button_was_clicked)
        bSettings.setFixedSize(170, 30)

        vboxGr1 = QHBoxLayout()
        vboxGr1.addWidget(cbMethod)
        vboxGr1.addWidget(bLoad)
        vboxGr1.addWidget(bSettings)
        vboxGr1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(vboxGr1)

        groupbox2 = QGroupBox()
        groupbox2.setCheckable(False)

        vbox = QVBoxLayout()


        i = 0
        while i < 2:
            a[i] = float('{:.3f}'.format(a[i]))
            i += 1

        # print(a)
        # НЕ СЧИТАЕТСЯ
        label_Stat1 = QLabel("Сера диоксид, SO2 г/м : " + str(a[0]))
        font = label_Stat1.font()
        font.setFamily('Courier New')
        font.setPointSize(20)

        label_Stat1.setFont(font)
        label_Stat1.setStyleSheet("color: rgb(85, 170, 255);")
        label_Stat1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label_Stat2 = QLabel("Азот диоксид, NO2 г/м : " + str(a[0]))
        font = label_Stat2.font()
        font.setFamily('Courier New')
        font.setPointSize(20)

        label_Stat2.setFont(font)
        label_Stat2.setStyleSheet("color: rgb(85, 170, 255);")
        label_Stat2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label_Stat3 = QLabel("Оксид углерода, CO2 : " + str(a[1]))
        font = label_Stat3.font()
        font.setFamily('Courier New')
        font.setPointSize(20)

        label_Stat3.setFont(font)
        label_Stat3.setStyleSheet("color: rgb(85, 170, 255);")
        label_Stat3.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if SO2:
            vbox.addWidget(label_Stat1)
        if NO2:
            vbox.addWidget(label_Stat2)
        if CO2:
            vbox.addWidget(label_Stat3)

        print(SO2)
        print(NO2)
        print(CO2)

        groupbox2.setLayout(vbox)

        vboxGr = QHBoxLayout()
        vboxGr.addWidget(groupbox1)
        if (SO2 or NO2 or CO2):
            vboxGr.addWidget(groupbox2)

        layout.addLayout(vboxGr)

        widget = QWidget()
        widget.setLayout(layout)

        # Устанавливаем центральный виджет окна. Виджет будет расширяться по умолчанию,
        # заполняя всё пространство окна.
        self.setCentralWidget(widget)

    def index_changed(self, i):  # i — это int
        current_method = i + 1
        print(current_method)

    def text_changed(self, s):  # s — это str
        current_method = s
        print(current_method)

    def the_button_was_clicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

        if sender.text() == "Загрузить":
            self.showDialog()
        else:
            self.close()
            self.w2.show()

    def showDialog(self):
        name = QFileDialog.getOpenFileName(self, 'Open file', './~')[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("MainWindow{background-color:rgb(39, 44, 54)}")
    window.show()

    sys.exit(app.exec())
