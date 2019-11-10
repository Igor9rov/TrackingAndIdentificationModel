from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox


class ChoiceTargetNumber(QWidget):
    """Виджет с выбором номера цели"""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Нужные компоненты
        label = QLabel(text="Выберите номер цели:")

        self.target_number_combo_box = QComboBox()
        self.target_number_combo_box.addItems(["1", "2", "3"])

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.target_number_combo_box)
