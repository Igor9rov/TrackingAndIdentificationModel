from PyQt5.QtWidgets import QHBoxLayout

from target_coordinate_line_edit import TargetCoordinateLineEdit


class TargetCoordinatesBoxLayout(QHBoxLayout):
    """
    Контейнер с вводом всех координат цели
    """
    def __init__(self, parent=None):
        QHBoxLayout.__init__(self, parent)
        # Основные компоненты
        self.coordinate_lines_edit = [TargetCoordinateLineEdit(f"{coord}") for coord in ["x", "y", "z"]]
        # Добавим их в контейнер
        for line_edit in self.coordinate_lines_edit:
            self.addWidget(line_edit)

    def can_get_coordinates(self):
        """
        :return: True/False в зависимости от того, можно ли получить координаты
        """
        try:
            _ = self.coordinates
        except ValueError:
            return False
        return True

    @property
    def coordinates(self):
        """
        :raise: ValueError если пользователь не ввёл ничего
        :return: Список координат цели
        """
        return [float(line_edit.text()) for line_edit in self.coordinate_lines_edit]

    @coordinates.setter
    def coordinates(self, new_coordinates: list):
        """
        Устанавливает координаты целей
        :param new_coordinates: Список координат целей
        :return: None
        """
        for index, line_edit in enumerate(self.coordinate_lines_edit):
            line_edit.setText(str(new_coordinates[index]))
