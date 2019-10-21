from time import perf_counter

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QProgressBar, QLabel


class ProgressGroupBox(QGroupBox):
    """
    GroupBox для отображения состояния моделирования.
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выполнение", parent=parent)
        # Переменная для времени старта
        self.starting_time = 0
        self.count_of_iteration = 0

        # Все компоненты
        self.simulation_progress_bar = QProgressBar()
        self.simulation_progress_bar.setAlignment(Qt.AlignCenter)

        # Строки состояний
        self.simulation_progress_label = QLabel()
        self.simulation_progress_label.setAlignment(Qt.AlignCenter)
        self.iteration_label = QLabel()
        self.iteration_label.setAlignment(Qt.AlignCenter)

        # Основной контейнер
        main_layout = QVBoxLayout(self)
        # Добавим виджеты
        main_layout.addWidget(self.simulation_progress_bar)
        main_layout.addWidget(self.simulation_progress_label)
        main_layout.addWidget(self.iteration_label)

    def prepare_for_simulation(self, repeating_time_max):
        """
        Подготавливает виджеты для перед стартом моделирования
        :param repeating_time_max: Максимальное число повторений
        :return: None
        """
        self.starting_time = perf_counter()
        self.count_of_iteration = repeating_time_max
        self.simulation_progress_bar.setRange(0, repeating_time_max)
        self.simulation_progress_bar.setValue(repeating_time_max / 2)

    def show_time_result(self):
        ending_time = perf_counter()
        simulation_time = (ending_time - self.starting_time)
        self.simulation_progress_bar.setValue(self.simulation_progress_bar.maximum())
        self.simulation_progress_label.setText(f"Конец моделирования. "
                                               f"Было потрачено времени: {simulation_time:.2f} c.")
        self.iteration_label.setText(f"Одна итерация выполняется за "
                                     f"{simulation_time / self.count_of_iteration:.2f} c.")
