from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QWidget, QGroupBox, QSpinBox

from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons
from structure_of_variant import KeyTime


class ChangeTimeParametersWidget(QWidget):
    """
    Виджет для изменения временных параметров варианта
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Основные компоненты
        # Ввод времени моделирования
        self.modelling_spin_box = QSpinBox()
        self.modelling_spin_box.setAlignment(Qt.AlignHCenter)
        self.modelling_spin_box.setRange(1, 600)

        # Ввод числа повторений варианта моделирования
        self.repeating_spin_box = QSpinBox()
        self.repeating_spin_box.setAlignment(Qt.AlignHCenter)
        self.repeating_spin_box.setRange(1, 100000)

        # Основная группа виджетов
        self.main_group = QGroupBox("Укажите временные параметры моделируемого варианта")
        # Внутри группы контейнер для компонентов формы
        self.main_group_form_layout = QFormLayout(self.main_group)
        self.main_group_form_layout.addRow("Время моделирования в секундах:", self.modelling_spin_box)
        self.main_group_form_layout.addRow("Число повторений варианта моделирования:", self.repeating_spin_box)

        # Контейнер с конпками назад/далее
        control_layout = LayoutWithBackAndNextButtons()

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.main_group)
        main_layout.addLayout(control_layout)

        # Для удобного доступа к кнопкам
        self.next_button = control_layout.next_button
        self.back_button = control_layout.back_button

    @property
    def parameters(self):
        """
        :return: Словарь параметров
        """
        return {KeyTime.modelling: self.modelling_spin_box.value(),
                KeyTime.repeating: self.repeating_spin_box.value()}

    @parameters.setter
    def parameters(self, new_parameters: dict):
        """
        Установка параметров
        :param new_parameters: Словарь с параметрами времени
        :return: None
        """
        self.modelling_spin_box.setValue(new_parameters[KeyTime.modelling])
        self.repeating_spin_box.setValue(new_parameters[KeyTime.repeating])

    def clear(self):
        """
        Очищение введённых от пользователя параметров
        :return: None
        """
        self.modelling_spin_box.setValue(1)
        self.repeating_spin_box.setValue(1)
