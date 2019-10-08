from abc import abstractmethod, ABC


class AbstractEstimator(ABC):
    @property
    @abstractmethod
    def coordinates(self):
        pass

    @property
    @abstractmethod
    def velocities(self):
        pass

    @property
    @abstractmethod
    def coordinates_covariance_matrix(self):
        pass
