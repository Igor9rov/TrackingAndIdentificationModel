from math import cos, sin

import numpy as np


# Класс, содержащий данные для неповижной части антенны
class FixedPartData:
    __slots__ = ("beta_north",
                 "eps_long",
                 "eps_cross",
                 "transform_matrix")

    def __init__(self):
        # Азимут строительной оси относительно направления на "Север"
        self.beta_north = 0.
        # Угол невертикальности в продольной плоскости
        self.eps_long = 0.
        # Угол невертикальности в поперечной плоскости
        self.eps_cross = 0.
        # Матрица отвечающая за неподвижную часть антенны
        self.transform_matrix = np.eye(3)

    # Вычисление матрицы поворота для неподвижной части антенны
    def calculate_transform_matrix(self):
        # Матрицы поворота
        matrix_beta_null = np.array([[cos(self.beta_north), 0, sin(self.beta_north)],
                                     [0, 1, 0],
                                     [-sin(self.beta_north), 0, cos(self.beta_north)]])

        matrix_eps_long = np.array([[cos(self.eps_long), sin(self.eps_long), 0],
                                    [-sin(self.eps_long), cos(self.eps_long), 0],
                                    [0, 0, 1]])

        matrix_eps_cross = np.array([[1, 0, 0],
                                     [0, cos(self.eps_cross), sin(self.eps_cross)],
                                     [0, -sin(self.eps_cross), cos(self.eps_cross)]])
        # Вычисление итоговой матрицы поворота
        self.transform_matrix = matrix_eps_cross @ matrix_eps_long @ matrix_beta_null
