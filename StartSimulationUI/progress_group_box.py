from os import cpu_count
from time import perf_counter

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout


class ProgressGroupBox(QGroupBox):
    """
    GroupBox для отображения состояния моделирования
    """
    # Сигнал о окончании работы
    simulation_ending_signal = pyqtSignal()

    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выполнение", parent=parent)
        # Переменная для времени старта
        self.starting_time = 0
        self.count_of_iteration = 0

        # Все компоненты
        self.simulation_progress_bar = QProgressBar()
        self.simulation_progress_bar.setAlignment(Qt.AlignCenter)

        thread_layout = QHBoxLayout()
        count_of_threads = cpu_count()
        self.thread_progress_bar_list = []
        for thread_number in range(count_of_threads):
            thread_progress_bar = QProgressBar()
            thread_progress_bar.setOrientation(Qt.Vertical)
            thread_layout.addWidget(thread_progress_bar)
            self.thread_progress_bar_list.append(thread_progress_bar)

        # Строки состояний
        self.simulation_progress_label = QLabel()
        self.simulation_progress_label.setAlignment(Qt.AlignCenter)
        self.iteration_label = QLabel()
        self.iteration_label.setAlignment(Qt.AlignCenter)

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        # Добавим виджеты
        main_layout.addWidget(self.simulation_progress_bar)
        main_layout.addLayout(thread_layout)
        main_layout.addWidget(self.simulation_progress_label)
        main_layout.addWidget(self.iteration_label)

        self.simulation_progress_bar.valueChanged.connect(self.set_time_result)

    def prepare_for_simulation(self, repeating_time_max, modelling_time_max):
        """
        Подготавливает виджеты для перед стартом моделирования
        :param repeating_time_max: Максимальное число повторений
        :param modelling_time_max: Максимальное время моделирования
        :return: None
        """
        self.starting_time = perf_counter()
        self.count_of_iteration = repeating_time_max
        self.simulation_progress_bar.setRange(0, repeating_time_max)
        self.simulation_progress_bar.setValue(0)
        for thread_progress_bar in self.thread_progress_bar_list:
            thread_progress_bar.setRange(0, modelling_time_max)
            thread_progress_bar.setValue(0)

    @pyqtSlot()
    def set_iteration(self):
        """
        Изменяет параметры виджетов, показывающие прогресс по итерациям
        :return: None
        """
        iteration = self.simulation_progress_bar.value()
        self.simulation_progress_bar.setValue(iteration + 1)

    @pyqtSlot(int)
    def set_time_result(self, progress_bar_value):
        """
        Изменяет параметры виджетов, показывающего среднее время моделирования одной итерации, общее время
        :param progress_bar_value: Значение с общего прогресс бара
        :return: None
        """
        if progress_bar_value == self.simulation_progress_bar.maximum():
            self.simulation_ending_signal.emit()
            ending_time = perf_counter()
            simulation_time = (ending_time - self.starting_time)
            self.simulation_progress_label.setText(f"Конец моделирования. "
                                                   f"Было потрачено времени: {simulation_time:.2f} c.")
            self.iteration_label.setText(f"Одна итерация выполняется за "
                                         f"{simulation_time/self.count_of_iteration:.2f} c.")
        else:
            self.simulation_progress_label.setText(f"Идёт моделирование...")
            self.iteration_label.clear()
