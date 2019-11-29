import json

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItem

from change_mfr_parameters_widget import ChangeMFRParametersWidget
from change_targets_parameters_widget import ChangeTargetsParametersWidget
from change_time_parametrs_widget import ChangeTimeParametersWidget
from error_message_box import ErrorMessageBox
from save_file_widget import SaveFileWidget
from starting_widget import StartingWidget
from structure_of_variant import KeyVariant
from load_variant_function_for_json import object_pairs_hook


class EditVariantStackedWidget(QtWidgets.QStackedWidget):
    """Виджет для работы с вариантом моделирования"""
    def __init__(self, parent=None):
        QtWidgets.QStackedWidget.__init__(self, parent)

        # Виджеты в стеке основного виджета
        self.starting_widget = StartingWidget()
        self.change_time_widget = ChangeTimeParametersWidget()
        self.change_mfr_widget = ChangeMFRParametersWidget()
        self.change_targets_widget = ChangeTargetsParametersWidget()
        self.save_file_widget = SaveFileWidget()

        self.addWidget(self.starting_widget)
        self.addWidget(self.change_time_widget)
        self.addWidget(self.change_mfr_widget)
        self.addWidget(self.change_targets_widget)
        self.addWidget(self.save_file_widget)

        # Связь кнопок и слотов
        self.starting_widget.create_variant_button.clicked.connect(self.clear_parameters_and_move_to_time_parameters)
        self.starting_widget.change_variant_button.clicked.connect(self.open_existing_variant)

        self.change_time_widget.next_button.clicked.connect(self.move_to_mfr_parameters)
        self.change_time_widget.back_button.clicked.connect(self.move_to_start)

        self.change_mfr_widget.next_button.clicked.connect(self.move_next_to_targets_parameters)
        self.change_mfr_widget.back_button.clicked.connect(self.move_to_time_parameters)

        self.change_targets_widget.back_button.clicked.connect(self.move_to_mfr_parameters)
        self.change_targets_widget.next_button.clicked.connect(self.move_to_save_variant)

        self.save_file_widget.save_file_button.clicked.connect(self.save_file)
        self.save_file_widget.back_button.clicked.connect(self.move_back_to_targets_parameters)

    @property
    def variant(self) -> dict:
        """
        :return: Вариант моделирования, представляет из себя словарь словарей
        :rtype: dict
        """
        return {KeyVariant.time: self.change_time_widget.parameters,
                KeyVariant.mfr: self.change_mfr_widget.parameters,
                KeyVariant.target: self.change_targets_widget.parameters}

    @variant.setter
    def variant(self, new_variant: dict):
        """
        :param new_variant: Запись варианта моделирования в виджеты
        :type new_variant: dict

        :return: None
        """
        self.change_time_widget.parameters = new_variant[KeyVariant.time]
        self.change_mfr_widget.parameters = new_variant[KeyVariant.mfr]
        self.change_targets_widget.parameters = new_variant[KeyVariant.target]

    @pyqtSlot()
    def move_to_time_parameters(self):
        """Слот для перемещения к параметрам времени

        :return: None
        """
        self.setCurrentWidget(self.change_time_widget)

    @pyqtSlot()
    def clear_parameters_and_move_to_time_parameters(self):
        """Очищение виджетов с параметрами и переход к виджету с редактированием параметров времени

        :return: None
        """
        self.clear_widgets_with_parameters()
        self.move_to_time_parameters()

    @pyqtSlot()
    def move_to_mfr_parameters(self):
        """Перемешение к параметрам МФР

        :return: None
        """
        self.setCurrentWidget(self.change_mfr_widget)

    @pyqtSlot()
    def move_to_start(self):
        """Возвращение на стартовый виджет

        :return: None
        """
        self.setCurrentWidget(self.starting_widget)

    @pyqtSlot()
    def move_next_to_targets_parameters(self):
        """Переход к параметрам целей

        :return: None
        """
        if self.change_mfr_widget.can_press_next_button():
            self.update_targets_parameters_associated_with_mfr()
            self.setCurrentWidget(self.change_targets_widget)

    def update_targets_parameters_associated_with_mfr(self):
        """Обновление виджета с параметрами целей

        :return: None
        """
        # Для удобства использования
        mfr_numbers_from_mfr_widget = set(self.change_mfr_widget.checked_mfr_numbers)
        mfr_numbers_from_target_widget = set(self.change_targets_widget.mfr_numbers_list)

        # Добавление для каждой таблицы параметров для новых МФР
        added_mfr_numbers = mfr_numbers_from_mfr_widget - mfr_numbers_from_target_widget
        self.change_targets_widget.append_for_each_tab_mfr_widgets_with_numbers(added_mfr_numbers)

        # Удаление для каждой таблицы параметров по удалённых МФР
        deleted_mfr_numbers = mfr_numbers_from_target_widget - mfr_numbers_from_mfr_widget
        self.change_targets_widget.delete_for_each_tab_mfr_widgets_with_numbers(deleted_mfr_numbers)

        # Приравняем номера МФР
        self.change_targets_widget.mfr_numbers_list = self.change_mfr_widget.checked_mfr_numbers

    @pyqtSlot()
    def move_back_to_targets_parameters(self):
        """Перемещение назад к параметрам целей

        :return: None
        """
        self.setCurrentWidget(self.change_targets_widget)

    @pyqtSlot()
    def move_to_save_variant(self):
        """Перемещение к виджету сохранения варианта моделирования

        :return: None
        """
        self.show_variant_in_tree_view()
        self.setCurrentWidget(self.save_file_widget)

    def show_variant_in_tree_view(self):
        """Показать вариант с моделированием

        :return: None
        """
        item_model = self.save_file_widget.model
        item_model.clear()
        item_model.setHorizontalHeaderLabels(["Параметр", "Значение"])

        # Записываем в QStandardItem рекурсивно элементы словаря
        def push_dict_in_item(dictionary, parent=item_model):
            if isinstance(dictionary, dict):
                for key, value in dictionary.items():
                    parameter_item = QStandardItem(str(key))
                    # Если значение словаря словарь, то запись снова
                    if isinstance(value, dict):
                        push_dict_in_item(value, parameter_item)
                        value_item = QStandardItem()
                    # Иначе запись значения во второй столбец
                    else:
                        value_item = QStandardItem(str(value))
                    parent.appendRow([parameter_item, value_item])
        # Запись в иерархический список
        push_dict_in_item(self.variant)

    @pyqtSlot()
    def save_file(self):
        """Сохранение параметра моделирования в файл

        :return: None
        """
        filename = self.get_save_file_name_from_user()
        if filename:
            self.processing_saving_file(filename)

    def get_save_file_name_from_user(self) -> str:
        """Вывод окна с запросом имени файла, куда будем сохранять вариант моделирования

        :return: Имя файла
        :rtype: str
        """
        return QtWidgets.QFileDialog.getSaveFileName(parent=self,
                                                     caption="Сохранить параметры моделирования",
                                                     directory=QtCore.QDir.homePath(),
                                                     filter="JSON файлы (*.json)")[0]

    def processing_saving_file(self, filename: str):
        """Обработка сохранения файла, если что-то пошло не так, кидаем информацию

        :param filename: Имя файла от пользователля
        :type filename: str

        :return: None
        """
        try:
            with open(filename, "w") as write_file:
                json.dump(self.variant, write_file, indent=4)
        # Перехватим все исключения, мало ли
        except Exception as e:
            self.show_message_about_error_with_exception(e)

    def clear_widgets_with_parameters(self):
        """Очищение виджетов c редактированием параметров при открытии нового варианта/редактировании существующего

        :return: None
        """
        self.change_time_widget.clear()
        self.change_mfr_widget.clear()
        self.change_targets_widget.clear()

    @pyqtSlot()
    def open_existing_variant(self):
        """Открываем существующий вариант

        :return: None
        """
        filename = self.get_open_file_name_from_user()
        if filename:
            self.clear_widgets_with_parameters()
            self.processing_open_variant_from_file(filename)

    def get_open_file_name_from_user(self) -> str:
        """Получение имени файла с параметром моделирования для открытия

        :return: Имя файла от пользователя
        :rtype: str
        """
        return QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                     caption="Выберите файл с параметрами моделирования",
                                                     directory=QtCore.QDir.homePath(),
                                                     filter="JSON файлы (*.json)")[0]

    def processing_open_variant_from_file(self, filename: str):
        """Обработка открытия существующего файла, если что-то пошло не так, кидаем информацию

        :param filename: Имя файла от пользователя
        :type filename: str
        :return: None
        """
        try:
            with open(filename, "r") as read_file:
                # Попытка забить значениями из файла окна ввода параметров
                self.variant = json.load(read_file, object_pairs_hook=object_pairs_hook)
            self.setCurrentWidget(self.change_time_widget)
        except Exception as e:
            self.show_message_about_error_with_exception(e)

    def show_message_about_error_with_exception(self, exception: Exception):
        """Показать пользователю ошибку с выбитым исключением

        :param exception: Выбитое исключение
        :type exception: Exception

        :return: None
        """
        error_window = ErrorMessageBox(self)
        error_window.setText(f"Неудача по причине {exception}")
        error_window.exec()
