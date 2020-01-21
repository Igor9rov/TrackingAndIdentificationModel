from PyQt5.QtWidgets import QVBoxLayout

from error_angle_spin_box import ErrorAngleSpinBox


class FixedPartErrorsLayout(QVBoxLayout):
    """Определяет контейнер с данными по ошибкам углов, определяющих положение неподвижной части антенны"""
    def __init__(self, parent=None) -> None:
        QVBoxLayout.__init__(self, parent)

        self.beta_north = ErrorAngleSpinBox(label="Азимут строительной оси относительно направления на 'Север' ")
        self.eps_long = ErrorAngleSpinBox(label="Угол невертикальности в продольной плоскости ")
        self.eps_cross = ErrorAngleSpinBox(label="Угол невертикальности в поперечной плоскости ")

        self.addWidget(self.beta_north)
        self.addWidget(self.eps_long)
        self.addWidget(self.eps_cross)

        # Пока отключим (не используем)
        self.eps_long.setEnabled(False)
        self.eps_cross.setEnabled(False)
