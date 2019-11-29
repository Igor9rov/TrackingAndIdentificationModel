from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QFormLayout

from fixed_part_errors_layout import FixedPartErrorsLayout
from mfr_coordinate_spin_box import MFRCoordinateSpinBox
from mobile_part_errors_layout import MobilePartErrorsLayout
from structure_of_variant import KeyMFR, KeyMFRError


class ChangeOneMfrParametersWidget(QGroupBox):
    """Виджет для изменения параметров одного МФР"""
    def __init__(self, mfr_number: int = 0, parent=None):
        QGroupBox.__init__(self, f"МФР №{mfr_number}:", parent)
        # Сохраним номер МФР в экземпляре
        self.number = mfr_number

        # Основные компоненты
        self.coordinate_spin_boxes = [MFRCoordinateSpinBox(coord) for coord in ["x", "y", "z"]]
        coordinates_layout = QHBoxLayout()
        for spin_box in self.coordinate_spin_boxes:
            coordinates_layout.addWidget(spin_box)

        self.mobile_part_layout = MobilePartErrorsLayout()
        self.fixed_part_layout = FixedPartErrorsLayout()
        # Основной контейнер
        layout = QFormLayout(self)
        layout.addRow("Координаты точки стояния:", coordinates_layout)
        layout.addRow("Ошибки в определении углов \nнеподвижной части антенны:", self.fixed_part_layout)
        layout.addRow("Ошибки в определении углов \nподвижной части антенны:", self.mobile_part_layout)

        # Сделаем его возможным для отмечания галкой
        self.setCheckable(True)

    @property
    def coordinates(self) -> list:
        """Точка стояния МФР

        :return: Координаты МФР
        :rtype: list
        """
        return [spin_box.value() for spin_box in self.coordinate_spin_boxes]

    @coordinates.setter
    def coordinates(self, new_coordinates: list):
        """Устанавливает координаты МФР

        :param new_coordinates: Список с координатами x, y, z
        :return: None
        """
        for index, spin_box in enumerate(self.coordinate_spin_boxes):
            spin_box.setValue(new_coordinates[index])

    @property
    def errors(self) -> dict:
        """Ошибки в определении собственных переменных одним МФР
        :return: Словарь с параметрами
        :rtype: dict
        """
        return {KeyMFRError.beta_north: self.fixed_part_layout.beta_north.error_angle,
                KeyMFRError.beta: self.mobile_part_layout.beta.error_angle}

    @errors.setter
    def errors(self, new_errors: dict):
        """Устанавливает в виджеты ошибки в определеннии собственных переменных МФР

        :param new_errors: Словарь с параметрами
        :type new_errors: dict

        :return: None
        """
        self.fixed_part_layout.beta_north.error_angle = new_errors[KeyMFRError.beta_north]
        self.mobile_part_layout.beta.error_angle = new_errors[KeyMFRError.beta]

    @property
    def parameters(self) -> dict:
        """
        :return: Параметры одного МФР
        :rtype: dict
        """
        return {KeyMFR.coordinates: self.coordinates,
                KeyMFR.errors: self.errors}

    @parameters.setter
    def parameters(self, new_parameters: dict):
        """Устанавливает параметры МФР

        :param new_parameters: Словарь с параметрами МФР
        :type new_parameters: dict

        :return: None
        """
        self.coordinates = new_parameters[KeyMFR.coordinates]
        self.errors = new_parameters[KeyMFR.errors]

    def clear(self):
        """Очищает виджет

        :return: None
        """
        self.setChecked(False)
        for spin_box in self.coordinate_spin_boxes:
            spin_box.setValue(0)
