import numpy as np


class PreviousTrackData:
    """Класс описывающий данные по трассе цели на предыдущий шаг"""
    __slots__ = ("covariance_est_coord_vel",
                 "variance_estimate_velocities")

    def __init__(self):
        # Ковариация оценок координат и скорости
        self.covariance_est_coord_vel = np.zeros(3)
        # Дисперсии оценки скоростей
        self.variance_estimate_velocities = np.zeros(3)
