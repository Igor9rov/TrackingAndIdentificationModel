from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit


class MFRCoordinateLineEdit(QLineEdit):
    """
    Текстовое поле с вводом координат МФР
    """
    def __init__(self, coordinate_name="x", parent=None):
        QLineEdit.__init__(self, parent)
        # Маскимальная координата МФР
        max_value = 2000
        min_value = -max_value
        self.setPlaceholderText(f"Координата {coordinate_name}, м")
        # Ограничения на ввод информации
        self.setValidator(QIntValidator(min_value, max_value))
        # Выравнивание по центру
        self.setAlignment(Qt.AlignHCenter)
