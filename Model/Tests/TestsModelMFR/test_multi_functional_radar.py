from unittest import TestCase

import numpy as np
from math import pi
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

from multi_functional_radar import MultiFunctionalRadar
from target import Target


class TestMultiFunctionalRadar(TestCase):
    def setUp(self):
        # Подготовка цели
        target_coordinates = np.array([10000., 5000., 1000.])
        target_velocities = np.array([300., 0., 10.])
        is_anj = {0: False}
        is_auto_tracking = {0: False}
        first_target = Target(0, target_coordinates, target_velocities, "Aerodynamic", is_anj, is_auto_tracking)
        self.target_list = [first_target]
        mfr_coordinates = np.array([1100., 20., -800.])
        # Собственный локатор
        self.multi_functional_radar = MultiFunctionalRadar(mfr_coordinates, 0, self.target_list)
        # Сообщение о AttributeError
        self.failure_msg = "Что-то было переименовано."

    def test_operate(self):
        # Здесь просто постараемся вывести график сопровождения нашей цели
        x_line = []
        y_line = []
        z_line = []

        x_points = []
        y_points = []
        z_points = []
        for time in range(0, 270):
            for target in self.target_list:
                target.operate(time)
            self.multi_functional_radar.operate(time)
            if self.multi_functional_radar.trace_list:
                x_line.append(self.multi_functional_radar.trace_list[0].coordinates_data.estimate_coordinates_dec[0])
                y_line.append(self.multi_functional_radar.trace_list[0].coordinates_data.estimate_coordinates_dec[1])
                z_line.append(self.multi_functional_radar.trace_list[0].coordinates_data.estimate_coordinates_dec[2])

                x_points.append(self.multi_functional_radar.trace_list[0].coordinates_data.measure_coordinates_dec[0])
                y_points.append(self.multi_functional_radar.trace_list[0].coordinates_data.measure_coordinates_dec[1])
                z_points.append(self.multi_functional_radar.trace_list[0].coordinates_data.measure_coordinates_dec[2])
        ax = plt.axes(projection="3d")
        ax.plot3D(x_line, z_line, y_line, 'gray')
        ax.scatter3D(x_points, z_points, y_points, c=x_points)
        plt.show(block=False)

    # Проверим, что длина списка всех трасс корректно меняется с изменением параметров целей
    def test_update_trace_list(self):
        is_anj = {0: False}
        is_auto_tracking = {0: False}
        # Параметры первой цели
        first_target_coordinates = np.array([10000., 5000., 1000.])
        first_target_velocities = np.array([300., 0., 10.])
        first_target = Target(0, first_target_coordinates, first_target_velocities, "Aerodynamic", is_anj, is_auto_tracking)
        # Параметры второй цели
        second_target_coordinates = np.array([30000., 4900., 30000.])
        second_target_velocities = np.array([300., 0., 10.])
        second_target = Target(0, second_target_coordinates, second_target_velocities, "Aerodynamic", is_anj, is_auto_tracking)
        # Параметры третьей цели
        third_target_coordinates = np.array([55000., 4950., 3000.])
        third_target_velocities = np.array([300., 0., 10.])
        third_target = Target(0, third_target_coordinates, third_target_velocities, "Aerodynamic", is_anj, is_auto_tracking)
        # Объединили в массив целей
        self.target_list = [first_target, second_target, third_target]
        # Обновим собственный МФР
        mfr_coordinates = np.array([1100., 20., -800.])
        self.multi_functional_radar = MultiFunctionalRadar(mfr_coordinates, 0, self.target_list)
        # Сейчас можем сопровождать все цели
        self.multi_functional_radar.update_trace_list()
        self.assertEqual(3, len(self.multi_functional_radar.trace_list))
        # Не можем сопровождать первую цель из-за некорректного азимута
        self.multi_functional_radar.target_list[0].coordinates = np.array([1000, 5000, 30000])
        self.multi_functional_radar.update_trace_list()
        self.assertEqual(2, len(self.multi_functional_radar.trace_list))
        # Не можем сопровождать вторую цель из-за некорректного угла места
        self.multi_functional_radar.target_list[1].coordinates = np.array([1000, 10000, 1000])
        self.multi_functional_radar.update_trace_list()
        self.assertEqual(1, len(self.multi_functional_radar.trace_list))
        # Снова можем сопровождать первую цель
        self.multi_functional_radar.target_list[0].coordinates = np.array([30000, 5000, 30000])
        self.multi_functional_radar.update_trace_list()
        self.assertEqual(2, len(self.multi_functional_radar.trace_list))
        # Снова можем сопровождать вторую цель
        self.multi_functional_radar.target_list[1].coordinates = np.array([30000, 5000, 30000])
        self.multi_functional_radar.update_trace_list()
        self.assertEqual(3, len(self.multi_functional_radar.trace_list))

    # Тест сопровождения
    def test_tracking(self):
        # В отрицательный момент времени
        self.multi_functional_radar.tick = -1
        self.multi_functional_radar.tracking()
        # Трасса цели
        trace = self.multi_functional_radar.trace_list[0]
        # Нулевой вектор
        null_vec = [0, 0, 0]
        self.assertEqual(null_vec, trace.coordinates_data.measure_coordinates_dec.tolist())
        self.assertEqual(null_vec, trace.coordinates_data.estimate_coordinates_dec.tolist())
        self.assertEqual(null_vec, trace.coordinates_data.extrapolate_coordinates_dec.tolist())
        # В положительный момент времени
        self.multi_functional_radar.tick = 20
        self.multi_functional_radar.tracking()
        # Проверка, что нужных струкурах данных не нули
        self.assertNotEqual(null_vec, trace.coordinates_data.measure_coordinates_dec.tolist())
        self.assertNotEqual(null_vec, trace.coordinates_data.estimate_coordinates_dec.tolist())
        self.assertNotEqual(null_vec, trace.coordinates_data.extrapolate_coordinates_dec.tolist())

    def test_create_measurement(self):
        self.multi_functional_radar.tick = 20
        # Трасса цели
        trace = self.multi_functional_radar.trace_list[0]
        self.multi_functional_radar.create_measurement(trace)
        # Нулевой вектор
        null_vec = [0, 0, 0]
        # Проверка, что нужных струкурах данных не нули
        self.assertNotEqual(null_vec, trace.coordinates_data.measure_coordinates_bcs.tolist())
        self.assertNotEqual(null_vec, trace.variance_bcs_data.sigma_measure_coordinates.tolist())
        self.assertNotEqual(null_vec, trace.variance_bcs_data.variance_measure_coordinates.tolist())

    def test_calculate_trace_to_dec(self):
        self.multi_functional_radar.tick = 20
        # Трасса цели
        trace = self.multi_functional_radar.trace_list[0]
        # нужные для функции данные
        trace.coordinates_data.measure_coordinates_bcs = np.array([10000., pi/6, pi/6])
        trace.coordinates_data.estimate_coordinates_bcs = np.array([10000., pi/6, pi/6])
        trace.coordinates_data.extrapolate_coordinates_bcs = np.array([10000., pi/6, pi/6])
        trace.velocities_data.extrapolate_velocities_bcs = np.array([100., 0., 0.])
        trace.variance_bcs_data.variance_measure_coordinates = np.array([5.0, 0.00087, 0.00087])
        trace.variance_bcs_data.variance_estimate_coordinates = np.array([5.0, 0.00087, 0.00087])
        trace.variance_bcs_data.variance_extrapolate_coordinates = np.array([5.0, 0.00087, 0.00087])
        # Вызов тестируемой функции
        self.multi_functional_radar.calculate_trace_to_dec(trace)
        # Нулевой вектор
        null_vec = [0., 0., 0.]
        null_matrix = np.zeros((3, 3)).tolist()
        # Проверка, что нужных струкурах данных не нули
        self.assertNotEqual(null_vec, trace.coordinates_data.measure_coordinates_dec.tolist())
        self.assertNotEqual(null_vec, trace.coordinates_data.estimate_coordinates_dec.tolist())
        self.assertNotEqual(null_vec, trace.coordinates_data.extrapolate_coordinates_dec.tolist())
        self.assertNotEqual(null_vec, trace.velocities_data.extrapolate_velocities_dec.tolist())

        self.assertNotEqual(null_matrix, trace.covariance_matrix_data.measure_covariance_matrix.tolist())
        self.assertNotEqual(null_matrix, trace.covariance_matrix_data.estimate_covariance_matrix.tolist())
        self.assertNotEqual(null_matrix, trace.covariance_matrix_data.extrapolate_covariance_matrix.tolist())

    def test_update_source_traces(self):
        # Тестить нечего, здесь вызов функии trace в цикле
        try:
            self.multi_functional_radar.update_source_traces()
        except AttributeError:
            self.fail(self.failure_msg)
