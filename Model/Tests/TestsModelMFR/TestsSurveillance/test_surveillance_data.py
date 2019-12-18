from unittest import TestCase

import numpy as np

from surveillance_data import SurveillanceData


class TestSurveillanceData(TestCase):
    def setUp(self) -> None:
        """Сохраним ссылку на собственные данные обзора"""
        self.surveillance_data = SurveillanceData()

    def test_validate_tracking(self) -> None:
        """Тест проверки на возможность сопровождения

        :return: None
        """
        # Не можем сопровождать цель из-за некорректного азимута
        self.assertFalse(self.can_tracking_target_with_bad_azimuth())
        # Не можем сопровождать цель из-за некорректного угла места
        self.assertFalse(self.can_tracking_target_with_bad_elevation_angle())
        # Можем сопровождать цель с корректными координатами
        self.assertTrue(self.can_tracking_correct_target())

    def can_tracking_target_with_bad_azimuth(self) -> bool:
        """Проверка на сопровождение цели с некорректным азимутом

        :return: Возможность сопровождения
        :rtype: bool
        """
        coordinates = np.array([1_000, 5_000, 30_000])
        return self.surveillance_data.validate_tracking(coordinates)

    def can_tracking_target_with_bad_elevation_angle(self) -> bool:
        """Проверка на сопровождение координаты с некорректным углом места

        :return: Возможность сопровождения
        :rtype: bool
        """
        coordinates = np.array([1_000, 10_000, 1_000])
        return self.surveillance_data.validate_tracking(coordinates)

    def can_tracking_correct_target(self) -> bool:
        """Проверка на сопровождение корректной координаты

        :return: Возможность сопровождения
        :rtype: bool
        """
        coordinates = np.array([30_000, 5_000, 30_000])
        return self.surveillance_data.validate_tracking(coordinates)
