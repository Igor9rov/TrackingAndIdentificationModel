import json
from time import perf_counter

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QFileDialog

from choice_input_file_group_box import ChoiceInputFileGroupBox
from choise_output_file_group_box import ChoiceOutputFileGroupBox
from control_buttons_layout import ControlButtonsLayout
from error_message_box import ErrorMessageBox
from generate_variant import GenerateVariant
from progress_group_box import ProgressGroupBox


class ThreadUI(QThread):
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.variant = None
        self.progress_group_box = None

    # Запуск существующего варианта
    def run(self):
        time_start = perf_counter()
        for iteration in range(self.variant.repeating_time):
            for time in range(20 * self.variant.modelling_time):
                for target in self.variant.target_list:
                    target.operate(time)
                for radar in self.variant.mfr_list:
                    radar.operate(time)
                self.variant.command_post.operate(time)
            self.progress_group_box.label.setText(f"Конец итерации №{iteration+1}")
        time_stop = perf_counter()
        one_iteration_time = (time_stop - time_start) / self.variant.repeating_time
        self.progress_group_box.label.setText(f"Конец. Время моделирования = {one_iteration_time:.2f}")


class StartSimulationUI(QWidget):
    """
    GUI для запуска моделирования
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Основные компоненты
        self.choice_input_file_group_box = ChoiceInputFileGroupBox()
        self.choice_output_file_group_box = ChoiceOutputFileGroupBox()
        self.progress_group_box = ProgressGroupBox()
        self.control_buttons_layout = ControlButtonsLayout()

        # Основной контейнер
        layout = QVBoxLayout(self)
        layout.addWidget(self.choice_input_file_group_box)
        layout.addWidget(self.choice_output_file_group_box)
        layout.addWidget(self.progress_group_box)
        layout.addLayout(self.control_buttons_layout)

        self.control_buttons_layout.start_button.setEnabled(False)
        self.control_buttons_layout.stop_button.setEnabled(False)

        # Создаем экземпляр класса
        self.thread_ui = ThreadUI()
        # Связь кнопки для начала моделирования
        self.control_buttons_layout.start_button.clicked.connect(self.start_simulate)
        # Связь конпки для открытия варианта моделирования
        self.choice_input_file_group_box.button.clicked.connect(self.open_existing_variant)

    @pyqtSlot()
    def start_simulate(self):
        self.thread_ui.variant = self.choice_input_file_group_box.variant
        self.thread_ui.progress_group_box = self.progress_group_box
        self.thread_ui.start()

    # Открытие существующего варианта
    @pyqtSlot()
    def open_existing_variant(self):
        filename = self.get_open_file_name_from_user()
        if filename:
            self.processing_open_variant_from_file(filename)

    # Получение имени файла с параметром моделирования для открытия
    def get_open_file_name_from_user(self):
        return QFileDialog.getOpenFileName(parent=self,
                                           caption="Выберите файл с параметрами моделирования",
                                           directory=QtCore.QDir.homePath(),
                                           filter="JSON файлы (*.json)")[0]

    # Обработка открытия существующего файла, если что-то пошло не так, кидаем информацию
    def processing_open_variant_from_file(self, filename):
        # Покажем абсолютный путь к файлу
        self.choice_input_file_group_box.path_label.setText(filename)
        try:
            with open(filename, "r") as read_file:
                # Сгенерили вариант
                self.choice_input_file_group_box.variant = GenerateVariant(json.load(read_file))
            self.control_buttons_layout.start_button.setEnabled(True)
        except Exception as e:
            self.show_message_about_error_with_exception(e)

    # Показать пользователю ошибку с выбитым исключением
    def show_message_about_error_with_exception(self, exception: Exception):
        error_window = ErrorMessageBox(self)
        error_window.setText(f"Неудача по причине {exception}")
        error_window.exec()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    application = StartSimulationUI()
    application.show()
    sys.exit(app.exec())
