from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTabWidget, QSpinBox

from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons
from structure_of_variant import KeyTarget
from target_parameters_widget import TargetParametersWidget


class ChangeTargetsParametersWidget(QWidget):
    """Основной виджет, содержит кнопки управления и таблицу с редактированием параметров цели"""
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)

        # Переменная для хранения списка выбранных номеров МФР, нужна для корректной отрисовки таблицы
        self.mfr_numbers_list = []
        # Хранят минимальное и максимально количество целей
        self.min_count_of_target = 1
        self.max_count_of_target = 10

        # Основные компоненты
        set_target_number_line = QLabel("Укажите количество целей")
        self.number_spin_box = QSpinBox()
        self.number_spin_box.setRange(self.min_count_of_target, self.max_count_of_target)
        self.accept_count_of_target_button = QPushButton("Изменить их параметры")
        self.cancel_count_of_target_button = QPushButton("Удалить все цели, начать ввод заново")
        # Горизонтальный контейнер для группы виджетов для указания номера цели
        set_numbers_layout = QHBoxLayout()
        set_numbers_layout.addWidget(set_target_number_line)
        set_numbers_layout.addWidget(self.number_spin_box)
        set_numbers_layout.addWidget(self.accept_count_of_target_button)
        set_numbers_layout.addWidget(self.cancel_count_of_target_button)
        # Таблица с параметрами целей
        self.target_parameters_tab = QTabWidget()
        # Контейнер с кнопками вперёд/назад
        control_layout = LayoutWithBackAndNextButtons()

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(set_numbers_layout)
        main_layout.addWidget(self.target_parameters_tab)
        main_layout.addLayout(control_layout)

        # Это для более удобного обращения к ним
        self.next_button = control_layout.next_button
        self.back_button = control_layout.back_button

        # Связь сигналов и слотов
        self.accept_count_of_target_button.clicked.connect(self.clicked_on_accept_target_number_button)
        self.cancel_count_of_target_button.clicked.connect(self.clicked_on_cancel_target_number_button)

        # Отключение кнопок
        self.cancel_count_of_target_button.setEnabled(False)
        self.next_button.setEnabled(False)

    def append_for_each_tab_mfr_widgets_with_numbers(self, added_mfr_numbers: set) -> None:
        """Для вкладок таблицы добавить виджеты для параметров МФР с номерами

        :param added_mfr_numbers: Множество с номерами МФР, которые необходимо добавить
        :type added_mfr_numbers: set

        :return: None
        """
        for tab in self.all_tab_with_target_parameters:
            tab.add_mfr_widgets_with_numbers(added_mfr_numbers)

    def delete_for_each_tab_mfr_widgets_with_numbers(self, deleted_mfr_numbers: set) -> None:
        """Для вкладок таблицы удалить виджеты для параметров МФР с номерами

        :param deleted_mfr_numbers: Множество с номерами МФР, которые необходимо удалить
        :type deleted_mfr_numbers: set

        :return: None
        """
        for tab in self.all_tab_with_target_parameters:
            tab.delete_mfr_widgets_with_numbers(deleted_mfr_numbers)

    @property
    def parameters(self) -> dict:
        """
        :return: Параметры цели в виде словаря для каждой цели из таблицы
        :rtype: dict
        """
        return dict(zip(range(self.number_spin_box.value()),
                        [tab.parameters for tab in self.all_tab_with_target_parameters]))

    @parameters.setter
    def parameters(self, new_parameters: dict) -> None:
        """Устанавливает параметры целей

        :param new_parameters: Словарь со значением параметров для ключа равного номеру цели
        :type new_parameters: dict

        :return: None
        """
        self.mfr_numbers_list = list((new_parameters[0][KeyTarget.mfr].keys()))
        self.number_spin_box.setReadOnly(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.cancel_count_of_target_button.setEnabled(False)
        self.number_spin_box.setValue(1 + int(max(new_parameters)))
        self.accept_count_of_target_button.click()
        for number_target, tab in enumerate(self.all_tab_with_target_parameters):
            tab.parameters = new_parameters[number_target]

    def clear(self) -> None:
        """Очищение виджета

        :return: None
        """
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.cancel_count_of_target_button.click()

    @property
    def all_tab_with_target_parameters(self) -> list:
        """
        :return: Все вкладки таблицы с параметрами цели
        :rtype: list
        """
        return [self.target_parameters_tab.widget(index) for index in range(self.target_parameters_tab.count())]

    @pyqtSlot()
    def clicked_on_accept_target_number_button(self) -> None:
        """Слот для отрисовки таблицы с параметрами для каждой цели

        :return: None
        """
        self.accept_count_of_target_button.setEnabled(False)
        self.cancel_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(True)
        self.number_spin_box.setReadOnly(True)
        for number_target in range(self.number_spin_box.value()):
            self.target_parameters_tab.addTab(TargetParametersWidget(number_target, self.mfr_numbers_list),
                                              f"Цель №{number_target}")

    @pyqtSlot()
    def clicked_on_cancel_target_number_button(self) -> None:
        """Слот для очищения таблицы

        :return: None
        """
        self.cancel_count_of_target_button.setEnabled(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(False)
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.target_parameters_tab.clear()
