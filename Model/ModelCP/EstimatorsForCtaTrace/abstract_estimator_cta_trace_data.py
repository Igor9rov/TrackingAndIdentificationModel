from abc import abstractmethod, ABC


class AbstractEstimator(ABC):
    """
    Абстрактный класс для оценивателей координат, скоростей, ковариационной матрицы трассы ЕМТ
    """
    @property
    @abstractmethod
    def coordinates(self):
        """
        :return: Вектор координат трассы ЕМТ
        """
        pass

    @property
    @abstractmethod
    def velocities(self):
        """
        :return: Вектор скоростей трассы ЕМТ
        """
        pass

    @property
    @abstractmethod
    def coordinates_covariance_matrix(self):
        """
        :return: Ковариационная матрица координат трассы ЕМТ
        """
        pass
