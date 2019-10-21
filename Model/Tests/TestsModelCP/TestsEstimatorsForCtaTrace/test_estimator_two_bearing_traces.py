from unittest import TestCase

import numpy as np
from numpy.random import normal

from calc_covariance_matrix import sph2dec_cov_matrix
from coordinate_system_math import dec2sph, sph2dec
from estimator_two_bearing_traces import EstimatorTwoBearingTraces
from source_trace import SourceTrace


class TestEstimatorTwoBearingCtaTraces(TestCase):
    def setUp(self) -> None:
        # Первая трасса
        first_trace = SourceTrace(mfr_position=np.array([1500., 0., 0.]))
        first_trace.coordinates = np.array([750., 0., 750.])
        self.mean_first_sph_coord = dec2sph(first_trace.coordinates - first_trace.mfr_position)
        # Вторая трасса
        second_trace = SourceTrace(mfr_position=np.array([-1500., 0., 0.]))
        second_trace.coordinates = np.array([-750., 0., 750.])
        self.mean_second_sph_coord = dec2sph(second_trace.coordinates - second_trace.mfr_position)
        # Свой оцениватель
        self.estimator = EstimatorTwoBearingTraces(first_trace, second_trace)

    # Тест для координат
    def test_coordinates(self):
        # Оценка координат
        coordinates = self.estimator.coordinates
        # Сравнение с уже посчитанным
        self.assertEqual(coordinates.round(1).tolist(), np.array([0., 0., 1500]).tolist())

    def test_velocities(self):
        # Оценка скоростей
        velocities = self.estimator.velocities
        # Сравнение с уже посчитанным
        self.assertEqual(velocities.tolist(), np.zeros(3).tolist())

    # Тест для расчета ковариационных матриц
    def test_coordinate_covariance_matrix(self):
        # Получаем координаты цели и ковариационные матрицы
        def estimate_coords_and_covariance_matrix(trace, mean_sph_coord, sigma):
            est_sph_coords = normal(mean_sph_coord, sigma)
            trace.coordinates = sph2dec(est_sph_coords) + trace.mfr_position
            trace.coordinate_covariance_matrix = sph2dec_cov_matrix(np.diag(sigma ** 2), est_sph_coords)
        # Параметры измерений
        first_sigma = np.array([0., 0.0029, 0.0029])
        second_sigma = 10 * first_sigma
        # Количество измерений
        n = 1000
        coord_array = np.zeros((n, 3))
        cov_array = np.zeros((n, 3, 3))
        for iteration in range(n):
            # Измерения координат и ковариационных матриц
            estimate_coords_and_covariance_matrix(self.estimator.first_trace, self.mean_first_sph_coord, first_sigma)
            estimate_coords_and_covariance_matrix(self.estimator.second_trace, self.mean_second_sph_coord, second_sigma)

            coord_array[iteration, :] = self.estimator.coordinates
            cov_array[iteration, :, :] = self.estimator.coordinates_covariance_matrix
        # Вычисление ковариационных матриц как МО оценки ков. матрицы и оценка по реальному распредлению
        real_covariance_matrix = np.cov(coord_array, rowvar=False)
        estimated_covariance_matrix = np.mean(cov_array, axis=0)
        # Разница ковариационных матриц
        difference_in_matrix = abs((estimated_covariance_matrix - real_covariance_matrix))
        diff_x = 100 * difference_in_matrix[0][0] / real_covariance_matrix[0][0]
        diff_y = 100 * difference_in_matrix[1][1] / real_covariance_matrix[1][1]
        diff_z = 100 * difference_in_matrix[2][2] / real_covariance_matrix[2][2]
        # Допускаем различие в 12%
        threshold = 12
        # Сравнение интересуемых дисперсий
        self.assertLess(diff_x, threshold)
        self.assertLess(diff_y, threshold)
        self.assertLess(diff_z, threshold)
