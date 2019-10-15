import json

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QPushButton, QHBoxLayout, QLabel, QFileDialog

from error_message_box import ErrorMessageBox
from generated_variant import GeneratedVariant


class ChoiceInputFileGroupBox(QGroupBox):
    # Сигнал для активации кнопки старт в виджете управления запуска моделирования
    variant_ready_signal = pyqtSignal()
    """
    GroupBox для выбора файла с вариантом моделирования
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выберите файл с вариантом моделирования", parent=parent)

        # Все компоненты
        self.path_label = QLabel("Файл не выбран")
        self.button = QPushButton("Выберите файл")

        # Основной контейнер
        layout = QHBoxLayout(self)
        layout.addWidget(self.path_label)
        layout.addWidget(self.button)

        # Переменная с сохранённым вариантом моделирования
        self.variant = None

        # Связь кнопки для открытия варианта моделирования
        self.button.clicked.connect(self.open_existing_variant)

    @pyqtSlot()
    def open_existing_variant(self):
        """
        Открытие существующего варианта
        :return: None
        """
        filename = self.get_open_file_name_from_user()
        if filename:
            self.processing_open_variant_from_file(filename)

    def get_open_file_name_from_user(self):
        """
        Получение имени файла с параметром моделирования для открытия
        :return: Строка с именем файла
        """
        return QFileDialog.getOpenFileName(parent=self,
                                           caption="Выберите файл с параметрами моделирования",
                                           directory=QtCore.QDir.homePath(),
                                           filter="JSON файлы (*.json)")[0]

    def processing_open_variant_from_file(self, filename):
        """
        Обработка открытия существующего файла, если что-то пошло не так, кидаем информацию
        :param filename: Строка с именем файла
        :return: None
        """
        try:
            with open(filename, "r") as read_file:
                # Сгенерили вариант
                self.variant = GeneratedVariant(json.load(read_file))
            # Покажем абсолютный путь к файлу
            self.path_label.setText(filename)
            # Назначение сигнала - разрешить запуск моделирования
            self.variant_ready_signal.emit()
        except Exception as e:
            self.show_message_about_error_with_exception(e)

    def show_message_about_error_with_exception(self, exception: Exception):
        """
        Показать пользователю ошибку с выбитым исключением
        :param exception: Имя исключения
        :return: None
        """
        error_window = ErrorMessageBox(self)
        error_window.setText(f"Неудача по причине {exception}")
        error_window.exec()
