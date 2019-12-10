import numpy as np
from numpy import ndarray
from numpy.linalg import inv

from abstract_estimator_cta_trace_data import AbstractEstimator
from source_trace import SourceTrace


class EstimatorTwoNotBearingTraces(AbstractEstimator):
    """Оценщик в случае, когда по трассе есть два источника, при этом они не под АШП"""
    def __init__(self, first_source_trace: SourceTrace, second_source_trace: SourceTrace):
        self.matrix_a = np.zeros((3, 3))
        self.matrix_b = np.zeros((3, 3))

        self.first_trace = first_source_trace
        self.second_trace = second_source_trace

    @property
    def coordinates(self) -> ndarray:
        """
        :return: Линейная оценка координат с минимальной дисперсией
        :rtype: ndarray
        """
        summary_covariance_matrix = self.first_trace.coordinate_covariance_matrix + \
                                    self.second_trace.coordinate_covariance_matrix

        self.matrix_a = self.second_trace.coordinate_covariance_matrix @ inv(summary_covariance_matrix)
        self.matrix_b = self.first_trace.coordinate_covariance_matrix @ inv(summary_covariance_matrix)

        return self.matrix_a @ self.first_trace.coordinates + self.matrix_b @ self.second_trace.coordinates

    @property
    def velocities(self) -> ndarray:
        """
        :return: Пока вернём оценку скоростей как скорость трассы головного источника
        :rtype: ndarray
        """
        return self.first_trace.velocities

    @property
    def coordinates_covariance_matrix(self) -> ndarray:
        """
        :return: Ковариационная матрица получившейся оценки
        :rtype: ndarray
        """
        return self.matrix_a @ self.first_trace.coordinate_covariance_matrix @ self.matrix_a.T + \
               self.matrix_b @ self.second_trace.coordinate_covariance_matrix @ self.matrix_b.T
