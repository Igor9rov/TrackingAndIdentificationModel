from PyQt5.QtWidgets import QGroupBox, QPushButton, QHBoxLayout, QLabel


class ChoiceInputFileGroupBox(QGroupBox):
    """
    GroupBox для выбора файла с вариантом моделирования
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выберите файл с вариантом моделирования", parent=parent)

        # Все компоненты
        self.path_label = QLabel("Файл не выбран")
        self.button = QPushButton("Выберите файл")

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(self.path_label)
        layout.addWidget(self.button)

        # Переменная с сохранённым вариантом моделирования
        self.variant = None
