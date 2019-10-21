from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel

from mfr_coordinate_line_edit import MFRCoordinateLineEdit
from structure_of_variant import KeyMFR


class ChangeOneMfrParametersWidget(QGroupBox):
    """
    Виджет для изменения параметров одного МФР
    """
    def __init__(self, mfr_number: str = "0", parent=None):
        QGroupBox.__init__(self, f"МФР №{mfr_number}:", parent)
        # Сохраним номер МФР в экземпляре
        self.number = mfr_number

        # Основные компоненты
        coordinates_label = QLabel(f"Координаты МФР №{mfr_number}:")
        self.coordinate_lines_edit = [MFRCoordinateLineEdit(coord) for coord in ["x", "y", "z"]]

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(coordinates_label)
        for line_edit in self.coordinate_lines_edit:
            layout.addWidget(line_edit)

        # Сделаем его возможным для отмечания галкой
        self.setCheckable(True)

    def can_get_coordinates(self):
        """
        Попытка получения координат, можем поймать исключение ValueError, если пользователь ничего не введёт
        :return: True/False в зависимости от успеха попытки
        """
        try:
            _ = self.coordinates
        except ValueError:
            return False
        return True

    @property
    def coordinates(self):
        """
        :raise: ValueError Если пользователь ничего не ввёл
        :return: Координаты МФР
        """
        return [float(line_edit.text()) for line_edit in self.coordinate_lines_edit]

    @coordinates.setter
    def coordinates(self, new_coordinates: list):
        """
        Устанавливает координаты МФР
        :param new_coordinates: Список с координатами x, y, z
        :return: None
        """
        for index, line_edit in enumerate(self.coordinate_lines_edit):
            line_edit.setText(str(new_coordinates[index]))

    @property
    def parameters(self):
        """
        :return: Параметры одного МФР
        """
        return {KeyMFR.coordinates: self.coordinates}

    @parameters.setter
    def parameters(self, new_parameters: dict):
        """
        Устанавливает параметры МФР
        :param new_parameters: Словарь с параметрами МФР
        :return: None
        """
        self.coordinates = new_parameters[KeyMFR.coordinates]

    def clear(self):
        """
        Очищает виджет
        :return: None
        """
        self.setChecked(False)
        for line_edit in self.coordinate_lines_edit:
            line_edit.clear()
