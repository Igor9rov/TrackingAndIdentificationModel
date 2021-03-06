import numpy as np
from numpy import ndarray


class TraceVarianceBCSData:
    """Класс для хранения дисперсий в биконическиой системе координат"""
    __slots__ = ("sigma_measure_coordinates",
                 "variance_measure_coordinates",
                 "variance_estimate_coordinates",
                 "variance_extrapolate_coordinates")

    def __init__(self) -> None:
        # Вектор СКО измеренных координат
        self.sigma_measure_coordinates = np.zeros(3)
        # Вектор дисперсий измеренных координат
        self.variance_measure_coordinates = np.zeros(3)
        # Вектор дисперсий оцененных координат
        self.variance_estimate_coordinates = np.zeros(3)
        # Вектор дисперсий экстраполированных координат
        self.variance_extrapolate_coordinates = np.zeros(3)

    def update_errors_measure_data(self, sigma_meas_bcs: ndarray) -> None:
        """Обновляет ошибки измерения

        :param sigma_meas_bcs: Вектор СКО оценки биконических координат цели
        :type sigma_meas_bcs: ndarray

        :return: None
        """
        self.sigma_measure_coordinates = sigma_meas_bcs
        self.variance_measure_coordinates = sigma_meas_bcs ** 2
