from math import sqrt

import numpy as np
from numpy import dot
from numpy.linalg import inv

from abstract_estimator_cta_trace_data import AbstractEstimator
from calc_covariance_matrix import calculate_derivative_eps, calculate_derivative_beta, calculate_dec_derivative_matrix
from calc_covariance_matrix import sph2dec_cov_matrix, dec2sph_cov_matrix
from coordinate_system_math import dec2sph
from source_trace import SourceTrace


class EstimatorTwoBearingTraces(AbstractEstimator):
    def __init__(self, first_trace: SourceTrace, second_trace: SourceTrace):
        """
        Должен подготовить экземпляр класса к вычислению координат,
        скоростей и ковариационной матрицы триангуляционной точки
        :param first_trace: Трасса первой цели (SourceTrace)
        :param second_trace: Трасса второй цели (SourceTrace)
        """
        # Сохраним ссылки на трассы
        self.first_trace = first_trace
        self.second_trace = second_trace
        # Инициализируем нужные данные нулями для удобного доступа
        self.mfr_anj_1 = self.mfr_anj_2 = self.base = np.zeros(3)

        self.a = self.b = self.c = self.d = self.f = 0.

        self.num_t = self.num_s = self.den_ts = self.square_den_ts = 0.

        self.t_derivative_1 = self.t_derivative_2 = self.s_derivative_1 = self.s_derivative_2 = np.zeros(3)

        self.variance_s = self.variance_t = self.covariance_st = 0.
        self.beta_derivative_1 = self.eps_derivative_1 = self.beta_derivative_2 = self.eps_derivative_2 = np.zeros(3)

        self.nearest_point_first_bearing = self.nearest_point_second_bearing = np.zeros(3)

        self.real_covariance_matrix_1 = self.real_covariance_matrix_2 = np.zeros((3, 3))

        self.covariance_matrix_12 = self.covariance_matrix_21 = np.zeros(3)

        self.coefficient_1 = self.coefficient_2 = np.zeros((3, 3))

    @property
    def coordinates(self):
        """
        Метод для расчёт координат триангуляционной точки.
        Подробнее можно узнать о алгоритме в 513 отделе.
        :return: Координаты триангуляционной точки (ndarrray)
        """
        # Вектор координат первого измерения в МЗСК МФР
        self.mfr_anj_1 = self.first_trace.coordinates - self.first_trace.mfr_position
        # Вектор координат второго измерения в МЗСК МФР
        self.mfr_anj_2 = self.second_trace.coordinates - self.second_trace.mfr_position
        # Вектор базы между МФР
        self.base = self.first_trace.mfr_position - self.second_trace.mfr_position
        # Коэффициенты
        self.a = dot(self.mfr_anj_1, self.mfr_anj_2)
        self.b = dot(self.mfr_anj_2, self.mfr_anj_2)
        self.c = dot(self.base, self.mfr_anj_2)
        self.d = dot(self.mfr_anj_1, self.mfr_anj_1)
        self.f = dot(self.base, self.mfr_anj_1)
        # Числитель коэффициента t
        self.num_t = self.c * self.d - self.a * self.f
        # Числитель коэффициента s
        self.num_s = self.a * self.c - self.f * self.b
        # Общий знаменатель у коэффициентов t и s
        self.den_ts = self.b * self.d - self.a ** 2
        self.square_den_ts = self.den_ts ** 2

        # Производные t и s по соответсвующим координатам
        self.t_derivative_1 = self._calculate_t_derivative_1()
        self.t_derivative_2 = self._calculate_t_derivative_2()

        self.s_derivative_1 = self._calculate_s_derivative_1()
        self.s_derivative_2 = self._calculate_s_derivative_2()

        # Дисперсия коэффициента s
        self.variance_s = self._calculate_variance_s()
        # Проиводные углов по соответсвующим координатам
        self.beta_derivative_1 = calculate_derivative_beta(self.mfr_anj_1)
        self.eps_derivative_1 = calculate_derivative_eps(self.mfr_anj_1)

        # Коэффициент s для расчёта ближайшей точки на пеленге для первой трассы
        s = self.num_s / self.den_ts
        self.nearest_point_first_bearing = self.first_trace.mfr_position + s * self.mfr_anj_1

        # Реальная ковариационная матрица ближайшей точки на пеленге для первой трассы
        self.real_covariance_matrix_1 = self._calculate_real_covariance_matrix_1()

        # Дисперсия коэффициента t
        self.variance_t = self._calculate_variance_t()
        # Проиводные углов по соответсвующим координатам
        self.beta_derivative_2 = calculate_derivative_beta(self.mfr_anj_2)
        self.eps_derivative_2 = calculate_derivative_eps(self.mfr_anj_2)

        # Коэффициент s для расчёта ближайшей точки на пеленге для второй трассы
        t = self.num_t / self.den_ts
        self.nearest_point_second_bearing = self.second_trace.mfr_position + t * self.mfr_anj_2

        # Реальная ковариационная матрица ближайшей точки на пеленге для второй трассы
        self.real_covariance_matrix_2 = self._calculate_real_covariance_matrix_2()

        # Ковариация коэффициентов s и t
        self.covariance_st = self._calculate_covariance_st()

        # Матрица ковариаций первого и второго измерения ближайших точек на пеленгах
        self.covariance_matrix_12 = self._calculate_covariances_matrix_between_1_and_2()
        # Матрица ковариаций второго и первого измерения ближайших точек на пеленгах
        self.covariance_matrix_21 = self.covariance_matrix_12.transpose()

        # Вспомогательная переменная для расчёта матриц коэффициентов
        sum_covariance_matrix = (self.covariance_matrix_12 + self.covariance_matrix_21) / 4
        # Общая ковариационная матрица (в знаменателе выражения для коэффициентов)
        den_matrix = self.real_covariance_matrix_1 + self.real_covariance_matrix_2 - 2 * sum_covariance_matrix
        # Матрицы коэффициентов
        self.coefficient_1 = inv(den_matrix) @ (self.real_covariance_matrix_2 - sum_covariance_matrix)
        self.coefficient_2 = inv(den_matrix) @ (self.real_covariance_matrix_1 - sum_covariance_matrix)

        return self.coefficient_1 @ self.nearest_point_first_bearing + \
            self.coefficient_2 @ self.nearest_point_second_bearing

    @property
    def velocities(self):
        """
        По одному единичному измерению нельзя определить скорость
        :return: Скорость триангуляционной точки равная 0 (ndarray)
        """
        return np.zeros(3)

    @property
    def coordinates_covariance_matrix(self):
        """
        Ковариационная матрица для координат триангуляционной точки вычисляется как
        A1*K1*A1' + A2*K2*A2' + A1*K12*A2' + A2*K21*A1',
        где A - матрица коээфициентов, K - ковариационные матрицы соотвествующих измерений
        :return: Ковариационная матрица для координат триангуляционной точки (ndarray)
        """
        cov_matrix = self.coefficient_1 @ self.real_covariance_matrix_1 @ self.coefficient_1.transpose()
        cov_matrix += self.coefficient_2 @ self.real_covariance_matrix_2 @ self.coefficient_2.transpose()
        cov_matrix += self.coefficient_1 @ self.covariance_matrix_12 @ self.coefficient_2.transpose()
        cov_matrix += self.coefficient_2 @ self.covariance_matrix_21 @ self.coefficient_1.transpose()
        return cov_matrix

    # Скрытые методы для вычисления

    def _calculate_coefficients_derivatives_1(self):
        """
        :return: Производные коэффициентов по декартовым координатам первой трассы (tuple of ndarrays)
        """
        a_derivative_1 = self.mfr_anj_2
        d_derivative_1 = 2 * self.mfr_anj_1
        f_derivative_1 = self.base
        return a_derivative_1, d_derivative_1, f_derivative_1

    def _calculate_coefficients_derivatives_2(self):
        """
        :return: Производные коэффициентов по декартовым координатам второй трассы (tuple of ndarray)
        """
        a_derivative_2 = self.mfr_anj_1
        b_derivative_2 = 2 * self.mfr_anj_2
        c_derivative_2 = self.base
        return a_derivative_2, b_derivative_2, c_derivative_2

    def _calculate_t_derivative_1(self):
        """
        :return: Производная t по декартовым координатам первой трассы (ndarray)
        """
        a_derivative_1, d_derivative_1, f_derivative_1 = self._calculate_coefficients_derivatives_1()
        num_t_derivative_1 = self.c * d_derivative_1 - self.f * a_derivative_1 - self.a * f_derivative_1
        den_ts_derivative_1 = self.b * d_derivative_1 - 2 * self.a * a_derivative_1
        return (num_t_derivative_1 * self.den_ts - den_ts_derivative_1 * self.num_t) / self.square_den_ts

    def _calculate_t_derivative_2(self):
        """
        :return: Производная t по декартовым координатам второй трассы (ndarray)
        """
        a_derivative_2, b_derivative_2, c_derivative_2 = self._calculate_coefficients_derivatives_2()
        num_t_derivative_2 = self.d * c_derivative_2 - self.f * a_derivative_2
        den_ts_derivative_2 = self.d * b_derivative_2 - 2 * self.a * a_derivative_2
        return (num_t_derivative_2 * self.den_ts - den_ts_derivative_2 * self.num_t) / self.square_den_ts

    def _calculate_s_derivative_1(self):
        """
        :return: Производная s по декартовым координатам первой трассы (ndarray)
        """
        a_derivative_1, d_derivative_1, f_derivative_1 = self._calculate_coefficients_derivatives_1()
        num_s_derivative_1 = a_derivative_1 * self.c - f_derivative_1 * self.b
        den_ts_derivative_1 = self.b * d_derivative_1 - 2 * self.a * a_derivative_1
        return (num_s_derivative_1 * self.den_ts - den_ts_derivative_1 * self.num_s) / self.square_den_ts

    def _calculate_s_derivative_2(self):
        """
        :return: Производная s по декартовым координатам второй трассы (ndarray)
        """
        a_derivative_2, b_derivative_2, c_derivative_2 = self._calculate_coefficients_derivatives_2()
        num_s_derivative_2 = c_derivative_2 * self.a + a_derivative_2 * self.c - b_derivative_2 * self.f
        den_ts_derivative_2 = self.d * b_derivative_2 - 2 * self.a * a_derivative_2
        return (num_s_derivative_2 * self.den_ts - den_ts_derivative_2 * self.num_s) / self.square_den_ts

    # Вычисление дисперсии t
    def _calculate_variance_t(self):
        """
        :return: Дисперсия t (float)
        """
        cov_matrix_1 = self.first_trace.coordinate_covariance_matrix
        cov_matrix_2 = self.second_trace.coordinate_covariance_matrix
        return self.t_derivative_1 @ cov_matrix_1 @ self.t_derivative_1.transpose() + \
            self.t_derivative_2 @ cov_matrix_2 @ self.t_derivative_2.transpose()

    def _calculate_variance_s(self):
        """
        :return: Дисперсия s (float)
        """
        cov_matrix_1 = self.first_trace.coordinate_covariance_matrix
        cov_matrix_2 = self.second_trace.coordinate_covariance_matrix
        return self.s_derivative_1 @ cov_matrix_1 @ self.s_derivative_1.transpose() + \
            self.s_derivative_2 @ cov_matrix_2 @ self.s_derivative_2.transpose()

    def _calculate_covariance_st(self):
        """
        :return: Ковариация s и t (float)
        """
        cov_matrix_1 = self.first_trace.coordinate_covariance_matrix
        cov_matrix_2 = self.second_trace.coordinate_covariance_matrix
        return self.s_derivative_1 @ cov_matrix_1 @ self.t_derivative_1.transpose() + \
            self.s_derivative_2 @ cov_matrix_2 @ self.t_derivative_2.transpose()

    def _calculate_real_covariance_matrix_1(self):
        """
        :return: Настоящая ковариационная матрица ближайшей точки на пеленге от первой трассы (ndarray)
        """
        cov_matrix_1 = self.first_trace.coordinate_covariance_matrix

        variance_r1 = self.d * self.variance_s
        covariance_r1b1 = sqrt(self.d) * (self.s_derivative_1 @ cov_matrix_1 @ self.beta_derivative_1.transpose())
        covariance_r1e1 = sqrt(self.d) * (self.s_derivative_1 @ cov_matrix_1 @ self.eps_derivative_1.transpose())

        sph_covariance_matrix1 = dec2sph_cov_matrix(cov_matrix_1, self.mfr_anj_1)
        sph_covariance_matrix1[0][0] = variance_r1
        sph_covariance_matrix1[0][1] = sph_covariance_matrix1[1][0] = covariance_r1b1
        sph_covariance_matrix1[0][2] = sph_covariance_matrix1[2][0] = covariance_r1e1

        nearest_point_in_sph_mfr_coord_1 = dec2sph(self.nearest_point_first_bearing - self.first_trace.mfr_position)
        return sph2dec_cov_matrix(sph_covariance_matrix1, nearest_point_in_sph_mfr_coord_1)

    def _calculate_real_covariance_matrix_2(self):
        """
        :return: Настоящая ковариационная матрица ближайшей точки на пеленге от второй трассы (ndarray)
        """
        cov_matrix_2 = self.second_trace.coordinate_covariance_matrix

        variance_r2 = self.b * self.variance_t
        covariance_r2b2 = sqrt(self.b) * (self.t_derivative_2 @ cov_matrix_2 @ self.beta_derivative_2.transpose())
        covariance_r2e2 = sqrt(self.b) * (self.t_derivative_2 @ cov_matrix_2 @ self.eps_derivative_2.transpose())

        sph_covariance_matrix2 = dec2sph_cov_matrix(cov_matrix_2, self.mfr_anj_2)
        sph_covariance_matrix2[0][0] = variance_r2
        sph_covariance_matrix2[0][1] = sph_covariance_matrix2[1][0] = covariance_r2b2
        sph_covariance_matrix2[0][2] = sph_covariance_matrix2[2][0] = covariance_r2e2

        nearest_point_in_sph_mfr_coord_2 = dec2sph(self.nearest_point_second_bearing - self.second_trace.mfr_position)
        return sph2dec_cov_matrix(sph_covariance_matrix2, nearest_point_in_sph_mfr_coord_2)

    def _calculate_covariances_matrix_between_1_and_2(self):
        """
        :return: Матрица ковариации между ближайшими точками от первой и второй трассы (ndarray)
        """
        cov_matrix_1 = self.first_trace.coordinate_covariance_matrix
        cov_matrix_2 = self.second_trace.coordinate_covariance_matrix

        covariance_r1r2 = sqrt(self.b * self.d) * self.covariance_st
        covariance_r1b2 = sqrt(self.d) * (self.s_derivative_2 @ cov_matrix_2 @ self.beta_derivative_2)
        covariance_r1e2 = sqrt(self.d) * (self.s_derivative_2 @ cov_matrix_2 @ self.eps_derivative_2)
        covariance_r2b1 = sqrt(self.b) * (self.t_derivative_1 @ cov_matrix_1 @ self.beta_derivative_1)
        covariance_r2e1 = sqrt(self.b) * (self.t_derivative_1 @ cov_matrix_1 @ self.eps_derivative_1)

        sph_covariance_matrix12 = np.zeros((3, 3))
        sph_covariance_matrix12[0][0] = covariance_r1r2
        sph_covariance_matrix12[0][1] = covariance_r1b2
        sph_covariance_matrix12[0][2] = covariance_r1e2
        sph_covariance_matrix12[1][0] = covariance_r2b1
        sph_covariance_matrix12[2][0] = covariance_r2e1

        nearest_point_in_sph_mfr_coord_1 = dec2sph(self.nearest_point_first_bearing - self.first_trace.mfr_position)
        derivative_matrix_1 = calculate_dec_derivative_matrix(nearest_point_in_sph_mfr_coord_1)

        nearest_point_in_sph_mfr_coord_2 = dec2sph(self.nearest_point_second_bearing - self.second_trace.mfr_position)
        derivative_matrix_2 = calculate_dec_derivative_matrix(nearest_point_in_sph_mfr_coord_2)

        return derivative_matrix_1 @ sph_covariance_matrix12 @ derivative_matrix_2.transpose()
