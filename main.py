import sys
from datetime import datetime, date
from random import random, randint
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *

current_method = 1

SO2_statistic = randint(1, 100)
NO2_statistic = randint(1, 100)
CO2_statistic = randint(1, 100)


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.setGeometry(100, 100, 400, 400)
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

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.setText("Сохранить и выйти")
        self.pushButton.setStyleSheet(
            "QPushButton {background-color: rgb(51,122,183); color: White; border-radius: 5px;}"
            "QPushButton:pressed {background-color:rgb(31,101,163) ; }")

    def btnClosed(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w2 = SettingsWindow()
        self.setWindowTitle("PEMS-System SUSU")
        # self.setGeometry(100, 100, 800, 400)
        layout = QVBoxLayout()

        self.setFixedSize(QSize(800, 400))

        label_title = QLabel("Мониторинг выбросов")

        font = label_title.font();
        font.setFamily('Arial Black')
        font.setPointSize(15);

        label_title.setFont(font)
        label_title.setStyleSheet("color: rgb(85, 170, 255);")
        label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(label_title)

        label_namePipe = "Дымовая труба №1"

        label_namePipe = QLabel("Название источника: " + label_namePipe)

        font = label_namePipe.font();
        font.setFamily('Lucida Sans Unicode')
        font.setPointSize(15);

        label_namePipe.setFont(font)

        label_namePipe.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label_namePipe.setStyleSheet("color: rgb(85, 170, 255);")
        layout.addWidget(label_namePipe)

        current_datetime = date.today()

        label_Date = QLabel("Дата: " + str(current_datetime))

        font = label_Date.font()
        font.setPointSize(15)
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

        pic = QLabel("Дата: " + str(current_datetime))
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
        groupbox2.setLayout(vbox)

        label_Stat1 = QLabel("Сера диоксид, SO2 г/м : " + str(SO2_statistic))
        font = label_Stat1.font()
        font.setFamily('Courier New')
        font.setPointSize(15)

        label_Stat1.setFont(font)
        label_Stat1.setStyleSheet("color: rgb(85, 170, 255);")
        label_Stat1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label_Stat2 = QLabel("Азот диоксид, NO2 г/м : " + str(NO2_statistic))
        font = label_Stat2.font()
        font.setFamily('Courier New')
        font.setPointSize(15)

        label_Stat2.setFont(font)
        label_Stat2.setStyleSheet("color: rgb(85, 170, 255);")
        label_Stat2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        label_Stat3 = QLabel("Оксид углерода, CO2 : " + str(CO2_statistic))
        font = label_Stat3.font()
        font.setFamily('Courier New')
        font.setPointSize(15)

        label_Stat3.setFont(font)
        label_Stat3.setStyleSheet("color: rgb(85, 170, 255);")
        label_Stat3.setAlignment(Qt.AlignmentFlag.AlignLeft)

        vbox.addWidget(label_Stat1)
        vbox.addWidget(label_Stat2)
        vbox.addWidget(label_Stat3)

        vboxGr = QHBoxLayout()
        vboxGr.addWidget(groupbox1)
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
            self.w2.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './~')[0]
        try:
            f = open(fname, 'r')
            with f:
                data = f.read()
                print(data)
                f.close()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("MainWindow{background-color:rgb(39, 44, 54)}")
    window.show()

    sys.exit(app.exec())
