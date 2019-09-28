from PyQt5.QtWidgets import QHBoxLayout, QPushButton


# Контейнер с кнопками назад и далее
class LayoutWithBackAndNextButtons(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)

        self.back_button = QPushButton("Назад")
        self.addWidget(self.back_button)

        self.next_button = QPushButton("Далее")
        self.addWidget(self.next_button)
