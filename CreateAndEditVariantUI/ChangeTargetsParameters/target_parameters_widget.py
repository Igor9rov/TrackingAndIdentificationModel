from PyQt5.QtWidgets import QWidget, QFormLayout

from structure_of_variant import KeyTarget
from target_coordinates_box_layout import TargetCoordinatesBoxLayout
from target_parameters_associated_with_mfr import TargetParametersAssociatedWithMFR
from target_type_box_layout import TargetTypeBoxLayout
from target_velocities_box_layout import TargetVelocitiesBoxLayout


class TargetParametersWidget(QWidget):
    """
    Виджет для редактирования параметров одной цели, появляется в таблице
    """
    def __init__(self, number_target: int, mfr_numbers: list, parent=None) -> None:
        QWidget.__init__(self, parent)
        # Номер цели
        self.number_target = number_target

        # Основные компоненты
        self.coordinates_box = TargetCoordinatesBoxLayout()
        self.velocities_box = TargetVelocitiesBoxLayout()
        self.target_type_box = TargetTypeBoxLayout()
        self.mfr_parameters_widgets = [TargetParametersAssociatedWithMFR(number=num) for num in mfr_numbers]

        # Основной контейнер
        self.form_layout = QFormLayout(self)
        self.form_layout.addRow("Координаты:", self.coordinates_box)
        self.form_layout.addRow("Скорость:", self.velocities_box)
        self.form_layout.addRow("Тип цели:", self.target_type_box)
        # Для каждого из МФР добавить виджет с редактированием его параметров
        for mfr_parameters_widget in self.mfr_parameters_widgets:
            self.form_layout.addRow(f"МФР №{mfr_parameters_widget.number}:", mfr_parameters_widget)

    def delete_all_mfr_widgets(self) -> None:
        """Очистить виджеты связанные с МФР

        :return: None
        """
        for mfr_widget in self.mfr_parameters_widgets:
            self.form_layout.removeRow(mfr_widget)
        self.mfr_parameters_widgets = []

    def add_mfr_widgets_with_numbers(self, added_mfr_numbers: set) -> None:
        """Добавить виджетов для редактирования параметров МФР

        :param added_mfr_numbers: Множество добавленнных номеров МФР
        :type added_mfr_numbers: set

        :return: None
        """
        added_mfr_widgets = [TargetParametersAssociatedWithMFR(number=num) for num in added_mfr_numbers]
        for widget in added_mfr_widgets:
            self.mfr_parameters_widgets.append(widget)
            self.form_layout.addRow(f"МФР №{widget.number}:", widget)

    def delete_mfr_widgets_with_numbers(self, deleted_mfr_numbers: set) -> None:
        """Удалить виджеты для редактирования параметров МФР по номерам

        :param deleted_mfr_numbers: Множество удалённых номеров МФР
        :type deleted_mfr_numbers: set

        :return: None
        """
        # Сначала удалим строки в форме
        for widget in self.mfr_parameters_widgets:
            if widget.number in deleted_mfr_numbers:
                self.form_layout.removeRow(widget)
        # Потом из списка
        self.mfr_parameters_widgets = [widget for widget in self.mfr_parameters_widgets
                                       if widget.number not in deleted_mfr_numbers]

    @property
    def mfr_numbers(self) -> list:
        """
        :return: Номера МФР
        :rtype: list
        """
        return [widget.number for widget in self.mfr_parameters_widgets]

    @property
    def has_coordinates(self) -> bool:
        """
        :return: True/False в зависимости от того, можем ли мы получить координаты
        :rtype: bool
        """
        return self.coordinates_box.can_get_coordinates()

    @property
    def has_velocities(self) -> bool:
        """
        :return: True/False в зависимости от того, можем ли мы получить скорость
        :rtype: bool
        """
        return self.velocities_box.can_get_velocities()

    @property
    def mfr_parameters(self) -> dict:
        """
        :return: Словарь параметров с ключом равным номеру МФР, и значением равным параметрам цели по этому МФР
        :rtype: dict
        """
        return dict(zip(self.mfr_numbers, [widget.parameters for widget in self.mfr_parameters_widgets]))

    @mfr_parameters.setter
    def mfr_parameters(self, new_parameters: dict) -> None:
        """Устанавливает параметры целей, связанные с МФР

        :param new_parameters: Словарь с параметрами
        :type new_parameters: dict

        :return: None
        """
        self.delete_all_mfr_widgets()
        self.mfr_parameters_widgets = [TargetParametersAssociatedWithMFR(number=num) for num in new_parameters]
        for mfr_parameters_widget in self.mfr_parameters_widgets:
            self.form_layout.addRow(f"МФР №{mfr_parameters_widget.number}:", mfr_parameters_widget)
            mfr_parameters_widget.parameters = new_parameters[mfr_parameters_widget.number]

    @property
    def parameters(self) -> dict:
        """
        :return: Словарь из параметров одной цели
        :rtype: dict
        """
        return {KeyTarget.coordinates: self.coordinates_box.coordinates,
                KeyTarget.velocities: self.velocities_box.velocities,
                KeyTarget.type: self.target_type_box.type,
                KeyTarget.mfr: self.mfr_parameters}

    @parameters.setter
    def parameters(self, new_parameters: dict) -> None:
        """Устанавливает параметры одной цели

        :param new_parameters: Словарь параметров одной цели
        :type new_parameters: dict

        :return: None
        """
        self.coordinates_box.coordinates = new_parameters[KeyTarget.coordinates]
        self.velocities_box.velocities = new_parameters[KeyTarget.velocities]
        self.target_type_box.type = new_parameters[KeyTarget.type]
        self.mfr_parameters = new_parameters[KeyTarget.mfr]
