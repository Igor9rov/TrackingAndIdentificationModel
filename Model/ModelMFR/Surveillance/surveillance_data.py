from math import pi

import numpy as np
from numpy import ndarray

from coordinate_system_math import dec2sph
from errors_namedtuple import SurveillanceErrors
from position_antenna_data import PositionAntennaData


class SurveillanceData:
    """Класс, описывающий данные по обзору МФР"""
    __slots__ = ("mode",
                 "sigma_bcs",
                 "max_azimuth",
                 "min_azimuth",
                 "max_elevation",
                 "min_elevation",
                 "position_antenna_data")

    def __init__(self, errors: SurveillanceErrors = SurveillanceErrors(0, 0)) -> None:
        # Режим обзора
        self.mode = "SM"
        # Вектор ошибок измерения в БСК
        self.sigma_bcs = np.array([5.0, 0.00087, 0.00087])
        # Верхняя граница азимута
        self.max_azimuth = pi / 3
        # Нижняя граница азимута
        self.min_azimuth = -pi / 3
        # Верхняя граница угла места
        self.max_elevation = pi / 4
        # Нижняя граница угла места
        self.min_elevation = -pi / 60
        # Данные по положению антенны
        self.position_antenna_data = PositionAntennaData(errors)

    def validate_tracking(self, real_coord: ndarray) -> bool:
        """Проверка на возможность сопровождения

        :param real_coord: Вектор настоящих координат в прямоугольной декартовой СК
        :type real_coord: ndarray

        :return: Признак возможности сопровождения
        :rtype: bool
        """
        # Пересчёт реальных координат в сферические координаты
        distance, azimuth, elevation = dec2sph(real_coord)

        # Проверка корректности расстояния до цели
        not_null_distance = distance != 0.
        # Проверка по углам в сферической системе координат
        azimuth_in_threshold = self.min_azimuth < azimuth < self.max_azimuth
        elevation_in_threshold = self.min_elevation < elevation < self.max_elevation

        can_tracking = azimuth_in_threshold and elevation_in_threshold and not_null_distance
        return can_tracking
