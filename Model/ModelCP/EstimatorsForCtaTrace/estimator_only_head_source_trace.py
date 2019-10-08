from abstract_estimator_cta_trace_data import AbstractEstimator
from source_trace import SourceTrace


class EstimatorOnlyHeadSourceTrace(AbstractEstimator):
    def __init__(self, source_trace: SourceTrace):
        self.source_trace = source_trace

    @property
    def coordinates(self):
        return self.source_trace.coordinates

    @property
    def velocities(self):
        return self.source_trace.velocities

    @property
    def coordinates_covariance_matrix(self):
        return self.source_trace.coordinate_covariance_matrix
