from unittest import TestCase
import numpy as np
from calc_covariance_matrix import calc_dec_from_scs, calc_scs_from_dec
from coordinate_system_math import dec2sph


class TestCalculationCovarianceMatrix(TestCase):
    # Проверка пересчётов ковариационных матриц из декартовых координат в сферические и обратно
    def test_dec_from_scs_and_scs_from_dec(self):
        # Декартовые координаты
        coordinate_dec = [40000., 5000., 89000.]
        # Для сферических координат
        covariance_matrix_scs = np.diag([25, 0.01, 1]).tolist()
        coordinate_scs = dec2sph(coordinate_dec)

        # Пересчитываем в декартовые координаты ковариационную матрицу
        covariance_matrix_dec = calc_dec_from_scs(covariance_matrix_scs, coordinate_scs)
        # Пересчитываем обратно в сферические координаты ковариационную матрицу
        calc_covariance_matrix_scs = calc_scs_from_dec(covariance_matrix_dec, coordinate_dec)

        # Должны получаться после последовательного преобразования одни и те же матрицы
        self.assertEqual(np.array(covariance_matrix_scs).round(7).tolist(),
                         np.array(calc_covariance_matrix_scs).round(7).tolist())
