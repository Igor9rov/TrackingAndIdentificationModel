from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit


class TargetVelocityLineEdit(QLineEdit):
    """
    Поле для ввода скоростей целей, поддерживает ограничения на ввод параметров
    """
    def __init__(self,  coordinate: str = "x", parent=None):
        QLineEdit.__init__(self, parent)
        max_velocity = 700
        min_velocity = -700
        validator = QIntValidator()
        validator.setRange(min_velocity, max_velocity)
        self.setValidator(validator)
        self.setPlaceholderText(f"Скорость {coordinate}, м")

