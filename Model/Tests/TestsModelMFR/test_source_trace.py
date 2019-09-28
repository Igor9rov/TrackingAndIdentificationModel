from unittest import TestCase

import math
import numpy as np
from numpy import sqrt
from numpy.linalg import inv

from source_trace import SourceTrace


# Тест для класса SourceTrace
class TestSourceTrace(TestCase):
    def setUp(self) -> None:
        mfr_pos = np.array([1100, 0, 0])
        self.source_trace = SourceTrace(mfr_number=1, mfr_position=mfr_pos)

    def test_get_identified_cta_trace_numbers(self):
        # Номера трасс ЕМТ
        cta_numbers = [5, 2]
        # Обобщённые расстояния
        generalized_distances = [1.25, 8.65]
        # Создаём словарь
        self.source_trace.identified_number_cta_trace_dict = dict(zip(generalized_distances, cta_numbers))
        # Получаем номера трасс ЕМТ
        res_cta_numbers = self.source_trace.get_identified_cta_trace_numbers()
        self.assertEqual(cta_numbers, res_cta_numbers)

    def test_clear_identified_number_cta_trace_dict(self):
        # Пустой словарь
        null_dict = {}
        # Должен быть нулевым словарём псоле вызова функции
        res_dict = self.source_trace.identified_number_cta_trace_dict
        # Вызов функции
        self.source_trace.clear_identified_number_cta_trace_dict()
        # Проверка
        self.assertDictEqual(null_dict, res_dict)

    def test_get_num_cta_trace_with_min_distance(self):
        # Номера трасс ЕМТ
        cta_numbers = [5, 2]
        # Обобщённые расстояния
        generalized_distances = [1.25, 8.65]
        # Создаём словарь
        self.source_trace.identified_number_cta_trace_dict = dict(zip(generalized_distances, cta_numbers))
        # Номер трассы ЕМТ с минимальным расстоянием
        num_cta_trace_with_min_distance = 10
        # Минимальное расстояние
        min_distance = min(generalized_distances) - 1.
        # Добавим в него трассу ЕМТ с номером 10 и расстоянием, меньшим, чем остальные
        self.source_trace.identified_number_cta_trace_dict[min_distance] = num_cta_trace_with_min_distance
        # Получение номера трассы ЕМТ с минимальным расстоянием
        res_num_cta_trace_with_min_distance = self.source_trace.get_num_cta_trace_with_min_distance()
        # Проверка
        self.assertEqual(num_cta_trace_with_min_distance, res_num_cta_trace_with_min_distance)

    def test_append_cta_info_and_number(self):
        # Номер трассы ЕМТ с минимальным расстоянием
        num_cta_trace_with_min_distance = 10
        # Минимальное расстояние
        min_distance = 1.23
        # Признак головного источника
        is_head = True
        # Добавим в него трассу ЕМТ с номером 10 и расстоянием, меньшим, чем остальные
        self.source_trace.identified_number_cta_trace_dict[min_distance] = num_cta_trace_with_min_distance
        # Проверка для головного источника
        self.source_trace.append_cta_info_and_number(num=num_cta_trace_with_min_distance, is_head=is_head)

        self.assertEqual(num_cta_trace_with_min_distance, self.source_trace.cta_number)
        self.assertTrue(self.source_trace.is_head_source)
        self.assertTrue(self.source_trace.is_in_common_trace_array)
        self.assertEqual(0, self.source_trace.probability_measure)
        # Проверка для дополнительного источника
        is_head = False
        self.source_trace.append_cta_info_and_number(num=num_cta_trace_with_min_distance, is_head=is_head)

        self.assertEqual(num_cta_trace_with_min_distance, self.source_trace.cta_number)
        self.assertFalse(self.source_trace.is_head_source)
        self.assertTrue(self.source_trace.is_in_common_trace_array)
        self.assertEqual(min_distance, self.source_trace.probability_measure)

    def test_delete_cta_info_and_number(self):
        # Вызов функции
        self.source_trace.delete_cta_info_and_number()
        # Проверка
        self.assertEqual(-1, self.source_trace.cta_number)
        self.assertFalse(self.source_trace.is_head_source)
        self.assertFalse(self.source_trace.is_in_common_trace_array)
        self.assertEqual(0, self.source_trace.probability_measure)

    def test_extrapolate_coordinates_to_tick(self):
        self.source_trace.estimate_tick = 20
        self.source_trace.coordinates = np.array([20., 40., 12.])
        self.source_trace.velocities = np.array([2., -8., 9.])
        extrapolate_tick = 30
        coordinates = np.array([21., 36., 16.5])

        self.source_trace.extrapolate_coordinates_to_tick(extrapolate_tick)
        self.assertEqual(coordinates.tolist(), self.source_trace.coordinates.tolist())

    def test_calculate_generalized_distance(self):
        covariance_matrix = np.diag([25, 1, 0.01])
        range_between_traces = np.array([9, 3, 1])

        generalized_distance = range_between_traces @ inv(covariance_matrix) @ range_between_traces.transpose()
        res_generalized_distance = SourceTrace.calculate_generalized_distance(covariance_matrix,
                                                                              range_between_traces)
        self.assertEqual(generalized_distance, res_generalized_distance)

    def test_calculate_common_point_for_target_and_target(self):
        self.source_trace.coordinates = np.array([1., 0., 0.])
        self.source_trace.coordinate_covariance_matrix = np.diag([2., 1., 2.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        trace.coordinates = np.array([0., 0, 3.])
        trace.coordinate_covariance_matrix = np.diag([1., 2., 1])
        common_point = self.source_trace.calculate_common_point_for_target_and_target(trace)
        res_common_point = np.array([0.3333333333333333, 0, 2.])
        self.assertEqual(common_point.tolist(), res_common_point.tolist())

    def test_identification_jammer_and_target(self):
        self.source_trace.coordinates = np.array([0., 0., 1100.])
        self.source_trace.is_bearing = False
        self.source_trace.coordinate_covariance_matrix = np.diag([22443., 258., 3344.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        trace.cta_number = 4
        trace.coordinates = np.array([0., 0, 550.])
        trace.is_bearing = True
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        self.source_trace.identification_jammer_and_target(trace)
        # Трассы должны были отождествиться (это одна точка и обобщённое расстояние равно нулю)
        identified_dict = {0.: trace.cta_number}
        self.assertDictEqual(identified_dict, self.source_trace.identified_number_cta_trace_dict)

    def test_identification_target_and_target(self):
        self.source_trace.coordinates = np.array([0., 0., 1100.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22443., 258., 3344.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        trace.cta_number = 4
        trace.coordinates = np.array([0., 0, 1100.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        self.source_trace.identification_target_and_target(trace)
        # Трассы должны были отождествиться (это одна точка и обобщённое расстояние равно нулю)
        identified_dict = {0.: trace.cta_number}
        self.assertDictEqual(identified_dict, self.source_trace.identified_number_cta_trace_dict)

    def test_identification_jammer_and_jammer(self):
        self.source_trace.coordinates = np.array([550., 0., 5500.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22443., 258., 3344.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.array([-1100., 0., 0.]))
        trace.cta_number = 4
        trace.coordinates = np.array([-550., 0, 550.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        self.source_trace.identification_jammer_and_jammer(trace)
        # Трассы должны были отождествиться (это одна точка и обобщённое расстояние равно нулю)
        identified_dict = {0.: trace.cta_number}
        self.assertDictEqual(identified_dict, self.source_trace.identified_number_cta_trace_dict)

    def test_calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self):
        self.source_trace.coordinates = np.array([1., 0., 0.])
        self.source_trace.mfr_position = np.ones(3)
        self.source_trace.coordinate_covariance_matrix = np.diag([1., 1., 0.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        trace.coordinates = np.array([0., 0, 1.])
        trace.coordinate_covariance_matrix = np.diag([1., 0., 1])

        res_estimated_anj_coords = np.array([1, 0, 0])
        res_estimated_anj_cov_matrix = np.diag([1., 1., 0.])

        estimated_anj_coords, estimated_anj_cov_matrix = self.source_trace.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(trace)

        self.assertEqual(estimated_anj_coords.tolist(), res_estimated_anj_coords.tolist())
        self.assertEqual(estimated_anj_cov_matrix.tolist(), res_estimated_anj_cov_matrix.tolist())

    def test_calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(self):
        self.source_trace.coordinates = np.array([1., 0., 0.])
        self.source_trace.mfr_position = np.ones(3)
        self.source_trace.coordinate_covariance_matrix = np.diag([1., 1., 0.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        trace.coordinates = np.array([0., 0, 1.])
        trace.coordinate_covariance_matrix = np.diag([1., 0., 1])


        res_est_anj_coords = np.array([1., 0.5, 0.5])
        res_est_anj_cov_matrix = np.array([[0.25, 0.0, 0.0], [0.0, 0.25, 0.0], [0.0, 0.0, 0.0]])

        est_anj_coords, est_anj_cov_matrix = self.source_trace.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(trace)

        self.assertEqual(est_anj_coords.tolist(), res_est_anj_coords.tolist())
        self.assertEqual(est_anj_cov_matrix.tolist(), res_est_anj_cov_matrix.tolist())

    def test_identification_with_trace(self):
        # Отождествление двух постановщиков АШП
        self.source_trace.is_bearing = True
        self.source_trace.coordinates = np.array([550., 0., 5500.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22443., 258., 3344.])
        trace = SourceTrace(mfr_number=2, mfr_position=np.array([-1100., 0., 0.]))
        trace.is_bearing = True
        trace.cta_number = 4
        trace.coordinates = np.array([-550., 0, 550.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        self.source_trace.identification_with_trace(trace)
        # Трассы должны были отождествиться (это одна точка и обобщённое расстояние равно нулю)
        identified_dict = {0.: trace.cta_number}
        self.assertDictEqual(identified_dict, self.source_trace.identified_number_cta_trace_dict)
        self.source_trace.clear_identified_number_cta_trace_dict()

        # Отождествление постановщика АШП и чистой цели
        self.source_trace.coordinates = np.array([0., 0., 1100.])
        self.source_trace.is_bearing = False
        trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        trace.cta_number = 4
        trace.coordinates = np.array([0., 0, 550.])
        trace.is_bearing = True
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        self.source_trace.identification_jammer_and_target(trace)
        # Трассы должны были отождествиться (это одна точка и обобщённое расстояние равно нулю)
        self.assertDictEqual(identified_dict, self.source_trace.identified_number_cta_trace_dict)
        self.source_trace.clear_identified_number_cta_trace_dict()

        # Отождествление чистых целей
        self.source_trace.is_bearing = False
        trace.is_bearing = False
        trace.coordinates = np.array([0., 0, 1100.])

        self.source_trace.identification_target_and_target(trace)
        # Трассы должны были отождествиться (это одна точка и обобщённое расстояние равно нулю)
        self.assertDictEqual(identified_dict, self.source_trace.identified_number_cta_trace_dict)

    def test_calc_anj_trg_cov_matrix(self):
        # Заполняем данные
        anj_mfr_pos = np.array([-1., 0., 0.])
        anj_coords = np.array([0., 2., 1.])
        trg_mfr_pos = np.array([2., 0., 0.])
        trg_coords = np.array([1., 2., 2.])
        anj_cov_matrix = np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 1.]])
        trg_cov_matrix = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
        self.source_trace.coordinates = anj_coords
        self.source_trace.is_bearing = True
        self.source_trace.mfr_position = anj_mfr_pos
        self.source_trace.coordinate_covariance_matrix = anj_cov_matrix
        trace = SourceTrace(mfr_number=2, mfr_position=trg_mfr_pos)
        trace.coordinates = trg_coords
        trace.is_bearing = False
        trace.coordinate_covariance_matrix = trg_cov_matrix
        # Посчитанное значение ковариационной матрицы ручками
        res_method_cov_matrix = np.array([[20*sqrt(6)/18, 32*sqrt(6)/30, -52*sqrt(6/5)/162],[0., 0., 0.], [0., 0., 0.]])
        # Посчитанное значение ковариационной матрицы функцией
        method_cov_matrix = self.source_trace.calc_anj_trg_cov_matrix(trace)
        self.assertEqual(method_cov_matrix.round(7).tolist(), res_method_cov_matrix.round(7).tolist())

    def test_calc_anj_cov_matrix(self):
        # Заполняем данные
        anj_mfr_pos = np.array([-1., 0., 0.])
        anj_coords = np.array([-0.5, 2., 1.])
        trg_mfr_pos = np.array([2., 0., 0.])
        trg_coords = np.array([1., 2., 2.])
        anj_cov_matrix = np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 1.]])
        trg_cov_matrix = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
        self.source_trace.coordinates = anj_coords
        self.source_trace.is_bearing = True
        self.source_trace.mfr_position = anj_mfr_pos
        self.source_trace.coordinate_covariance_matrix = anj_cov_matrix
        trace = SourceTrace(mfr_number=2, mfr_position=trg_mfr_pos)
        trace.coordinates = trg_coords
        trace.is_bearing = False
        trace.coordinate_covariance_matrix = trg_cov_matrix
        # Посчитанное значение ковариационной матрицы ручками
        res_cov_matrix_dec = np.array(
            [[2.83023104, -6.27847245, -2.23189066], [-6.27847245, 5.94408288, -0.15734082],
             [-2.23189066, -0.15734082, -1.39336154]])
        # Посчитанное значение ковариационной матрицы функцией
        cov_matrix_dec = self.source_trace.calc_anj_cov_matrix(trace)
        self.assertEqual(cov_matrix_dec.round(7).tolist(), res_cov_matrix_dec.round(7).tolist())

    def test_calculate_method_cov_matrix_for_jammer(self):
        # Заполняем данные
        anj_mfr_pos = np.array([-1., 0., 0.])
        anj_coords = np.array([0., 2., 1.])
        trg_mfr_pos = np.array([2., 0., 0.])
        trg_coords = np.array([1., 2., 2.])
        anj_cov_matrix = np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 1.]])
        trg_cov_matrix = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
        self.source_trace.coordinates = anj_coords
        self.source_trace.is_bearing = True
        self.source_trace.mfr_position = anj_mfr_pos
        self.source_trace.coordinate_covariance_matrix = anj_cov_matrix
        trace = SourceTrace(mfr_number=2, mfr_position=trg_mfr_pos)
        trace.coordinates = trg_coords
        trace.is_bearing = False
        trace.coordinate_covariance_matrix = trg_cov_matrix
        # Посчитанное значение ковариационной матрицы ручками
        res_method_cov_matrix = np.array(
            [[16/3, -math.inf, sqrt(6)/45 * (12-6/sqrt(5))], [-math.inf, 0., 0.], [sqrt(6)/45 * (12-6/sqrt(5)), 0., 0.]])
        # Посчитанное значение ковариационной матрицы функцией
        method_cov_matrix = self.source_trace.calculate_method_cov_matrix_for_jammer(trace)
        self.assertEqual(method_cov_matrix.round(7).tolist(), res_method_cov_matrix.round(7).tolist())