from unittest import TestCase

import numpy as np
from math import tan

from position_antenna_data import PositionAntennaData


# Тест для класса PositionAntennaData
class TestPositionAntennaData(TestCase):
    def setUp(self):
        self.position_antenna_data = PositionAntennaData()

    # Опять же тестить нечего, здесь простой вызов методов из других классов
    def test_calculate_data(self):
        try:
            self.position_antenna_data.calculate_data()
        except AttributeError:
            self.fail("Возможно забыли переименовать метод по расчёту матриц поворота")

    # Проверка пересчётов координат из АСК в БСК и обратно
    def test_acs2bcs_and_bcs2acs(self):
        # Определим матрицы поворота
        self.position_antenna_data.calculate_data()
        # Измеряемые координаты в АСК
        coordinates, velocities = np.array([30000, 5000, 30000]), np.array([100, 100, 100])
        acs2bcs = self.position_antenna_data.acs2bcs
        bcs2acs = self.position_antenna_data.bcs2acs
        # После пересчёта из АСК в БСК и обратно в АСК должны получиться те же самые значения
        res_coordinates, res_velocities = bcs2acs(*acs2bcs(coordinates, velocities))
        self.assertEqual(res_coordinates.round(7).tolist(), coordinates.round(7).tolist())
        self.assertEqual(res_velocities.round(7).tolist(), velocities.round(7).tolist())

    # Проверка пересчётов из МЗСК в АСК и обратно
    def test_dec2acs_and_acs2dec(self):
        # Определим матрицы поворота
        self.position_antenna_data.calculate_data()
        # Измеряемые координаты в АСК
        coordinates, velocities = np.array([30000, 5000, 30000]), np.array([100, 100, 100])
        dec2acs = self.position_antenna_data.dec2acs
        acs2dec = self.position_antenna_data.acs2dec
        # После пересчёта из МЗСК в АСК и обратно в МЗСК должны получиться те же самые значения
        res_coordinates, res_velocities = acs2dec(*dec2acs(coordinates, velocities))
        self.assertEqual(res_coordinates.round(7).tolist(), coordinates.round(7).tolist())
        self.assertEqual(res_velocities.round(7).tolist(), velocities.round(7).tolist())

    # Проверка пересчётов из МЗСК в БСК и обратно
    def test_dec2bcs_and_bcs2dec(self):
        # Определим матрицы поворота
        self.position_antenna_data.calculate_data()
        # Измеряемые координаты в АСК
        coordinates, velocities = np.array([30000, 5000, 30000]), np.array([100, 100, 100])
        dec2bcs = self.position_antenna_data.dec2bcs
        bcs2dec = self.position_antenna_data.bcs2dec
        # После пересчёта из МЗСК в БСК и обратно в МЗСК должны получиться те же самые значения
        res_coordinates, res_velocities = bcs2dec(*dec2bcs(coordinates, velocities))
        self.assertEqual(res_coordinates.round(7).tolist(), coordinates.round(7).tolist())
        self.assertEqual(res_velocities.round(7).tolist(), velocities.round(7).tolist())

    def test_calc_dec_covariance_matrix_from_bcs(self):
        # По умолчанию матрицы поворота единичные
        # Начальные данные
        covariance_matrix_bcs = np.diag(np.array([5.0, 0.00087, 0.00087]))
        coordinate_bcs = np.array([30000, 0, 0])
        # Вычисленная ковариационная матрица в МЗСК руками
        covariance_matrix_dec = np.diag(np.array([5.0, 30000**2*tan(0.00087), 30000**2*tan(0.00087)]))
        # Вычисление ковариационной матрицы в МЗСК
        calc_dec_matrix = self.position_antenna_data.calc_dec_covariance_matrix_from_bcs
        res_covariance_matrix_dec = calc_dec_matrix(covariance_matrix_bcs, coordinate_bcs)
        # Округлим до целого, не имеет смысла дробная часть в дисперсиях ошибки
        self.assertEqual(covariance_matrix_dec.round().tolist(), res_covariance_matrix_dec.round().tolist())
