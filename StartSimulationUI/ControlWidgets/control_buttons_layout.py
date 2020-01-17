from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QPushButton


class ControlButtonsLayout(QHBoxLayout):
    """Контейнер с кнопками управления"""
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)

        # Нужные кнопки
        self.stop_button = QPushButton("Стоп")
        self.start_button = QPushButton("Старт")

        # Добавим их
        self.addWidget(self.stop_button)
        self.addWidget(self.start_button)

        # И выключим, чтоб не трогали
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)

    @pyqtSlot()
    def start_button_on(self):
        """Активация конпки старт

        :return: None
        """
        self.start_button.setEnabled(True)
