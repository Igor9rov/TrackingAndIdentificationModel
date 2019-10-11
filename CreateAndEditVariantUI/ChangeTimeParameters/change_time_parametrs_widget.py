from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout
from PyQt5.QtWidgets import QWidget, QGroupBox, QSpinBox

from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons
from structure_of_variant import KeyTime


# Класс для изменения временных параметров варианта
class ChangeTimeParametersWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # Основной контейнер
        self.main_layout = QVBoxLayout(self)
        # Основная группа виджетов
        self.main_group = QGroupBox("Укажите временные параметры моделируемого варианта")
        self.main_layout.addWidget(self.main_group)
        # Внутри группы контейнер для компонентов формы
        self.main_group_form_layout = QFormLayout(self.main_group)

        # Ввод времени моделирования
        self.modelling_time_spin_box = QSpinBox()
        self.modelling_time_spin_box.setAlignment(Qt.AlignHCenter)
        self.modelling_time_spin_box.setRange(1, 600)
        self.main_group_form_layout.addRow("Укажите время моделирования в секундах:",
                                           self.modelling_time_spin_box)

        # Ввод числа повторений варианта моделирования
        self.repeating_time_spin_box = QSpinBox()
        self.repeating_time_spin_box.setAlignment(Qt.AlignHCenter)
        self.repeating_time_spin_box.setRange(1, 100000)
        self.main_group_form_layout.addRow("Укажите число повторений варианта моделирования:",
                                           self.repeating_time_spin_box)

        # Нижние кнопки управления
        self.layout_with_back_and_next_buttons = LayoutWithBackAndNextButtons()
        self.main_layout.addLayout(self.layout_with_back_and_next_buttons)

        # Для удобного доступа к кнопкам
        self.next_button = self.layout_with_back_and_next_buttons.next_button
        self.back_button = self.layout_with_back_and_next_buttons.back_button

    # Получение параметров
    @property
    def parameters(self):
        return {KeyTime.modelling: self.modelling_time_spin_box.value(),
                KeyTime.repeating: self.repeating_time_spin_box.value()}

    # Установка параметров
    @parameters.setter
    def parameters(self, new_parameters):
        self.modelling_time_spin_box.setValue(new_parameters[KeyTime.modelling])
        self.repeating_time_spin_box.setValue(new_parameters[KeyTime.repeating])

    # Очищение введённых от пользователя параметров
    def clear(self):
        self.modelling_time_spin_box.setValue(1)
        self.repeating_time_spin_box.setValue(1)
