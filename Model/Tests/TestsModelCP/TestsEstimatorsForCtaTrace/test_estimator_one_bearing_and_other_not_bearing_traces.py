import unittest
import numpy as np
from math import sqrt
from numpy.random import normal

from coordinate_system_math import dec2sph, sph2dec
from calc_covariance_matrix import calc_dec_from_scs
from source_trace import SourceTrace
from estimator_one_bearing_and_other_not_bearing_traces import EstimatorOneBearingAndOtherNotBearingTraces


class TestEstimatorOneBearingOtherNotBearingCtaTraces(unittest.TestCase):
    def setUp(self) -> None:
        first_trace = SourceTrace()
        first_trace.is_bearing = True
        second_trace = SourceTrace()
        self.estimator = EstimatorOneBearingAndOtherNotBearingTraces(first_trace, second_trace)

    def test_coordinates(self):
        self.estimator.jammer_trace.coordinates = np.array([-0.5, 2., 1.])
        self.estimator.jammer_trace.mfr_position = np.array([-1., 0., 0.])
        self.estimator.jammer_trace.coordinate_covariance_matrix = np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 1.]])

        self.estimator.target_trace.coordinates = np.array([1., 2., 2.])
        self.estimator.target_trace.mfr_position = np.array([2., 0., 0.])
        self.estimator.target_trace.coordinate_covariance_matrix = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
        # Посчитанное значение координат руками
        res_coords = np.array([0.40364773, 2.07310214, 1.55998843])
        # Посчитанное значение ковариационной матрицы функцией
        coords = self.estimator.coordinates
        self.assertEqual(coords.round(7).tolist(), res_coords.round(7).tolist())

    def test_coordinates_covariance_matrix(self):
        # Измерение координат трассы
        def measure_trace_coordinates(trace, mean_dec_coord, sigma):
            mean_sph_coord = dec2sph(mean_dec_coord)
            est_sph_coords = normal(mean_sph_coord, sigma)
            trace.coordinates = sph2dec(est_sph_coords) + trace.mfr_position
            trace.coordinate_covariance_matrix = calc_dec_from_scs(np.diag(sigma ** 2), est_sph_coords)
        # Мат. ожидание измерений декартовых координат постановщика АШП
        mean_jammer_coordinates = np.array([0., 0., 1500.])
        # Мат. ожидание измерений декартовых координат чистой цели
        mean_target_coordinates = np.array([0., 0., 3000.])
        # Параметры измерений
        jammer_sigma = np.array([0., 0.01, 0.0087])
        target_sigma = np.array([10., 0.009, 0.003])
        # Количество итераций
        n = 1000
        # Вспомогательные массивы
        coord_array = np.zeros((n, 3))
        cov_array = np.zeros((n, 3, 3))
        for i in range(n):
            measure_trace_coordinates(self.estimator.jammer_trace, mean_jammer_coordinates, jammer_sigma)
            measure_trace_coordinates(self.estimator.target_trace, mean_target_coordinates, target_sigma)
            # Определяем оценку координат результирующей точки
            est_anj_coords = self.estimator.coordinates
            # Считаем ковариационную матрицу результирующей точки
            cov_matrix = self.estimator.coordinates_covariance_matrix
            # Добавляем эту матрицу в массив
            coord_array[i, :] = est_anj_coords
            cov_array[i, :, :] = cov_matrix
        # Меняем тип
        coord_array = np.array(coord_array)
        cov_array = np.array(cov_array)
        # Создаем общую ковариационную матрицу координат
        coords_cov_matrix = np.cov(coord_array, rowvar=False)
        # Мат ожидание посчинанных ковариационных матриц
        est_coords_cov_matrix = np.mean(cov_array, axis=0)
        # Допускаем различие в 15%
        threshold = 15
        # Сравнение интересуемых дисперсий
        # Разница ковариационных матриц
        difference_in_matrix = abs(est_coords_cov_matrix - coords_cov_matrix)
        diff_x = 100 * difference_in_matrix[0][0] / coords_cov_matrix[0][0]
        diff_y = 100 * difference_in_matrix[1][1] / coords_cov_matrix[1][1]
        diff_z = 100 * difference_in_matrix[2][2] / coords_cov_matrix[2][2]
        self.assertLess(diff_x, threshold)
        self.assertLess(diff_y, threshold)
        self.assertLess(diff_z, threshold)
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
        A, B = self.estimator.calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, anj_trg_cov_matrix)
        self.assertEqual(A.tolist(), res_A.tolist())
        self.assertEqual(B.tolist(), res_B.tolist())

    def test_calc_anj_cov_matrix(self):
        # Заполняем данные
        anj_mfr_pos = np.array([-1., 0., 0.])
        anj_coords = np.array([-0.5, 2., 1.])
        trg_mfr_pos = np.array([2., 0., 0.])
        trg_coords = np.array([1., 2., 2.])
        anj_cov_matrix = np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 1.]])
        trg_cov_matrix = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
        self.estimator.jammer_trace.coordinates = anj_coords
        self.estimator.jammer_trace.is_bearing = True
        self.estimator.jammer_trace.mfr_position = anj_mfr_pos
        self.estimator.jammer_trace.coordinate_covariance_matrix = anj_cov_matrix
        self.estimator.target_trace.coordinates = trg_coords
        self.estimator.target_trace.is_bearing = False
        self.estimator.target_trace.mfr_position = trg_mfr_pos
        self.estimator.target_trace.coordinate_covariance_matrix = trg_cov_matrix
        # Посчитанное значение ковариационной матрицы ручками
        res_cov_matrix_dec = np.array([[-0.0539683, -0.3365079, 0.0126984],
                                       [-0.3365079, 4.5555556, 2.0539683],
                                       [0.0126984, 2.0539683, 1.1650794]])
        # Посчитанное значение ковариационной матрицы функцией
        cov_matrix_dec = self.estimator.calc_anj_cov_matrix()
        self.assertEqual(cov_matrix_dec.round(7).tolist(), res_cov_matrix_dec.round(7).tolist())

    def test_calculate_method_cov_matrix_for_jammer(self):
        self.estimator.jammer_trace.coordinates = np.array([0., 0., 15000.])
        self.estimator.jammer_trace.coordinate_covariance_matrix = np.zeros((3, 3))
        self.estimator.target_trace.coordinates = np.array([0., 0., 30000.])
        self.estimator.target_trace.coordinate_covariance_matrix = np.diag(np.ones(3))
        # Посчитанное значение ковариационной матрицы метода
        res_method_cov_matrix = np.array([[self.estimator.target_trace.coordinate_covariance_matrix[0][0], 0., 0.],
                                          [0., 0., 0.],
                                          [0., 0., 0.]])
        # Посчитанное значение ковариационной матрицы функцией
        method_cov_matrix = self.estimator.calculate_method_cov_matrix_for_jammer()
        self.assertEqual(method_cov_matrix.round(7).tolist(), res_method_cov_matrix.round(7).tolist())

    def test_calc_anj_trg_cov_matrix(self):
        # Заполняем данные
        anj_mfr_pos = np.array([-1., 0., 0.])
        anj_coords = np.array([0., 2., 1.])
        trg_mfr_pos = np.array([2., 0., 0.])
        trg_coords = np.array([1., 2., 2.])
        anj_cov_matrix = np.array([[0., 0., 0.], [0., 1., 1.], [0., 1., 1.]])
        trg_cov_matrix = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])
        self.estimator.jammer_trace.coordinates = anj_coords
        self.estimator.jammer_trace.is_bearing = True
        self.estimator.jammer_trace.mfr_position = anj_mfr_pos
        self.estimator.jammer_trace.coordinate_covariance_matrix = anj_cov_matrix
        self.estimator.target_trace.coordinates = trg_coords
        self.estimator.target_trace.is_bearing = False
        self.estimator.target_trace.mfr_position = trg_mfr_pos
        self.estimator.target_trace.coordinate_covariance_matrix = trg_cov_matrix
        # Посчитанное значение ковариационной матрицы ручками
        res_method_cov_matrix = np.array([[2 * sqrt(2), 0., 0.],
                                          [0., 0., 0.],
                                          [0., 0., 0.]])
        # Посчитанное значение ковариационной матрицы функцией
        method_cov_matrix = self.estimator.calc_anj_trg_cov_matrix()
        self.assertEqual(method_cov_matrix.round(7).tolist(), res_method_cov_matrix.round(7).tolist())


if __name__ == '__main__':
    unittest.main()
