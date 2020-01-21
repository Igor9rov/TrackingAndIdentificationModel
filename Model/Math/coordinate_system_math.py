"""Модуль содержит математические функции для перехода от прямоугольной декартовой СК к сферической СК и обратно"""
from math import sqrt, cos, sin, atan2, hypot

import numpy as np
from numpy import ndarray, dot


def dec2sph(coordinate_dec: ndarray) -> ndarray:
    """Функция для перехода от прямоугольных декартовых координат к сферическим координатам

    :param coordinate_dec: Вектор декартовых координат
    :type coordinate_dec: ndarray

    :return: Вектор сферических координат
    :rtype: ndarray
    """
    x, y, z = coordinate_dec

    # Вычисление элементов результирующего вектора
    r = sqrt(dot(coordinate_dec, coordinate_dec))
    beta = atan2(z, x)
    eps = atan2(y, hypot(x, z))
    # Результирующий вектор
    coordinate_sph = np.array([r, beta, eps])
    return coordinate_sph


def sph2dec(coordinate_sph: ndarray) -> ndarray:
    """Функция для перехода от сферических координат к прямоугольным декартовым

    :param coordinate_sph: Вектор сферических координат
    :type coordinate_sph: ndarray

    :return: Вектор декартовых координат
    :rtype: ndarray
    """
    r, beta, eps = coordinate_sph

    # Вычисление элементов результирующего вектора
    x = r * cos(beta) * cos(eps)
    y = r * sin(eps)
    z = r * sin(beta) * cos(eps)
    # Результирующий вектор
    coordinate_dec = np.array([x, y, z])
    return coordinate_dec
