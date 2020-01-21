import numpy as np


class TraceCovarianceMatrixData:
    """Класс для хранения данных по ковариационным матрицам в декартовых координатах МФР"""
    __slots__ = ("measure_covariance_matrix",
                 "estimate_covariance_matrix",
                 "extrapolate_covariance_matrix")

    def __init__(self) -> None:
        # Ковариационная матрица измеренных координат
        self.measure_covariance_matrix = np.zeros((3, 3))
        # Ковариационная матрица оценки координат
        self.estimate_covariance_matrix = np.zeros((3, 3))
        # Ковариационная матрица экстраполированных координат
        self.extrapolate_covariance_matrix = np.zeros((3, 3))
