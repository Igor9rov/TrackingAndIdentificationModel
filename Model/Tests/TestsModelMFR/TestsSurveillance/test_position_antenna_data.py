from unittest import TestCase

import numpy as np

from position_antenna_data import PositionAntennaData


class TestPositionAntennaData(TestCase):
    """Тест для класса PositionAntennaData"""
    def setUp(self) -> None:
        """Сохранение ссылки на данные по положению антенны

        :return: None
        """
        self.position_data = PositionAntennaData()

    def test_acs2bcs_and_bcs2acs(self) -> None:
        """Проверка пересчётов координат из АСК в БСК и обратно,
        после последовательного пересчёта должны получить то же самое

        :return: None
        """
        # Подготовка данных для функций
        real_coordinates, real_velocities = np.array([30_000., 5_000., 30_000.]), np.array([100., 100., 100.])

        # Выполнение тестируемых функций
        acs2bcs, bcs2acs = self.position_data.acs2bcs, self.position_data.bcs2acs
        coordinates, velocities = bcs2acs(*acs2bcs(real_coordinates, real_velocities))

        # Проверка для координат
        coordinates = coordinates.round(7).tolist()
        real_coordinates = [30_000., 5_000., 30_000.]
        self.assertEqual(real_coordinates, coordinates, "Координаты не совпадают")

        # Проверка для скоростей
        velocities = velocities.round(7).tolist()
        real_velocities = [100., 100., 100.]
        self.assertEqual(real_velocities, velocities, "Скорости не совпадают")

    def test_dec2acs_and_acs2dec(self) -> None:
        """Проверка пересчётов из МЗСК в АСК и обратно,
        после последовательного пересчёта должны получить то же самое

        :return: None
        """
        # Подготовка данных для функций
        real_coordinates, real_velocities = np.array([312_000., 5_000., 30_000.]), np.array([100., 100., 100.])

        # Выполнение тестируемых функций
        dec2acs, acs2dec = self.position_data.dec2acs, self.position_data.acs2dec
        coordinates, velocities = acs2dec(*dec2acs(real_coordinates, real_velocities))

        # Проверка для координат
        coordinates = coordinates.round(7).tolist()
        real_coordinates = [312_000., 5_000., 30_000.]
        self.assertEqual(real_coordinates, coordinates, "Координаты не совпадают")

        # Проверка для скоростей
        velocities = velocities.round(7).tolist()
        real_velocities = [100., 100., 100.]
        self.assertEqual(real_velocities, velocities, "Скорости не совпадают")

    def test_dec2bcs_and_bcs2dec(self) -> None:
        """Проверка пересчётов из МЗСК в БСК и обратно,
        после последовательного пересчёта должны получить то же самое

        :return: None
        """
        # Подготовка данных для функций
        real_coordinates, real_velocities = np.array([30_000, 5_000, 30_000]), np.array([120, 100, 100])

        # Выполнение тестируемых функций
        dec2bcs, bcs2dec = self.position_data.dec2bcs, self.position_data.bcs2dec
        # После пересчёта из МЗСК в БСК и обратно в МЗСК должны получиться те же самые значения
        coordinates, velocities = bcs2dec(*dec2bcs(real_coordinates, real_velocities))

        # Проверка для координат
        coordinates = coordinates.round(7).tolist()
        real_coordinates = [30_000., 5_000., 30_000.]
        self.assertEqual(real_coordinates, coordinates, "Координаты не совпадают")

        # Проверка для скоростей
        velocities = velocities.round(7).tolist()
        real_velocities = [120., 100., 100.]
        self.assertEqual(real_velocities, velocities, "Скорости не совпадают")

    def test_calc_dec_covariance_matrix_from_bcs(self) -> None:
        """Проверка для расчёта ковариационной матрицы в прямоугольной декартовой СК, имея матрицу в БСК

        :return: None
        """
        # Вычисление тестируемой функцией
        calc_dec_covariance_matrix_from_bcs = self.position_data.calc_dec_covariance_matrix_from_bcs
        cov_matrix = calc_dec_covariance_matrix_from_bcs(covariance_matrix_bcs=np.diag([5.0, 0.00087, 0.00087]),
                                                         coordinate_bcs=np.array([30_000, 0, 0]))

        # Проверка для ковариационной матрицы
        cov_matrix = cov_matrix.round().tolist()
        real_cov_matrix = [[195754.0, -339047.0, 0.0],
                           [-339047.0, 587251.0, 0.0],
                           [0.0, 0.0, 783000.0]]
        self.assertEqual(real_cov_matrix, cov_matrix, "Ковариационная матрица оценена неверно")
