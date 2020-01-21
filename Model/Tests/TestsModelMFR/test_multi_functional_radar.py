from math import pi
from unittest import TestCase

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from multi_functional_radar import MultiFunctionalRadar
from target import Target


class TestMultiFunctionalRadar(TestCase):
    def setUp(self) -> None:
        """Сохраняет ссылки на нужные атрибуты

        :return: None
        """
        # Подготовка цели
        self.first_target = Target(number=0,
                                   coordinates=np.array([10_000., 5_000., 1_000.]),
                                   velocities=np.array([300., 0., 10.]),
                                   target_type="Aerodynamic")

        self.target_list = [self.first_target]

        # Собственный локатор
        self.multi_functional_radar = MultiFunctionalRadar(target_list=self.target_list,
                                                           stable_point=np.array([1_100., 20., -800.]),
                                                           mfr_number=2)

        # Сообщение о AttributeError
        self.failure_msg = "Что-то было переименовано."

    def test___init__(self) -> None:
        """Тест для инициализатора с аргументами, вопользуемся МФР из метода setUp

        :return: None
        """
        # Проверка для начального времени работы
        start_tick = self.multi_functional_radar.start_tick
        real_start_tick = 0.
        self.assertEqual(real_start_tick, start_tick, "Начальное время работы неверно")

        # Проверка для текущего времени в тиках
        tick = self.multi_functional_radar.tick
        real_tick = 0.
        self.assertEqual(real_tick, tick, "Текущее время в тиках задано неверно")

        # Проверка для номера МФР
        number = self.multi_functional_radar.number
        real_number = 2
        self.assertEqual(real_number, number, "Номер МФР задан неверно")

        # Проверка для точки стояния
        stable_point = self.multi_functional_radar.stable_point.tolist()
        real_stable_point = [1_100., 20., -800.]
        self.assertEqual(real_stable_point, stable_point, "Точка стояния задана неверно")

        # Проверка для признака юстированности
        is_adjustment = self.multi_functional_radar.is_adjustment
        real_is_adjustment = False
        self.assertEqual(real_is_adjustment, is_adjustment, "Признак юстированности задан неверно")

        # Проверка для вектора поправок
        residuals = self.multi_functional_radar.residuals
        real_residuals = None
        self.assertEqual(real_residuals, residuals, "Вектор поправок задан неверно")

        # Проверка для массива целей, которых пытается сопровождать МФР
        target_list = self.multi_functional_radar.target_list
        real_target_list = self.target_list
        self.assertEqual(real_target_list, target_list, "Массив целей задан неверно")

        # Проверка для массива информации о каждой трассе этого МФР
        registration = self.multi_functional_radar.registration
        real_registration = []
        self.assertEqual(real_registration, registration, "Регистрация задана неверно")

    def test_operate(self) -> None:
        """Юнит-тестом это назвать сложно (зависимостей уже СЛИШКОМ много), просто выведем 3D график сопровождения цели

        :return: None
        """
        # Подготовка массивов для координат оцененных (с выхода фильтра) и измеренных
        x_est, y_est, z_est = [], [], []
        x_meas, y_meas, z_meas = [], [], []

        # Выполнение тестируемой функции
        for time in range(0, 270):
            for target in self.target_list:
                target.operate(time)
            self.multi_functional_radar.operate(time)

            # Сбор данных в массивы
            if self.multi_functional_radar.trace_list:
                # Первая трасса
                first_trace = self.multi_functional_radar.trace_list[0]
                # Связь между индексами массива и координатами
                x, y, z = 0, 1, 2

                estimated_coordinates = first_trace.coordinates_data.estimate_coordinates_dec
                x_est.append(estimated_coordinates[x])
                y_est.append(estimated_coordinates[y])
                z_est.append(estimated_coordinates[z])

                measured_coordinates = first_trace.coordinates_data.measure_coordinates_dec
                x_meas.append(measured_coordinates[x])
                y_meas.append(measured_coordinates[y])
                z_meas.append(measured_coordinates[z])

        # Построение графика
        ax = plt.axes(projection=Axes3D.name)
        ax.plot3D(x_est, z_est, y_est, 'gray')
        ax.scatter3D(x_meas, z_meas, y_meas, c=x_meas)
        plt.show(block=False)

    def test_update_trace_list(self) -> None:
        """Проверим, что все цели с корректными координатами могут сопровождаться, а с некоректными нет

        :return: None
        """
        # Определение нужных для функции данных
        # Создадим три цели, которые можем сопровождать
        first_target = Target(coordinates=np.array([10_000., 5_000., 1_000.]))
        second_target = Target(coordinates=np.array([30_000., 4_900., 30_000.]))
        third_target = Target(coordinates=np.array([55_000., 4_950., 3_000.]))
        # Создание тестируемого МФР
        mfr = MultiFunctionalRadar(target_list=[first_target, second_target, third_target])

        # Вызов тестируемой функции
        mfr.update_trace_list()

        # Проверка для длины массива трасс
        len_trace_list = len(mfr.trace_list)
        real_len_trace_list = 3
        self.assertEqual(real_len_trace_list, len_trace_list, "Длина списка трасс определена неверно")

        # ______________________________________________________________________________________________________________
        # Если координаты целей стали некорректными, то и массив трасс должен измениться
        # Первую и вторую цель не можем сопровождать из-за некорректного азимута и угла места соответственно
        first_target.coordinates = np.array([10_000., 5_000., 30_000.])
        second_target.coordinates = np.array([1_000., 10_000., 1_000.])

        # Вызов тестируемой функции
        mfr.update_trace_list()

        # Проверка для длины массива трасс
        len_trace_list = len(mfr.trace_list)
        real_len_trace_list = 1
        self.assertEqual(real_len_trace_list, len_trace_list, "Длина списка трасс определена неверно")

        # ______________________________________________________________________________________________________________
        # Если при этом координаты целей снова станут корректными, то сопровождение станет возможным
        first_target.coordinates = np.array([30_000., 5_000., 30_000.])
        second_target.coordinates = np.array([10_000., 5_000., 1_000.])

        # Вызов тестируемой функции
        mfr.update_trace_list()

        # Проверка для длины массива трасс
        len_trace_list = len(mfr.trace_list)
        real_len_trace_list = 3
        self.assertEqual(real_len_trace_list, len_trace_list, "Длина списка трасс определена неверно")

    def test_append_trace_for_target(self) -> None:
        """Тестирование добавление трассы по цели, по которой не было трассы

        :return: None
        """
        # Создадим цель, которой нет в составе трасс
        new_target = Target()

        # Вызов тестируемой функции
        self.multi_functional_radar.append_trace_for_target(new_target)

        # Проверка для признака создания трассы по такой цели
        is_new_trace_in_trace_list = any(new_target is trace.target for trace in self.multi_functional_radar.trace_list)
        self.assertTrue(is_new_trace_in_trace_list, "Трасса не была добавлена")

        # Проверка для длины массива трасс после удаления
        real_len_trace_list = 2
        len_trace_list = len(self.multi_functional_radar.trace_list)
        self.assertEqual(real_len_trace_list, len_trace_list, "Длина списка трасс определена неверно")

    def test_remove_trace_for_target(self) -> None:
        """Тестирование удаление трассы по цели

        :return: None
        """
        # Удаление трассы по цели тестируемой функцией
        self.multi_functional_radar.remove_trace_for_target(self.first_target)

        # Проверка для длины массива трасс после удаления
        len_trace_list = len(self.multi_functional_radar.trace_list)
        real_len_trace_list = 0
        self.assertEqual(real_len_trace_list, len_trace_list, "Длина списка трасс определена неверно")

        # Проверка для признака удаления трассы по такой цели
        is_trace_in_trace_list = any(self.first_target is trace.target
                                     for trace in self.multi_functional_radar.trace_list)
        self.assertFalse(is_trace_in_trace_list, "Трасса не была удалена")

    def test_tracking_in_negative_time(self) -> None:
        """Тест сопровождения в отрицательный момент времени

        :return: None
        """
        # Определим нужные для функции данные
        self.multi_functional_radar.tick = -1

        # Вызов тестируемой функции
        self.multi_functional_radar.tracking()

        # Доступ к нужным структурам
        trace = self.multi_functional_radar.trace_list[0]
        trace_coordinates_data = trace.coordinates_data

        # Проверка для измеренных координат
        measure_coordinates = trace_coordinates_data.measure_coordinates_dec.tolist()
        real_measure_coordinates = [0., 0., 0.]
        self.assertEqual(real_measure_coordinates, measure_coordinates, "Измеренные координаты отличаются от нулевых")

        # Проверка для оцененных координат
        estimate_coordinates = trace_coordinates_data.estimate_coordinates_dec.tolist()
        real_estimate_coordinates = [0., 0., 0.]
        self.assertEqual(real_estimate_coordinates, estimate_coordinates, "Оцененные координаты отличаются от нулевых")

        # Проверка для экстраполированных координат
        extrapolate_coordinates = trace_coordinates_data.extrapolate_coordinates_dec.tolist()
        real_extrapolate_coordinates = [0., 0., 0.]
        self.assertEqual(real_extrapolate_coordinates, extrapolate_coordinates, "Экстраполированные координаты "
                                                                                "отличаются от нулевых")

    def test_tracking_in_positive_time(self) -> None:
        """Тест сопровождения в положительный момент времени

        :return: None
        """
        # В положительный момент времени, во время такта выполнения
        self.multi_functional_radar.tick = 20

        # Вызов тестируемой функции
        self.multi_functional_radar.tracking()

        # Доступ к нужным структурам
        trace = self.multi_functional_radar.trace_list[0]
        trace_coordinates_data = trace.coordinates_data

        # В такт сопровождения интересуемые величины точно не равны нулевому вектору
        null_vec = [0., 0., 0.]

        # Проверка для измеренных координат
        measure_coordinates = trace_coordinates_data.measure_coordinates_dec.tolist()
        self.assertNotEqual(null_vec, measure_coordinates, "Измеренные координаты не отличаются от нулевых")

        # Проверка для оцененных координат
        estimate_coordinates = trace_coordinates_data.estimate_coordinates_dec.tolist()
        self.assertNotEqual(null_vec, estimate_coordinates, "Оцененнные координаты не отличаются от нулевых")

        # Проверка для экстраполированных координат
        extrapolate_coordinates = trace_coordinates_data.extrapolate_coordinates_dec.tolist()
        self.assertNotEqual(null_vec, extrapolate_coordinates, "Экстраполированные координаты не отличаются от нулевых")

        # ______________________________________________________________________________________________________________
        # Если вызвать эту функцию в недопустимый такт сопровождения, то данные не должны измениться
        # Копия старых значений
        old_measure_coordinates = list(measure_coordinates)
        old_estimate_coordinates = list(estimate_coordinates)
        old_extrapolate_coordinates = list(extrapolate_coordinates)

        self.multi_functional_radar.tick = 21

        # Вызов тестируемой функции
        self.multi_functional_radar.tracking()

        # Проверка для измереннных координат
        measure_coordinates = trace_coordinates_data.measure_coordinates_dec.tolist()
        self.assertEqual(old_measure_coordinates, measure_coordinates, "Измеренные координаты изменились")

        # Проверка для оцененных координат
        estimate_coordinates = trace_coordinates_data.estimate_coordinates_dec.tolist()
        self.assertEqual(old_estimate_coordinates, estimate_coordinates, "Оцененнные координаты изменились")

        # Провекра для экстраполированных координат
        extrapolate_coordinates = trace_coordinates_data.extrapolate_coordinates_dec.tolist()
        self.assertEqual(old_extrapolate_coordinates, extrapolate_coordinates, "Экстраполированные координаты "
                                                                               "изменились")

    def test_create_measurement(self) -> None:
        """Тест для создания измерений по цели

        :return: None
        """
        # Подготовка нужных данных для функции
        target = Target(coordinates=np.array([10_000., 0., 10_000.]))
        mfr = MultiFunctionalRadar(target_list=[target], stable_point=np.array([0., 0., 10_000.]))
        trace = mfr.trace_list[0]
        mfr.tick = 20

        # Вызов тестируемой функии
        mfr.create_measurement(trace)

        # Измеренные биконические координаты
        range_, phi_v, phi_n = trace.coordinates_data.measure_coordinates_bcs

        # Так как процесс вероятностный, можем только предполагать пределы для биконических координат
        # Проверка для дальности
        is_range_in_limits = 9_980 <= range_ <= 10_020
        self.assertTrue(is_range_in_limits)

        # Проверка для первого угла
        is_phi_v_in_limits = -0.53 <= phi_v <= -0.51
        self.assertTrue(is_phi_v_in_limits)

        # Проверка для второго угла
        is_phi_n_in_limits = -0.01 <= phi_n <= 0.01
        self.assertTrue(is_phi_n_in_limits)

    def test_calculate_trace_to_dec(self) -> None:
        """Проверка вычислений для координат, скоростей, ковариационной мтарицы в прямоугольной декартвой МЗСК МФР
        Функция просто предоставляет доступ к функции пересчета для функций пересчета класса trace,
        не имееет смысла её досконально проверять, проверим на неравенство нулю некоторых элементов

        :return: None
        """
        # Определим нужные для функции данные
        self.multi_functional_radar.tick = 20
        trace = self.multi_functional_radar.trace_list[0]

        # Координаты БСК
        coordinates_data = trace.coordinates_data
        coordinates_data.measure_coordinates_bcs = np.array([10_000., pi/6, pi/6])
        coordinates_data.estimate_coordinates_bcs = np.array([10_000., pi/6, pi/6])
        coordinates_data.extrapolate_coordinates_bcs = np.array([10_000., pi/6, pi/6])

        # Скорость БСК
        velocities_data = trace.velocities_data
        velocities_data.extrapolate_velocities_bcs = np.array([100., 0., 0.])

        # Дисперсии для координат в БСК
        variance_bcs_data = trace.variance_bcs_data
        variance_bcs_data.variance_measure_coordinates = np.array([5.0, 0.00087, 0.00087])
        variance_bcs_data.variance_estimate_coordinates = np.array([5.0, 0.00087, 0.00087])
        variance_bcs_data.variance_extrapolate_coordinates = np.array([5.0, 0.00087, 0.00087])

        # ______________________________________________________________________________________________________________
        # Вызов тестируемой функции
        self.multi_functional_radar.calculate_trace_to_dec(trace)

        # ______________________________________________________________________________________________________________
        # Знаем, что отслеживаемые величины точно не равны нулевому вектору и нулевой матрице
        null_vector = [0., 0., 0.]

        # Проверка для измереннных координат
        measure_coordinates = coordinates_data.measure_coordinates_dec.tolist()
        self.assertNotEqual(null_vector, measure_coordinates, "Измеренные координаты - нулевой вектор")

        # Проверка для оцененных координат
        estimate_coordinates = coordinates_data.estimate_coordinates_dec.tolist()
        self.assertNotEqual(null_vector, estimate_coordinates, "Оцененные координаты - нулевой вектор")

        # Проверка для экстраполированных координат
        extrapolate_coordinates = coordinates_data.extrapolate_coordinates_dec.tolist()
        self.assertNotEqual(null_vector, extrapolate_coordinates, "Эктсраполированные координаты - нулевой вектор")

        # Проверка для экстраполированных скоростей
        extrapolate_velocities = velocities_data.extrapolate_velocities_dec.tolist()
        self.assertNotEqual(null_vector, extrapolate_velocities, "Экстраполированные скорости - нулевой вектор")

        # ______________________________________________________________________________________________________________
        # Струкутра данных с ковариационными матрицами
        covariance_matrix_data = trace.covariance_matrix_data

        # Знаем, что отслеживаемые величины точно не равны нулевой матрице
        null_matrix = [[0., 0., 0.],
                       [0., 0., 0.],
                       [0., 0., 0.]]

        # Проверка для ковариационной матрицы измерений
        measure_covariance_matrix = covariance_matrix_data.measure_covariance_matrix.tolist()
        self.assertNotEqual(null_matrix, measure_covariance_matrix, "Матрица для измеренных координат - нулевая")

        # Проверка для ковариационной матрицы оценки координат
        estimate_covariance_matrix = covariance_matrix_data.estimate_covariance_matrix.tolist()
        self.assertNotEqual(null_matrix, estimate_covariance_matrix, "Матрица для оцененных координат - нулевая")

        # Проверка для ковариационной матрицы экстраполированных координат
        extrapolate_covariance_matrix = covariance_matrix_data.extrapolate_covariance_matrix.tolist()
        self.assertNotEqual(null_matrix, extrapolate_covariance_matrix, "Матрица для экстр. кооринат - нулевая")

    def test_update_source_traces(self) -> None:
        """Тестить нечего, здесь обёртка над функией trace в цикле

        :return: None
        """
        try:
            self.multi_functional_radar.update_source_traces()
        except AttributeError:
            self.fail(self.failure_msg)

    def test_register(self) -> None:
        # Определим нужные для функции данные
        self.multi_functional_radar.tick = 20

        # Регистрация тестируемой функцией
        self.multi_functional_radar.register()

        # Проверка для регистрации
        registration = self.multi_functional_radar.registration
        real_registration = [[20, 2, False, 10000.0, 5000.0, 1000.0, 300.0, 0.0, 10.0,
                              0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, False, -1, 0.0]]
        self.assertEqual(real_registration, registration, "Регистрация не совпадает")
        # ______________________________________________________________________________________________________________
        # Изменим время и ещё раз прорегистриуем
        self.multi_functional_radar.tick = 40

        # Регистрация тестируемой функцией
        self.multi_functional_radar.register()

        # # Проверка для регистрации
        real_registration = [[20, 2, False, 10000.0, 5000.0, 1000.0, 300.0, 0.0, 10.0,
                              0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, False, -1, 0.0],
                             [40, 2, False, 10000.0, 5000.0, 1000.0, 300.0, 0.0, 10.0,
                              0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, False, -1, 0.0]]
        self.assertEqual(real_registration, registration, "Регистрация не совпадает")
