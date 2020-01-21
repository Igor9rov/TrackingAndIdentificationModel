from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox


class MFRCoordinateSpinBox(QSpinBox):
    """Текстовое поле с вводом координат МФР"""
    def __init__(self, coordinate_name="x", parent=None) -> None:
        QSpinBox.__init__(self, parent)
        # Маскимальная координата МФР
        max_value = 2000
        min_value = -max_value
        self.setPrefix(f"{coordinate_name}: ")
        self.setSuffix(", м")
        # Ограничения на ввод информации
        self.setRange(min_value, max_value)
        # Выравнивание по центру
        self.setAlignment(Qt.AlignHCenter)
        # Значение по умолчанию
        self.setValue(0)
