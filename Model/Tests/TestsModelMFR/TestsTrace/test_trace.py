from math import pi
from unittest import TestCase

import numpy as np

from target import Target
from trace_ import Trace


class TestTrace(TestCase):
    def setUp(self) -> None:
        """Сохраняет ссылки на нужные объекты, откатывает их к первоначальному состоянию после теста

        :return: None
        """
        # Цель, по которой будет завязана трасса
        self.target = Target(number=1,
                             coordinates=np.array([10_000., 5_000., 1_000.]),
                             velocities=np.array([300., 0., 10.]),
                             target_type="Aerodynamic")

        # Собственная трасса
        self.trace = Trace(target=self.target,
                           mfr_number=1,
                           mfr_stable_point=np.array([1100, 20, -500]))
        # Сообщение о ошибке
        self.failure_msg = "Что-то было переименовано."

    def test___init__(self) -> None:
        """Проверяет иницализатор

        :return: None
        """
        # Проверка для текущего времени в тиках
        estimate_tick = self.trace.estimate_tick
        real_estimate_tick = 0
        self.assertEqual(real_estimate_tick, estimate_tick, "Текущеее время неверно")

        # Проверка для цели
        target = self.trace.target
        real_target = self.target
        self.assertEqual(real_target, target, "Цель установлена неверно")

        # Проверка для признака пеленга
        is_bearing = self.trace.is_bearing
        real_is_bearing = False
        self.assertEqual(real_is_bearing, is_bearing, "Признак пеленга неверен")

        # Проверка для типа сопровождения
        is_auto_tracking = self.trace.is_auto_tracking
        real_is_auto_tracking = False
        self.assertEqual(real_is_auto_tracking, is_auto_tracking, "Тип сопровождения неверен")

        # Проверка для априорной дальности
        default_range = self.trace.default_range
        real_default_range = 50_000.
        self.assertEqual(real_default_range, default_range, "Априорная дальность неверна")

        # Проверка временных тиков между измерениями
        frame_tick = self.trace.frame_tick
        real_frame_tick = 20
        self.assertEqual(real_frame_tick, frame_tick, "Временные тики между измерениями неверны")

    def test_measure(self) -> None:
        """Проверка измерений корординат цели

        :return: None
        """
        # Определяем нужные для функции данные
        sigma_measure = np.array([5.0, 0.00087, 0.00087])
        mean_coordinate_bcs = np.array([30000, pi/6, pi/6])
        # Столько измерений будет выполнено
        n = 100
        # Массив для хранения измерений
        measure_coordinates_bcs = np.zeros((3, n))

        # Вызов тестируемой функции в цикле
        for index in range(n):
            self.trace.measure(mean_coordinate_bcs, sigma_measure)
            # Запись измерений в отдельный массив
            measure_coordinates_bcs[:, index] = self.trace.coordinates_data.measure_coordinates_bcs

        # Проверять здесь особо нечего, проверим соотвествие сигм распределения указанным, и МО измеренных координат
        # Порог для сравнения (15% процентов)
        threshold = [0.15, 0.15, 0.15]

        # Проверка для МО
        estimated_mean_coordinates_bcs = np.mean(measure_coordinates_bcs, axis=1)
        difference_coordinates = (abs(estimated_mean_coordinates_bcs-mean_coordinate_bcs)/mean_coordinate_bcs).tolist()
        self.assertLess(difference_coordinates, threshold)

        # Проверка для СКО
        estimated_sigma_measure = np.std(measure_coordinates_bcs, axis=1)
        difference_sigma = (abs(estimated_sigma_measure - sigma_measure) / sigma_measure).tolist()
        self.assertLess(difference_sigma, threshold)

    def test_filtrate(self) -> None:
        """Тестить нечего, тестируемая функция это просто обёртка над тремя функциями этого же класса

        :return: None
        """
        # Подготовка нужных для функции данных
        real_sigma_measure = np.array([5.0, 0.00087, 0.00087])
        real_coordinates = np.array([30_000., pi / 6, pi / 6])
        coordinates_data = self.trace.coordinates_data
        coordinates_data.measure_coordinates_bcs = real_coordinates
        variance_bcs_data = self.trace.variance_bcs_data
        variance_bcs_data.sigma_measure_coordinates = real_sigma_measure

        # Запуск тестируемой функции
        self.trace.filtrate()

        # Проверка для измеренных координат
        measure_coordinates = coordinates_data.measure_coordinates_bcs.tolist()
        real_measure_coordinates = real_coordinates.tolist()
        self.assertEqual(real_measure_coordinates, measure_coordinates, "Координаты измерены неверно")

        # Проверка для оценных координат
        estimate_coordinates = coordinates_data.estimate_coordinates_bcs.tolist()
        real_estimate_coordinates = real_coordinates.tolist()
        self.assertEqual(real_estimate_coordinates, estimate_coordinates, "Координаты оценены неверно")

        # Проверка для экстраполированных координат
        extrapolate_coordinates = coordinates_data.extrapolate_coordinates_bcs.tolist()
        real_extrapolate_coordinates = real_coordinates.tolist()
        self.assertEqual(real_extrapolate_coordinates, extrapolate_coordinates, "Координаты экстраполированы неверно")

        # Проверка для экстраполированной скоростей
        extrapolate_velocities = self.trace.velocities_data.extrapolate_velocities_bcs.tolist()
        real_extrapolate_velocities = [0., 0., 0.]
        self.assertEqual(real_extrapolate_velocities, extrapolate_velocities, "Скорость экстраполирована неверно")

        # Проверка для дисперсий оцененных координат
        variance_estimate_coordinates = variance_bcs_data.variance_estimate_coordinates.tolist()
        real_variance_estimate_coordinates = [25.0, 7.569e-07, 7.569e-07]
        self.assertEqual(real_variance_estimate_coordinates, variance_estimate_coordinates, "Дисперсии неверны")

        # Проверка для дисперсий экстраполированных координат
        variance_extrapolate_coordinates = variance_bcs_data.variance_extrapolate_coordinates.tolist()
        real_variance_extrapolate_coordinates = [100.0, 3.0276e-06, 3.0276e-06]
        self.assertEqual(real_variance_extrapolate_coordinates, variance_extrapolate_coordinates, "Дипсерсии неверны")

    def test_update_filter_data(self) -> None:
        """Тест обновления данных фильтра

        :return: None
        """
        # Подготовка нужных для функции данных
        self.trace.coordinates_data.measure_coordinates_bcs = np.array([30000, pi / 6, pi / 6])
        self.trace.variance_bcs_data.sigma_measure_coordinates = np.array([5.0, 0.00087, 0.00087])

        # Запуск тестируемой функции
        self.trace.update_filter_data()

        # Проверка для измеренных координат
        measure_coordinates = self.trace.filter.current_data.measure_coordinates.tolist()
        real_measure_coordinates = [30000, pi / 6, pi / 6]
        self.assertEqual(real_measure_coordinates, measure_coordinates, "Координаты записались неправильно")

        # Проверка для СКО измеренных координат
        sigma = self.trace.filter.current_data.sigma_bcs.tolist()
        real_sigma = [5.0, 0.00087, 0.00087]
        self.assertEqual(real_sigma, sigma, "СКО записались неправильно")

    def test_run_filter(self) -> None:
        """Тест для обёртки над запуском operate фильтра, тестировать нечего

        :return: None
        """
        self.trace.filter.current_data.measure_coordinates = np.array([30000, pi / 6, pi / 6])
        self.trace.filter.current_data.sigma_bcs = np.array([5.0, 0.00087, 0.00087])
        try:
            self.trace.run_filter()
        except AttributeError:
            self.fail(self.failure_msg)

    def test_update_self_data(self) -> None:
        """Обновление собсивенных данных резултатами работы фильтра

        :return: None
        """
        # Подготовка нужных для функции данных
        current_data = self.trace.filter.current_data
        # Координаты
        current_data.measure_coordinates = np.array([10_000., pi/6, 0.])
        current_data.estimate_coordinates = np.array([10_033., pi/7, 0.2])
        current_data.extrapolate_coordinates = np.array([10_040., pi/8, 0.4])
        # Скорость
        current_data.extrapolate_velocities = np.array([20., -0.00009, 0.9])
        # Дисперсии
        current_data.variance_estimate_coordinates = np.array([25.0, 7.569e-07, 7.569e-07])
        current_data.variance_extrapolate_coordinates = np.array([100.0, 3.0276e-06, 3.0276e-06])

        # Вызов тестируемой функции
        self.trace.update_self_data()

        # Проверка для измеренных координат
        measure_coordinates = self.trace.coordinates_data.measure_coordinates_bcs.tolist()
        real_measure_coordinates = [10_000., pi / 6, 0.]
        self.assertEqual(real_measure_coordinates, measure_coordinates, "Измеренные координаты неверны")

        # Проверка для оцененных координат
        estimate_coordinates = self.trace.coordinates_data.estimate_coordinates_bcs.tolist()
        real_estimate_coordinates = [10_033., pi / 7, 0.2]
        self.assertEqual(real_estimate_coordinates, estimate_coordinates, "Оцененные координаты неверны")

        # Проверка для экстраполированных координат
        extrapolate_coordinates = self.trace.coordinates_data.extrapolate_coordinates_bcs.tolist()
        real_extrapolate_coordinates = [10_040., pi / 8, 0.4]
        self.assertEqual(real_extrapolate_coordinates, extrapolate_coordinates, "Экстраполированные координаты неверны")

        # Проверка для экстраполированной скорости
        extrapolate_velocities = self.trace.velocities_data.extrapolate_velocities_bcs.tolist()
        real_extrapolate_velocities = [20., -0.00009, 0.9]
        self.assertEqual(real_extrapolate_velocities, extrapolate_velocities, "Скорость неверна")

        # Проверка для дисперсии оценных координат
        variance_estimate_coordinates = self.trace.variance_bcs_data.variance_estimate_coordinates.tolist()
        real_variance_estimate_coordinates = [25.0, 7.569e-07, 7.569e-07]
        self.assertEqual(real_variance_estimate_coordinates, variance_estimate_coordinates, "Дипсерсии неверны")

        # Проверка для дисперсии экстраполированных координат
        variance_extrapolate_coordinates = self.trace.variance_bcs_data.variance_extrapolate_coordinates.tolist()
        real_variance_extrapolate_coordinates = [100.0, 3.0276e-06, 3.0276e-06]
        self.assertEqual(real_variance_extrapolate_coordinates, variance_extrapolate_coordinates, "Дипсерсии неверны")

    def test_calculate_dec_coord_and_vel(self) -> None:
        """Тест для вычисления координат и скоростей в декартовой системе координат

        :return: None
        """
        # Подготовка данных для функции
        # Данные о координатах
        coordinates_data = self.trace.coordinates_data
        coordinates_data.measure_coordinates_bcs = np.array([20_000., 1_000., 2_000.])
        coordinates_data.estimate_coordinates_bcs = np.array([30_000., 2_000., 3_000.])
        coordinates_data.extrapolate_coordinates_bcs = np.array([40_000., 3_000., 1_000.])
        # Данные о скорости
        self.trace.velocities_data.extrapolate_velocities_bcs = np.array([20., 200., 0.])

        # Вызов тестируемой функции
        self.trace.calculate_dec_coord_and_vel(func=lambda x, v: (2*x, 2*v), residuals=np.zeros(3))

        # Проверка для измеренных координат
        measure_coordinates = coordinates_data.measure_coordinates_dec.round(1).tolist()
        real_measure_coordinates = [40_000., 2_000., 4_000.]
        self.assertEqual(real_measure_coordinates, measure_coordinates, "Координаты неверны")

        # Проверка для оценнных координат
        estimate_coordinates = coordinates_data.estimate_coordinates_dec.round(1).tolist()
        real_estimate_coordinates = [60_000., 4_000., 6_000.]
        self.assertEqual(real_estimate_coordinates, estimate_coordinates, "Координаты неверны")

        # Проверка для экстраполированных координат
        extrapolate_coordinates = coordinates_data.extrapolate_coordinates_dec.round(1).tolist()
        real_extrapolate_coordinates = [80_000., 6_000., 2_000.]
        self.assertEqual(real_extrapolate_coordinates, extrapolate_coordinates, "Координаты неверны")

        # Проверка для экстраполированной скорости
        extrapolate_velocities = self.trace.velocities_data.extrapolate_velocities_dec.round(1).tolist()
        real_extrapolate_velocities = [40., 400., 0.]
        self.assertEqual(real_extrapolate_velocities, extrapolate_velocities, "Скорости неверны")

    def test_calc_with_zero_residuals(self):
        """Тест для расчета координат с нулевыми поправками

        :return: None
        """
        # Вызов тестируемой функции
        coordinates = self.trace.calc_with_residuals(coord=np.array([20_000., 220., 239.]),
                                                     residuals=None)
        coordinates = coordinates.tolist()

        # Оценка
        real_coordinates = [20_000., 220., 239.]

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Расчет без поправок неверный")

    def test_calc_with_nonzero_residuals(self):
        """Тест для расчета координат с ненулевыми поправками

        :return: None
        """
        # Вызов тестируемой функции
        coordinates = self.trace.calc_with_residuals(coord=np.array([20_000., 220., 239.]),
                                                     residuals=np.array([0., pi/10, 0.]))
        coordinates = coordinates.round(3).tolist()

        # Оценка
        real_coordinates = [19094.985, 220.0, -5953.037]

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Расчет без поправок неверный")

    def test_calculate_dec_covariance_matrix(self) -> None:
        """Тестирует пересчет ковариационной матрицы

        :return: None
        """
        # Подготовка данных для функции
        self.trace.variance_bcs_data.variance_measure_coordinates = np.array([20., 10., 2.])
        self.trace.coordinates_data.measure_coordinates_bcs = np.array([20., 2., 70.])

        self.trace.variance_bcs_data.variance_estimate_coordinates = np.array([30., 20., 10.])
        self.trace.coordinates_data.estimate_coordinates_bcs = np.array([29., 12., 21.])

        self.trace.variance_bcs_data.variance_extrapolate_coordinates = np.array([212., 42., 23.])
        self.trace.coordinates_data.extrapolate_coordinates_bcs = np.array([12., 323., 23.])

        # Вызов тестируемой функции
        self.trace.calculate_dec_covariance_matrix(func=lambda matrix, vec: 2*matrix)

        # Проверка для ковариационной матрицы измеренных координат
        measure_covariance_matrix = self.trace.covariance_matrix_data.measure_covariance_matrix.tolist()
        real_measure_covariance_matrix = [[40., 0., 0.],
                                          [0., 20., 0.],
                                          [0., 0., 4.]]
        self.assertEqual(real_measure_covariance_matrix, measure_covariance_matrix, "Ковариационная матрица неверна")

        # Проверка для ковариационной матрицы оценнных координат
        estimate_covariance_matrix = self.trace.covariance_matrix_data.estimate_covariance_matrix.tolist()
        real_estimate_covariance_matrix = [[60., 0., 0.],
                                           [0., 40., 0.],
                                           [0., 0., 20.]]
        self.assertEqual(real_estimate_covariance_matrix, estimate_covariance_matrix, "Ковариационная матрица неверна")

        # Проверка для ковариационной матрицы экстраполированных координат
        extrapolate_covariance_matrix = self.trace.covariance_matrix_data.extrapolate_covariance_matrix.tolist()
        real_extrapolate_covariance_matrix = [[424., 0., 0.],
                                              [0., 84., 0.],
                                              [0., 0., 46.]]
        self.assertEqual(real_extrapolate_covariance_matrix, extrapolate_covariance_matrix, "Ков. матрица неверна")

    def test_update_source_trace(self) -> None:
        """Тестирование обновления данных source_trace

        :return: None
        """
        # Подготовка данных для функции
        self.trace.is_auto_tracking = True
        self.trace.coordinates_data.estimate_coordinates_dec = np.array([20_000., 2_000., 1_000.])
        self.trace.source_trace.mfr_position = np.array([0., 0., 500.])
        self.trace.velocities_data.extrapolate_velocities_dec = np.array([200., 100., 0.])
        self.trace.estimate_tick = 25
        self.trace.is_bearing = True
        self.trace.covariance_matrix_data.extrapolate_covariance_matrix = np.diag([30., 20., 10.])

        # Вызов тестируемой функции
        self.trace.update_source_trace()
        source_trace = self.trace.source_trace

        # Проверка для признака АС
        is_auto_tracking = source_trace.is_auto_tracking
        real_is_auto_tracking = True
        self.assertEqual(real_is_auto_tracking, is_auto_tracking, "Признак АС неверен")

        # Проверка для координат
        coordinates = source_trace.coordinates.tolist()
        real_coordinates = [20_000., 2_000., 1_500.]
        self.assertEqual(real_coordinates, coordinates, "Координаты неверны")

        # Проверка для скоростей
        velocities = source_trace.velocities.tolist()
        real_velocities = [200., 100., 0.]
        self.assertEqual(real_velocities, velocities, "Скорости неверны")

        # Проверка для времени оценки
        estimate_tick = source_trace.estimate_tick
        real_estimate_tick = 25
        self.assertEqual(real_estimate_tick, estimate_tick, "Время оценки неверно")

        # Проверка для признака пеленга
        is_bearing = source_trace.is_bearing
        real_is_bearing = True
        self.assertEqual(real_is_bearing, is_bearing, "Признак пеленга неверен")

        # Проверка для ковариационной матрицы
        covariance_matrix = source_trace.coordinate_covariance_matrix.tolist()
        real_covariance_matrix = [[30., 0., 0.],
                                  [0., 20., 0.],
                                  [0., 0., 10.]]
        self.assertEqual(real_covariance_matrix, covariance_matrix, "Ковариационная матрица неверна")