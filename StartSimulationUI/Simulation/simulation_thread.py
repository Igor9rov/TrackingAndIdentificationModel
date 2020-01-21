from multiprocessing import Pool
from os import cpu_count

from PyQt5.QtCore import QThread, pyqtSignal

from generated_variant import GeneratedVariant
from registration_write_functions import write_cp_registration, write_mfr_registration
from simulation_func import simulation


class SimulationThread(QThread):
    """Отдельный от GUI поток для моделирования"""
    # Сигнал для окончания моделирования
    ending_simulation = pyqtSignal()

    def __init__(self, variant: GeneratedVariant, parent=None) -> None:
        """Конструктор потока для запуска пула процессов, экземпляр сохраняет ссылку на вариант моделирования.

        :param variant: Сгенерированный вариант моделрования
        :type variant: GeneratedVariant
        :param parent: Родительский виджет
        :type parent: QWidget
        """
        QThread.__init__(self, parent)
        self.variant = variant

    def run(self) -> None:
        """Тело функции, исполненное потоком после вызова метода start().
        Поток запускает пул из процессов.
        Перед пулом стоит задача выполнить моделирование столько раз, сколько указал пользователь.
        После выполнения моделирования пул уничтожается и идёт запись в файл регистрации данных от ПБУ и МФР

        :return: None
        """
        # Получение нужных ссылок из варианта моделирования
        simulation_variant = [(time, self.variant.modelling_time, *self.variant.objects)
                              for time in range(self.variant.repeating_time)]
        # Создание пула процессов, которые будут производить моделирование
        process_count = cpu_count()
        pool = Pool(processes=process_count)
        registration = pool.map(simulation, simulation_variant)
        self.ending_simulation.emit()
        # Убъём процессы, чтобы не висели
        pool.close()
        # Запись в файлы
        write_cp_registration(registration, "registry_cp.csv")
        write_mfr_registration(registration, "registry_mfr.csv")
