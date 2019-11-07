from math import cos, sin, pi

import numpy as np


class MobilePartData:
    """Класс, содержащий данные по подвижной части антенны"""
    __slots__ = ("gamma",
                 "eps",
                 "beta",
                 "matrix_gamma",
                 "matrix_eps",
                 "matrix_beta",
                 "transform_matrix")

    def __init__(self, error_beta: int = 0):
        # Пересчёт ошибки по углу в радианы
        error_beta_rad = error_beta * pi / (180 * 60)
        # Угол скручивания антенны
        self.gamma = 0.
        # Угол наклона антенны
        self.eps = pi / 6
        # TODO: Добавить зависимость от времени для кругового режима
        # Азимут оси антенны
        self.beta = 0. + error_beta_rad

        # Матрицы поворота по каждому из углов
        self.matrix_gamma = np.array([[1., 0., 0.],
                                      [0., cos(self.gamma), sin(self.gamma)],
                                      [0., -sin(self.gamma), cos(self.gamma)]])

        self.matrix_eps = np.array([[cos(self.eps), sin(self.eps), 0.],
                                    [-sin(self.eps), cos(self.eps), 0.],
                                    [0., 0., 1.]])

        self.matrix_beta = np.array([[cos(self.beta), 0., sin(self.beta)],
                                     [0., 1., 0.],
                                     [-sin(self.beta), 0., cos(self.beta)]])
        # Матрица, отвечающая за подвижную часть антенны
        self.transform_matrix = self.matrix_gamma @ self.matrix_eps @ self.matrix_beta

    def calculate_transform_matrix(self):
        """
        :return: Матрица поворота для подвижной части антенны
        """
        # TODO: Временно ничего, так как кругового режима пока нет, значит матрица не изменяется
        pass
