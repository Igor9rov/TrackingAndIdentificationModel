from PyQt5.QtWidgets import QSpinBox


class TargetVelocitySpinBox(QSpinBox):
    """Поле для ввода скоростей целей, поддерживает ограничения на ввод параметров"""
    def __init__(self,  coordinate: str = "x", parent=None):
        QSpinBox.__init__(self, parent)
        max_velocity = 700
        min_velocity = -700
        self.setRange(min_velocity, max_velocity)
        self.setPrefix(f"{coordinate}: ")
        self.setSuffix(", м")
        # Значение по умолчанию
        self.setValue(0)
