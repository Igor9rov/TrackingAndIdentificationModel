import numpy as np
from math import sqrt, hypot
from numpy import cross, dot, ndarray
from numpy.linalg import inv

from calc_covariance_matrix import calc_dec_from_scs, calc_scs_from_dec
from coordinate_system_math import dec2sph
from model_time import time_in_tick

# Порог отождествления для случая с двумя степенями свободы
identification_threshold_2d = 9.21
# Порог отождествления для случая с тремя степенями свободы
identification_threshold_3d = 11.345


# Класс, описывающий данные по трассе источника, которыми пользуется ПБУ
class SourceTrace:
    def __init__(self, mfr_number: int, mfr_position: ndarray, target_number: int = 0):
        # Номер МФР
        self.mfr_number = mfr_number
        # Номер цели
        self.target_number = target_number
        # Точка стояния МФР
        self.mfr_position = mfr_position
        # Координаты в системе координат ПБУ
        self.coordinates = np.zeros(3)
        # Скорости в системе координат ПБУ
        self.velocities = np.zeros(3)
        # Ковариационная матрица координат
        self.coordinate_covariance_matrix = np.eye(3)
        # Признак пеленга
        self.is_bearing = False
        # Признак АС
        self.is_auto_tracking = False
        # Время оценки координат
        self.estimate_tick = 0
        # Признак, есть ли трасса ЕМТ по такой трассе источника
        self.is_in_common_trace_array = False
        # Признак головного источника
        self.is_head_source = False
        # Обобщённое рассстояние между головным источником по той же трассе ЕМТ
        self.probability_measure = 0.
        # Номер трассы в ЕМТ
        self.cta_number = -1
        # Словарь для трасс, с которыми отождествилась трасса
        self.identified_number_cta_trace_dict = {}

    # Получение номеров трасс с которыми отождествилась трасса
    def get_identified_cta_trace_numbers(self):
        return list(self.identified_number_cta_trace_dict.values())

    # Очищение словаря трасс, с которыми отождествилась трасса
    def clear_identified_number_cta_trace_dict(self):
        self.identified_number_cta_trace_dict = {}

    # Получение номера трассы ЕМТ с минимальным обобщённым расстоянием
    def get_num_cta_trace_with_min_distance(self):
        min_generalized_distance = min(self.identified_number_cta_trace_dict)
        return self.identified_number_cta_trace_dict.get(min_generalized_distance)

    # Добавление информации и номера трассы ЕМТ
    def append_cta_info_and_number(self, num: int, is_head: bool):
        self.cta_number = num
        self.is_head_source = is_head
        self.is_in_common_trace_array = True
        self.probability_measure = 0 if is_head else min(self.identified_number_cta_trace_dict)

    # Удаление информации и номера трассы ЕМТ
    def delete_cta_info_and_number(self):
        self.cta_number = -1
        self.is_head_source = False
        self.is_in_common_trace_array = False
        self.probability_measure = 0.

    # Эктсраполяция координат на заданное время
    def extrapolate_coordinates_to_tick(self, tick: int):
        # Время между оценкой координат и временем, на которое нужно экстраполировать
        time = (tick - self.estimate_tick) * time_in_tick
        self.coordinates += self.velocities * time

    # Отождествление с трассой
    def identification_with_trace(self, trace):
        # Случай двух пеленгов
        if self.is_bearing and trace.is_bearing:
            self.identification_jammer_and_jammer(trace)
        # Случай чистых целей
        elif not self.is_bearing and not trace.is_bearing:
            self.identification_target_and_target(trace)
        # Случай одного пеленга
        else:
            self.identification_jammer_and_target(trace)

    # Отождествление чистых целей
    def identification_target_and_target(self, trace):
        # Отрезок между целями трасс
        range_between_traces = trace.coordinates - self.coordinates
        # Итоговая матрица ошибок
        summary_covariance_matrix = self.coordinate_covariance_matrix + trace.coordinate_covariance_matrix
        # Обобщённое растояние
        generalized_distance = self.calculate_generalized_distance(summary_covariance_matrix, range_between_traces)
        # Результат отождествления
        is_identified = (generalized_distance <= identification_threshold_3d)
        if is_identified:
            # Записываем обобщённое расстояние и номер трассы, с которой отждествляли в словарь
            self.identified_number_cta_trace_dict[generalized_distance] = trace.cta_number

    # Поиск ближайшей точки при двух АЦ
    def calculate_common_point_for_target_and_target(self, trace):
        # Расчёт оценки координат (мб скорости)
        common_coord_cov_matrix = self.coordinate_covariance_matrix + trace.coordinate_covariance_matrix
        # TODO: Исправить
        A = inv(common_coord_cov_matrix) * trace.coordinate_covariance_matrix
        B = inv(common_coord_cov_matrix) * self.coordinate_covariance_matrix
        common_point = A @ self.coordinates + B @ trace.coordinates

        return common_point

    # Отождествление двух постановщиков АШП
    def identification_jammer_and_jammer(self, trace):
        # Расчёт координат для каждой цели в случае двух АШП
        est_anj_coords_1, est_anj_cov_matrix_1 = self.calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(trace)
        est_anj_coords_2, est_anj_cov_matrix_2 = trace.calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self)
        # Итоговая ковариационная матрица
        summary_covariance_matrix = est_anj_cov_matrix_1 + est_anj_cov_matrix_2
        # Вектор от предполагаемого источника АШП от первого МФР до предполагаемого источника АШП из ЕМТ
        range_between_traces = est_anj_coords_2 - est_anj_coords_1
        # Обобщённое растояние
        generalized_distance = self.calculate_generalized_distance(summary_covariance_matrix, range_between_traces)
        # Результат отождествления
        is_identified = (generalized_distance <= identification_threshold_2d)
        if is_identified:
            # Записываем обобщённое расстояние и номер трассы, с которой отждествляли в словарь
            self.identified_number_cta_trace_dict[generalized_distance] = trace.cta_number

    # Расчёт координат и ковариационой матрицы АШП, для которого вызываем функцию, в случае двух АШП
    def calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self, trace):
        # Вспомогательные векторы
        mfr_anj_1 = self.coordinates - self.mfr_position
        mfr_anj_2 = trace.coordinates - trace.mfr_position
        base = trace.mfr_position - self.mfr_position

        crossed_vec = cross(mfr_anj_2, cross(mfr_anj_2, mfr_anj_1))
        # Коэффициент для поиска координат предполагаемого положения АШП на пеленге от первого МФР
        coefficient_for_anj_range = dot(base, crossed_vec) / dot(mfr_anj_1, crossed_vec)
        # Координаты предполагаемого положения постановщика АШП на пеленге от первого МФР
        estimated_anj_coords = coefficient_for_anj_range * mfr_anj_1 + self.mfr_position

        # Вспомогательный вектор
        mfr_est_1 = estimated_anj_coords - self.mfr_position
        # Коэффициент для поиска ковариационной матрицы координат предполагаемого положения АШП от первого МФР
        coefficient_for_anj_cov_matrix = dot(mfr_est_1, mfr_est_1) / dot(mfr_anj_1, mfr_anj_1)
        # Ковариационная матрица координат предполагаемого положения АШП от первого МФР
        estimated_anj_cov_matrix = coefficient_for_anj_cov_matrix * self.coordinate_covariance_matrix

        return estimated_anj_coords, estimated_anj_cov_matrix

    # Поиск ближайшей точки при двух пеленгах
    def calculate_common_point_for_jammer_and_jammer(self, trace):
        # Расчёт координат для каждой цели в случае двух АШП
        est_anj_coords_1, est_anj_cov_matrix_1 = self.calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(trace)
        est_anj_coords_2, est_anj_cov_matrix_2 = trace.calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self)
        # TODO: Итоговые формулы немного отличаются (из-за ковариаций между измерениями)
        # Расчёт оценки координат (мб скорости)
        common_coord_cov_matrix = est_anj_cov_matrix_1 + est_anj_cov_matrix_2
        # TODO: Исправить
        A = np.linalg.inv(common_coord_cov_matrix) * est_anj_cov_matrix_2
        B = np.linalg.inv(common_coord_cov_matrix) * est_anj_cov_matrix_1
        common_point = A @ est_anj_coords_1 + B @ est_anj_coords_2

        return common_point

    # Отождествление постановщика АШП и чистой цели
    def identification_jammer_and_target(self, trace):
        # Если трасса по постановщику АШП
        if self.is_bearing:
            # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
            est_anj_coords, est_anj_cov_matrix = self.calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(trace)
            # Итоговая ковариационная матрица
            summary_covariance_matrix = est_anj_cov_matrix + trace.coordinate_covariance_matrix
            # Вектор от цели до предполагаемого источника АШП
            range_between_traces = est_anj_coords - trace.coordinates
        else:
            est_anj_coords, est_anj_cov_matrix = trace.calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(self)
            # Итоговая ковариационная матрица
            summary_covariance_matrix = est_anj_cov_matrix + self.coordinate_covariance_matrix
            # Вектор от цели до предполагаемого источника АШП
            range_between_traces = est_anj_coords - self.coordinates
        # Обобщённое растояние
        generalized_distance = self.calculate_generalized_distance(summary_covariance_matrix, range_between_traces)
        is_identified = (generalized_distance <= identification_threshold_2d)
        if is_identified:
            # Записываем обобщённое расстояние и номер трассы, с которой отждествляли в словарь
            self.identified_number_cta_trace_dict[generalized_distance] = trace.cta_number

    # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
    def calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(self, trace):
        # Вспомогательные векторы
        mfr_anj = self.coordinates - self.mfr_position
        trg_anj = self.coordinates - trace.coordinates
        # Коэффициент для поиска координат предполагаемого положения постановщика АШП на пеленге
        coefficient_for_anj_range = - dot(mfr_anj, trg_anj) / dot(mfr_anj, mfr_anj)
        # Координаты предполагаемого положения постановщика АШП на пеленге
        est_anj_coordinates = coefficient_for_anj_range * mfr_anj + self.coordinates

        # Вспомогательный вектор
        mfr_est = est_anj_coordinates - self.mfr_position
        # Коэффициент для поиска ковариационной матрицы координат предполагаемого положения АШП на пеленге
        coefficient_for_anj_cov_matrix = dot(mfr_est, mfr_est) / dot(mfr_anj, mfr_anj)
        # Ковариационная матрица координат предполагаемого положения АШП
        estimated_anj_covariance_matrix = coefficient_for_anj_cov_matrix * self.coordinate_covariance_matrix

        return est_anj_coordinates, estimated_anj_covariance_matrix

    # Поиск ближайшей точки при одном пеленге
    def calculate_common_point_for_jammer_and_target(self, trace_target):
        # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
        est_anj_coords, est_anj_cov_matrix = self.calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(trace_target)
        # TODO: Итоговые формулы немного отличаются (из-за ковариаций между измерениями)
        # Расчёт оценки координат (мб скорости)
        common_coord_cov_matrix = est_anj_cov_matrix + trace_target.coordinate_covariance_matrix
        anj_matrix_coeff = inv(common_coord_cov_matrix) * trace_target.coordinate_covariance_matrix
        trg_matrix_coeff = inv(common_coord_cov_matrix) * est_anj_cov_matrix
        common_point = anj_matrix_coeff @ est_anj_coords + trg_matrix_coeff @ trace_target.coordinates
        return common_point

    # Поиск ближайшей точки при любой ситуации
    def calculate_common_point(self, trace):
        # TODO: Предлагаю оформить как с отождествлением для унификации
        # Случай чистых целей
        if not self.is_bearing and not trace.is_bearing:
            coords = self.calculate_common_point_for_target_and_target(trace)
        # Случай двух пеленгов
        elif self.is_bearing and trace.is_bearing:
            coords = self.calculate_common_point_for_jammer_and_jammer(trace)
        # Случай одного пеленга
        elif self.is_bearing and not trace.is_bearing:
            coords = self.calculate_common_point_for_jammer_and_target(trace)
        else:
            coords = trace.calculate_common_point_for_jammer_and_target(self)
        return coords

    # Расчёт обобщённого расстояния
    @staticmethod
    def calculate_generalized_distance(covariance_matrix: np.ndarray, range_between_traces: np.ndarray):
        return range_between_traces @ inv(covariance_matrix) @ range_between_traces.transpose()

    # Расчёт ковариационной матрицы между координатами точек АШП(self) и АЦ
    def calc_anj_trg_cov_matrix(self, trace_target):
        """
        trg_.. или anj_.. показывают к чему относится
        .._trg или .._anj показыкает по координатам чего производная
        """
        # Вспомогательные векторы
        mfr_anj = self.coordinates - self.mfr_position
        # Производная коэфициента по координатам трассы АЦ
        coeff_trg = mfr_anj / dot(mfr_anj, mfr_anj)

        # Координаты АЦ
        x = trace_target.coordinates[0]
        y = trace_target.coordinates[1]
        z = trace_target.coordinates[2]
        # Производная beta АЦ по координатам трассы АЦ
        trg_beta_trg = np.array([-x / (x ** 2 + z ** 2), 0, (x ** 2 + 2 * z ** 2) / (x * (x ** 2 + z ** 2))])
        # Производная eps по координатам трассы АШП
        q = x ** 2 + y ** 2 + z ** 2
        # TODO: math.hypot
        trg_eps_trg = np.array([-x * y / (sqrt(x ** 2 + z ** 2) * q), sqrt(x ** 2 + z ** 2) / q ** 1.5,
                                -z * y / (sqrt(x ** 2 + z ** 2) * q)])
        # Производная R до АЦ по координатам АЦ
        r = sqrt(q)
        trg_dist_trg = np.array([x / r, y / r, z / r])
        # Ковариация расстояния до АШП и расстояния до АЦ
        # TODO: np.dot в помощь
        d = sqrt(mfr_anj[0] ** 2 + mfr_anj[1] ** 2 + mfr_anj[2] ** 2)
        cov_dist_anj_dist_trg = d * coeff_trg @ trace_target.coordinate_covariance_matrix @ trg_dist_trg
        # Ковариация расстояния до АШП и азимута АЦ
        cov_dist_anj_beta_trg = d * coeff_trg @ trace_target.coordinate_covariance_matrix @ trg_beta_trg
        # Ковариация расстояния до АШП и угла места АЦ
        cov_dist_anj_eps_trg = d * coeff_trg @ trace_target.coordinate_covariance_matrix @ trg_eps_trg
        # Ковариационная матрица между координатами АШП и АЦ
        # TODO: Можно ведь красивее перенести, np.zeros(3) для нулевых векторов
        anj_trg_cov_matrix = np.array(
            [[cov_dist_anj_dist_trg, cov_dist_anj_beta_trg, cov_dist_anj_eps_trg], [0, 0, 0], [0, 0, 0]])
        return anj_trg_cov_matrix

    # Расчёт итоговой ковариационной матрицы АШП(self) в декартовых координатах
    def calc_anj_cov_matrix(self, trace_target):
        # Матрица ошибок метода в сферических координатах
        method_cov_matrix_sph = self.calculate_method_cov_matrix_for_jammer(trace_target)
        # Матрица ошибок измерений в сферических координатах
        measure_cov_matrix_sph = calc_scs_from_dec(self.coordinate_covariance_matrix, self.coordinates)
        # TODO: Можно в несколько присваиваний и объединить их в группы, можно вынести в отдельную функцию
        measure_cov_matrix_sph[0][0] = 0.
        measure_cov_matrix_sph[1][0] = 0.
        measure_cov_matrix_sph[2][0] = 0.
        measure_cov_matrix_sph[0][1] = 0.
        measure_cov_matrix_sph[0][2] = 0.
        # Итоговая матрица ошибок в сферических координатах
        cov_matrix_sph = measure_cov_matrix_sph + method_cov_matrix_sph
        # Координаты АШП в сферических координатах
        coords_sph = dec2sph(self.coordinates)
        # Итоговая матрица в декартовых координатах
        cov_matrix_dec = calc_dec_from_scs(cov_matrix_sph, coords_sph)
        return cov_matrix_dec

    # Расчёт матрицы ошибок метода в сферических координатах
    def calculate_method_cov_matrix_for_jammer(self, trace_target):
        # Обозначаем для удобства
        anj_cov_matrix = self.coordinate_covariance_matrix
        trg_cov_matrix = trace_target.coordinate_covariance_matrix
        anj_coords = self.coordinates
        # Вспомогательные векторы
        mfr_anj = self.coordinates - self.mfr_position
        trg_anj = self.coordinates - trace_target.coordinates
        # Производная коэфициента по координатам трассы АЦ
        coeff_trg = mfr_anj / dot(mfr_anj, mfr_anj)
        # Производная коэфициента по координатам трассы АШП
        # TODO: В отдельные переменные, что считается несколько раз
        coeff_anj = -((trg_anj + mfr_anj) * dot(mfr_anj, mfr_anj) - 2 * mfr_anj * dot(mfr_anj, trg_anj)) / (
            dot(mfr_anj, mfr_anj)) ** 2
        # Дисперсия расстояния от МФР до предпологаемого положения АШП
        d = mfr_anj[0] ** 2 + mfr_anj[1] ** 2 + mfr_anj[2] ** 2
        var_dist_mfr_est_anj = d * (coeff_anj @ anj_cov_matrix @ coeff_anj.transpose() +
                                    coeff_trg @ trg_cov_matrix @ coeff_trg.transpose())
        # Производная beta по координатам трассы АШП
        x = anj_coords[0]
        y = anj_coords[1]
        z = anj_coords[2]

        hypot_xz = hypot(x, z)
        beta_anj = np.array([-z / hypot_xz**2, 0., x / hypot_xz**2])
        # Производная eps по координатам трассы АШП
        eps_anj = np.array([-x*y / (hypot_xz * d), hypot_xz / d, -y*z / (hypot_xz * d)])
        # Ковариация расстояния от МФР до предпологаемого положения АШП и азимута
        cov_dist_beta = sqrt(d) * coeff_anj @ anj_cov_matrix @ beta_anj
        # Ковариация расстояния от МФР до предпологаемого положения АШП и угла места
        cov_dist_eps = sqrt(d) * coeff_anj @ anj_cov_matrix @ eps_anj
        # TODO: Если переносить, то каждую компоненту на отдельную строчку
        # Ковариационная матрица ошибок метода
        method_cov_matrix = np.array([[var_dist_mfr_est_anj, cov_dist_beta, cov_dist_eps],
                                      [cov_dist_beta, 0, 0],
                                      [cov_dist_eps, 0, 0]])
        return method_cov_matrix
