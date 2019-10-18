from math import sin, cos, sqrt, hypot

import numpy as np
from numpy import ndarray


def sph2dec_cov_matrix(covariance_matrix_sph: ndarray, coordinate_sph: ndarray):
    """
    # Расчёт ковариационной матрицы в декартовых координатах из сферических
    :param covariance_matrix_sph: Ковариационная матрица сферических координат
    :param coordinate_sph: Вектор сферических координат
    :return: Ковариационная матрица декартовых координат
    """
    # Матрица производных для перехода к декартовым координатам
    derivative_matrix = calculate_dec_derivative_matrix(coordinate_sph)
    # Ковариационная матрица в декартовых координатах равна S*K_sph*S'
    covariance_matrix_dec = derivative_matrix @ covariance_matrix_sph @ derivative_matrix.transpose()
    return covariance_matrix_dec


def dec2sph_cov_matrix(covariance_matrix_dec: ndarray, coordinate_dec: ndarray):
    """
    # Расчёт ковариационной матрицы в декартовых координатах из сферических
    :param covariance_matrix_dec: Ковариационная матрица в декартовых координатах
    :param coordinate_dec: Вектор декартовых координат
    :return: Ковариационная матрица в сферичсеких координатах
    """
    x, y, z = coordinate_dec.tolist()

    r = sqrt(x**2 + y**2 + z**2)
    hypot_xz = hypot(x, z)
    # Формируем элементы матрицы производных
    derivative_matrix = np.zeros((3, 3))

    derivative_matrix[0][0] = x / r
    derivative_matrix[0][1] = y / r
    derivative_matrix[0][2] = z / r

    derivative_matrix[1][0] = -z / hypot_xz**2
    derivative_matrix[1][1] = 0.
    derivative_matrix[1][2] = x / hypot_xz**2

    derivative_matrix[2][0] = -x*y / (hypot_xz * r**2)
    derivative_matrix[2][1] = hypot_xz / r**2
    derivative_matrix[2][2] = -y*z / (hypot_xz * r**2)
    # Ковариационная матрица в декартовых координатах равна S*K_dec*S'
    covariance_matrix_sph = derivative_matrix @ covariance_matrix_dec @ derivative_matrix.transpose()
    return covariance_matrix_sph


def calculate_derivative_beta(coordinate_dec: ndarray):
    """
    Расчёт вектора производных Beta по декартовым координатам
    :param coordinate_dec: Вектор декартовых координат
    :return: Вектор производных угла Beta по декартовым координатам
    """
    x, _, z = coordinate_dec.tolist()
    hypot_xz = hypot(x, z)

    return np.array([-z / hypot_xz ** 2,
                    0.,
                    x / hypot_xz ** 2])


def calculate_derivative_eps(coordinate_dec: ndarray):
    """
    Расчёт вектора производных Eps по декартовым координатам
    :param coordinate_dec: Вектор декартовых координат
    :return: Вектор производных угла Eps по декартовым координатам
    """
    x, y, z = coordinate_dec.tolist()

    r = sqrt(x**2 + y**2 + z**2)
    hypot_xz = hypot(x, z)

    return np.array([-x*y / (hypot_xz * r**2),
                    hypot_xz / r**2,
                    -y*z / (hypot_xz * r**2)])


def calculate_dec_derivative_matrix(coordinate_sph: ndarray):
    """
    Расчёт матрицы производных декартовых координат по сферическим координатам
    :param coordinate_sph: Сферические координаты
    :return: Матрица производных: перехода к декартовым координатам
    """
    r, beta, eps = coordinate_sph.tolist()
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
