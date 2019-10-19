from math import cos, sin, pi

import numpy as np


class MobilePartData:
    """
    Класс, содержащий данные по подвижной части антенны
    """
    __slots__ = ("gamma",
                 "eps",
                 "beta",
                 "transform_matrix")

    def __init__(self):
        # Угол скручивания антенны
        self.gamma = 0.
        # Угол наклона антенны
        self.eps = pi / 6
        # TODO: Добавить зависимость от времени для кругового режима
        # Азимут оси антенны
        self.beta = 0.
        # Матрица, отвечающая за подвижную часть антенны
        self.transform_matrix = np.eye(3)

    def calculate_transform_matrix(self):
        """
        :return: Матрица поворота для подвижной части антенны
        """
        # Матрицы поворота по каждому из углов
        matrix_gamma = np.array([[1, 0, 0],
                                 [0, cos(self.gamma), sin(self.gamma)],
                                 [0, -sin(self.gamma), cos(self.gamma)]])

        matrix_eps = np.array([[cos(self.eps), sin(self.eps), 0],
                               [-sin(self.eps), cos(self.eps), 0],
                               [0, 0, 1]])

        matrix_beta = np.array([[cos(self.beta), 0, sin(self.beta)],
                                [0, 1, 0],
                                [-sin(self.beta), 0, cos(self.beta)]])
        # Вычисление итоговой матрицы поворота
        self.transform_matrix = matrix_gamma @ matrix_eps @ matrix_beta
