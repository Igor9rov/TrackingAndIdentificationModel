import json
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QApplication

from change_mfr_parameters_widget import ChangeMFRParametersWidget
from change_targets_parameters_widget import ChangeTargetsParametersWidget
from change_time_parametrs_widget import ChangeTimeParametersWidget
from error_massage_box import ErrorMessageBox
from save_file_widget import SaveFileWidget
from starting_widget import StartingWidget


# Виджет для работы с вариантом моделирования
class EditVariantStackedWidget(QtWidgets.QStackedWidget):
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

    # Вариант моделирования, представляет из себя словарь словарей
    @property
    def variant(self):
        return {"Time_Parameters": self.change_time_widget.parameters,
                "MFR_Parameters": self.change_mfr_widget.parameters,
                "Target_Parameters": self.change_targets_widget.parameters}

    # Запись варианта моделирования, в виджет
    @variant.setter
    def variant(self, new_variant):
        self.change_time_widget.parameters = new_variant["Time_Parameters"]
        self.change_mfr_widget.parameters = new_variant["MFR_Parameters"]
        self.change_targets_widget.parameters = new_variant["Target_Parameters"]

    # Слоты для перемещения
    @pyqtSlot()
    def move_to_time_parameters(self):
        self.setCurrentWidget(self.change_time_widget)

    # Очищение виджетов с параметрами и переход на к виджету с редактированием параметров времени
    @pyqtSlot()
    def clear_parameters_and_move_to_time_parameters(self):
        self.clear_widgets_with_parameters()
        self.move_to_time_parameters()

    # Перемешение к параметрам МФР
    @pyqtSlot()
    def move_to_mfr_parameters(self):
        self.setCurrentWidget(self.change_mfr_widget)

    # Возвращение на стартовый виджет
    @pyqtSlot()
    def move_to_start(self):
        self.setCurrentWidget(self.starting_widget)

    # Переход к параметрам целей
    @pyqtSlot()
    def move_next_to_targets_parameters(self):
        if self.change_mfr_widget.can_press_next_button():
            self.update_targets_parameters_associated_with_mfr()
            self.setCurrentWidget(self.change_targets_widget)

    # Обновление виджета с параметрами целей
    def update_targets_parameters_associated_with_mfr(self):
        # Для удобства использования
        mfr_numbers_from_mfr_widget = set(self.change_mfr_widget.numbers_checked_mfr)
        mfr_numbers_from_target_widget = set(self.change_targets_widget.mfr_numbers_list)

        # Добавление для каждой таблицы параметров для новых МФР
        added_mfr_numbers = mfr_numbers_from_mfr_widget - mfr_numbers_from_target_widget
        self.change_targets_widget.append_for_each_tab_mfr_widgets_with_numbers(added_mfr_numbers)

        # Удаление для каждой таблицы параметров по удалённых МФР
        deleted_mfr_numbers = mfr_numbers_from_target_widget - mfr_numbers_from_mfr_widget
        self.change_targets_widget.delete_for_each_tab_mfr_widgets_with_numbers(deleted_mfr_numbers)

        # Приравняем номера МФР
        self.change_targets_widget.mfr_numbers_list = self.change_mfr_widget.numbers_checked_mfr

    @pyqtSlot()
    def move_back_to_targets_parameters(self):
        self.setCurrentWidget(self.change_targets_widget)

    @pyqtSlot()
    def move_to_save_variant(self):
        if self.change_targets_widget.can_press_next_button():
            self.show_variant_in_tree_view()
            self.setCurrentWidget(self.save_file_widget)

    # Показать вариант с моделированием
    def show_variant_in_tree_view(self):
        item_model = self.save_file_widget.model
        item_model.clear()
        item_model.setHorizontalHeaderLabels(["Параметр", "Значение"])

        # Записываем в QStandartItem рекурсивно элементы словаря
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

    # Сохранение параметра моделирования в файл
    @pyqtSlot()
    def save_file(self):
        filename = self.get_save_file_name_from_user()
        if filename:
            self.processing_saving_file(filename)

    # Запрос имени файла от пользователя
    def get_save_file_name_from_user(self):
        # Вывод окна с запросом имени файла, куда будем сохранять вариант моделирования
        return QtWidgets.QFileDialog.getSaveFileName(parent=self,
                                                     caption="Сохранить параметры моделирования",
                                                     directory=QtCore.QDir.homePath(),
                                                     filter="JSON файлы (*.json)")[0]

    # Обработка сохранения файла, если что-то пошло не так, кидаем информацию
    def processing_saving_file(self, filename: str):
        try:
            with open(filename, "w") as write_file:
                json.dump(self.variant, write_file)
        # TODO: Может быть стоит предусмотреть разные исключения, нехорошо перехватывать их все
        # Перехватим все исключения, мало ли
        except Exception as e:
            self.show_message_about_error_with_exception(e)

    # Очищение виджетов c редактированием параметров при открытии нового варианта/редактировании существующего
    def clear_widgets_with_parameters(self):
        self.change_time_widget.clear()
        self.change_mfr_widget.clear()
        self.change_targets_widget.clear()

    # Открываем существующий вариант
    @pyqtSlot()
    def open_existing_variant(self):
        filename = self.get_open_file_name_from_user()
        if filename:
            self.clear_widgets_with_parameters()
            self.processing_open_variant_from_file(filename)

    # Получение имени файла с параметром моделирования для открытия
    def get_open_file_name_from_user(self):
        return QtWidgets.QFileDialog.getOpenFileName(parent=self,
                                                     caption="Выберите файл с параметрами моделирования",
                                                     directory=QtCore.QDir.homePath(),
                                                     filter="JSON файлы (*.json)")[0]

    # Обработка открытия существующего файла, если что-то пошло не так, кидаем информацию
    def processing_open_variant_from_file(self, filename):
        try:
            with open(filename, "r") as read_file:
                # Попытка забить значениями из файла окна ввода параметров
                self.variant = json.load(read_file)
            self.setCurrentWidget(self.change_time_widget)
        except Exception as e:
            self.show_message_about_error_with_exception(e)

    # Показать пользователю ошибку с выбитым исключением
    def show_message_about_error_with_exception(self, exception: Exception):
        error_window = ErrorMessageBox(self)
        error_window.setText(f"Неудача по причине {exception}")
        error_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = EditVariantStackedWidget()
    application.show()
    sys.exit(app.exec())
