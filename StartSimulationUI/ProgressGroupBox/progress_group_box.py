from time import perf_counter

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QProgressBar, QLabel


class ProgressGroupBox(QGroupBox):
    """GroupBox для отображения состояния моделирования"""
    def __init__(self, parent=None) -> None:
        QGroupBox.__init__(self, title="Выполнение", parent=parent)
        # Переменная для времени старта моделирования
        self.starting_simulation_time = 0.
        # Переменная для времени старта записи в файл
        self.starting_writing_time = 0.
        # Число выполянемых итераций
        self.count_of_iteration = 0

        # Все компоненты
        # Прогресс бар
        self.bar = QProgressBar()
        self.bar.setRange(0, 10)

        # Строки состояний
        self.simulation_label = QLabel()
        self.iteration_label = QLabel()
        self.writing_label = QLabel()

        # Объеденим все виджеты в лист
        all_widgets = [self.bar,
                       self.simulation_label,
                       self.iteration_label,
                       self.writing_label]

        # Основной контейнер
        layout = QVBoxLayout(self)

        # Для всех виджетов указываем выравнивание и добавим в контейнер
        for widget in all_widgets:
            widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(widget)

    def prepare_for_simulation(self, repeating_time_max: int) -> None:
        """Подготавливает виджеты для перед стартом моделирования

        :param repeating_time_max: Максимальное число повторений
        :type repeating_time_max: int

        :return: None
        """
        # Сохраним время запуска моделирования
        self.starting_simulation_time = perf_counter()

        # Сохраним число моделирований
        self.count_of_iteration = repeating_time_max

        # Очистка надписей
        self.simulation_label.setText(f"Идёт моделирование...")
        self.iteration_label.clear()
        self.writing_label.clear()

        # Псевдоиндикация
        self.bar.setValue(int(0.5 * self.bar.maximum()))

    @pyqtSlot()
    def show_simulation_time(self) -> None:
        """Показывает время моделирования

        :return: None
        """
        # Считаем время моделирования
        ending_simulation_time = perf_counter()
        simulation_time = ending_simulation_time - self.starting_simulation_time
        # Время выполнения одной итерации
        iteration_time = simulation_time / self.count_of_iteration

        # Псевдоиндикация
        self.bar.setValue(int(0.9 * self.bar.maximum()))

        # Покажем время моделирования
        self.simulation_label.setText(f"Моделирование проведено за {simulation_time:.2f} c.")
        self.iteration_label.setText(f"Одна итерация выполняется за {iteration_time:.2f} c.")

        # Если закончилось моделирование, то сейчас идёт запись в файл
        self.writing_label.setText("Идёт запись в файл")
        self.starting_writing_time = perf_counter()

    @pyqtSlot()
    def show_writing_time(self) -> None:
        """Показывает время записи в файл

        :return: None
        """
        # Определение времени записи в файл
        ending_writing_time = perf_counter()
        writing_time = ending_writing_time - self.starting_writing_time

        # Псевдоиндикация
        self.bar.setValue(self.bar.maximum())

        # Покажем время записи в файл
        self.writing_label.setText(f"Запись в файл заняла {writing_time:.2f} c.")
