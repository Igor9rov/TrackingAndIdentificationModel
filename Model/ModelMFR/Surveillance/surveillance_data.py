from math import pi

import numpy as np
from numpy import ndarray

from coordinate_system_math import dec2sph
from position_antenna_data import PositionAntennaData


# Класс, описывающий данные по обзору МФР
class SurveillanceData:
    __slots__ = ("mode",
                 "sigma_bcs",
                 "max_azimuth",
                 "min_azimuth",
                 "max_elevation",
                 "min_elevation",
                 "position_antenna_data")

    def __init__(self):
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
        self.position_antenna_data = PositionAntennaData()

    # Вычисление данных позиции антенны
    def calculate_position_antenna_data(self):
        self.position_antenna_data.calculate_data()

    # Проверка на возможность сопровождения
    def validate_tracking(self, real_coord: ndarray):
        # Пересчёт реальных координат в сферические координаты
        real_coord_sph = dec2sph(real_coord)
        # Углы реального положения цели
        azimuth = real_coord_sph[1]
        elevation = real_coord_sph[2]
        # Проверка по углам в сферической системе координат
        azimuth_in_threshold = self.min_azimuth < azimuth < self.max_azimuth
        elevation_in_threshold = self.min_elevation < elevation < self.max_elevation
        can_tracking = azimuth_in_threshold and elevation_in_threshold
        return can_tracking
