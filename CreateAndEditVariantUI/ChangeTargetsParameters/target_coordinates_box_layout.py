from PyQt5.QtWidgets import QHBoxLayout

from target_coordinate_spin_box import TargetCoordinateSpinBox


class TargetCoordinatesBoxLayout(QHBoxLayout):
    """Контейнер с вводом всех координат цели"""
    def __init__(self, parent=None) -> None:
        QHBoxLayout.__init__(self, parent)
        # Основные компоненты
        self.coordinate_spin_boxes = [TargetCoordinateSpinBox(f"{coord}") for coord in ["x", "y", "z"]]
        # Добавим их в контейнер
        for spin_box in self.coordinate_spin_boxes:
            self.addWidget(spin_box)

    @property
    def coordinates(self) -> list:
        """Получает координаты цели в виде списка из 3 элементов

        :return: Список координат цели
        :rtype: list
        """
        return [spin_box.value() for spin_box in self.coordinate_spin_boxes]

    @coordinates.setter
    def coordinates(self, new_coordinates: list) -> None:
        """Устанавливает координаты целей

        :param new_coordinates: Список координат целей
        :type new_coordinates: list

        :return: None
        """
        for index, spin_box in enumerate(self.coordinate_spin_boxes):
            spin_box.setValue(new_coordinates[index])
