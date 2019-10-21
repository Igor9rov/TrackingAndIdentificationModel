from PyQt5.QtWidgets import QHBoxLayout, QPushButton


class LayoutWithBackAndNextButtons(QHBoxLayout):
    """
    Контейнер с кнопками назад и далее
    """
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        # Основные компоненты
        self.back_button = QPushButton("Назад")
        self.next_button = QPushButton("Далее")
        # Добавим их
        self.addWidget(self.back_button)
        self.addWidget(self.next_button)
