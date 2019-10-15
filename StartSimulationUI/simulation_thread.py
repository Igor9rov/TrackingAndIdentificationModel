from queue import Queue

from PyQt5.QtCore import QThread, pyqtSignal


class SimulationThread(QThread):
    """
    Поток для запуска варианта моделирования
    """
    # Сигнал для окончания работы одной итерации моделирования
    simulation_signal = pyqtSignal()
    # Сигнал для передачи текущего моделируемого времени
    time_signal = pyqtSignal(int)

    def __init__(self, queue: Queue, parent=None):
        """
        Конструктор потока для запуска варианта моделирования, создаётся по потоку на ядро
        :param parent: Родительский виджет
        """
        QThread.__init__(self, parent)
        self.queue = queue

    def run(self):
        """
        Тело функции, исполненное потоком
        Запуск варианта модедлирования, получаемого из очереди
        :return: None
        """
        while True:
            # Если очередь пуста, то нечего её ждать
            if self.queue.empty():
                break
            # Получение объектов и времени моделирования из очереди
            objects_and_time = self.queue.get()
            target_list, mfr_list, command_post = objects_and_time[0]
            modelling_time = objects_and_time[1]
            # Внутренний цикл по времени
            for time in range(20 * modelling_time):
                # Моделирование
                for target in target_list:
                    target.operate(time)
                for mfr in mfr_list:
                    mfr.operate(time)
                command_post.operate(time)
                self.time_signal.emit((time+1)/20)
            self.simulation_signal.emit()
            self.queue.task_done()
