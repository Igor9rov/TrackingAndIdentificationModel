import numpy as np
from math import sqrt
from numpy import dot, linalg

from calc_covariance_matrix import calc_dec_from_scs, calc_scs_from_dec
from coordinate_system_math import dec2sph


# Поиск триангуляционной точки при одном пеленге
def calculate_triangular_point_for_jammer_and_target(trace_jammer, trace_target):
    # Получаем ковариационная матрица координат чистой цели
    trg_cov_matrix = trace_target.coordinate_covariance_matrix
    # Получаем ковариационная матрица координат АШП
    anj_cov_matrix = calc_anj_cov_matrix(trace_jammer, trace_target)
    # Получаем ковариационная матрица между координатами первой и второй целей
    ang_trg_cov_matrix = calc_anj_trg_cov_matrix(trace_jammer, trace_target)
    # Получаем матрицы коэффициентов для точек положения целей от разных МФР
    A, B = calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, ang_trg_cov_matrix)
    # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
    est_anj_coords, est_anj_cov_matrix = trace_jammer.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(
        trace_target)
    # Расчёт оценки координат триангуляционной точки (мб скорости)
    common_point = A @ est_anj_coords + B @ trace_target.coordinates
    return common_point


# Расчёт матриц коэффициентов триангуляционной точки
def calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, anj_trg_cov_matrix):
    # Ковариационная матрица между координатами второй и первой цели
    trg_anj_cov_matrix = anj_trg_cov_matrix.transpose()
    # Вспомогательные матрицы
    cov_matrix = anj_cov_matrix + trg_cov_matrix - anj_trg_cov_matrix - trg_anj_cov_matrix
    anj_g_matrix = anj_cov_matrix - (trg_anj_cov_matrix + anj_trg_cov_matrix) / 2
    trg_g_matrix = trg_cov_matrix - (trg_anj_cov_matrix + anj_trg_cov_matrix) / 2
    cov_matrix_ = linalg.inv(cov_matrix)
    # Матрица коэффициентов для цели первого МФР
    A = cov_matrix_ @ trg_g_matrix
    # Матрица коэффициентов для цели второго МФР
    B = cov_matrix_ @ anj_g_matrix
    return A, B


# Расчёт ковариационной матрицы триангуляционной точки
def calculate_cov_matrix_of_triangular_point_for_jammer_and_target (trace_jammer, trace_target):
    # Получаем ковариационная матрица координат чистой цели
    trg_cov_matrix = trace_target.coordinate_covariance_matrix
    # Получаем ковариационная матрица координат АШП
    anj_cov_matrix = calc_anj_cov_matrix(trace_jammer, trace_target)
    # Получаем ковариационная матрица между координатами первой и второй целей
    ang_trg_cov_matrix = calc_anj_trg_cov_matrix(trace_jammer, trace_target)
    # Получаем матрицы коэффициентов для точек положения целей от разных МФР
    A, B = calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, ang_trg_cov_matrix)
    A_t = A.transpose()
    B_t = B.transpose()
    # Ковариационная матрица триангуляционной точки
    triang_cov_matrix = A @ anj_cov_matrix @ A_t + B @ trg_cov_matrix @ B_t + A @ ang_trg_cov_matrix @ B_t + \
                        (A @ ang_trg_cov_matrix @ B_t).transpose
    return triang_cov_matrix


# Расчёт ковариационной матрицы между координатами точек АШП и АЦ
def calc_anj_trg_cov_matrix(trace_jammer, trace_target):
    # Обозначаем для удобства
    trg_cov_matrix = trace_target.coordinate_covariance_matrix
    coords_trg = trace_target.coordinates
    # Вспомогательные векторы
    mfr_anj = trace_jammer.coordinates - trace_jammer.mfr_position
    # Производная коэфициента по координатам трассы АЦ
    coeff_trg = mfr_anj / dot(mfr_anj, mfr_anj)
    # Производная beta АЦ по координатам трассы АЦ
    # Координаты АЦ
    x = coords_trg[0]
    y = coords_trg[1]
    z = coords_trg[2]
    trg_beta_trg = np.array([-x / (x ** 2 + z ** 2), 0, (x ** 2 + 2 * z ** 2) / (x * (x ** 2 + z ** 2))])
    # Производная eps по координатам трассы АШП
    q = x ** 2 + y ** 2 + z ** 2
    trg_eps_trg = np.array([-x * y / (sqrt(x ** 2 + z ** 2) * q), sqrt(x ** 2 + z ** 2) / q ** 1.5,
                       -z * y / (sqrt(x ** 2 + z ** 2) * q)])
    # Производная R до АЦ по координатам АЦ
    r = sqrt(q)
    trg_dist_trg = np.array([x / r, y / r, z / r])
    # Ковариация расстояния до АШП и расстояния до АЦ
    d = sqrt(mfr_anj[0]**2 + mfr_anj[1]**2 + mfr_anj[2]**2)
    cov_dist_anj_dist_trg = d @ coeff_trg @ trg_cov_matrix @ trg_dist_trg
    # Ковариация расстояния до АШП и азимута АЦ
    cov_dist_anj_beta_trg = d @ coeff_trg @ trg_cov_matrix @ trg_beta_trg
    # Ковариация расстояния до АШП и угла места АЦ
    cov_dist_anj_eps_trg = d @ coeff_trg @ trg_cov_matrix @ trg_eps_trg
    # Ковариационная матрица между координатами АШП и АЦ
    enj_trg_cov_matrix = np.array([[cov_dist_anj_dist_trg, cov_dist_anj_beta_trg, cov_dist_anj_eps_trg], [0, 0, 0], [0, 0, 0]])
    return enj_trg_cov_matrix


# Расчёт итоговой ковариационной матрицы АШП в декартовых координатах
def calc_anj_cov_matrix(trace_jammer, trace_target):
    # Матрица ошибок метода в сферических координатах
    method_cov_matrix_sph = calculate_method_cov_matrix_for_jammer(trace_jammer, trace_target)
    # Матрица ошибок измерений в сферических координатах
    measure_cov_matrix_sph = calc_scs_from_dec(trace_jammer.coordinate_covariance_matrix, trace_jammer.coordinates)
    # Итоговая матрица ошибок в сферических координатах
    cov_matrix_sph = measure_cov_matrix_sph + method_cov_matrix_sph
    # Координаты АШП в сферических координатах
    coords_sph = dec2sph(trace_jammer.coordinates)
    # Итоговая матрица в декартовых координатах
    cov_matrix_dec = calc_dec_from_scs(cov_matrix_sph, coords_sph)
    return cov_matrix_dec


# Расчёт матрицы ошибок метода в сферических координатах
def calculate_method_cov_matrix_for_jammer(trace_jammer, trace_target):
    # Обозначаем для удобства
    cov_matrix_anj = trace_jammer.coordinate_covariance_matrix
    cov_matrix_trg = trace_target.coordinate_covariance_matrix
    coords_anj = trace_jammer.coordinates
    # Вспомогательные векторы
    mfr_anj = trace_jammer.coordinates - trace_jammer.mfr_position
    trg_anj = trace_jammer.coordinates - trace_target.coordinates
    # Производная коэфициента по координатам трассы АЦ
    coeff_trg = mfr_anj / dot(mfr_anj, mfr_anj)
    # Производная коэфициента по координатам трассы АШП
    coeff_anj = -((trg_anj + mfr_anj) * dot(mfr_anj, mfr_anj) - 2 * mfr_anj * dot(mfr_anj, trg_anj)) / (dot(mfr_anj, mfr_anj))**2
    # Дисперсия расстояния от МФР до предпологаемого положения АШП
    d = mfr_anj[0]**2 + mfr_anj[1]**2 + mfr_anj[2]**2
    var_dist_mfr_est_anj = d * (coeff_anj @ cov_matrix_anj @ coeff_anj.transpose() +
                           coeff_trg @ cov_matrix_trg @ coeff_trg.transpose())
    # Производная beta по координатам трассы АШП
    x = coords_anj[0]
    y = coords_anj[1]
    z = coords_anj[2]
    beta_anj = np.array([-x/(x**2+z**2), 0, (x**2+2*z**2)/(x*(x**2+z**2))])
    # Производная eps по координатам трассы АШП
    q = x ** 2 + y ** 2 + z ** 2
    eps_anj = np.array([-x*y/(sqrt(x**2+z**2)*q), sqrt(x**2+z**2)/q**1.5],
                       -z*y/(sqrt(x**2+z**2)*q))
    # Ковариация расстояния от МФР до предпологаемого положения АШП и азимута
    cov_dist_beta = sqrt(d) * coeff_anj * cov_matrix_anj * beta_anj
    # Ковариация расстояния от МФР до предпологаемого положения АШП и угла места
    cov_dist_eps = sqrt(d) * coeff_anj * cov_matrix_anj * eps_anj

    # Ковариационная матрица ошибок метода
    method_cov_matrix = np.array([[var_dist_mfr_est_anj, cov_dist_beta, cov_dist_eps], [cov_dist_beta, 0, 0],
                                  [cov_dist_eps, 0, 0]])
    return method_cov_matrix
