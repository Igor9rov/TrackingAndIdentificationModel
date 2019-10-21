from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTabWidget, QSpinBox

from error_message_box import ErrorMessageBox
from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons
from structure_of_variant import KeyTarget
from target_parameters_widget import TargetParametersWidget


class ChangeTargetsParametersWidget(QWidget):
    """
    Основной виджет, содержит кнопки управления и таблицу с редактированием параметров цели
    """
    def __init__(self, parent=None):
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

    def append_for_each_tab_mfr_widgets_with_numbers(self, added_mfr_numbers: set):
        """
        Для вкладок таблицы добавить виджеты для параметров МФР с номерами
        :param added_mfr_numbers: Множество с номерами МФР, которые необходимо добавить
        :return: None
        """
        for tab in self.all_tab_with_target_parameters:
            tab.add_mfr_widgets_with_numbers(added_mfr_numbers)

    def delete_for_each_tab_mfr_widgets_with_numbers(self, deleted_mfr_numbers: set):
        """
        Для вкладок таблицы удалить виджеты для параметров МФР с номерами
        :param deleted_mfr_numbers: Множество с номерами МФР, которые необходимо удалить
        :return: None
        """
        for tab in self.all_tab_with_target_parameters:
            tab.delete_mfr_widgets_with_numbers(deleted_mfr_numbers)

    @property
    def parameters(self):
        """
        :return: Параметры цели в виде словаря для каждой цели из таблицы
        """
        return dict(zip(range(self.number_spin_box.value()),
                        [tab.parameters for tab in self.all_tab_with_target_parameters]))

    @parameters.setter
    def parameters(self, new_parameters: dict):
        """
        Устанавливает параметры целей
        :param new_parameters: Словарь со значением параметров для ключа равного номеру цели
        :return: None
        """
        self.mfr_numbers_list = list((new_parameters["0"][KeyTarget.mfr].keys()))
        self.number_spin_box.setReadOnly(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.cancel_count_of_target_button.setEnabled(False)
        self.number_spin_box.setValue(1 + int(max(new_parameters)))
        self.accept_count_of_target_button.click()
        for number_target, tab in enumerate(self.all_tab_with_target_parameters):
            tab.parameters = new_parameters[f"{number_target}"]

    def clear(self):
        """
        Очищение виджета
        :return:
        """
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.cancel_count_of_target_button.click()

    @property
    def all_tab_with_target_parameters(self):
        """
        :return: Все вкладки таблицы с параметрами цели
        """
        return [self.target_parameters_tab.widget(index) for index in range(self.target_parameters_tab.count())]

    @pyqtSlot()
    def clicked_on_accept_target_number_button(self):
        """
        Слот для отрисовки таблицы с параметрами для каждой цели
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
    def clicked_on_cancel_target_number_button(self):
        """
        Слот для очищения таблицы
        :return: None
        """
        self.cancel_count_of_target_button.setEnabled(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(False)
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.target_parameters_tab.clear()

    def can_press_next_button(self):
        """
        Проверяет можно ли нажать кнопку далее (сгенерировать вариант моделирования)
        А это можно сделать, если:
        1) У всех целей введены координаты
        2) У всех целей введены скорость
        :return: True/False
        """
        if self._processing_all_targets_has_coordinates():
            return self._processing_all_targets_has_velocities()
        return False

    def _processing_all_targets_has_coordinates(self):
        """
        Обработка того, что все цели имеют координаты
        :return: Если у не у всех целей есть координаты, то показать сообщение и вернуть False, иначе True
        """
        return self._all_targets_has_coordinates() or self.processing_message_about_lack_of_coordinates()

    def _all_targets_has_coordinates(self):
        """
        :return: True/False в зависимости от того, есть ли координаты у всех целей
        """
        return all([widget.has_coordinates for widget in self.all_tab_with_target_parameters])

    def processing_message_about_lack_of_coordinates(self):
        """
        Обработка сообщения о том, что у целей нет координат
        :return: False
        """
        self.show_message_about_lack_of_coordinates()
        return False

    def show_message_about_lack_of_coordinates(self):
        """
        Вывод сообщения о том, что у целей отсутсвуют координаты
        :return: None
        """
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют координаты у целей")
        message_box.exec()

    def _processing_all_targets_has_velocities(self):
        """
        Обработка того, что все цели имеют скорости
        :return: Если у не у всех целей есть скорости, то показать сообщение и вернуть False, иначе True
        """
        return self._all_targets_has_velocities() or self.processing_message_about_lack_of_velocities()

    def _all_targets_has_velocities(self):
        """
        :return: True/False в зависимости от того, есть ли скорость у всех целей
        """
        return all([widget.has_velocities for widget in self.all_tab_with_target_parameters])

    def processing_message_about_lack_of_velocities(self):
        """
        Обработка сообщения о том, что у целей нет скорости: вывод диалогового окна
        :return: False
        """
        self.show_message_about_lack_of_velocities()
        return False

    def show_message_about_lack_of_velocities(self):
        """
        Вывод сообщения о том, что у целей отсутсвуют скорости
        :return: None
        """
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют скорости у целей")
        message_box.exec()
