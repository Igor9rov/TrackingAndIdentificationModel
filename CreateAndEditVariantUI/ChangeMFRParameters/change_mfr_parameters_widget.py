from functools import partial
from itertools import combinations

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QWidget, QGroupBox, QLabel

from change_one_mfr_parameters_widget import ChangeOneMfrParametersWidget
from error_message_box import ErrorMessageBox
from layout_with_back_and_next_buttons import LayoutWithBackAndNextButtons


class ChangeMFRParametersWidget(QWidget):
    """Основной виджет для изменения параметров МФР"""
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Основные компоненты
        # Все виджеты с параметрами МФР
        self.all_mfr_widgets = [ChangeOneMfrParametersWidget(mfr_number=i) for i in range(1, 4)]
        # Объединим их в группу
        mfr_parameters_group_box = QGroupBox("Укажите какие МФР будут входить в состав ЗРС:")
        change_mfr_parameters_layout = QVBoxLayout(mfr_parameters_group_box)
        for widget in self.all_mfr_widgets:
            change_mfr_parameters_layout.addWidget(widget)

        # Контейнер с конопками вперёд/назад
        control_layout = LayoutWithBackAndNextButtons()

        # Выбор эталонного МФР
        self.added_numbers = []
        self.select_ref_mfr = QLabel("Укажите эталонный МФР:")
        self.mfr_number_combo_box = QComboBox()
        # Горизонтальный контейнер для группы виджетов для указания эталонного локатора
        set_numbers_layout = QHBoxLayout()
        set_numbers_layout.addWidget(self.select_ref_mfr)
        set_numbers_layout.addWidget(self.mfr_number_combo_box)

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(mfr_parameters_group_box)
        main_layout.addLayout(set_numbers_layout)
        main_layout.addLayout(control_layout)

        # Это для более удобного обращения
        self.next_button = control_layout.next_button
        self.back_button = control_layout.back_button

        # Сигнал кликнутости галочки
        for widget in self.all_mfr_widgets:
            widget.clicked.connect(partial(self.on_clicked, widget))

    @property
    def parameters(self) -> dict:
        """Возвращает параметры всех МФР

        :return: Параметры МФР
        :rtype: dict
        """
        return dict(zip(self.checked_mfr_numbers,
                        [mfr_widget.parameters for mfr_widget in self.checked_mfr_widgets]))

    @parameters.setter
    def parameters(self, new_parameters: dict):
        """Установка параметров МФР

        :param new_parameters: Словарь с параметрами МФР
        :type new_parameters: dict

        :return: None
        """
        for mfr_widget in self.all_mfr_widgets:
            mfr_widget.setChecked(mfr_widget.number in new_parameters)
            if mfr_widget.isChecked():
                mfr_widget.parameters = new_parameters[mfr_widget.number]

    def clear(self):
        """Очищение введённых параметров от пользователя

        :return: None
        """
        for widget in self.all_mfr_widgets:
            widget.clear()

    def can_press_next_button(self) -> bool:
        """Производит проверку можно ли нажать кнопку далее, а это можно сделать, только если:
        1) хотя бы один локатор был отмечен;
        2) у всех отмеченных локаторов есть координаты;
        3) у любой пары отмеченных мфр не совпадают координаты.

        :return: False если нельзя перейти на следующий виджет, True - если можно
        :rtype: bool
        """
        # Обработка проверки на наличие хотя бы одного отмеченного локатора
        if self._processing_all_checked_mfr_widgets():
            # Обработка проверки на одинаковые координаты
            return self._processing_is_any_same_coordinates()
        return False

    @property
    def checked_mfr_widgets(self) -> list:
        """Возвращает список из всех отмеченных локаторов

        :return: Список из всех отмеченных локаторов
        :rtype: list
        """
        return [widget for widget in self.all_mfr_widgets if widget.isChecked()]

    @property
    def checked_mfr_numbers(self) -> list:
        """
        :return: Список из всех номеров отмеченных локаторов
        :rtype: list
        """
        return [widget.number for widget in self.checked_mfr_widgets]

    def _processing_is_any_same_coordinates(self) -> bool:
        """Обработка запроса о том, что некоторые координаты не повторяются

        :return: Если координаты повторяются, то показываем пользователю окно с ошибкой, возвращаем False, иначе True
        :rtype: bool
        """
        return self._is_any_same_coordinates() or self.processing_message_about_same_coordinates()

    def _processing_all_checked_mfr_widgets(self) -> bool:
        """Обработка запроса о том, что отмечен ли хотя бы один локатор

        :return: Если ни один не отмечен, то показываем пользователю окно с ошибкой, возвращаем False, иначе True
        :rtype: bool
        """
        return self.checked_mfr_widgets or self.processing_message_about_lack_of_checked_mfr()

    def _is_any_same_coordinates(self) -> bool:
        """
        :return: Есть ли хотя бы одни повторяющиеся координаты
        :rtype: bool
        """
        all_mfr_coordinates = [mfr_widget.coordinates for mfr_widget in self.checked_mfr_widgets]
        return not any([coord[0] == coord[1] for coord in combinations(all_mfr_coordinates, 2)])

    def processing_message_about_lack_of_checked_mfr(self) -> bool:
        """Обработка сообщения о том, что не выбран ни один из МФР: показываем окно с ошибкой

        :return: False после закрытия окна
        :rtype: bool
        """
        self.show_message_about_lack_of_checked_mfr()
        return False

    def processing_message_about_same_coordinates(self) -> bool:
        """Обработка сообщения о том, что координаты одинаковы

        :return: False после закрытия окна
        :rtype: bool
        """
        self.show_message_about_same_coordinates()
        return False

    def show_message_about_lack_of_checked_mfr(self):
        """Вывод сообщения о том, что не выбран ни один из МФР

        :return: None
        """
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Не выбран ни один из представленных МФР")
        message_box.exec()

    def show_message_about_same_coordinates(self):
        """Вывод сообщения о том, что координаты одинаковы

        :return: None
        """
        message_box = ErrorMessageBox(parent=self)
        message_box.setText("Некоторые из выбранных МФР имеют одинаковые координаты. \n"
                            "Измените их координаты.")
        message_box.exec()

    def on_clicked(self, one_mfr_widget: QGroupBox):
        """Добавление и удаление в ComboBox номеров МФР при клике на галочки

        :return: None
        """
        one_mfr_widget.is_chosen = not one_mfr_widget.is_chosen
        number = str(one_mfr_widget.number)
        if one_mfr_widget.is_chosen and not self.added_numbers.count(number):
            self.added_numbers.append(number)
        if not one_mfr_widget.is_chosen and self.added_numbers.count(number):
            self.added_numbers.remove(number)
        self.mfr_number_combo_box.clear()
        self.mfr_number_combo_box.addItems(self.added_numbers)
