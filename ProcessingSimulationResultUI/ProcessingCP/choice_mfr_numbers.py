from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox


class ChoiceMFRNumbers(QWidget):
    """
    Выджет с выбором номеров МФР
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Нужные компоненты
        label = QLabel(text="Выберите номера МФР, от которых\n нужны трассы целей")

        self.first_mfr_number_combo_box = QComboBox()
        self.first_mfr_number_combo_box.addItems(["1", "2", "3"])

        self.second_mfr_number_combo_box = QComboBox()
        self.second_mfr_number_combo_box.addItems(["1", "2", "3"])

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.first_mfr_number_combo_box)
        layout.addWidget(self.second_mfr_number_combo_box)
