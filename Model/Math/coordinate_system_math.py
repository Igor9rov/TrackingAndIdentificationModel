"""
Модуль содержит математические функции для расчётов
"""
from math import sqrt, cos, sin, atan2, hypot

import numpy as np
from numpy import ndarray


def dec2sph(coordinate_dec: ndarray):
    """
    Функция для перехода от прямоугольных декартовых координат к сферическим координатам

    :param coordinate_dec: Вектор декартовых координат

    :return: Вектор сферических координат
    """
    x, y, z = coordinate_dec.tolist()

    # Вычисление элементов результирующего вектора
    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    beta = atan2(z, x)
    eps = atan2(y, hypot(x, z))
    # Результирующий вектор
    coordinate_sph = np.array([r, beta, eps])
    return coordinate_sph


def sph2dec(coordinate_sph: ndarray):
    """
    Функция для перехода от сферических координат к прямоугольным декартовым

    :param coordinate_sph: Вектор сферических координат

    :return: Вектор декартовых координат
    """
    r, beta, eps = coordinate_sph.tolist()

    # Вычисление элементов результирующего вектора
    x = r * cos(beta) * cos(eps)
    y = r * sin(eps)
    z = r * sin(beta) * cos(eps)
    # Результирующий вектор
    coordinate_dec = np.array([x, y, z])
    return coordinate_dec
