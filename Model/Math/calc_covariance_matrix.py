import numpy as np
from math import sin, cos, sqrt, hypot


# Расчёт ковариационной матрицы в декартовых координатах из сферических
def calc_dec_from_scs(covariance_matrix_scs, coordinate_scs):
    # Вводим обозначения для удобства записи
    r = coordinate_scs[0]
    beta = coordinate_scs[1]
    eps = coordinate_scs[2]
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
    # Ковариационная матрица в декартовых координатах равна S*K_sph*S'
    covariance_matrix_dec = derivative_matrix @ covariance_matrix_scs @ derivative_matrix.transpose()
    return covariance_matrix_dec


# Расчёт ковариационной матрицы в декартовых координатах из сферических
def calc_scs_from_dec(covariance_matrix_dec, coordinate_dec):
    # Вводим обозначения для удобства записи
    x = coordinate_dec[0]
    y = coordinate_dec[1]
    z = coordinate_dec[2]

    r = sqrt(x ** 2 + y ** 2 + z ** 2)
    hypot_xz = hypot(x, z)
    # Формируем элементы матрицы производных
    derivative_matrix = np.zeros([3, 3])

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
