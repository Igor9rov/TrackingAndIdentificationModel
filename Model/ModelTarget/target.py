from numpy import ndarray

from model_time import time_in_tick


# Класс цели
class Target:
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

    # Основной алгоритм работы
    def operate(self, ticks: int):
        self.ticks = ticks
        # Гипотеза о равномерном прямолинейном движении
        self.coordinates += self.velocities * time_in_tick
