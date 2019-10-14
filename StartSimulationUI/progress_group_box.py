from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QProgressBar, QLabel


class ProgressGroupBox(QGroupBox):
    """
    GroupBox для отображения состояния моделирования
    """
    def __init__(self, parent=None):
        QGroupBox.__init__(self, title="Выполнение", parent=parent)

        # Все компоненты
        self.iteration_progress_bar = QProgressBar()
        self.iteration_label = QLabel()
        self.time_progress_bar = QProgressBar()
        self.time_label = QLabel()
        self.result_time_label = QLabel()

        # Список всех виджетов
        all_widgets = [self.iteration_progress_bar,
                       self.iteration_label,
                       self.time_progress_bar,
                       self.time_label,
                       self.result_time_label]

        # Основной контейнер
        layout = QVBoxLayout(self)

        # Добавим виджеты и применим выравнивание
        for widget in all_widgets:
            widget.setAlignment(Qt.AlignHCenter)
            layout.addWidget(widget)

    def prepare_for_simulation(self, repeating_time_max, modelling_time_max):
        """
        Подготавливает виджеты для перед стартом моелирования
        :param repeating_time_max: Максимальное число повторений
        :param modelling_time_max: Максимальное время моделирования
        :return: None
        """
        self.iteration_progress_bar.setRange(0, repeating_time_max)
        self.iteration_progress_bar.setValue(0)
        self.time_progress_bar.setRange(0, modelling_time_max)
        self.time_progress_bar.setValue(0)
        self.iteration_label.clear()
        self.time_label.clear()
        self.result_time_label.clear()

    @pyqtSlot(int)
    def set_time(self, time):
        """
        Изменяет параметры виджетов, показывающие прогресс по времени моделирования одной реализации
        :param time: Время моделирования одной итерации
        :return: None
        """
        self.time_progress_bar.setValue(time)
        self.time_label.setText(f"Текущее время {time} с.")

    @pyqtSlot(int)
    def set_iteration(self, iteration):
        """
        Изменяет параметры виджетов, показывающие прогресс по итерациям
        :param iteration: Номер итерации, которая сейчас завершилась
        :return: None
        """
        self.iteration_progress_bar.setValue(iteration)
        self.iteration_label.setText(f"Итерация № {iteration} завершена.")

    @pyqtSlot(float)
    def set_time_result(self, result_time):
        """
        Изменяет параметры виджета, показывающего среднее время моделирования одной итерации
        :param result_time: Среднее время моделирования одной итерации
        :return: None
        """
        self.result_time_label.setText(f"Конец. Время моделирования одной итерации {result_time:.2f} с.")
