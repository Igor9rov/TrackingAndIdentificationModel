from ErrorMessageBox import ErrorMessageBox
from LayoutWithBackAndNextButtons import LayoutWithBackAndNextButtons
from PyQt5.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from itertools import combinations


# Текстовое поле с вводом координат МФР
class MFRCoordinateLineEdit(QLineEdit):
    def __init__(self, coordinate_name="x", parent=None):
        QLineEdit.__init__(self, parent)
        max_value = 2000
        min_value = -max_value
        self.setPlaceholderText(f"Координата {coordinate_name}, м")
        input_coordinate_validator = QIntValidator(min_value, max_value)
        self.setValidator(input_coordinate_validator)
        self.setAlignment(Qt.AlignHCenter)


# Виджет для изменения параметров одного МФР
class ChangeOneMfrParametersWidget(QGroupBox):
    def __init__(self, mfr_number=0, parent=None):
        QGroupBox.__init__(self, f"МФР №{mfr_number}:", parent)
        self.number = mfr_number
        self.setCheckable(True)

        self.main_layout = QHBoxLayout(self)

        self.coordinates_label = QLabel(f"Координаты МФР №{mfr_number}:")
        self.main_layout.addWidget(self.coordinates_label)

        self.x_coordinate_line_edit = MFRCoordinateLineEdit("x")
        self.main_layout.addWidget(self.x_coordinate_line_edit)

        self.y_coordinate_line_edit = MFRCoordinateLineEdit("y")
        self.main_layout.addWidget(self.y_coordinate_line_edit)

        self.z_coordinate_line_edit = MFRCoordinateLineEdit("z")
        self.main_layout.addWidget(self.z_coordinate_line_edit)

    # Попытка получения координат
    def can_get_coordinates(self):
        try:
            coordinates = self.coordinates
        except ValueError:
            return False
        return True

    # Координаты
    @property
    def coordinates(self):
        return [float(self.x_coordinate_line_edit.text()),
                float(self.y_coordinate_line_edit.text()),
                float(self.z_coordinate_line_edit.text())]

    # Получение параметров одного МФР
    def get_parameters(self):
        return {"coordinates": self.coordinates}


# Основной виджет для изменения параметров МФР
class ChangeMFRParametersWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.main_layout = QVBoxLayout(self)

        self.edit_mfr_parameters_group_box = QGroupBox("Укажите какие МФР будут входить в состав ЗРС:")
        self.edit_mfr_parameters_vertical_layout = QVBoxLayout(self.edit_mfr_parameters_group_box)

        self.mfr_1_widget = ChangeOneMfrParametersWidget(mfr_number=1)
        self.edit_mfr_parameters_vertical_layout.addWidget(self.mfr_1_widget)

        self.mfr_2_widget = ChangeOneMfrParametersWidget(mfr_number=2)
        self.edit_mfr_parameters_vertical_layout.addWidget(self.mfr_2_widget)

        self.mfr_3_widget = ChangeOneMfrParametersWidget(mfr_number=3)
        self.edit_mfr_parameters_vertical_layout.addWidget(self.mfr_3_widget)

        self.main_layout.addWidget(self.edit_mfr_parameters_group_box)

        self.layout_with_back_and_next_buttons = LayoutWithBackAndNextButtons()
        # Это для более удобного обращения к ним
        self.all_mfr_widgets = [self.mfr_1_widget, self.mfr_2_widget, self.mfr_3_widget]
        self.next_button = self.layout_with_back_and_next_buttons.next_button
        self.back_button = self.layout_with_back_and_next_buttons.back_button

        self.main_layout.addLayout(self.layout_with_back_and_next_buttons)

    # Получение параметров МФР
    def get_parameters(self):
        return dict(zip(self.numbers_checked_mfr,
                        [mfr_widget.get_parameters() for mfr_widget in self.all_checked_mfr_widgets]))

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
