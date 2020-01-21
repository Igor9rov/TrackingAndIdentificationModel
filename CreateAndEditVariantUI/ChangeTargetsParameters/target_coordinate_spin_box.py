from PyQt5.QtWidgets import QSpinBox


class TargetCoordinateSpinBox(QSpinBox):
    """Поле для ввода координат цели, поддерживает ограничения на ввод"""
    def __init__(self, coordinate: str = "x", parent=None) -> None:
        QSpinBox.__init__(self, parent)
        max_value_dict = {"x": 150000, "y": 20000, "z": 150000}
        max_value_dict.setdefault(coordinate, 1)
        min_value_dict = {"x": -150000, "y": 0, "z": -150000}
        min_value_dict.setdefault(coordinate, 0)
        self.setRange(min_value_dict[coordinate], max_value_dict[coordinate])
        self.setPrefix(f"{coordinate}: ")
        self.setSuffix(", м")
        # Значение по умолчанию
        self.setValue(0)
