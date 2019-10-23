from numpy import ndarray

from model_time import time_in_tick


class Target:
    """
    Класс цели
    """
    __slots__ = ("ticks",
                 "number",
                 "coordinates",
                 "velocities",
                 "type",
                 "is_auto_tracking",
                 "is_anj")

    def __init__(self,
                 number: int,
                 coordinates: ndarray,
                 velocities: ndarray,
                 target_type: str,
                 is_auto_tracking: dict,
                 is_anj: dict):
        # Текущее время в тиках
        self.ticks = 0
        # Номер цели
        self.number = number
        # Вектор координат на текущий момент
        self.coordinates = coordinates
        # Вектор скорости на текущий момент
        self.velocities = velocities
        # Тип цели
        self.type = target_type
        # Тип сопровождения, представляет собой словарь с ключом равным номеру МФР и булевым значением
        self.is_auto_tracking = is_auto_tracking
        # Признак помехи, представляет собой словарь с ключом равным номеру МФР и булевым значением
        self.is_anj = is_anj

    def operate(self, ticks: int):
        """
        Основной алгоритм работы

        :param ticks: Текущее время в тиках

        :return: None
        """
        self.ticks = ticks
        # Гипотеза о равномерном прямолинейном движении
        self.coordinates += self.velocities * time_in_tick

    @property
    def registration(self):
        """
        Регистрация данных о цели

        :return: Список из регистрируемых данных
        """
        return [*self.coordinates, *self.velocities]
