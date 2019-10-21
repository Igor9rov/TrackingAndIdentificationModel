from multiprocessing import Pool
from os import cpu_count

from PyQt5.QtCore import QThread

from generated_variant import GeneratedVariant
from simulation_func import simulation


class SimulationThread(QThread):
    """
    Отдельный от GUI поток для моделирования.
    """
    def __init__(self, variant: GeneratedVariant, parent=None):
        """
        Конструктор потока для запуска пула процессов, экземпляр сохраняет ссылку на вариант моделирования.
        :param parent: Родительский виджет
        """
        QThread.__init__(self, parent)
        self.variant = variant

    def run(self):
        """
        Тело функции, исполненное потоком после вызова метода start().
        Отедльный от GUI поток запускает пул из процессов.
        Перед пулом стоит задача выполнить моделирование столько раз, сколько указал пользователь.
        После выполнения задачи пул уничтожается.
        :return: None
        """
        # Получение нужных ссылок из варианта моделирования
        simulation_variant = [(time, self.variant.modelling_time, *self.variant.objects)
                              for time in range(self.variant.repeating_time)]
        # Создание пула процессов, которые будут производить моделирование
        process_count = cpu_count()
        pool = Pool(processes=process_count)
        pool.map(simulation, simulation_variant)
        # Убъём процессы, чтобы не висели
        pool.close()
