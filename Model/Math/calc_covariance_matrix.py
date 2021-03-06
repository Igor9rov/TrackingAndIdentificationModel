"""Модуль содержит математические функции для различных расчётов, связанных с ковариационными матрицами"""
from math import sin, cos, sqrt, hypot

import numpy as np
from numpy import ndarray, dot


def elements_of_covariance_matrix(covariance_matrix: ndarray) -> list:
    """Получение элементов ковариационнай матрицы

    :param covariance_matrix: Ковариационная матрица
    :type covariance_matrix: ndarray

    :return: Список из 6 элементов: 3 дисперсии и 3 ковариации
    :rtype: list
    """
    # Связь между индексами и координатами
    x, y, z = 0, 1, 2
    # Уникальные элементы ковариационной матрицы
    # Дисперсии
    var_x = covariance_matrix[x][x]
    var_y = covariance_matrix[y][y]
    var_z = covariance_matrix[z][z]
    # Ковариации
    cov_xy = covariance_matrix[x][y]
    cov_xz = covariance_matrix[x][z]
    cov_yz = covariance_matrix[y][z]

    return [var_x, var_y, var_z, cov_xy, cov_xz, cov_yz]


def sph2dec_cov_matrix(covariance_matrix_sph: ndarray, coordinate_sph: ndarray) -> ndarray:
    """Расчёт ковариационной матрицы в декартовых координатах из сферических

    :param covariance_matrix_sph: Ковариационная матрица сферических координат
    :type covariance_matrix_sph: ndarray
    :param coordinate_sph: Вектор сферических координат
    :type coordinate_sph: ndarray

    :return: Ковариационная матрица декартовых координат
    :rtype: ndarray
    """
    # Матрица производных для перехода к декартовым координатам
    derivative_matrix = calc_dec_derivative_matrix(coordinate_sph)
    # Ковариационная матрица в декартовых координатах равна S*K_sph*S'
    covariance_matrix_dec = derivative_matrix @ covariance_matrix_sph @ derivative_matrix.T
    return covariance_matrix_dec


def dec2sph_cov_matrix(covariance_matrix_dec: ndarray, coordinate_dec: ndarray) -> ndarray:
    """Расчёт ковариационной матрицы в декартовых координатах из сферических

    :param covariance_matrix_dec: Ковариационная матрица в декартовых координатах
    :type covariance_matrix_dec: ndarray
    :param coordinate_dec: Вектор декартовых координат
    :type coordinate_dec: ndarray

    :return: Ковариационная матрица в сферичсеких координатах
    """
    # Матрица производных
    derivative_matrix = calc_sph_derivative_matrix(coordinate_dec)

    # Ковариационная матрица в декартовых координатах равна S*K_dec*S'
    covariance_matrix_sph = derivative_matrix @ covariance_matrix_dec @ derivative_matrix.T
    return covariance_matrix_sph


def calc_derivative_r(coordinate_dec: ndarray) -> ndarray:
    """Расчёт вектора производных дальности по декартовым координатам

    :param coordinate_dec: Вектор декартовых координат
    :type coordinate_dec: ndarray

    :return: Вектор производных дальности по декартовым координатам
    :rtype: ndarray
    """
    # Формула для дальности
    r = sqrt(dot(coordinate_dec, coordinate_dec))

    # Производная по дальности
    derivative_r = coordinate_dec / r
    return derivative_r


def calc_derivative_beta(coordinate_dec: ndarray) -> ndarray:
    """Расчёт вектора производных Beta по декартовым координатам

    :param coordinate_dec: Вектор декартовых координат
    :type coordinate_dec: ndarray

    :return: Вектор производных угла Beta по декартовым координатам
    :rtype: ndarray
    """
    x, _, z = coordinate_dec
    hypot_xz = hypot(x, z)

    derivative_beta = np.array([-z / hypot_xz ** 2,
                                0.,
                                x / hypot_xz ** 2])
    return derivative_beta


def calc_derivative_eps(coordinate_dec: ndarray) -> ndarray:
    """Расчёт вектора производных Eps по декартовым координатам

    :param coordinate_dec: Вектор декартовых координат
    :type coordinate_dec: ndarray

    :return: Вектор производных угла Eps по декартовым координатам
    :rtype: ndarray
    """
    x, y, z = coordinate_dec

    r = sqrt(dot(coordinate_dec, coordinate_dec))
    hypot_xz = hypot(x, z)

    derivative_eps = np.array([-x*y / (hypot_xz * r**2),
                               hypot_xz / r**2,
                               -y*z / (hypot_xz * r**2)])
    return derivative_eps


def calc_dec_derivative_matrix(coordinate_sph: ndarray) -> ndarray:
    """Расчёт матрицы производных декартовых координат по сферическим координатам

    :param coordinate_sph: Вектор сферических координат
    :type coordinate_sph: ndarray

    :return: Матрица производных для перехода к декартовым координатам
    :rtype: ndarray
    """
    r, beta, eps = coordinate_sph
    # Формируем элементы матрицы производных
    derivative_matrix = np.zeros([3, 3])

    derivative_matrix[0][0] = cos(beta) * cos(eps)
    derivative_matrix[0][1] = -r * cos(eps) * sin(beta)
    derivative_matrix[0][2] = -r * sin(eps) * cos(beta)

    derivative_matrix[1][0] = sin(eps)
    derivative_matrix[1][1] = 0.
    derivative_matrix[1][2] = r * cos(eps)

    derivative_matrix[2][0] = cos(eps) * sin(beta)
    derivative_matrix[2][1] = r * cos(eps) * cos(beta)
    derivative_matrix[2][2] = -r * sin(eps) * sin(beta)
    return derivative_matrix


def calc_sph_derivative_matrix(coordinate_dec: ndarray) -> ndarray:
    """Расчёт матрицы производных сферических координат по декартовым координатам

    :param coordinate_dec: Вектор декартовых координат
    :type coordinate_dec: ndarray

    :return: Матрица производных для перехода к сферическим координатам
    :rtype: ndarray
    """
    # Матрица производных
    derivative_matrix = np.array([calc_derivative_r(coordinate_dec),
                                  calc_derivative_beta(coordinate_dec),
                                  calc_derivative_eps(coordinate_dec)])
    return derivative_matrix
