from model_time import time_in_tick
from numpy import ndarray


# Класс цели
class Target:
    def __init__(self, number: int, coordinates: ndarray, velocities: ndarray, target_type: str):
        # Текущее время в тиках
        self.ticks = 0
        # Номер цели
        self.number = number
        # Вектор координат на текущий момент
        self.coordinates = coordinates
        # Вектор скорости на текущий момент
        self.velocities = velocities
        # Признак помехи
        self.is_anj = False
        # Тип цели
        self.type = target_type
        # Тип сопровождения
        self.is_auto_tracking = False

    # Основной алгоритм работы
    def operate(self, ticks: int):
        self.ticks = ticks
        # Гипотеза о равномерном прямолинейном движении
        self.coordinates += self.velocities * time_in_tick
