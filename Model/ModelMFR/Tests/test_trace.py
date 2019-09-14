import numpy as np
from unittest import TestCase
from trace import Trace
from target import Target
from math import pi
from surveillance_data import PositionAntennaData


class TestSurveillanceData(TestCase):
    def setUp(self):
        # Подготовка цели
        coordinates = np.array([10000, 5000, 1000])
        velocities = np.array([300, 0, 10])
        target = Target(number=1, coordinates=coordinates, velocities=velocities, target_type="Aerodynamic")
        # Данные о локаторе
        mfr_stable_point = np.array([1100, 20, -500])
        mfr_number = 1
        # Собственная трасса
        self.trace = Trace(target, mfr_number, mfr_stable_point)
        self.failure_msg = "Что-то было переименовано."

    def test_measure(self):
        # Начальные значения
        sigma_measure = np.array([5.0, 0.00087, 0.00087])
        coordinate_bcs = np.array([30000, pi/6, pi/6])
        res_vector = []
        try:
            for i in range(75000):
                self.trace.measure(coordinate_bcs, sigma_measure)
                res_vector.append(self.trace.coordinates_data.measure_coordinates_bcs)
            # Проверять здесь особо нечего, проверим соотвествие сигм распределния указанным, и МО измеренных координат
            res_coordinates = np.array(res_vector)
            mean_res_coordinates = np.mean(res_coordinates, axis=0)
            res_sigma_vector = np.std(res_coordinates, axis=0)
            # Проверка на координаты
            self.assertEqual(mean_res_coordinates.round()[0], coordinate_bcs[0])
            self.assertEqual(mean_res_coordinates.round(5)[1], coordinate_bcs.round(5)[1])
            self.assertEqual(mean_res_coordinates.round(5)[2], coordinate_bcs.round(5)[2])
            # Проверка на сигмы
            self.assertEqual(res_sigma_vector.round()[0], sigma_measure[0])
            self.assertEqual(res_sigma_vector.round(5)[1], sigma_measure[1])
            self.assertEqual(res_sigma_vector.round(5)[2], sigma_measure[2])
        except AttributeError:
            self.fail(self.failure_msg)

    # Тестить нечего, вызов трёх функций, две занимаются присваиваниями, вторая запускает работу фильтра
    def test_filtrate(self):
        sigma_measure = np.array([5.0, 0.00087, 0.00087])
        coordinate_bcs = np.array([30000, pi / 6, pi / 6])
        self.trace.coordinates_data.measure_coordinates_bcs = coordinate_bcs
        self.trace.variance_bcs_data.sigma_measure_coordinates = sigma_measure
        # Запуск тестируемой функции
        self.trace.filtrate()
        # Смотрим на получившиеся значения
        # Так как шаг фильтра у нас нулевой, то никакой экстраполяции нет и измерения скорости тоже
        # проверим всё, что приходит с выхода функции
        self.assertEqual(self.trace.coordinates_data.measure_coordinates_bcs.tolist(), coordinate_bcs.tolist())
        self.assertEqual(self.trace.coordinates_data.estimate_coordinates_bcs.tolist(), coordinate_bcs.tolist())
        self.assertEqual(self.trace.coordinates_data.extrapolate_coordinates_bcs.tolist(), coordinate_bcs.tolist())
        # Скорость
        self.assertEqual(self.trace.velocities_data.extrapolate_velocities_bcs.tolist(), np.zeros(3).tolist())
        # Дисперсии
        self.assertEqual(self.trace.variance_bcs_data.variance_estimate_coordinates.tolist(),
                         (sigma_measure**2).tolist())
        self.assertEqual(self.trace.variance_bcs_data.variance_extrapolate_coordinates.tolist(),
                         (4*sigma_measure**2).tolist())

    def test_update_filter_data(self):
        sigma_measure = np.array([5.0, 0.00087, 0.00087])
        coordinate_bcs = np.array([30000, pi / 6, pi / 6])
        self.trace.coordinates_data.measure_coordinates_bcs = coordinate_bcs
        self.trace.variance_bcs_data.sigma_measure_coordinates = sigma_measure
        try:
            self.trace.update_filter_data()
        except AttributeError:
            self.fail(self.failure_msg)

    def test_run_filter(self):
        coordinate_bcs = np.array([30000, pi / 6, pi / 6])
        sigma_measure = np.array([5.0, 0.00087, 0.00087])
        self.trace.filter.current_data.measure_coordinates = coordinate_bcs
        self.trace.filter.current_data.sigma_bcs = sigma_measure
        try:
            self.trace.run_filter()
        except AttributeError:
            self.fail(self.failure_msg)

    def test_update_self_data(self):
        try:
            self.trace.update_self_data()
        except AttributeError:
            self.fail(self.failure_msg)

    def test_calculate_dec_coord_and_vel(self):
        try:
            # Создание функции для пересчёта
            position_antenna_data = PositionAntennaData()
            position_antenna_data.calculate_data()
            bcs2dec = position_antenna_data.bcs2dec
            # Вызов функции
            self.trace.calculate_dec_coord_and_vel(bcs2dec)
        except AttributeError:
            self.fail(self.failure_msg)

    def test_calculate_dec_covariance_matrix(self):
        try:
            # Создание функции для пересчёта
            position_antenna_data = PositionAntennaData()
            position_antenna_data.calculate_data()
            function_for_calc_dec_cov_matrix = position_antenna_data.calc_dec_covariance_matrix_from_bcs
            # Вызов функции
            self.trace.calculate_dec_covariance_matrix(function_for_calc_dec_cov_matrix)
        except AttributeError:
            self.fail(self.failure_msg)

    def test_update_source_trace(self):
        try:
            self.trace.update_source_trace()
        except AttributeError:
            self.fail(self.failure_msg)
