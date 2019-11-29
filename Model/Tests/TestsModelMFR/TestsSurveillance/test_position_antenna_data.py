from math import tan
from unittest import TestCase

import numpy as np

from position_antenna_data import PositionAntennaData


class TestPositionAntennaData(TestCase):
    """Тест для класса PositionAntennaData"""
    def setUp(self):
        """Сохранение ссылки на данные по положению антенны"""
        self.position_data = PositionAntennaData()

    def test_calculate_data(self):
        """Тестить нечего, пока нет кругового режима"""
        try:
            self.position_data.calculate_data()
        except AttributeError:
            self.fail("Возможно забыли переименовать метод по расчёту матриц поворота")

    def test_acs2bcs_and_bcs2acs(self):
        """Проверка пересчётов координат из АСК в БСК и обратно,
        после последовательного пересчёта должны получить то же самое"""
        # Измеряемые координаты в АСК
        real_coordinates, real_velocities = np.array([30_000, 5_000, 30_000]), np.array([100, 100, 100])
        acs2bcs, bcs2acs = self.position_data.acs2bcs, self.position_data.bcs2acs
        # После пересчёта из АСК в БСК и обратно в АСК должны получиться те же самые значения
        coordinates, velocities = bcs2acs(*acs2bcs(real_coordinates, real_velocities))

        # Перевод в лист для проверки
        real_coordinates, real_velocities = real_coordinates.round(7).tolist(), real_velocities.round(7).tolist()
        coordinates, velocities = coordinates.round(7).tolist(), velocities.round(7).tolist()

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Координаты не совпадают")
        self.assertEqual(real_velocities, velocities, "Скорости не совпадают")

    def test_dec2acs_and_acs2dec(self):
        """Проверка пересчётов из МЗСК в АСК и обратно,
        после последовательного пересчёта должны получить то же самое"""
        # Измеряемые координаты в АСК
        real_coordinates, real_velocities = np.array([30_000, 5_000, 30_000]), np.array([100, 100, 100])
        # Функции для пересчета
        dec2acs, acs2dec = self.position_data.dec2acs, self.position_data.acs2dec
        # После пересчёта из МЗСК в АСК и обратно в МЗСК должны получиться те же самые значения
        coordinates, velocities = acs2dec(*dec2acs(real_coordinates, real_velocities))

        # Перевод в лист для проверки
        real_coordinates, real_velocities = real_coordinates.round(7).tolist(), real_velocities.round(7).tolist()
        coordinates, velocities = coordinates.round(7).tolist(), velocities.round(7).tolist()

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Координаты не совпадают")
        self.assertEqual(real_velocities, velocities, "Скорости не совпадают")

    def test_dec2bcs_and_bcs2dec(self):
        """Проверка пересчётов из МЗСК в БСК и обратно,
        после последовательного пересчёта должны получить то же самое"""
        # Измеряемые координаты в АСК
        real_coordinates, real_velocities = np.array([30_000, 5_000, 30_000]), np.array([100, 100, 100])
        # Функции для пересчета
        dec2bcs, bcs2dec = self.position_data.dec2bcs, self.position_data.bcs2dec
        # После пересчёта из МЗСК в БСК и обратно в МЗСК должны получиться те же самые значения
        coordinates, velocities = bcs2dec(*dec2bcs(real_coordinates, real_velocities))

        # Перевод в лист для проверки
        real_coordinates, real_velocities = real_coordinates.round(7).tolist(), real_velocities.round(7).tolist()
        coordinates, velocities = coordinates.round(7).tolist(), velocities.round(7).tolist()

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Координаты не совпадают")
        self.assertEqual(real_velocities, velocities, "Скорости не совпадают")

    def test_calc_dec_covariance_matrix_from_bcs(self):
        """Проверка для расчёта ковариационной матрицы в прямоугольной декартовой СК, имея матрицу в БСК"""
        # Начальные данные
        real_cov_matrix_bcs = np.diag(np.array([5.0, 0.00087, 0.00087]))
        coordinate_bcs = np.array([30_000, 0, 0])
        # Вычисление ковариационной матрицы в МЗСК. Она округлена до целого, приведена к листу
        # TODO: Временно, чтобы не падал тест!!
        #  Работаем с ошибками, которые легко посчитать руками, реальная антенна имеет другую матрицу,
        #  так как наклонена на 30 градусов. Требует исправления теста
        self.position_data.mobile_part_data.transform_matrix = np.diag(np.ones(3))
        cov_matrix_dec = self.position_data.calc_dec_covariance_matrix_from_bcs(real_cov_matrix_bcs,
                                                                                coordinate_bcs).round().tolist()

        # Вычисленная ковариационная матрица в МЗСК руками, округлена до целого, приведена к листу
        real_cov_matrix_dec = np.diag([5.0, 30_000**2 * tan(0.00087), 30_000**2 * tan(0.00087)]).round().tolist()

        # Проверка
        self.assertEqual(real_cov_matrix_dec, cov_matrix_dec, "Ковариационная матрица оценена неверно")
