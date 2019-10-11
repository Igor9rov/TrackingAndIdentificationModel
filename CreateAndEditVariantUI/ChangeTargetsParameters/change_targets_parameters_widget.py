from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QTabWidget, QSpinBox

from error_message_box import ErrorMessageBox
from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons
from target_parameters_widget import TargetParametersWidget


# Основной виджет, содержит кнопки управления и таблицу с редактированием параметров цели
class ChangeTargetsParametersWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mfr_numbers_list = []

        self.set_target_number_line = QLabel("Укажите количество целей")
        self.min_count_of_target = 1
        self.max_count_of_target = 10
        self.number_spin_box = QSpinBox()
        self.number_spin_box.setRange(self.min_count_of_target, self.max_count_of_target)
        self.accept_count_of_target_button = QPushButton("Изменить их параметры")
        self.cancel_count_of_target_button = QPushButton("Удалить все цели, начать ввод заново")

        self.set_numbers_hbox = QHBoxLayout()
        self.set_numbers_hbox.addWidget(self.set_target_number_line)
        self.set_numbers_hbox.addWidget(self.number_spin_box)
        self.set_numbers_hbox.addWidget(self.accept_count_of_target_button)
        self.set_numbers_hbox.addWidget(self.cancel_count_of_target_button)

        self.target_parameters_tab = QTabWidget()

        self.layout_with_next_and_back_buttons = LayoutWithBackAndNextButtons()

        self.main_box = QVBoxLayout(self)
        self.main_box.addLayout(self.set_numbers_hbox)
        self.main_box.addWidget(self.target_parameters_tab)
        self.main_box.addLayout(self.layout_with_next_and_back_buttons)

        # Это для более удобного обращения к ним
        self.next_button = self.layout_with_next_and_back_buttons.next_button
        self.back_button = self.layout_with_next_and_back_buttons.back_button

        self.accept_count_of_target_button.clicked.connect(self.clicked_on_accept_target_number_button)
        self.cancel_count_of_target_button.clicked.connect(self.clicked_on_cancel_target_number_button)

        self.cancel_count_of_target_button.setEnabled(False)
        self.next_button.setEnabled(False)

    # Для вкладок таблицы добавить виджеты для параметров МФР с номерами
    def append_for_each_tab_mfr_widgets_with_numbers(self, added_mfr_numbers):
        for tab in self.all_tab_with_target_parameters:
            tab.add_mfr_widgets_with_numbers(added_mfr_numbers)

    # Для вкладок таблицы добавить виджеты для параметров МФР с номерами
    def delete_for_each_tab_mfr_widgets_with_numbers(self, deleted_mfr_numbers):
        for tab in self.all_tab_with_target_parameters:
            tab.delete_mfr_widgets_with_numbers(deleted_mfr_numbers)

    # Получение параметров целей
    @property
    def parameters(self):
        return dict(zip(range(self.number_spin_box.value()),
                        [tab.parameters for tab in self.all_tab_with_target_parameters]))

    @parameters.setter
    def parameters(self, new_parameters):
        self.mfr_numbers_list = list((new_parameters["0"]["MFRParameters"].keys()))
        self.number_spin_box.setReadOnly(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.cancel_count_of_target_button.setEnabled(False)
        self.number_spin_box.setValue(1 + int(max(new_parameters)))
        self.accept_count_of_target_button.click()
        for number_target, tab in enumerate(self.all_tab_with_target_parameters):
            tab.parameters = new_parameters[f"{number_target}"]

    def clear(self):
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.cancel_count_of_target_button.click()

    # Все вкладки таблицы с параметрами цели
    @property
    def all_tab_with_target_parameters(self):
        return [self.target_parameters_tab.widget(index) for index in range(self.target_parameters_tab.count())]

    # Слот для отрисовки таблицы с параметрами для каждой цели
    @pyqtSlot()
    def clicked_on_accept_target_number_button(self):
        self.accept_count_of_target_button.setEnabled(False)
        self.cancel_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(True)
        self.number_spin_box.setReadOnly(True)
        for number_target in range(self.number_spin_box.value()):
            self.target_parameters_tab.addTab(TargetParametersWidget(number_target, self.mfr_numbers_list),
                                              f"Цель №{number_target}")

    # Слот для очищения таблицы
    @pyqtSlot()
    def clicked_on_cancel_target_number_button(self):
        self.cancel_count_of_target_button.setEnabled(False)
        self.accept_count_of_target_button.setEnabled(True)
        self.next_button.setEnabled(False)
        self.number_spin_box.setReadOnly(False)
        self.number_spin_box.setValue(self.min_count_of_target)
        self.target_parameters_tab.clear()

    # Можно ли нажать кнопку далее (сгенерировать вариант моделирования)
    def can_press_next_button(self):
        if self._processing_all_targets_has_coordinates():
            return self._processing_all_targets_has_velocities()
        return False

    # Обработка того, что все цели имеют координаты
    def _processing_all_targets_has_coordinates(self):
        return self._all_targets_has_coordinates() or self.processing_message_about_lack_of_coordinates()

    # У всех целей есть координаты
    def _all_targets_has_coordinates(self):
        return all([widget.has_coordinates for widget in self.all_tab_with_target_parameters])

    # Обработка сообщения о том, что у целей нет координат
    def processing_message_about_lack_of_coordinates(self):
        self.show_message_about_lack_of_coordinates()
        return False

    # Вывод сообщения о том, что у целей отсутсвуют координаты
    def show_message_about_lack_of_coordinates(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют координаты у целей")
        message_box.exec()

    # Обработка того, что все цели имеют скорости
    def _processing_all_targets_has_velocities(self):
        return self._all_targets_has_velocities() or self.processing_message_about_lack_of_velocities()

    # У всех целей есть скорость
    def _all_targets_has_velocities(self):
        return all([widget.has_velocities for widget in self.all_tab_with_target_parameters])

    # Обработка сообщения о том, что у целей нет скорости
    def processing_message_about_lack_of_velocities(self):
        self.show_message_about_lack_of_velocities()
        return False

    # Вывод сообщения о том, что у целей отсутсвуют скорости
    def show_message_about_lack_of_velocities(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют скорости у целей")
        message_box.exec()
