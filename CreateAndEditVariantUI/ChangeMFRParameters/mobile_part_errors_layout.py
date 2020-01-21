from PyQt5.QtWidgets import QVBoxLayout

from error_angle_spin_box import ErrorAngleSpinBox


class MobilePartErrorsLayout(QVBoxLayout):
    """Определяет контейнер с данными по ошибкам углов, определяющих положение подвижной части антенны"""
    def __init__(self, parent=None) -> None:
        QVBoxLayout.__init__(self, parent)
        self.gamma = ErrorAngleSpinBox(label="Угол скручивания антенны ")
        self.eps = ErrorAngleSpinBox(label="Угол наклона антенны ")
        self.beta = ErrorAngleSpinBox(label="Азимут оси антенны ")

        self.addWidget(self.gamma)
        self.addWidget(self.eps)
        self.addWidget(self.beta)

        # Пока отключим (не используем)
        self.gamma.setEnabled(False)
        self.eps.setEnabled(False)
