from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox


class ChoiceMFRNumber(QWidget):
    """
    Выджет с выбором номеров МФР
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Нужные компоненты
        label = QLabel(text="Выберите номер МФР, от\nкоторого нужна трасса цели")

        self.mfr_number_combo_box = QComboBox()
        self.mfr_number_combo_box.addItems(["1", "2", "3"])

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.mfr_number_combo_box)
