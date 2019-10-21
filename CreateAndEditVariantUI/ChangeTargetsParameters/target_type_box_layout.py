from PyQt5.QtWidgets import QHBoxLayout, QRadioButton


class TargetTypeBoxLayout(QHBoxLayout):
    """
    Контейнер для ввода типа цели
    """
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)

        self.aerodynamic_radio_button = QRadioButton("Аэродинамическая цель")
        self.aerodynamic_radio_button.setChecked(True)
        self.ballistic_radio_button = QRadioButton("Баллистическая цель")

        self.addWidget(self.aerodynamic_radio_button)
        self.addWidget(self.ballistic_radio_button)

    @property
    def type(self):
        """
        :return: Тип цели: аэродинамическая или баллистическая
        """
        return "Aerodynamic" if self.aerodynamic_radio_button.isChecked() else "Ballistic"

    @type.setter
    def type(self, new_type: str):
        """
        Устаналвивает радиобаттон в зависимости от типа цели
        :param new_type: Строка с типом цели
        :return: None
        """
        self.aerodynamic_radio_button.setChecked(new_type == "Aerodynamic")
        self.ballistic_radio_button.setChecked(new_type == "Ballistic")
