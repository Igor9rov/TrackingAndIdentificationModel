from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
import sys


class SaveJsonFileDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        QtWidgets.QFileDialog.__init__(self, parent, caption="Сохранить параметр моделирования")
        self.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        self.setNameFilter("JSON файлы (*.json)")


class SaveFileWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.save_file_button = QtWidgets.QPushButton("Сохранить вариант моделирования")
        self.main_layout.addWidget(self.save_file_button)

        self.save_file_button.clicked.connect(self.show_save_file_dialog)

    @pyqtSlot()
    def show_save_file_dialog(self):
        window = SaveJsonFileDialog(self)
        window.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = SaveFileWidget()
    application.show()
    sys.exit(app.exec())
