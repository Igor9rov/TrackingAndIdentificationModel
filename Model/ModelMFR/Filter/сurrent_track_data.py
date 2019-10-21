import numpy as np


class CurrentTrackData:
    """
    Класс описывающий данные по цели на текущий шаг
    """
    __slots__ = ("measure_coordinates",
                 "estimate_coordinates",
                 "estimate_velocities",
                 "extrapolate_coordinates",
                 "extrapolate_velocities",
                 "sigma_bcs",
                 "variance_estimate_coordinates",
                 "variance_extrapolate_coordinates",
                 "covariance_est_coord_vel",
                 "variance_estimate_velocities")

    def __init__(self):
        # Измеренные координаты
        self.measure_coordinates = np.zeros(3)
        # Оцененные координаты
        self.estimate_coordinates = np.zeros(3)
        # Оцененные скорости
        self.estimate_velocities = np.zeros(3)
        # Эктсраполированные координаты
        self.extrapolate_coordinates = np.zeros(3)
        # Экстраполированные скорости
        self.extrapolate_velocities = np.zeros(3)
        # Вектор СКО измерений
        self.sigma_bcs = np.zeros(3)
        # Дисперсии оценки координат
        self.variance_estimate_coordinates = np.zeros(3)
        # Дисперсии экстраполированных координат
        self.variance_extrapolate_coordinates = np.zeros(3)
        # Ковариация оценок координат и скорости
        self.covariance_est_coord_vel = np.zeros(3)
        # Дисперсии оценки скоростей
        self.variance_estimate_velocities = np.zeros(3)
