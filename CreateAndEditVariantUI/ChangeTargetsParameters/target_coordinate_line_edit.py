from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit


class TargetCoordinateLineEdit(QLineEdit):
    """
    Поле для ввода координат цели, поддерживает ограничения на ввод
    """
    def __init__(self, coordinate: str = "x", parent=None):
        QLineEdit.__init__(self, parent)
        max_value_dict = {"x": 150000, "y": 20000, "z": 150000}
        max_value_dict.setdefault(coordinate, 1)
        min_value_dict = {"x": -150000, "y": 0, "z": -150000}
        min_value_dict.setdefault(coordinate, 0)
        validator = QIntValidator()
        validator.setRange(min_value_dict[coordinate], max_value_dict[coordinate])
        self.setValidator(validator)
        self.setPlaceholderText(f"Координата {coordinate}, м")
