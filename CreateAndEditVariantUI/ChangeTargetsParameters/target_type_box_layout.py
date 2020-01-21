from PyQt5.QtWidgets import QHBoxLayout, QRadioButton


class TargetTypeBoxLayout(QHBoxLayout):
    """Контейнер для ввода типа цели"""
    def __init__(self, parent=None) -> None:
        QHBoxLayout.__init__(self, parent)

        self.aerodynamic_radio_button = QRadioButton("Аэродинамическая цель")
        self.aerodynamic_radio_button.setChecked(True)
        self.ballistic_radio_button = QRadioButton("Баллистическая цель")

        self.addWidget(self.aerodynamic_radio_button)
        self.addWidget(self.ballistic_radio_button)

    @property
    def type(self) -> str:
        """
        :return: Тип цели: аэродинамическая или баллистическая
        :rtype: str
        """
        return "Aerodynamic" if self.aerodynamic_radio_button.isChecked() else "Ballistic"

    @type.setter
    def type(self, new_type: str) -> None:
        """Устаналвивает радиобаттон в зависимости от типа цели

        :param new_type: Строка с типом цели
        :type new_type: str

        :return: None
        """
        self.aerodynamic_radio_button.setChecked(new_type == "Aerodynamic")
        self.ballistic_radio_button.setChecked(new_type == "Ballistic")
