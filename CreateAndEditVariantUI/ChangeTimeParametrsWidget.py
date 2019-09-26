from LayoutWithBackAndNextButtons import LayoutWithBackAndNextButtons
from PyQt5 import QtWidgets
import sys


# Класс для изменения временных параметров варианта
class ChangeTimeParametersWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        # Основной контейнер
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # Основная группа виджетов
        self.main_group = QtWidgets.QGroupBox("Укажите временные параметры моделируемого варианта")
        self.main_layout.addWidget(self.main_group)
        # Внутри группы контейнер для компонентов формы
        self.main_group_form_layout = QtWidgets.QFormLayout(self.main_group)

        # Ввод времени моделирования
        self.modelling_time_spin_box = QtWidgets.QSpinBox()
        self.modelling_time_spin_box.setRange(1, 600)
        self.main_group_form_layout.addRow("Укажите время моделирования в секундах:",
                                           self.modelling_time_spin_box)

        # Ввод числа повторений варианта моделирования
        self.repeating_time_spin_box = QtWidgets.QSpinBox()
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
    def get_parameters(self):
        return {"Modelling_time": self.modelling_time_spin_box.value(),
                "Repeating_time": self.repeating_time_spin_box.value()}



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = ChangeTimeParametersWidget()
    application.show()
    sys.exit(app.exec())
