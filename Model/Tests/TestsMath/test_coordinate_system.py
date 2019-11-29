from unittest import TestCase

import numpy as np
from math import pi, sqrt
from coordinate_system_math import dec2sph, sph2dec


class TestCoordinateSystemMath(TestCase):
    def test_dec2sph(self):
        """Проверка корректности пересчёта из прямоугольной декартовой СК в сферическую СК

        :return: None
        """
        # Координаты в прямоугольной декартовой СК
        coordinate_dec = np.array([sqrt(2) * 2_500,
                                   sqrt(3) * 5_000 / 3,
                                   sqrt(2) * 2_500])
        # Оценка координат в сферической СК
        real_coordinate_sph = np.array([5000 * sqrt(4/3),
                                        pi / 4,
                                        pi / 6])
        # Оценка с помощью функции
        coordinate_sph = dec2sph(coordinate_dec)

        # Проверка
        self.assertEqual(real_coordinate_sph.tolist(), coordinate_sph.tolist())

    def test_sph2dec(self):
        """Проверка корректности пересчёта из сферической СК в прямоугольную декартовую СК

        :return: None
        """
        # Координаты в сферической СК
        coordinate_sph = np.array([10_000,
                                   pi,
                                   pi / 4])
        # Оценка координат в прямоугольной декартовой СК
        real_coordinate_dec = np.array([-sqrt(2) * 5000,
                                        sqrt(2) * 5000,
                                        0])
        # Оценка с помощью функции
        coordinate_dec = sph2dec(coordinate_sph)

        # Проверка
        self.assertEqual(real_coordinate_dec.round(7).tolist(), coordinate_dec.round(7).tolist())

    def test_dec2sph_and_sph2dec(self):
        """Заключительный тест. После двух последовательных пересчётов должны получиться начальные координаты.

        :return: None
        """
        # Декартовые координаты
        real_coordinate_dec = np.array([1565., 5650., 4540.])

        # Применяем последовательно функции пересчёта
        coordinate_sph = dec2sph(real_coordinate_dec)
        coordinate_dec = sph2dec(coordinate_sph)

        # Проверка
        self.assertEqual(real_coordinate_dec.tolist(), coordinate_dec.round(7).tolist())
