from PyQt5.QtWidgets import QGroupBox, QPushButton, QHBoxLayout, QLabel


class ChoiceOutputFileGroupBox(QGroupBox):
    """
    GroupBox для выбора файла для сохранения варианта моделирования
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выберите файл для сохранения результатов моделирования", parent=parent)

        # Все компоненты
        self.path_label = QLabel("Путь к файлу")
        self.button = QPushButton("Выберите файл")

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(self.path_label)
        layout.addWidget(self.button)

        self.button.setEnabled(False)
