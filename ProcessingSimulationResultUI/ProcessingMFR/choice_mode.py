from PyQt5.QtWidgets import QWidget, QComboBox, QLabel, QHBoxLayout


class ChoiceMode(QWidget):
    """Виджет с выбором режима, по которому будет проводиться оценивание"""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Нужные виджеты
        label = QLabel(text="Выберите режим:")
        self.mode_spin_box = QComboBox()
        self.mode_spin_box.addItem("усреднение по всем реализациям")
        self.mode_spin_box.addItem("конкретная реализация")

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.mode_spin_box)
