from math import cos, sin, pi

import numpy as np


class FixedPartData:
    """Класс, содержащий данные для неповижной части антенны"""
    __slots__ = ("beta_north",
                 "corrupted_beta_north",
                 "eps_long",
                 "eps_cross",
                 "transform_matrix",
                 "corrupted_transform_matrix")

    def __init__(self, error_beta_north: int = 0) -> None:
        # Пересчёт ошибки по углу в радианы (в конструктор она приходит в угловых минутах)
        error_beta_north_rad = error_beta_north * pi / (180 * 60)
        # Азимут строительной оси относительно направления на "Север"
        beta_north = 0.
        # Азимут строительной оси относительно направления на "Север", определённый с ошибками
        corrupted_beta_north = beta_north + error_beta_north_rad
        # Угол невертикальности в продольной плоскости
        eps_long = 0.
        # Угол невертикальности в поперечной плоскости
        eps_cross = 0.

        # Матрицы поворота по каждому из углов
        matrix_beta_north = np.array([[cos(beta_north), 0., sin(beta_north)],
                                     [0., 1., 0.],
                                     [-sin(beta_north), 0., cos(beta_north)]])

        matrix_corrupted_beta_north = np.array([[cos(corrupted_beta_north), 0., sin(corrupted_beta_north)],
                                                [0., 1., 0.],
                                                [-sin(corrupted_beta_north), 0., cos(corrupted_beta_north)]])

        matrix_eps_long = np.array([[cos(eps_long), sin(eps_long), 0.],
                                    [-sin(eps_long), cos(eps_long), 0.],
                                    [0., 0., 1.]])

        matrix_eps_cross = np.array([[1., 0., 0.],
                                     [0., cos(eps_cross), sin(eps_cross)],
                                     [0., -sin(eps_cross), cos(eps_cross)]])
        # Матрица поворота, отвечающая за неподвижную часть антенны
        self.transform_matrix = matrix_eps_cross @ matrix_eps_long @ matrix_beta_north
        # Матрица поворота, отвечающая за неподвижную часть антенны, определенная с ошибками
        self.corrupted_transform_matrix = matrix_eps_cross @ matrix_eps_long @ matrix_corrupted_beta_north
