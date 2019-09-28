from PyQt5.QtWidgets import QHBoxLayout

from target_coordinate_line_edit import TargetCoordinateLineEdit


# Контейнер с вводом всех трёх координат цели
class TargetCoordinatesBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        self.x_coordinate_line_edit = TargetCoordinateLineEdit("x")
        self.addWidget(self.x_coordinate_line_edit)
        self.y_coordinate_line_edit = TargetCoordinateLineEdit("y")
        self.addWidget(self.y_coordinate_line_edit)
        self.z_coordinate_line_edit = TargetCoordinateLineEdit("z")
        self.addWidget(self.z_coordinate_line_edit)

    # Попытка получения координат
    def can_get_coordinates(self):
        try:
            _ = self.coordinates
        except ValueError:
            return False
        return True

    # Координаты
    @property
    def coordinates(self):
        return [float(self.x_coordinate_line_edit.text()),
                float(self.y_coordinate_line_edit.text()),
                float(self.z_coordinate_line_edit.text())]

    @coordinates.setter
    def coordinates(self, new_coordinates):
        self.x_coordinate_line_edit.setText(str(new_coordinates[0]))
        self.y_coordinate_line_edit.setText(str(new_coordinates[1]))
        self.z_coordinate_line_edit.setText(str(new_coordinates[2]))
