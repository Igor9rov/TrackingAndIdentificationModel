from unittest import TestCase

from coordinate_system_math import dec2sph, sph2dec


class TestCalculationCovarianceMatrix(TestCase):
    # Проверка пересчётов координат из АСК в БСК и обратно
    def test_dec2sph_and_sph2dec(self):
        # Декартовые координаты
        coordinate_dec = [1, 0, 0]
        # Пересчитываем в сферические
        coordinate_sph = dec2sph(coordinate_dec)
        # Пересчитываем обратно в декартовые
        calc_coordinate_dec = sph2dec(coordinate_sph)

        self.assertEqual(coordinate_dec, calc_coordinate_dec.round(7).tolist())