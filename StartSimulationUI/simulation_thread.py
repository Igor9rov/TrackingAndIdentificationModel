from time import perf_counter

from PyQt5.QtCore import QThread, pyqtSignal


class SimulationThread(QThread):
    """
    Поток для запуска варианта моделирования
    """
    # Сигналы для изменения GUI
    iteration_signal = pyqtSignal(int)
    time_signal = pyqtSignal(int)
    ending_simulation_signal = pyqtSignal(float)

    def __init__(self, parent=None):
        """
        Конструктор потока для запуска варианта моделирования
        :param parent: Родительский виджет
        """
        QThread.__init__(self, parent)
        self.variant = None

    def run(self):
        """
        Тело функции, исполненное потоком
        Запуск существующего варианта
        :return: None
        """
        # Измерим время выполнения
        time_start = perf_counter()
        # Внешний цикл по реализациям
        for iteration in range(self.variant.repeating_time):
            # Копия нужных объектов
            target_list, mfr_list, command_post = self.variant.objects
            # Внутренний цикл по времени
            for time in range(20 * self.variant.modelling_time):
                # Моделирование
                for target in target_list:
                    target.operate(time)
                for radar in mfr_list:
                    radar.operate(time)
                command_post.operate(time)
                # Сигнал для времени
                self.time_signal.emit((time + 1) / 20)
            # Сигнал для итерации
            self.iteration_signal.emit(iteration + 1)
        # Расчёт времени выполнения
        time_stop = perf_counter()
        one_iteration_time = (time_stop - time_start) / self.variant.repeating_time
        self.ending_simulation_signal.emit(one_iteration_time)
