from math import sqrt

import numpy as np
from numpy import dot
from numpy.linalg import inv

from EstimatorsForCtaTrace.abstract_estimator_cta_trace_data import AbstractEstimator
from calc_covariance_matrix import calc_derivative_beta, calc_derivative_eps
from calc_covariance_matrix import sph2dec_cov_matrix, dec2sph_cov_matrix, calc_dec_derivative_matrix
from coordinate_system_math import dec2sph
from source_trace import SourceTrace


class EstimatorOneBearingAndOtherNotBearingTraces(AbstractEstimator):
    """
    Класс позволяет провести оценку координат точки с минимальной дисперсией при наличии
    трассы читсой цели и трассы постановщика АШП
    TODO: Требует проверки при большом отношении ошибок углов к ошибке по дальности
    """
    def __init__(self, first_source_trace: SourceTrace, second_source_trace: SourceTrace):
        """
            Должен подготовить экземпляр класса к вычислению координат,
            скоростей и ковариационной матрицы общей точки для пеленга и чистой цели
            :param first_source_trace: Трасса пеленга (SourceTrace)
            :param second_source_trace: Трасса чистой цели (SourceTrace)
        """
        # Сохраним ссылки на трассы
        self.jammer_trace = first_source_trace if first_source_trace.is_bearing else second_source_trace
        self.target_trace = second_source_trace if first_source_trace.is_bearing else first_source_trace
        # Матрицы коэффициентов
        self.coefficient_trg = self.coefficient_anj = np.zeros((3, 3))
        # Ковариационая матрица координат АШП
        self.real_cov_matrix_anj = np.zeros((3, 3))
        # Ковариационая матрица координат АЦ
        self.real_cov_matrix_trg = np.zeros((3, 3))
        # Ковариационные матрицы между координатами точек АШП и АЦ
        self.real_cov_matrix_anj_trg = np.zeros((3, 3))
        self.real_cov_matrix_trg_anj = np.zeros((3, 3))
        # Предсказанные координаты пеленга
        self.est_coordinates_anj = np.zeros(3)
        # Производная коэфициента по координатам трассы АЦ
        self.mfr_anj = np.zeros(3)
        self.coeff_derivative_trg = np.zeros(3)

    @property
    def coordinates(self):
        """
        Метод для расчёт координат общей точки для пеленга и чистой цели.
        Подробнее можно узнать о алгоритме в 513 отделе.
        :return: Координаты триангуляционной точки (ndarrray)
        """
        # Получаем ковариационную матрицу координат АШП
        self.calc_anj_cov_matrix()
        # Получаем ковариационную матрицу между координатами первой и второй целей
        self.calc_anj_trg_cov_matrix()
        # Получаем матрицы коэффициентов для точек положения целей от разных МФР
        self.calculate_coefficient_matrix()
        # Предсказанные координаты пеленга
        self.est_coordinates_anj = self.jammer_trace.calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(self.target_trace)[0]
        # Расчёт оценки координат триангуляционной точки (мб скорости)
        common_point = self.coefficient_anj @ self.est_coordinates_anj + self.coefficient_trg @ self.target_trace.coordinates
        return common_point

    @property
    def velocities(self):
        """
        скорость от пеленга не сильно поможет...
        :return: Вектор скоростей цели
        """
        return self.target_trace.velocities

    @property
    def coordinates_covariance_matrix(self):
        """
        Ковариационная матрица для координат общей точки для пеленга и чистой цели вычисляется как
        A1*K1*A1' + A2*K2*A2' + A1*K12*A2' + A2*K21*A1',
        где A - матрица коээфициентов, K - ковариационные матрицы соотвествующих измерений
        :return: Ковариационная матрица для координат получившейся оценки (ndarray)
        """
        # Ковариационная матрица общей точки для пеленга и чистой цели
        cov_matrix = self.coefficient_anj @ self.real_cov_matrix_anj @ self.coefficient_anj.transpose()
        cov_matrix += self.coefficient_trg @ self.real_cov_matrix_trg @ self.coefficient_trg.transpose()
        cov_matrix += self.coefficient_anj @ self.real_cov_matrix_anj_trg @ self.coefficient_trg.transpose()
        cov_matrix += (self.coefficient_anj @ self.real_cov_matrix_anj_trg @ self.coefficient_trg.transpose()).transpose()
        return cov_matrix

    def calculate_coefficient_matrix(self):
        """
        Расчёт матриц коэффициентов
        :return: None
        """
        # Ковариационная матрица между координатами второй и первой цели
        self.real_cov_matrix_trg_anj = self.real_cov_matrix_anj_trg.transpose()
        # Ковариационая матрица координат АЦ
        self.real_cov_matrix_trg = self.target_trace.coordinate_covariance_matrix
        # Вспомогательные матрицы
        cov_matrix = self.real_cov_matrix_anj + self.real_cov_matrix_trg - (self.real_cov_matrix_anj_trg + self.real_cov_matrix_trg_anj) / 2
        g_matrix_anj = self.real_cov_matrix_anj - (self.real_cov_matrix_trg_anj + self.real_cov_matrix_anj_trg) / 4
        g_matrix_trg = self.real_cov_matrix_trg - (self.real_cov_matrix_trg_anj + self.real_cov_matrix_anj_trg) / 4
        # Матрица коэффициентов для цели первого МФР
        self.coefficient_anj = inv(cov_matrix) @ g_matrix_trg
        # Матрица коэффициентов для цели второго МФР
        self.coefficient_trg = inv(cov_matrix) @ g_matrix_anj

    def calc_anj_cov_matrix(self):
        """
        Расчёт настоящей ковариационной матрицы АШП в декартовых координатах,
        как суммы матриц ковариаций измерений и матрицы ковариаций метода
        :return: None
        """
        # Матрица ошибок метода в сферических координатах
        method_cov_matrix_sph = self.calculate_method_cov_matrix_for_jammer()
        # Матрица ошибок измерений в сферических координатах
        measure_cov_matrix_sph = dec2sph_cov_matrix(self.jammer_trace.coordinate_covariance_matrix, self.jammer_trace.coordinates)
        # Необходимое обнуление некоторых элементов
        self.make_zero_elements_associated_with_range(measure_cov_matrix_sph)
        # Итоговая матрица ошибок в сферических координатах
        cov_matrix_sph = measure_cov_matrix_sph + method_cov_matrix_sph
        # Координаты АШП в сферических координатах
        coords_sph = dec2sph(self.est_coordinates_anj - self.jammer_trace.mfr_position)
        # Итоговая матрица в декартовых координатах
        self.real_cov_matrix_anj = sph2dec_cov_matrix(cov_matrix_sph, coords_sph)

    @staticmethod
    def make_zero_elements_associated_with_range(matrix: np.ndarray):
        """
        # Обнуление элементов ковариационной матрицы в сферических СК
        :param matrix: Ковариационная матрица в сферических координатах
        :return: None
        """
        matrix[0][0] = matrix[1][0] = matrix[2][0] = matrix[0][1] = matrix[0][2] = 0.

    def calculate_method_cov_matrix_for_jammer(self):
        """
        :return: Матрица ошибок метода в сферических координатах
        """
        # Переводим точку в СК МФР АШП
        anj_coords = self.jammer_trace.coordinates - self.jammer_trace.mfr_position
        # Обозначаем для удобства
        anj_cov_matrix = self.jammer_trace.coordinate_covariance_matrix
        trg_cov_matrix = self.target_trace.coordinate_covariance_matrix
        # Вспомогательные векторы
        trg_anj = self.jammer_trace.coordinates - self.target_trace.coordinates
        # Производная коэфициента по координатам трассы АЦ
        self.mfr_anj = self.jammer_trace.coordinates - self.jammer_trace.mfr_position
        mfr_anj_mult = dot(self.mfr_anj, self.mfr_anj)
        self.coeff_derivative_trg = self.mfr_anj / mfr_anj_mult
        # Производная коэфициента по координатам трассы АШП
        coeff_derivative_anj = (-(trg_anj + self.mfr_anj) * mfr_anj_mult + 2 * self.mfr_anj * dot(self.mfr_anj, trg_anj)) / (
                    mfr_anj_mult ** 2)

        d = mfr_anj_mult
        # Дисперсия расстояния от МФР до предпологаемого положения АШП
        var_dist_mfr_est_anj = d * (coeff_derivative_anj @ anj_cov_matrix @ coeff_derivative_anj.transpose() +
                                    self.coeff_derivative_trg @ trg_cov_matrix @ self.coeff_derivative_trg.transpose())
        # Производная beta по координатам трассы АШП
        beta_derivative_anj = calc_derivative_beta(anj_coords)
        # Производная eps по координатам трассы АШП
        eps_derivative_anj = calc_derivative_eps(anj_coords)
        # Ковариация расстояния от МФР до предпологаемого положения АШП и азимута
        cov_dist_beta = sqrt(d) * coeff_derivative_anj @ anj_cov_matrix @ beta_derivative_anj
        # Ковариация расстояния от МФР до предпологаемого положения АШП и угла места
        cov_dist_eps = sqrt(d) * coeff_derivative_anj @ anj_cov_matrix @ eps_derivative_anj
        # Ковариационная матрица ошибок метода
        method_cov_matrix = np.array([[var_dist_mfr_est_anj, cov_dist_beta, cov_dist_eps],
                                      [cov_dist_beta, 0, 0],
                                      [cov_dist_eps, 0, 0]])
        return method_cov_matrix

    def calc_anj_trg_cov_matrix(self):
        """
        Расчёт матрицы ковариаций между координатами точек постановщика АШП и чистой цели
        :return: None
        """
        # Обозначаем для удобства
        cov_matrix_trg = self.target_trace.coordinate_covariance_matrix
        # Переводим в СК МФР АШП
        trg_coords = self.target_trace.coordinates - self.jammer_trace.mfr_position
        # Производная beta по координатам трассы АЦ
        beta_derivative_trg = calc_derivative_beta(trg_coords)
        # Производная eps по координатам трассы АЦ
        eps_derivative_trg = calc_derivative_eps(trg_coords)
        # Производная R до АЦ по координатам АЦ
        x = trg_coords[0]
        y = trg_coords[1]
        z = trg_coords[2]
        r = sqrt(dot(trg_coords, trg_coords))
        dist_derivative_trg = np.array([x / r, y / r, z / r])

        d = sqrt(dot(self.mfr_anj, self.mfr_anj))
        # Ковариация расстояния до АШП и расстояния до АЦ
        cov_dist_anj_dist_trg = d * self.coeff_derivative_trg @ cov_matrix_trg @ dist_derivative_trg
        # Ковариация расстояния до АШП и азимута АЦ
        cov_dist_anj_beta_trg = d * self.coeff_derivative_trg @ cov_matrix_trg @ beta_derivative_trg
        # Ковариация расстояния до АШП и угла места АЦ
        cov_dist_anj_eps_trg = d * self.coeff_derivative_trg @ cov_matrix_trg @ eps_derivative_trg
        # Ковариационная матрица между координатами АШП и АЦ
        cov_matrix_anj_trg = np.array([[cov_dist_anj_dist_trg, cov_dist_anj_beta_trg, cov_dist_anj_eps_trg],
                                       np.zeros(3),
                                       np.zeros(3)])
        nearest_point_in_sph_mfr_coords = dec2sph(self.est_coordinates_anj - self.jammer_trace.mfr_position)

        derivatives_matrix_jammer = calc_dec_derivative_matrix(nearest_point_in_sph_mfr_coords)

        target_coordinates_in_sph_mfr2 = dec2sph(trg_coords)
        derivatives_matrix_target = calc_dec_derivative_matrix(target_coordinates_in_sph_mfr2)

        self.real_cov_matrix_anj_trg = derivatives_matrix_jammer @ cov_matrix_anj_trg @ derivatives_matrix_target.transpose()
