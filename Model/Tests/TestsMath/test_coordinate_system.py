from math import pi, sqrt
from unittest import TestCase

import numpy as np

from coordinate_system_math import dec2sph, sph2dec


class TestCoordinateSystemMath(TestCase):
    def test_dec2sph(self) -> None:
        """Проверка корректности пересчёта из прямоугольной декартовой СК в сферическую СК

        :return: None
        """
        # Определим нужные для функции данные
        coordinate_dec = np.array([sqrt(2) * 2_500, sqrt(3) * 5_000/3, sqrt(2) * 2_500])

        # Оценка с помощью тестируемой функции
        coordinate_sph = dec2sph(coordinate_dec)

        # Проверка для координат в сферической СК
        coordinate_sph = coordinate_sph.tolist()
        real_coordinate_sph = [5000 * sqrt(4/3), pi/4, pi/6]
        self.assertEqual(real_coordinate_sph, coordinate_sph, "Неверный расчёт координат в сферической СК")

    def test_sph2dec(self) -> None:
        """Проверка корректности пересчёта из сферической СК в прямоугольную декартовую СК

        :return: None
        """
        # Определим нужные для функции данные
        coordinate_sph = np.array([10_000, pi, pi/4])

        # Оценка с помощью тестируемой функции
        coordinate_dec = sph2dec(coordinate_sph)

        # Проверка для координат в декартовой прямоугольной СК
        coordinate_dec = coordinate_dec.round(7).tolist()
        real_coordinate_dec = [-7071.0678119, 7071.0678119, 0.]
        self.assertEqual(real_coordinate_dec, coordinate_dec, "Неверный расчёт координат в декартовой прямоугольной СК")

    def test_dec2sph_and_sph2dec(self) -> None:
        """Заключительный тест. После двух последовательных пересчётов должны получиться начальные координаты.

        :return: None
        """
        # Определим нужные для функции данные
        real_coordinate_dec = np.array([1565., 5650., 4540.])

        # Применяем последовательно тестируемые функции пересчёта
        coordinate_sph = dec2sph(real_coordinate_dec)
        coordinate_dec = sph2dec(coordinate_sph)

        # Проверка для последовательного пересчета координат
        coordinate_dec = coordinate_dec.round(7).tolist()
        real_coordinate_dec = [1565., 5650., 4540.]
        self.assertEqual(real_coordinate_dec, coordinate_dec, "После последовательного пересчета координаты изменились")
