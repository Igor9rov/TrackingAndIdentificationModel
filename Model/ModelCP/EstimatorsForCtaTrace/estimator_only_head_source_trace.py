from numpy import ndarray

from abstract_estimator_cta_trace_data import AbstractEstimator
from source_trace import SourceTrace


class EstimatorOnlyHeadSourceTrace(AbstractEstimator):
    """Оценщик в случае, когда нет дополнительных источников"""
    def __init__(self, source_trace: SourceTrace):
        self.source_trace = source_trace

    @property
    def coordinates(self) -> ndarray:
        """
        :return: Вектор координат трассы головного источника
        :rtype: ndarray
        """
        return self.source_trace.coordinates

    @property
    def velocities(self) -> ndarray:
        """
        :return: Веткор скоростей трассы головного источника
        :rtype: ndarray
        """
        return self.source_trace.velocities

    @property
    def coordinates_covariance_matrix(self) -> ndarray:
        """
        :return: Ковариационная матрица координат трассы головного источника
        :rtype: ndarray
        """
        return self.source_trace.coordinate_covariance_matrix
