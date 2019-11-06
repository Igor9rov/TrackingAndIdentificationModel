import numpy as np
from numpy import cross, dot, ndarray
from numpy.linalg import inv

from calc_covariance_matrix import elements_of_covariance_matrix
from model_time import time_in_tick


class SourceTrace:
    """Класс, описывающий данные по трассе источника, поддерживает отождествление"""
    # Порог отождествления для случая с двумя степенями свободы
    identification_threshold_2d = 9.21
    # Порог отождествления для случая с тремя степенями свободы
    identification_threshold_3d = 11.345
    __slots__ = ('mfr_number',
                 'target_number',
                 'mfr_position',
                 'coordinates',
                 'velocities',
                 'coordinate_covariance_matrix',
                 'is_bearing',
                 'is_auto_tracking',
                 'estimate_tick',
                 'is_in_common_trace_array',
                 'is_head_source',
                 'probability_measure',
                 'cta_number',
                 'identified_number_cta_trace_dict')

    def __init__(self, mfr_number: int = 0, mfr_position: ndarray = np.zeros(3), target_number: int = 0):
        """Конструктор трассы источника
        :param mfr_number: Номер МФР
        :param mfr_position: Точка стояния МФР
        :param target_number: Номер цели
        """
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

    @property
    def registration(self):
        """Регистрируем номер цели, координаты, скорость, элементы ковариационнной матрицы, признак АШП, номер трассы ЕМТ,
        обобщённое расстояние между головным источником по той же трассе ЕМТ

        :return: Региструриуемые величины в виде одномерного массива
        """
        return [self.target_number, *self.coordinates.tolist(), *self.velocities.tolist(),
                *elements_of_covariance_matrix(self.coordinate_covariance_matrix), self.is_bearing,
                self.cta_number, self.probability_measure]

    @property
    def identified_cta_trace_numbers(self):
        """
        :return: Номера трасс с которыми отождествилась трасса
        """
        return list(self.identified_number_cta_trace_dict.values())

    def clear_identified_number_cta_trace_dict(self):
        """Очищение словаря трасс, с которыми отождествилась трасса

        :return: None
        """
        self.identified_number_cta_trace_dict = {}

    @property
    def num_cta_trace_with_min_distance(self):
        """
        :return: Номер трассы ЕМТ с минимальным обобщённым расстоянием
        """
        min_generalized_distance = min(self.identified_number_cta_trace_dict)
        return self.identified_number_cta_trace_dict.get(min_generalized_distance)

    def append_cta_info_and_number(self, num: int, is_head: bool):
        """Добавление информации и номера трассы ЕМТ

        :param num: Номер трассы ЕМТ
        :param is_head: Признак головного источника

        :return: None
        """
        self.cta_number = num
        self.is_head_source = is_head
        self.is_in_common_trace_array = True
        self.probability_measure = 0 if is_head else min(self.identified_number_cta_trace_dict)

    def delete_cta_info_and_number(self):
        """Удаление информации и номера трассы ЕМТ

        :return: None
        """
        self.cta_number = -1
        self.is_head_source = False
        self.is_in_common_trace_array = False
        self.probability_measure = 0.

    def extrapolate_coordinates_to_tick(self, tick: int):
        """Эктсраполяция координат на заданное время

        :param tick: Время в тиках, на которое производится эктраполяция

        :return: None
        """
        # Время между оценкой координат и временем, на которое нужно экстраполировать
        time = (tick - self.estimate_tick) * time_in_tick
        self.coordinates += self.velocities * time

    def identification_with_trace(self, trace):
        """Отождествление с трассой

        :param trace: Другая трасса источника того же типа SourceTrace

        :return: None
        """
        trace: SourceTrace
        # Случай двух пеленгов
        if self.is_bearing and trace.is_bearing:
            self.identification_jammer_and_jammer(trace)
        # Случай чистых целей
        elif not self.is_bearing and not trace.is_bearing:
            self.identification_target_and_target(trace)
        # Случай одного пеленга
        else:
            self.identification_jammer_and_target(trace)

    def identification_target_and_target(self, trace):
        """Отождествление трасс чистых целей

        :param trace: Другая трасса источника того же типа SourceTrace

        :return: None
        """
        trace: SourceTrace
        # Отрезок между целями трасс
        range_between_traces = trace.coordinates - self.coordinates
        # Итоговая матрица ошибок
        summary_covariance_matrix = self.coordinate_covariance_matrix + trace.coordinate_covariance_matrix
        # Обобщённое растояние
        generalized_distance = self.calculate_generalized_distance(summary_covariance_matrix, range_between_traces)
        # Результат отождествления
        is_identified = (generalized_distance <= SourceTrace.identification_threshold_3d)
        if is_identified:
            self.identified_number_cta_trace_dict[generalized_distance] = trace.cta_number

    def identification_jammer_and_jammer(self, trace):
        """Отождествление трасс двух постановщиков АШП

        :param trace: Другая трасса источника того же типа SourceTrace

        :return: None
        """
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
        is_identified = (generalized_distance <= SourceTrace.identification_threshold_2d)
        if is_identified:
            self.identified_number_cta_trace_dict[generalized_distance] = trace.cta_number

    def calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self, trace):
        """Расчёт координат и ковариационой матрицы АШП, для которого вызываем функцию, в случае двух АШП

        :param trace: Другая трасса источника того же типа SourceTrace

        :return: None
        """
        trace: SourceTrace
        # Вспомогательные векторы
        mfr_anj_1 = self.coordinates - self.mfr_position
        mfr_anj_2 = trace.coordinates - trace.mfr_position
        base = trace.mfr_position - self.mfr_position

        crossed_vec = cross(mfr_anj_2, cross(mfr_anj_2, mfr_anj_1))

        # Коэффициент для координат предполагаемого положения АШП на пеленге от первого МФР
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

    def identification_jammer_and_target(self, trace):
        """Отождествление постановщика АШП и чистой цели

        :param trace: Другая трасса источника того же типа SourceTrace

        :return: None
        """
        trace: SourceTrace
        # Если трасса по постановщику АШП
        if self.is_bearing:
            # Расчёт координат и ковариационой матрицы АШП
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
        is_identified = (generalized_distance <= SourceTrace.identification_threshold_2d)
        if is_identified:
            self.identified_number_cta_trace_dict[generalized_distance] = trace.cta_number

    def calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(self, trace):
        """Расчёт координат и ковариационой матрицы АШП в случае АШП и чистой цели

        :param trace: Другая трасса источника того же типа SourceTrace

        :return: None
        """
        trace: SourceTrace
        # Вспомогательные векторы
        mfr_anj = self.coordinates - self.mfr_position
        trg_anj = self.coordinates - trace.coordinates
        # Коэффициент для координат положения постановщика АШП
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

    @staticmethod
    def calculate_generalized_distance(covariance_matrix: np.ndarray, range_between_traces: np.ndarray):
        """Расчёт обобщённого расстояния

        :param covariance_matrix: Суммарная ковариационная матрица
        :param range_between_traces: Вектор разности между координатами трасс

        :return: Обобщённое расстояние
        """
        return range_between_traces @ inv(covariance_matrix) @ range_between_traces.transpose()
