from itertools import combinations

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget, QGroupBox

from change_one_mfr_parameters_widget import ChangeOneMfrParametersWidget
from error_massage_box import ErrorMessageBox
from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons


# Основной виджет для изменения параметров МФР
class ChangeMFRParametersWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.main_layout = QVBoxLayout(self)

        self.edit_mfr_parameters_group_box = QGroupBox("Укажите какие МФР будут входить в состав ЗРС:")
        self.edit_mfr_parameters_vertical_layout = QVBoxLayout(self.edit_mfr_parameters_group_box)

        self.mfr_1_widget = ChangeOneMfrParametersWidget(mfr_number="1")
        self.edit_mfr_parameters_vertical_layout.addWidget(self.mfr_1_widget)

        self.mfr_2_widget = ChangeOneMfrParametersWidget(mfr_number="2")
        self.edit_mfr_parameters_vertical_layout.addWidget(self.mfr_2_widget)

        self.mfr_3_widget = ChangeOneMfrParametersWidget(mfr_number="3")
        self.edit_mfr_parameters_vertical_layout.addWidget(self.mfr_3_widget)

        self.main_layout.addWidget(self.edit_mfr_parameters_group_box)

        self.layout_with_back_and_next_buttons = LayoutWithBackAndNextButtons()
        # Это для более удобного обращения к ним
        self.all_mfr_widgets = [self.mfr_1_widget, self.mfr_2_widget, self.mfr_3_widget]
        self.next_button = self.layout_with_back_and_next_buttons.next_button
        self.back_button = self.layout_with_back_and_next_buttons.back_button

        self.main_layout.addLayout(self.layout_with_back_and_next_buttons)

    # Получение параметров МФР
    @property
    def parameters(self):
        return dict(zip(self.numbers_checked_mfr,
                        [mfr_widget.parameters for mfr_widget in self.all_checked_mfr_widgets]))

    # Установка параметров МФР
    @parameters.setter
    def parameters(self, new_parameters: dict):
        for mfr_widget in self.all_mfr_widgets:
            mfr_widget.setChecked(mfr_widget.number in new_parameters)
            if mfr_widget.isChecked():
                mfr_widget.parameters = new_parameters[mfr_widget.number]

    # Очищение параметров от пользователя
    def clear(self):
        self.mfr_1_widget.clear()
        self.mfr_2_widget.clear()
        self.mfr_3_widget.clear()

    # Можно ли нажать кнопку далее
    def can_press_next_button(self):
        # Обработка проверки на наличие хотя бы одного отмеченного локатора
        if self._processing_all_checked_mfr_widgets():
            # Обработка проверки на наличие у отмеченных локаторов координат
            if self._processing_all_checked_mfr_has_coordinates():
                # Обработка проверки на одинаковые координаты
                return self._processing_is_any_same_coordinates()
        return False

    # Все отмеченные локаторы
    @property
    def all_checked_mfr_widgets(self):
        return [mfr_widget for mfr_widget in self.all_mfr_widgets if mfr_widget.isChecked()]

    # Номера отмеченных МФР
    @property
    def numbers_checked_mfr(self):
        return [mfr_widget.number for mfr_widget in self.all_checked_mfr_widgets]

    # Обработка запроса о том, что некоторые координаты не повторяются
    def _processing_is_any_same_coordinates(self):
        # Проверяем, что ни одни координаты не повторяются, иначе кидаем ошибку
        return self._is_any_same_coordinates() or self.processing_message_about_same_coordinates()

    # Обработка запроса о том, что есть ли у отмеченных локаторов координаты
    def _processing_all_checked_mfr_has_coordinates(self):
        return self._all_checked_mfr_has_coordinates() or self.processing_message_about_lack_of_coordinates()

    # Обработка запроса о том, что отмечен ли хотя бы один локатор
    def _processing_all_checked_mfr_widgets(self):
        return self.all_checked_mfr_widgets or self.processing_message_about_lack_of_checked_mfr()

    # Все ли отмеченные МФР имеют координаты
    def _all_checked_mfr_has_coordinates(self):
        return all([mfr_widget.can_get_coordinates() for mfr_widget in self.all_checked_mfr_widgets])

    # Есть ли хотя бы одни повторяющиеся координаты
    def _is_any_same_coordinates(self):
        all_mfr_coordinates = [mfr_widget.coordinates for mfr_widget in self.all_checked_mfr_widgets]
        return not any([coord[0] == coord[1] for coord in combinations(all_mfr_coordinates, 2)])

    # Обработка сообщения о том, что не выбран ни один из МФР
    def processing_message_about_lack_of_checked_mfr(self):
        self.show_message_about_lack_of_checked_mfr()
        return False

    # Обработка сообщения о том, что у МФР отсутсвуют координаты
    def processing_message_about_lack_of_coordinates(self):
        self.show_message_about_lack_of_coordinates()
        return False

    # Обработка сообщения о том, что координаты одинаковы
    def processing_message_about_same_coordinates(self):
        self.show_message_about_same_coordinates()
        return False

    # Вывод сообщения о том, что не выбран ни один из МФР
    def show_message_about_lack_of_checked_mfr(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Не выбран ни один из представленных МФР")
        message_box.exec()

    # Вывод сообщения о том, что у МФР отсутсвуют координаты
    def show_message_about_lack_of_coordinates(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Отсутсвуют координаты у выбранных МФР")
        message_box.exec()

    # Вывод сообщения о том, что координаты одинаковы
    def show_message_about_same_coordinates(self):
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Некоторые из выбранных МФР имеют одинаковые координаты. \n"
                            " Измените их координаты.")
        message_box.exec()
