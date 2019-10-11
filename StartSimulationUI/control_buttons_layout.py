from PyQt5.QtWidgets import QHBoxLayout, QPushButton


class ControlButtonsLayout(QHBoxLayout):
    """
    Контейнер с кнопками управления
    """
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)

        # Нужные кнопки
        self.stop_button = QPushButton("Стоп")
        self.start_button = QPushButton("Старт")

        # Добавим их
        self.addWidget(self.stop_button)
        self.addWidget(self.start_button)
