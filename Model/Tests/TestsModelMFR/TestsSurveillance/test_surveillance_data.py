from unittest import TestCase

import numpy as np

from surveillance_data import SurveillanceData


class TestSurveillanceData(TestCase):
    def setUp(self):
        # Собственные данные обзора
        self.surveillance_data = SurveillanceData()

    # Проверять здесь нечего, здесь только вызов из другого класса, проверим что его не забыли переименовать
    def test_calculate_position_antenna_data(self):
        try:
            self.surveillance_data.calculate_position_antenna_data()
        except AttributeError:
            self.fail("Выброшено исключение AttributeError, возможно забыли переименовать метод")

    # Тест проверки на возможность споровождения
    def test_validate_tracking(self):
        # Не можем сопровождать цель из-за некорректного азимута
        first_coordinates = np.array([1000, 5000, 30000])
        can_tracking_first_target = self.surveillance_data.validate_tracking(first_coordinates)
        self.assertFalse(can_tracking_first_target)
        # Не можем сопровождать цель из-за некорректного угла места
        second_coordinates = np.array([1000, 10000, 1000])
        can_tracking_first_target = self.surveillance_data.validate_tracking(second_coordinates)
        self.assertFalse(can_tracking_first_target)
        # Можем сопровождать цель
        third_coordinates = np.array([30000, 5000, 30000])
        can_tracking_first_target = self.surveillance_data.validate_tracking(third_coordinates)
        self.assertTrue(can_tracking_first_target)
