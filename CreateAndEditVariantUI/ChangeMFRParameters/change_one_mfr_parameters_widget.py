from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel

from mfr_coordinate_ine_edit import MFRCoordinateLineEdit
from structure_of_variant import KeyMFR


# Виджет для изменения параметров одного МФР
class ChangeOneMfrParametersWidget(QGroupBox):
    def __init__(self, mfr_number="0", parent=None):
        QGroupBox.__init__(self, f"МФР №{mfr_number}:", parent)
        self.number = mfr_number
        self.setCheckable(True)

        self.main_layout = QHBoxLayout(self)

        self.coordinates_label = QLabel(f"Координаты МФР №{mfr_number}:")
        self.main_layout.addWidget(self.coordinates_label)

        self.x_coordinate_line_edit = MFRCoordinateLineEdit("x")
        self.main_layout.addWidget(self.x_coordinate_line_edit)

        self.y_coordinate_line_edit = MFRCoordinateLineEdit("y")
        self.main_layout.addWidget(self.y_coordinate_line_edit)

        self.z_coordinate_line_edit = MFRCoordinateLineEdit("z")
        self.main_layout.addWidget(self.z_coordinate_line_edit)

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

    # Получение параметров одного МФР
    @property
    def parameters(self):
        return {KeyMFR.coordinates: self.coordinates}

    @parameters.setter
    def parameters(self, new_parameters: dict):
        self.coordinates = new_parameters[KeyMFR.coordinates]

    def clear(self):
        self.setChecked(False)
        self.x_coordinate_line_edit.clear()
        self.y_coordinate_line_edit.clear()
        self.z_coordinate_line_edit.clear()
