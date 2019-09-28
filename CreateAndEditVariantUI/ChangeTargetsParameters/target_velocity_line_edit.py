from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit


# Поле для ввода скоростей целей
class TargetVelocityLineEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        max_velocity = 700
        min_velocity = -700
        validator = QIntValidator()
        validator.setRange(min_velocity, max_velocity)
        self.setValidator(validator)
