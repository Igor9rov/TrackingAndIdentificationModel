from PyQt5.QtWidgets import QHBoxLayout

from target_velocity_line_edit import TargetVelocityLineEdit


# Контейнер с вводом всех трёх скоростей цели
class TargetVelocitiesBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        self.x_velocity_line_edit = TargetVelocityLineEdit()
        self.addWidget(self.x_velocity_line_edit)

        self.y_velocity_line_edit = TargetVelocityLineEdit()
        self.addWidget(self.y_velocity_line_edit)

        self.z_velocity_line_edit = TargetVelocityLineEdit()
        self.addWidget(self.z_velocity_line_edit)

    # Попытка получения скоростей
    def can_get_velocities(self):
        try:
            _ = self.velocities
        except ValueError:
            return False
        return True

    # Скорость
    @property
    def velocities(self):
        return [float(self.x_velocity_line_edit.text()),
                float(self.y_velocity_line_edit.text()),
                float(self.z_velocity_line_edit.text())]

    @velocities.setter
    def velocities(self, new_velocities):
        self.x_velocity_line_edit.setText(str(new_velocities[0]))
        self.y_velocity_line_edit.setText(str(new_velocities[1]))
        self.z_velocity_line_edit.setText(str(new_velocities[2]))
