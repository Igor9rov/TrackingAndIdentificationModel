from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpinBox


class ErrorAngleSpinBox(QSpinBox):
    """Класс определяет SpinBox для ввода ошибок по углам при обзоре МФР"""
    def __init__(self, label: str = "", parent=None) -> None:
        QSpinBox.__init__(self, parent)
        # Максимальное значение ошибки
        error_threshold = 30
        self.setRange(-error_threshold, error_threshold)
        self.setPrefix(label)
        self.setSuffix(" угловых минут")
        # Значение внутри поля изменяется по кругу
        self.setWrapping(True)
        # Значение по умолчанию
        self.setValue(0)
        # Выравнивание
        self.setAlignment(Qt.AlignRight)

    @property
    def error_angle(self) -> int:
        """Возрващает ошибку по углам

        :return: Ошибка по углам
        """
        return self.value()

    @error_angle.setter
    def error_angle(self, new_value: int) -> None:
        """Установка значения ошибки по углам

        :return: None
        """
        self.setValue(new_value)
