import unittest

import numpy as np
from numpy.random import normal

from calc_covariance_matrix import sph2dec_cov_matrix
from coordinate_system_math import dec2sph, sph2dec
from estimator_one_bearing_and_other_not_bearing_traces import EstimatorOneBearingAndOtherNotBearingTraces
from source_trace import SourceTrace


class TestEstimatorOneBearingOtherNotBearingCtaTraces(unittest.TestCase):
    def setUp(self) -> None:
        first_trace = SourceTrace()
        first_trace.is_bearing = True
        second_trace = SourceTrace()
        self.estimator = EstimatorOneBearingAndOtherNotBearingTraces(first_trace, second_trace)

    def test_coordinates(self):
        # Подготовка тестового окружения
        self.estimator.jammer_trace.coordinates = np.array([500., 0., -500.])
        self.estimator.jammer_trace.mfr_position = np.array([0., 0., -1000.])
        self.estimator.jammer_trace.coordinate_covariance_matrix = np.eye(3)

        self.estimator.target_trace.coordinates = np.array([1000., 0., 0.])
        self.estimator.target_trace.mfr_position = np.array([0., 0., 1000.])
        self.estimator.target_trace.coordinate_covariance_matrix = np.eye(3)
        # Посчитанное значение координат руками
        res_coords = np.array([1000., 0., 0.])
        # Посчитанное значение координат функцией
        coords = self.estimator.coordinates
        self.assertEqual(coords.round(3).tolist(), res_coords.round(3).tolist())

    def test_coordinates_covariance_matrix(self):
        # Функция для измерения координат трассы
        def measure_trace_coordinates(trace, mean_dec_coord, sigma):
            mean_sph_coord = dec2sph(mean_dec_coord - trace.mfr_position)
            est_sph_coords = normal(mean_sph_coord, sigma)
            trace.coordinates = sph2dec(est_sph_coords) + trace.mfr_position
            trace.coordinate_covariance_matrix = sph2dec_cov_matrix(np.diag(sigma ** 2), est_sph_coords)
        # Координаты МФР
        self.estimator.jammer_trace.mfr_position = np.array([0., 0., -2000.])
        self.estimator.target_trace.mfr_position = np.array([0., 0., 2000.])
        # Мат. ожидание измерений декартовых координат постановщика АШП
        mean_jammer_coordinates = np.array([10000., 0., 0.])
        # Мат. ожидание измерений декартовых координат чистой цели
        mean_target_coordinates = np.array([20000., 0., 2000.])
        # Параметры измерений
        jammer_sigma = np.array([0., 0.00087, 0.00087])
        target_sigma = np.array([10., 0.00087, 0.00087])
        # Количество итераций
        n = 1000
        # Вспомогательные массивы
        coord_array = np.zeros((n, 3))
        cov_array = np.zeros((n, 3, 3))
        for i in range(n):
            measure_trace_coordinates(self.estimator.jammer_trace, mean_jammer_coordinates, jammer_sigma)
            measure_trace_coordinates(self.estimator.target_trace, mean_target_coordinates, target_sigma)
            # Определяем оценку координат результирующей точки
            est_anj_coords = self.estimator.coordinates
            # Считаем ковариационную матрицу результирующей точки
            cov_matrix = self.estimator.coordinates_covariance_matrix
            # Добавляем эту матрицу в массив
            coord_array[i, :] = est_anj_coords
            cov_array[i, :, :] = cov_matrix
        # Создаем общую ковариационную матрицу координат
        coords_cov_matrix = np.cov(coord_array, rowvar=False)
        # Мат ожидание посчинанных ковариационных матриц
        est_coords_cov_matrix = np.mean(cov_array, axis=0)
        # Допускаем различие в 15%
        threshold = 15
        # Разница ковариационных матриц
        difference_in_matrix = abs(est_coords_cov_matrix - coords_cov_matrix)
        # Отношение интересуемых дисперсий в процентах
        diff_x = 100 * difference_in_matrix[0][0] / coords_cov_matrix[0][0]
        diff_y = 100 * difference_in_matrix[1][1] / coords_cov_matrix[1][1]
        diff_z = 100 * difference_in_matrix[2][2] / coords_cov_matrix[2][2]
        self.assertLess(diff_x, threshold)
        self.assertLess(diff_y, threshold)
        self.assertLess(diff_z, threshold)


if __name__ == '__main__':
    unittest.main()
