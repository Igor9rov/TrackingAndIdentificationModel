import unittest
from math import pi

import numpy as np

from filter_alpha_beta import FilterAB


class TestFilterAB(unittest.TestCase):
    def setUp(self):
        """Создаём фильтр с перегрузкой 4 и периодом сопровождения 1 секунда"""
        self.filter_a_b = FilterAB(manoeuvre_overload=4, frame_time=1)

    def test_calc_manoeuvre_level(self):
        """Проверка вычисления относительной интенсивности манёвра

        :return: None
        """
        # Определим нужные для данной функции данные и заполним ими фильтр
        self.filter_a_b.current_data.measure_coordinates = np.array([30000, pi/4, pi/4])
        self.filter_a_b.current_data.sigma_bcs = np.array([5, 0.00087, 0.00087])

        # Считаем относительную интенсивность манёвра тестируемой функцией
        self.filter_a_b.calc_manoeuvre_level()

        # Проверка для относительной интеснивности маневра
        manoeuvre_level = self.filter_a_b.manoeuvre_level_array.round(5).tolist()
        real_manoeuvre_level = [4.99449, 0.95680, 0.95680]
        self.assertEqual(real_manoeuvre_level, manoeuvre_level, "Интенсивность манёвра определена неверно")

    def test_calc_alpha_beta_when_counter_more_than_2(self):
        """Вычисления коэффициентов alpha, beta при счётчике большем или равном 2

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.counter = 2
        self.filter_a_b.manoeuvre_level_array = np.array([4.99448583, 0.95679805, 0.95679805])

        # Считаем альфа и бета тестируемой функцией
        self.filter_a_b.calc_alpha_beta()

        # Проверка для коэффициента альфа
        alpha = self.filter_a_b.alpha_array.round(5).tolist()
        real_alpha = [0.47504, 0.49319, 0.49319]
        self.assertEqual(real_alpha, alpha, "Альфа оценена неверно")

        # Проверка для коэффициента бета
        beta = self.filter_a_b.beta_array.round(5).tolist()
        real_beta = [1.49675, 0.78021, 0.78021]
        self.assertEqual(real_beta, beta, "Бета оценена неверно")

    def test_calc_alpha_beta_when_counter_less_than_2(self):
        """Вычисления коэффициентов alpha, beta при счётчике меньшем 2

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.counter = 1
        self.filter_a_b.manoeuvre_level_array = np.array([4.99448583, 0.95679805, 0.95679805])

        # Считаем альфа и бета тестируемой функцией
        self.filter_a_b.calc_alpha_beta()

        # Проверка для коэффициента альфа
        alpha = self.filter_a_b.alpha_array.tolist()
        real_alpha = [1, 1, 1]
        self.assertEqual(real_alpha, alpha, "Альфа оценена неверно")

        # Проверка для коэффициента бета
        beta = self.filter_a_b.beta_array.tolist()
        real_beta = [1, 1, 1]
        self.assertEqual(real_beta, beta, "Бета оценена неверно")

    def test_filtrate_coord_and_vel_when_counter_is_null(self):
        """Проверка Alpha-Beta фильтрации координат и производных, когда счётчик в нуле (начало работы)

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.counter = 0
        self.filter_a_b.current_data.measure_coordinates = np.array([30_000, 390, 100])
        self.filter_a_b.current_data.extrapolate_coordinates = np.array([31_000, 410, 120])
        self.filter_a_b.alpha_array = np.ones(3)
        self.filter_a_b.beta_array = np.ones(3)

        # Считаем координаты и скорость тестируемой функцией
        self.filter_a_b.filtrate_coord_and_vel()

        # Проверка для координат
        coordinates = self.filter_a_b.current_data.estimate_coordinates.tolist()
        real_coordinates = [30_000, 390, 100]
        self.assertEqual(real_coordinates, coordinates, "Координаты оценены неверно")

        # Проверка для скоростей
        velocities = self.filter_a_b.current_data.estimate_velocities.tolist()
        real_velocities = [0, 0, 0]
        self.assertEqual(real_velocities, velocities, "Скорость оценена неверно")

    def test_filtrate_coord_and_vel_when_counter_is_not_null(self):
        """Проверка Alpha-Beta фильтрации координат и производных в середине работы

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.counter = 10
        self.filter_a_b.current_data.measure_coordinates = np.array([30_000, 390, 100])
        self.filter_a_b.current_data.extrapolate_coordinates = np.array([31_000, 410, 120])
        self.filter_a_b.current_data.extrapolate_velocities = np.array([100, 200, 20])
        self.filter_a_b.alpha_array = np.array([0.5, 0.5, 0.5])
        self.filter_a_b.beta_array = np.array([0.5, 0.5, 0.5])

        # Считаем координаты и скорость тестируемой функцией
        self.filter_a_b.filtrate_coord_and_vel()

        # Проверка для координат
        coordinates = self.filter_a_b.current_data.estimate_coordinates.tolist()
        real_coordinates = [30_500, 400, 110]
        self.assertEqual(real_coordinates, coordinates, "Координаты оценены неверно")

        # Проверка для скоростей
        velocities = self.filter_a_b.current_data.estimate_velocities.tolist()
        real_velocities = [-400.0, 190.0, 10.0]
        self.assertEqual(real_velocities, velocities, "Скорость оценена неверно")

    def test_extrapolate_coord_and_vel(self):
        """Проверка экстраполяции координат и скорости на следующий шаг

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.current_data.estimate_coordinates = np.array([40_000, 5_000, 10_000])
        self.filter_a_b.current_data.estimate_velocities = np.array([100, 200, 70])

        # Экстраполируем координаты и скорость тестируемой функцией
        self.filter_a_b.extrapolate_coord_and_vel()

        # Проверка для координат
        coordinates = self.filter_a_b.prolong_data.extrapolate_coordinates.tolist()
        real_coordinates = [40_100, 5_200, 10_070]
        self.assertEqual(real_coordinates, coordinates, "Координаты экстраполированы неверно")

        # Проверка для скоростей
        velocities = self.filter_a_b.prolong_data.extrapolate_velocities.tolist()
        real_velocities = [100, 200, 70]
        self.assertEqual(real_velocities, velocities, "Скорость экстраполирована неверно")

    def test_calculate_sigma(self):
        """Проверяет вычисление ошибок фильтра

        :return: None
        """
        # Определим нужные для функции данные
        self.filter_a_b.frame_time = 1
        self.filter_a_b.alpha_array = np.array([0.5, 0.5, 0.5])
        self.filter_a_b.beta_array = np.array([0.75, 0.75, 0.75])
        self.filter_a_b.previous_data.covariance_est_coord_vel = np.array([2., 1., 3.])
        self.filter_a_b.previous_data.variance_estimate_velocities = np.array([3., 5., 3.])
        self.filter_a_b.current_data.variance_extrapolate_coordinates = np.array([4., 6., 4.])
        self.filter_a_b.current_data.sigma_bcs = np.array([1., 1., 1.])

        # Выполним расчет ошибок фильтра тестируемой функцией
        self.filter_a_b.calculate_sigma()

        # Проверка для ковариации оцененных координаты и скорости на текущий шаг
        covariance_est_coord_vel = self.filter_a_b.current_data.covariance_est_coord_vel.tolist()
        real_covariance_est_coord_vel = [1.375, 1.125, 1.875]
        self.assertEqual(real_covariance_est_coord_vel, covariance_est_coord_vel, "Ковариации неверны")

        # Проверка для дисперии оцененнных координат на текущий шаг
        variance_estimate_coordinates = self.filter_a_b.current_data.variance_estimate_coordinates.tolist()
        real_variance_estimate_coordinates = [1.25, 1.75, 1.25]
        self.assertEqual(real_variance_estimate_coordinates, variance_estimate_coordinates, "Дипсерсии неверны")

        # Проверка для дисперсии оцененных скоростей на текущий шаг
        variance_estimate_velocities = self.filter_a_b.current_data.variance_estimate_velocities.tolist()
        real_variance_estimate_velocities = [-1.6875, -0.0625, -3.1875]
        self.assertEqual(real_variance_estimate_velocities, variance_estimate_velocities, "Дисперсии неверны")

        # Проверка для дисперии экстраполированных координат на следующий шаг
        variance_extrapolate_coordinates = self.filter_a_b.prolong_data.variance_extrapolate_coordinates.tolist()
        real_variance_extrapolate_coordinates = [2.3125, 3.9375, 1.8125]
        self.assertEqual(real_variance_extrapolate_coordinates, variance_extrapolate_coordinates, "Дисперсии неверны")

    def test_increment_data(self):
        """Проверяет смещение данных фильтра

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.prolong_data.extrapolate_coordinates = np.array([30_000, 90, 70_000])
        self.filter_a_b.prolong_data.extrapolate_velocities = np.array([20, 200, 150])
        self.filter_a_b.prolong_data.variance_extrapolate_coordinates = np.array([90_000, 9_000, 270_000])
        self.filter_a_b.current_data.covariance_est_coord_vel = np.array([24_000, 540, 34_000])
        self.filter_a_b.current_data.variance_estimate_velocities = np.array([190_000, 39_000, 630_000])

        # Сместим данные фильтра функцией
        self.filter_a_b.increment_data()

        # Проверка для координат
        coordinates = self.filter_a_b.current_data.extrapolate_coordinates.tolist()
        real_coordinates = [30_000, 90, 70_000]
        self.assertEqual(real_coordinates, coordinates, "Координаты смещены неверно")

        # Проверка для скоростей
        velocities = self.filter_a_b.current_data.extrapolate_velocities.tolist()
        real_velocities = [20, 200, 150]
        self.assertEqual(real_velocities, velocities, "Скорости смещены неверно")

        # Проверка для дисперсий координат
        variance_coordinates = self.filter_a_b.current_data.variance_extrapolate_coordinates .tolist()
        real_variance_coordinates = [90_000, 9_000, 270_000]
        self.assertEqual(real_variance_coordinates, variance_coordinates, "Дисперсии координат смещены неверно")

        # Проверка для ковариации координат и скоростей
        covariance_coord_vel = self.filter_a_b.previous_data.covariance_est_coord_vel.tolist()
        real_covariance_coord_vel = [24_000, 540, 34_000]
        self.assertEqual(real_covariance_coord_vel, covariance_coord_vel, "Ковариации смещены неверно")

        # Проверка для дисперсий скорости
        variance_velocities = self.filter_a_b.previous_data.variance_estimate_velocities.tolist()
        real_variance_velocities = [190_000, 39_000, 630_000]
        self.assertEqual(real_variance_velocities, variance_velocities, "Дисперсии скорости смещены неверно")

    def test_increment_counter(self):
        """Проверяет инкрементацию шага фильтра

        :return: None
        """
        # Определим нужные для данной функции данные
        self.filter_a_b.counter = 9

        # Инкрементируем счётчик сами
        self.filter_a_b.increment_counter()

        # Проверка для счетчика
        counter = self.filter_a_b.counter
        real_counter = 10
        self.assertEqual(real_counter, counter, "Инкрементация счётчика выполнена неверно")
