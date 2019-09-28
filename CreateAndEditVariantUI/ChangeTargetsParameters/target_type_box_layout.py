from PyQt5.QtWidgets import QHBoxLayout, QRadioButton


# Контейнер для ввода типа цели
class TargetTypeBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)

        self.aerodynamic_radio_button = QRadioButton("Аэродинамическая цель")
        self.aerodynamic_radio_button.setChecked(True)
        self.ballistic_radio_button = QRadioButton("Баллистическая цель")

        self.addWidget(self.aerodynamic_radio_button)
        self.addWidget(self.ballistic_radio_button)

    @property
    def type(self):
        return "Aerodynamic" if self.aerodynamic_radio_button.isChecked() else "Ballistic"

    @type.setter
    def type(self, new_type):
        self.aerodynamic_radio_button.setChecked(new_type == "Aerodynamic")
        self.ballistic_radio_button.setChecked(new_type == "Ballistic")
