from math import pi
from unittest import TestCase

import numpy as np

from calc_covariance_matrix import calc_dec_derivative_matrix, calc_sph_derivative_matrix
from calc_covariance_matrix import calc_derivative_r, calc_derivative_beta, calc_derivative_eps
from calc_covariance_matrix import sph2dec_cov_matrix, dec2sph_cov_matrix, elements_of_covariance_matrix
from coordinate_system_math import dec2sph


class TestCalcCovarianceMatrix(TestCase):
    def test_elements_of_covariance_matrix(self):
        """Проверка получения элементов ковариационной матрицы

        :return: None
        """
        # Псевдоковариационная матрица
        covariance_matrix = np.random.normal(size=(3, 3))

        # Посчитанные элементы тестируемой функцией
        elements = elements_of_covariance_matrix(covariance_matrix)

        # Нужные элементы, посчитанные вручную
        real_elements = [covariance_matrix[0][0],
                         covariance_matrix[1][1],
                         covariance_matrix[2][2],
                         covariance_matrix[0][1],
                         covariance_matrix[0][2],
                         covariance_matrix[1][2]]

        # Проверка
        self.assertEqual(real_elements, elements, "Неправильно предоставляется доступ "
                                                  "к элементам ковариационной матрицы")

    def test_dec2sph_and_sph2dec_cov_matrix(self):
        """Проверка пересчётов ковариационных матриц из декартовых координат в сферические и обратно

        :return: None
        """
        # Определим нужные для функции данные
        # Декартовые координаты
        coordinate_dec = np.array([4_000., 5_000., 3_000.])
        # Для сферических координат
        real_covariance_matrix_sph = np.diag([25, 0.01, 1])
        coordinate_sph = dec2sph(coordinate_dec)

        # Применяем последовательно тестируемые функции
        covariance_matrix_dec = sph2dec_cov_matrix(real_covariance_matrix_sph, coordinate_sph)
        covariance_matrix_sph = dec2sph_cov_matrix(covariance_matrix_dec, coordinate_dec)
        covariance_matrix_sph = covariance_matrix_sph.round(7).tolist()

        # Вручную оцененная получающаяся ков. матрица
        real_covariance_matrix_sph = real_covariance_matrix_sph.round(7).tolist()

        # Должны получаться после последовательного преобразования одни и те же матрицы
        self.assertEqual(real_covariance_matrix_sph, covariance_matrix_sph, "После последовательного пересчета "
                                                                            "получились разные ковариационные матрицы")

    def test_calc_derivative_r(self):
        """Проверка расчёта производной по дальности

        :return: None
        """
        # Определим нужные для функции данные
        # Удобные для ручного расчёта декартовые координаты
        coordinates_dec = np.array([3_000., 0., 4_000.])

        # Оценка тестируемой функцией
        derivative_r = calc_derivative_r(coordinates_dec)
        derivative_r = derivative_r.round(7).tolist()

        # Оцененный вручную вектор производных
        real_derivative_r = [3/5, 0, 4/5]

        # Проверка
        self.assertEqual(real_derivative_r, derivative_r, "Производная по дальности оценена неверно")

    def test_calc_derivative_beta(self):
        """Проверка расчета производной по азимуту

        :return: None
        """
        # Определим нужные для функции данные
        # Удобные для ручного расчёта декартовые координаты
        coordinates_dec = np.array([3_000., 1_000., 4_000.])

        # Оценка тестируемой функцией
        derivative_beta = calc_derivative_beta(coordinates_dec)
        derivative_beta = derivative_beta.round(7).tolist()

        # Оцененный вручную вектор производных
        real_derivative_beta = [-4/25_000, 0., 3/25_000]

        # Проверка
        self.assertEqual(real_derivative_beta, derivative_beta, "Производная по азимуту оценена неверно")

    def test_calc_derivative_eps(self):
        """Проверка расчета производной по углу подъёма

        :return: None
        """
        # Определим нужные для функции данные
        # Удобные для ручного расчёта декартовые координаты
        coordinates_dec = np.array([3_000., 5_000., 4_000.])

        # Оценка тестируемой функцией
        derivative_eps = calc_derivative_eps(coordinates_dec)
        derivative_eps = derivative_eps.round(7).tolist()

        # Оцененный вручную вектор производных
        real_derivative_eps = [-6e-05, 0.0001, -8e-05]

        # Проверка
        self.assertEqual(real_derivative_eps, derivative_eps, "Производная по углу подъёма оценена неврно")

    def test_calc_dec_derivative_matrix(self):
        """Проверка расчета матрицы производных декартовых координат по сферическим координатам

        :return: None
        """
        # Определим нужные для тестируемой функции данные
        coordinates_sph = np.array([5_000, pi/6, pi/4])

        # Оценка матрицы производных тестируемой функцией
        derivative_matrix = calc_dec_derivative_matrix(coordinates_sph)
        derivative_matrix = derivative_matrix.round(7).tolist()

        # Оценка матрицы производных вручную
        real_derivative_matrix = [[0.6123724, -1767.766953, -3061.8621785],
                                  [0.7071068, 0.0, 3535.5339059],
                                  [0.3535534, 3061.8621785, -1767.766953]]

        # Проверка
        self.assertEqual(real_derivative_matrix, derivative_matrix, "Матрица производных оценена неверно")

    def test_calc_sph_derivative_matrix(self):
        """Проверка расчета матрицы производных сферических координат по декартовым координатам

        :return: None
        """
        # Определим нужные для тестируемой функции данные
        coordinates_dec = np.array([3_000, 0, 4_000])

        # Оценка матрицы производных тестируемой функцией
        derivative_matrix = calc_sph_derivative_matrix(coordinates_dec)
        derivative_matrix = derivative_matrix.round(7).tolist()

        # Оценка матрицы производных вручную
        real_derivative_matrix = [[0.6, 0.0, 0.8],
                                  [-0.00016, 0.0, 0.00012],
                                  [0.0, 0.0002, 0.0]]

        # Проверка
        self.assertEqual(real_derivative_matrix, derivative_matrix, "Матрица производных оценена неверно")
