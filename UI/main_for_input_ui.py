from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from input_design import Ui_MainWindow
import sys
"""
Чтобы сконвертить .ui в .py в терминале:
pyuic5 InputUI.ui -o input_design.py
"""

"""
# Подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton.clicked.connect(self.btn_clicked)
        self.ui.pushButton.setText("Ракеты на Америку")

        # Работа с QLabel
        self.ui.label.setFont(QtGui.QFont("SansSerif", 30))
        self.ui.label.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.ui.label.setText("Anything...")

        # Работа с QLineEdit
        self.ui.lineEdit.setText("Мдээээ")

        self.ui.lineEdit_2.setMaxLength(10)

        self.ui.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)

        self.ui.lineEdit_4.setReadOnly(True)

        self.ui.lineEdit_5.setStyleSheet("color: rgb(28, 43, 255);")

        self.ui.lineEdit_6.setStyleSheet("background-color: rgb(28, 43, 255);")

    def btn_clicked(self):
        self.ui.label.setText("Button pressed!")
        # Если не использовать, то часть текста исчезнет
        # self.ui.label.adjustSize()   
"""


class InputWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(InputWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = InputWindow()
    application.show()

    sys.exit(app.exec())
