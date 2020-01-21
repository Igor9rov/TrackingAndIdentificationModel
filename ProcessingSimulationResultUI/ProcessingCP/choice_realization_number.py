from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox


class ChoiceRealizationNumber(QWidget):
    """Виджет с выбором номера реализации"""
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)

        # Нужные компоненты
        label = QLabel(text="Выберите номер реализации:")
        # Спинбокс для выбора номера реализации
        self.spinbox = QSpinBox()
        min_realization_number = 0
        max_realization_number = 1
        self.spinbox.setRange(min_realization_number, max_realization_number)

        # Основной контейнер
        self.main_layout = QHBoxLayout(self)
        self.main_layout.addWidget(label)
        self.main_layout.addWidget(self.spinbox)
