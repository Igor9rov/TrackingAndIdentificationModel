from multiprocessing import Pool
from os import cpu_count

from PyQt5.QtCore import QThread

from generated_variant import GeneratedVariant


def simulation(sim_variant):
    """
    Тело функции, исполненное процессом, должно быть объявлено на верхнем уровне модуля
    Функция запускает цикл по времени для моделируемых объектов
    :param sim_variant: Вариант моделирования
    :return: None
    """
    # Распаковка
    _, modelling_time, target_list, mfr_list, command_post = sim_variant
    # Внутренний цикл по времени
    for time in range(20 * modelling_time):
        # Моделирование
        for target in target_list:
            target.operate(time)
        for mfr in mfr_list:
            mfr.operate(time)
        command_post.operate(time)


class SimulationThread(QThread):
    """
    Поток для запуска варианта моделирования
    """
    def __init__(self, variant: GeneratedVariant, parent=None):
        """
        Конструктор потока для запуска варианта моделирования, создаётся по потоку на ядро
        :param parent: Родительский виджет
        """
        QThread.__init__(self, parent)
        self.variant = variant

    def run(self):
        """
        Тело функции, исполненное потоком
        :return: None
        """
        # Получение нужных ссылок из варианта
        simulation_variant = [(time, self.variant.modelling_time, *self.variant.objects)
                              for time in range(self.variant.repeating_time)]
        # Создание пула процессов, которые будут производить моделирование
        process_count = cpu_count()
        pool = Pool(processes=process_count)
        pool.map(simulation, simulation_variant)
        # Убъём процессы, чтобы не висели
        pool.close()
