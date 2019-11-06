import numpy as np


class TraceCoordinatesData:
    """Класс для хранения данных по координатам"""
    __slots__ = ("measure_coordinates_bcs",
                 "measure_coordinates_dec",
                 "estimate_coordinates_bcs",
                 "estimate_coordinates_dec",
                 "extrapolate_coordinates_bcs",
                 "extrapolate_coordinates_dec")

    def __init__(self):
        # Измеренные координаты цели
        self.measure_coordinates_bcs = np.zeros(3)
        self.measure_coordinates_dec = np.zeros(3)
        # Оценка координат цели
        self.estimate_coordinates_bcs = np.zeros(3)
        self.estimate_coordinates_dec = np.zeros(3)
        # Экстраполированные координаты цели
        self.extrapolate_coordinates_bcs = np.zeros(3)
        self.extrapolate_coordinates_dec = np.zeros(3)
