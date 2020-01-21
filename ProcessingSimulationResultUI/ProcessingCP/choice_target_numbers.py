from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox


class ChoiceTargetNumbers(QWidget):
    """Виджет с выбором номеров целей"""
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)

        # Нужные компоненты
        label = QLabel(text="Выберите номера целей:")

        self.first_target_number_combo_box = QComboBox()
        self.first_target_number_combo_box.addItems(["1", "2", "3"])

        self.second_target_number_combo_box = QComboBox()
        self.second_target_number_combo_box.addItems(["1", "2", "3"])

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.first_target_number_combo_box)
        layout.addWidget(self.second_target_number_combo_box)
