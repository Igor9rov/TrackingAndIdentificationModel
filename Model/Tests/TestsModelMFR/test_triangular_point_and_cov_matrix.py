import numpy as np


# Поиск ближайшей точки при одном пеленге
def calculate_common_point_for_jammer_and_target(trace_jammer, trace_target):
    # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
    est_anj_coords, est_anj_cov_matrix = trace_jammer.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(
        trace_target)
    # Расчёт оценки координат (мб скорости)
    common_coord_cov_matrix = est_anj_cov_matrix + trace_target.coordinate_covariance_matrix
    A = np.linalg.inv(common_coord_cov_matrix) * trace_target.coordinate_covariance_matrix
    B = np.linalg.inv(common_coord_cov_matrix) * est_anj_cov_matrix
    common_point = A @ est_anj_coords + B @ trace_target.coordinates

    return common_point