import numpy as np
from numpy import cross, dot, ndarray
from numpy.linalg import inv
from model_time import time_in_tick

# Порог отождествления для случая с двумя степенями свободы
identification_threshold_2d = 9.21
# Порог отождествления для случая с тремя степенями свободы
identification_threshold_3d = 11.345


# Класс, описывающий данные по трассе источника, которыми пользуется ПБУ
class SourceTrace:
    def __init__(self, mfr_number: int, mfr_position: ndarray):
        # Номер МФР
        self.mfr_number = mfr_number
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
        A = inv(common_coord_cov_matrix) * trace.coordinate_covariance_matrix
        B = inv(common_coord_cov_matrix) * self.coordinate_covariance_matrix
        common_point = A @ self.coordinates + B @ trace.coordinates

        return common_point

    # Отождествление двух постановщиков АШП
    def identification_jammer_and_jammer(self, trace):
        # Расчёт координат для каждой цели в случае двух АШП
        est_anj_coords_1, est_anj_cov_matrix_1 = self.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(trace)
        est_anj_coords_2, est_anj_cov_matrix_2 = trace.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self)
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
    def calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self, trace):
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
        est_anj_coords_1, est_anj_cov_matrix_1 = self.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(
            trace)
        est_anj_coords_2, est_anj_cov_matrix_2 = trace.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(
            self)
        # TODO: Итоговые формулы немного отличаются (из-за ковариаций между измерениями)
        # Расчёт оценки координат (мб скорости)
        common_coord_cov_matrix = est_anj_cov_matrix_1 + est_anj_cov_matrix_2
        A = np.linalg.inv(common_coord_cov_matrix) * est_anj_cov_matrix_2
        B = np.linalg.inv(common_coord_cov_matrix) * est_anj_cov_matrix_1
        common_point = A @ est_anj_coords_1 + B @ est_anj_coords_2

        return common_point

    # Отождествление постановщика АШП и чистой цели
    def identification_jammer_and_target(self, trace):
        # Если трасса по постановщику АШП
        if self.is_bearing:
            # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
            est_anj_coords, est_anj_cov_matrix = self.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(trace)
            # Итоговая ковариационная матрица
            summary_covariance_matrix = est_anj_cov_matrix + trace.coordinate_covariance_matrix
            # Вектор от цели до предполагаемого источника АШП
            range_between_traces = est_anj_coords - trace.coordinates
        else:
            est_anj_coords, est_anj_cov_matrix = trace.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(self)
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
    def calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(self, trace):
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
        est_anj_coords, est_anj_cov_matrix = self.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(
            trace_target)
        # TODO: Итоговые формулы немного отличаются (из-за ковариаций между измерениями)
        # Расчёт оценки координат (мб скорости)
        common_coord_cov_matrix = est_anj_cov_matrix + trace_target.coordinate_covariance_matrix
        A = np.linalg.inv(common_coord_cov_matrix) * trace_target.coordinate_covariance_matrix
        B = np.linalg.inv(common_coord_cov_matrix) * est_anj_cov_matrix
        common_point = A @ est_anj_coords + B @ trace_target.coordinates

        return common_point

    # Поиск ближайшей точки при любой ситуации
    def calculate_common_point(self, trace):
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
