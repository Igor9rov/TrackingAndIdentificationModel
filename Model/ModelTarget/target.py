import numpy as np
from numpy import ndarray

from model_time import time_in_tick


class Target:
    """Класс цели"""
    __slots__ = ("ticks",
                 "number",
                 "coordinates",
                 "velocities",
                 "type",
                 "is_auto_tracking",
                 "is_anj")

    def __init__(self,
                 number: int = -1,
                 coordinates: ndarray = np.zeros(3),
                 velocities: ndarray = np.zeros(3),
                 target_type: str = "Aerodynamic",
                 is_auto_tracking=None,
                 is_anj=None) -> None:
        """Подготавливает экземпляр класса цели

        :param number: Уникальный номер цели
        :type number: int
        :param coordinates: Начальный вектор координат в прямоугольной декартовой СК ПБУ
        :type coordinates: ndarray
        :param velocities: Начальный вектор скоростей в прямоугольной декартовой СК ПБУ
        :type velocities: ndarray
        :param target_type: Тип цели: или это аэродинамика, или баллистика
        :type target_type: str
        :param is_auto_tracking: Признак АС, представляет собой словарь с ключом равным номеру МФР и булевым значением,
        по умолчанию меняется при инициализации
        :type is_auto_tracking: NoneType
        :param is_anj: Признак помехи, представляет собой словарь с ключом равным номеру МФР и булевым значением,
        по умолчанию меняется при инициализации
        :type is_anj: NoneType
        """
        # Обработка значений по умолчанию для изменяемых типов данных
        # (так как все объекты для генерации используют ссылку на один и тот же объект, а это чревато)
        if is_auto_tracking is None:
            is_auto_tracking = {0: False}
        if is_anj is None:
            is_anj = {0: False}
        # Текущее время в тиках
        self.ticks = 0
        # Номер цели
        self.number = number
        # Вектор координат на текущий момент
        self.coordinates = coordinates.astype(float)
        # Вектор скорости на текущий момент
        self.velocities = velocities
        # Тип цели
        self.type = target_type
        # Признак АС, представляет собой словарь с ключом равным номеру МФР и булевым значением
        self.is_auto_tracking = is_auto_tracking
        # Признак помехи, представляет собой словарь с ключом равным номеру МФР и булевым значением
        self.is_anj = is_anj

    def __repr__(self) -> str:
        return f"Цель c номером {self.number!r}, типа {self.type!r}, c координатами {self.coordinates!r}. " \
               f"Объект класса {self.__class__.__name__} по адресу в памяти {hex(id(self))}"

    def operate(self, ticks: int) -> None:
        """Основной алгоритм работы, цель просто движется и обновляет время

        :param ticks: Текущее время в тиках
        :type ticks: int

        :return: None
        """
        self.ticks = ticks
        # Гипотеза о равномерном прямолинейном движении
        self.coordinates += self.velocities * time_in_tick

    @property
    def registration(self) -> list:
        """Регистрация данных о цели

        :return: Список из регистрируемых данных
        :rtype: list
        """
        return [*self.coordinates, *self.velocities]
