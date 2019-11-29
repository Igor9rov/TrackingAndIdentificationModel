from unittest import TestCase

import numpy as np


from calc_covariance_matrix import sph2dec_cov_matrix, dec2sph_cov_matrix, elements_of_covariance_matrix
from calc_covariance_matrix import calc_derivative_r, calc_derivative_beta, calc_derivative_eps
from coordinate_system_math import dec2sph


class TestCalcCovarianceMatrix(TestCase):
    def test_elements_of_covariance_matrix(self):
        """Проверка получения элементов ковариационной матрицы

        :return: None
        """
        # Псевдоковариационная матрица
        covariance_matrix = np.random.normal(size=(3, 3))
        # Нужные элементы
        real_elements = [covariance_matrix[0][0],
                         covariance_matrix[1][1],
                         covariance_matrix[2][2],
                         covariance_matrix[0][1],
                         covariance_matrix[0][2],
                         covariance_matrix[1][2]]

        # Посчитанные элементы
        elements = elements_of_covariance_matrix(covariance_matrix)

        # Проверка
        self.assertEqual(real_elements, elements)

    def test_dec2sph_and_sph2dec_cov_matrix(self):
        """Проверка пересчётов ковариационных матриц из декартовых координат в сферические и обратно

        :return: None
        """
        # Декартовые координаты
        coordinate_dec = np.array([4_000., 5_000., 3_000.])
        # Для сферических координат
        covariance_matrix_sph = np.diag([25, 0.01, 1])
        coordinate_sph = dec2sph(coordinate_dec)

        # Пересчитываем в декартовые координаты ковариационную матрицу
        covariance_matrix_dec = sph2dec_cov_matrix(covariance_matrix_sph, coordinate_sph)
        # Пересчитываем обратно в сферические координаты ковариационную матрицу
        calc_covariance_matrix_sph = dec2sph_cov_matrix(covariance_matrix_dec, coordinate_dec)

        # Должны получаться после последовательного преобразования одни и те же матрицы
        self.assertEqual(np.array(covariance_matrix_sph).round(7).tolist(),
                         np.array(calc_covariance_matrix_sph).round(7).tolist())

    def test_calc_derivative_r(self):
        """Проверка расчёта производной по дальности

        :return: None
        """
        # Удобные для ручного расчёта декартовые координаты
        coordinates_dec = np.array([3_000., 0., 4_000.])
        # Оцененный вручную вектор производных
        real_derivative_r = np.array([3/5, 0, 4/5])
        # Оценка функцией
        derivative_r = calc_derivative_r(coordinates_dec)

        # Проверка
        self.assertEqual(real_derivative_r.round(7).tolist(), derivative_r.round(7).tolist())

    def test_calc_derivative_beta(self):
        """Проверка расчета производной по углу бета

        :return: None
        """
        # Удобные для ручного расчёта декартовые координаты
        coordinates_dec = np.array([3_000., 1_000., 4_000.])
        # Оцененный вручную вектор производных
        real_derivative_beta = np.array([-4/25_000, 0., 3/25_000])

        # Оценка функцией
        derivative_beta = calc_derivative_beta(coordinates_dec)

        # Проверка
        self.assertEqual(real_derivative_beta.round(7).tolist(), derivative_beta.round(7).tolist())

    def test_calc_derivative_eps(self):
        """Проверка расчета производной по углу бета

        :return: None
        """
        # Удобные для ручного расчёта декартовые координаты
        coordinates_dec = np.array([3_000., 5_000., 4_000.])
        # Оцененный вручную вектор производных
        real_derivative_eps = np.array([-6e-05, 0.0001, -8e-05])

        # Оценка функцией
        derivative_eps = calc_derivative_eps(coordinates_dec)

        # Проверка
        self.assertEqual(real_derivative_eps.round(7).tolist(), derivative_eps.round(7).tolist())

    def test_calc_dec_derivative_matrix(self):
        """Проверка расчета матрицы производных декартовых координат по сферическим координатам

        :return: None
        """
        # TODO: Написать тест, нужно придумать матрицу и координаты для легкого ручного расчёта
        pass

    def test_calc_sph_derivative_matrix(self):
        """Проверка расчета матрицы производных сферических координат по декартовым координатам

        :return: None
        """
        # TODO: Написать тест, нужно придумать матрицу и координаты для легкого ручного расчёта
        pass
