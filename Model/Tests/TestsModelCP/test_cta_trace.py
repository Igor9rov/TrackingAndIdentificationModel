from unittest import TestCase

import numpy as np

from cta_trace import CTATrace
from source_trace import SourceTrace
from numpy import random
from math import sqrt

from calc_covariance_matrix import calc_scs_from_dec


# TODO: Комменты
# Тест для класса трассы ЕМТ
class TestCTATrace(TestCase):
    def setUp(self) -> None:
        self.head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        self.cta_trace = CTATrace(self.head_source_trace)

    def test_get_all_sources_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        all_source_traces = self.cta_trace.all_source_traces

        self.assertTrue(self.cta_trace.head_source_trace in all_source_traces)
        self.assertTrue(add_source_trace in all_source_traces)
        self.assertEqual(2, len(all_source_traces))

    def test_must_identify_with_source_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        # Не должны отождествлять (номера мфр)
        another_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        must_identify = self.cta_trace.must_identify_with_source_trace(another_source_trace)
        self.assertFalse(must_identify)

        # Должны отождествлять
        another_source_trace = SourceTrace(mfr_number=3, mfr_position=np.zeros(3))
        must_identify = self.cta_trace.must_identify_with_source_trace(another_source_trace)
        self.assertTrue(must_identify)

    def test_must_identify_with_cta_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        identifying_head_source_trace = SourceTrace(mfr_number=4, mfr_position=np.zeros(3))
        identifying_cta_trace = CTATrace(identifying_head_source_trace)
        identifying_add_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        identifying_cta_trace.additional_source_trace_array.append(identifying_add_source_trace)

        # Не должны отождествлять (номера мфр)
        must_identify = self.cta_trace.must_identify_with_cta_trace(identifying_cta_trace)
        self.assertFalse(must_identify)

        identifying_head_source_trace = SourceTrace(mfr_number=4, mfr_position=np.zeros(3))
        identifying_cta_trace = CTATrace(identifying_head_source_trace)
        identifying_add_source_trace = SourceTrace(mfr_number=3, mfr_position=np.zeros(3))
        identifying_cta_trace.additional_source_trace_array.append(identifying_add_source_trace)

        # Должны отождествлять
        must_identify = self.cta_trace.must_identify_with_cta_trace(identifying_cta_trace)
        self.assertTrue(must_identify)

    def test_add_new_source_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        add_source_trace.identified_number_cta_trace_dict = {0.: self.cta_trace.number}

        self.cta_trace.add_new_source_trace(add_source_trace)

        self.assertEqual(1, len(self.cta_trace.additional_source_trace_array))
        self.assertTrue(add_source_trace in self.cta_trace.additional_source_trace_array)

    def test_del_additional_source_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        self.cta_trace.del_additional_source_trace(add_source_trace)

        self.assertEqual(0, len(self.cta_trace.additional_source_trace_array))
        self.assertFalse(add_source_trace in self.cta_trace.additional_source_trace_array)

    def test_sort_sources(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        add_source_trace.is_auto_tracking = True
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        # Дполнительный и головной иоточник должны поменяться местами (у доп. АС - он точнее)
        self.cta_trace.sort_sources()

        self.assertTrue(add_source_trace is self.cta_trace.head_source_trace)
        self.assertTrue(self.head_source_trace in self.cta_trace.additional_source_trace_array)

    def test_delete_sources_traces(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        self.cta_trace.delete_sources_traces()

        self.assertEqual([], self.cta_trace.additional_source_trace_array)
        self.assertIsNone(self.cta_trace.head_source_trace)

    def test_change_numbers(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)
        changed_num = 89

        self.cta_trace.change_numbers(changed_num)

        self.assertEqual(changed_num, self.cta_trace.number)
        self.assertEqual(changed_num, self.head_source_trace.cta_number)
        self.assertEqual(changed_num, add_source_trace.cta_number)

    # TODO: Добавление реализации теста для calculate_self_data
    def test_calculate_self_data(self):
        pass

    def test_calculate_coefficient_matrix(self):
        # Введем данные
        anj_cov_matrix = np.array([[0., 1., 0.], [1., 0., 1.], [1., 1., 0.]])
        trg_cov_matrix = np.array([[1., 0., 1.], [0., 1., 0.], [1., 1., 1.]])
        anj_trg_cov_matrix = np.array([[1., 1., 1.], [0., 0., 0.], [0., 0., 0.]])
        # Матрицы, посчитанная руками
        res_A = np.array([[0., 0.5, -0.5], [1., -0.5, 1.5], [-1.5, 1.5, -1.5]])
        res_B = np.array([[1., -0.5, 0.5], [-1., 1.5, -1.5], [1.5, -1.5, 2.5]])
        # Матрицы, посчитанная функцией
        A, B = self.cta_trace.calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, anj_trg_cov_matrix)
        self.assertEqual(A.tolist(), res_A.tolist())
        self.assertEqual(B.tolist(), res_B.tolist())

    def test_cov_matrix(self):
        # TODO:
        #  Сравнение должно быть распределений оценки ближайшей точки на пеленге и ковариационной матрицы этой точки,
        #  получаемой по твоей формуле (так себя легче проверить)
        #  Ковариация многомерного массива: для корректной работы нужен shape(num_of_coordinates, num_of_iteraction)
        # Обозначения для удобства
        anj_cov_matrix = np.eye(3)
        trg_cov_matrix = np.eye(3) / 100
        # Заполняем данные
        trace_jammer = SourceTrace(mfr_number=1, mfr_position=np.array([0., 0., 0.]))
        trace_jammer.coordinate_covariance_matrix = anj_cov_matrix
        trace_jammer.is_bearing = True
        trace_target = SourceTrace(mfr_number=2, mfr_position=np.array([100., 0., 0.]))
        trace_target.coordinate_covariance_matrix = trg_cov_matrix
        # Количество итераций
        n = 10000
        # Вспомогательные массивы
        arr_cov_matrix = np.zeros((n, 3, 3))
        arr_common_coords = np.zeros((3, n))
        for i in range(n):
            # Задаем данные
            anj_coors = np.array([0, 0, 15000])
            anj_var = np.array([np.sqrt(anj_cov_matrix[0][0]), np.sqrt(anj_cov_matrix[1][1]), np.sqrt(anj_cov_matrix[2][2])])
            trg_coors = np.array([0, 0, 30000])
            trg_var = np.array([np.sqrt(trg_cov_matrix[0][0]), np.sqrt(trg_cov_matrix[1][1]), np.sqrt(trg_cov_matrix[2][2])])
            trace_jammer.coordinates = random.normal(anj_coors, anj_var)
            trace_target.coordinates = random.normal(trg_coors, trg_var)
            # Определяем оценку координат точки АШП
            est_anj_coords = trace_jammer.calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(trace_target)[0]
            # Добавляем полученные координаты в массивы
            arr_common_coords[:, i] = est_anj_coords
            # Считаем ковариационную матрицу точки АШП
            cov_matrix = trace_jammer.calc_anj_cov_matrix(trace_target)
            # Добавляем эту матрицу в массив
            arr_cov_matrix[i, :, :] = cov_matrix
        # Меняем тип
        arr_common_coords = np.array(arr_common_coords)
        arr_cov_matrix = np.array(arr_cov_matrix)
        # Создаем общую ковариационную матрицу координат
        coords_cov_matrix = np.cov(arr_common_coords)
        # Мат ожидание посчинанных ковариационных матриц
        mid_coords_cov_matrix = np.mean(arr_cov_matrix, axis=0)
        self.assertEqual(coords_cov_matrix.tolist(), mid_coords_cov_matrix.tolist())


    def test_another_test(self):
        def calc_m(eq, q, l):
            return eq * l + q

        def calculate_l(eq, pq):
            return -np.dot(eq, pq) / np.dot(eq, eq)

        def calculate_var_l(eq, pq, kq, kp):
            grad_l_q = (np.dot(eq, pq) * 2 *eq - (pq+eq)*np.dot(eq, eq)) / (np.dot(eq, eq) ** 2)
            grad_l_p = (-eq) / np.dot(eq, eq)

            return grad_l_q @ kq @ grad_l_q.transpose() + grad_l_p @ kp @ grad_l_p.transpose()

        q_cov_sigma = np.array([1, 1, 1])
        p_cov_sigma = q_cov_sigma / 100

        q_cov_matrix = np.diag(q_cov_sigma ** 2)
        p_cov_matrix = np.diag(p_cov_sigma ** 2)

        e = np.zeros(3)
        mean_q = np.array([0, 0, 50])
        mean_p = np.array([0, 0, 100])

        n = 100000
        m_pred = np.zeros((n, 3))
        l = np.zeros(n)
        var_l = np.zeros(n)
        r_new = np.zeros(n)
        for iter in range(n):
            q = np.random.normal(mean_q, q_cov_sigma)
            p = np.random.normal(mean_p, p_cov_sigma)

            eq = q - e
            pq = q - p
            l[iter] = calculate_l(eq, pq)
            var_l[iter] = calculate_var_l(eq, pq, q_cov_matrix, p_cov_matrix)
            m_pred[iter, :] = calc_m(eq, q, l[iter])

            r_new[iter] = q[2]*(l[iter]+1)
        estimate_variance_l = np.mean(var_l)
        real_variance_l = np.var(l)
        estimate_var_r = estimate_variance_l * np.dot(mean_q-e, mean_q-e)
        est_cov_matrix_dec = np.cov(m_pred.transpose())
        est_cov_matrix_sph = calc_scs_from_dec(est_cov_matrix_dec, np.mean(m_pred, axis=0))
        pass




