from math import cos, sin, pi

import numpy as np


class MobilePartData:
    """Класс, содержащий данные по подвижной части антенны"""
    __slots__ = ("gamma",
                 "eps",
                 "beta",
                 "corrupted_beta",
                 "matrix_gamma",
                 "matrix_eps",
                 "matrix_beta",
                 "matrix_corrupted_beta",
                 "transform_matrix",
                 "corrupted_transform_matrix")

    def __init__(self, error_beta: int = 0) -> None:
        # Пересчёт ошибки по углу в радианы
        error_beta_rad = error_beta * pi / (180 * 60)
        # Угол скручивания антенны
        gamma = 0.
        # Угол наклона антенны
        eps = pi / 6
        # Азимут оси антенны
        beta = 0.
        # Азимут оси антенные с ошибками
        corrupted_beta = beta + error_beta_rad

        # Матрицы поворота по каждому из углов
        matrix_gamma = np.array([[1., 0., 0.],
                                 [0., cos(gamma), sin(gamma)],
                                 [0., -sin(gamma), cos(gamma)]])

        matrix_eps = np.array([[cos(eps), sin(eps), 0.],
                               [-sin(eps), cos(eps), 0.],
                               [0., 0., 1.]])

        matrix_beta = np.array([[cos(beta), 0., sin(beta)],
                                [0., 1., 0.],
                                [-sin(beta), 0., cos(beta)]])

        matrix_corrupted_beta = np.array([[cos(corrupted_beta), 0., sin(corrupted_beta)],
                                          [0., 1., 0.],
                                          [-sin(corrupted_beta), 0., cos(corrupted_beta)]])
        # Матрица, отвечающая за подвижную часть антенны
        self.transform_matrix = matrix_gamma @ matrix_eps @ matrix_beta
        # Матрица, отвечающая за подвижную часть антенны, определённая с ошибками
        self.corrupted_transform_matrix = matrix_gamma @ matrix_eps @ matrix_corrupted_beta
