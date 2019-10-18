from unittest import TestCase

import numpy as np

from calc_covariance_matrix import sph2dec_cov_matrix, dec2sph_cov_matrix
from coordinate_system_math import dec2sph


class TestCalculationCovarianceMatrix(TestCase):
    # Проверка пересчётов ковариационных матриц из декартовых координат в сферические и обратно
    def test_dec2sph_and_sph2dec_cov_matrix(self):
        # Декартовые координаты
        coordinate_dec = [40000., 5000., 89000.]
        # Для сферических координат
        covariance_matrix_sph = np.diag([25, 0.01, 1]).tolist()
        coordinate_sph = dec2sph(coordinate_dec)

        # Пересчитываем в декартовые координаты ковариационную матрицу
        covariance_matrix_dec = sph2dec_cov_matrix(covariance_matrix_sph, coordinate_sph)
        # Пересчитываем обратно в сферические координаты ковариационную матрицу
        calc_covariance_matrix_sph = dec2sph_cov_matrix(covariance_matrix_dec, coordinate_dec)

        # Должны получаться после последовательного преобразования одни и те же матрицы
        self.assertEqual(np.array(covariance_matrix_sph).round(7).tolist(),
                         np.array(calc_covariance_matrix_sph).round(7).tolist())
