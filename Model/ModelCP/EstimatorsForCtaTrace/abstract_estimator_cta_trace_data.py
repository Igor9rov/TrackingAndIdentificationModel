from abc import abstractmethod, ABC


class AbstractEstimator(ABC):
    """Абстрактный класс для оценивателей координат, скоростей, ковариационной матрицы трассы ЕМТ"""
    @property
    @abstractmethod
    def coordinates(self) -> None:
        """
        :return: Вектор координат трассы ЕМТ
        """
        pass

    @property
    @abstractmethod
    def velocities(self) -> None:
        """
        :return: Вектор скоростей трассы ЕМТ
        """
        pass

    @property
    @abstractmethod
    def coordinates_covariance_matrix(self) -> None:
        """
        :return: Ковариационная матрица координат трассы ЕМТ
        """
        pass
