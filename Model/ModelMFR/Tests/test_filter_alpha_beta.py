import unittest
import numpy as np
from math import exp, sqrt, log10, fabs, pi, e
from filter_alpha_beta import FilterAB


class TestFilterAB(unittest.TestCase):
    def setUp(self):
        # Создаём фильтр с перегрузкой 4 и периодом сопровождения 1 секунда
        self.filter_a_b = FilterAB(manoeuvre_overload=4, frame_time=1)

    # Проверка вычисления относительной интенсивности манёвра
    def test_calc_manoeuvre_level(self):
        # Определим нужные для данной функции данные
        sigma_bcs = [5, 0.00087, 0.00087]
        coordinates = [30000, pi/4, pi/4]
        # Заполним ими фильтр
        self.filter_a_b.current_data.measure_coordinates = np.array(coordinates)
        self.filter_a_b.current_data.sigma_bcs = np.array(sigma_bcs)
        # Считаем относительную интенсивность манёвра тестируемой функцией
        self.filter_a_b.calc_manoeuvre_level()

        # Считаем относительную интенсивность манёвра сами
        # Ускорение свободного падения
        g_earth = 9.80665
        # Перегрузка при манёвре цели
        manoeuvre_overload = self.filter_a_b.manoeuvre_overload
        # Время между сопровождением в секундах
        frame_time = self.filter_a_b.frame_time
        # Дальность цели
        target_range = coordinates[0]

        manoeuvre_level_r = (2 * manoeuvre_overload * g_earth * frame_time**2) / (pi * sigma_bcs[0])
        manoeuvre_level_phi_v = (2 * manoeuvre_overload * g_earth * frame_time**2) / (pi * target_range * sigma_bcs[1])
        manoeuvre_level_phi_n = (2 * manoeuvre_overload * g_earth * frame_time**2) / (pi * target_range * sigma_bcs[2])
        # Объединили в массив
        manoeuvre_level = np.array([manoeuvre_level_r, manoeuvre_level_phi_v, manoeuvre_level_phi_n])
        self.assertEqual(self.filter_a_b.manoeuvre_level_array.round(7).tolist(), manoeuvre_level.round(7).tolist())

    # Вычисление коэффициентов alpha, beta для каждого такта фильтрации
    def test_calc_alpha_beta(self):
        # Определим нужные для данной функции данные
        sigma_bcs = [5, 0.00087, 0.00087]
        coordinates = [30000, pi / 4, pi / 4]
        # Заполним ими фильтр
        self.filter_a_b.current_data.measure_coordinates = np.array(coordinates)
        self.filter_a_b.current_data.sigma_bcs = np.array(sigma_bcs)
        self.filter_a_b.counter = 4
        # Получим относительную интенсивность манёвра
        self.filter_a_b.calc_manoeuvre_level()
        manoeuvre_level = self.filter_a_b.manoeuvre_level_array
        # Считаем альфа и бета тестируемой функцией
        self.filter_a_b.calc_alpha_beta()

        # Считаем альфа и бета сами
        alpha_array = []
        beta_array = []
        for coordinate in manoeuvre_level:
            lg_coordinate = log10(coordinate)
            if lg_coordinate <= 0.15:
                alpha = 0.5 * exp(-fabs(lg_coordinate - 0.15) ** 1.7 / (1.3*e))
                beta = 2 * (1 - alpha - sqrt(1 - 2 * alpha))
            elif 0.15 < lg_coordinate <= 0.65:
                alpha = 0.5 * exp(-fabs(lg_coordinate - 0.15) ** 1.9 / e)
                beta = 2 * (1 - alpha + sqrt(1 - 2 * alpha))
            else:
                alpha = 0.5 * exp(-fabs(0.65 - 0.15) ** 1.9 / e)
                beta = 2 * (1 - alpha + sqrt(1 - 2 * alpha))
            alpha_array.append(alpha)
            beta_array.append(beta)
        alpha_array = np.array(alpha_array)
        beta_array = np.array(beta_array)

        self.assertEqual(self.filter_a_b.alpha_array.round(5).tolist(), alpha_array.round(5).tolist())
        self.assertEqual(self.filter_a_b.beta_array.round(5).tolist(), beta_array.round(5).tolist())

    # Alpha-Beta фильтрация координат и производных
    def test_filtrate_coord_and_vel(self):
        # Определим нужные для данной функции данные
        sigma_bcs = np.array([5, 0.00087, 0.00087])
        measure_coordinates = np.array([30000, pi / 4, pi / 4])
        extrapolate_coordinates = np.array([30000, pi / 4, pi / 4])
        extrapolate_velocities = np.array([300, 300, 300])
        # Время в секундах между сопровождением
        dt = self.filter_a_b.frame_time
        # Заполняем текущие данные
        self.filter_a_b.counter = 0
        self.filter_a_b.current_data.measure_coordinates = measure_coordinates
        self.filter_a_b.current_data.sigma_bcs = sigma_bcs
        self.filter_a_b.current_data.extrapolate_coordinates = extrapolate_coordinates
        self.filter_a_b.current_data.extrapolate_velocities = extrapolate_velocities
        # Получим альфа и бета для данного случая
        self.filter_a_b.calc_manoeuvre_level()
        self.filter_a_b.calc_alpha_beta()
        alpha = self.filter_a_b.alpha_array
        beta = self.filter_a_b.beta_array
        # Считаем координаты и скорость тестируемой функцией
        self.filter_a_b.filtrate_coord_and_vel()

        # Считаем координаты и скорость сами
        estimate_coordinates = alpha * measure_coordinates + (1 - alpha) * extrapolate_coordinates
        estimate_velocities = (beta / dt) * (measure_coordinates - extrapolate_coordinates) + extrapolate_velocities

        self.assertEqual(self.filter_a_b.current_data.estimate_coordinates.all(), estimate_coordinates.all())
        self.assertEqual(self.filter_a_b.current_data.estimate_velocities.all(), estimate_velocities.all())
