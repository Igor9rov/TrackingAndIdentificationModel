from unittest import TestCase
from target import Target, time_in_tick
import numpy as np


class TestTarget(TestCase):
    def setUp(self):
        number = 1
        coordinate = np.array([100000., 5000., 30000.])
        velocity = np.array([-300., -30., 1000.])
        target_type = "Aerodynamic"
        self.target = Target(number, coordinate, velocity, target_type)

    # Тест для __init__
    def test___init__(self):
        self.assertFalse(self.target.is_anj, "Выставлен признак пеленга равный True")
        self.assertFalse(self.target.is_auto_tracking, "Выставлен признак АС равный True")
        self.assertEqual(0, self.target.ticks, "Начальное значение времени не ноль")

    # Функция для расчёта координат после перемещения
    def get_coordinates_after_ticks(self, ticks):
        return self.target.coordinates + self.target.velocities * ticks * time_in_tick

    # Тест для Operate
    def test_operate(self):
        # Прошло столько тиков
        ticks = 100
        # Реальные координаты после стольки тиков
        real_coordinate = self.get_coordinates_after_ticks(ticks)
        # Вызов operate
        for tick in range(ticks):
            self.target.operate(tick)

        self.assertEqual(ticks, self.target.ticks + 1, "Не совпадают временные тики")
        self.assertEqual(real_coordinate.tolist(), self.target.coordinates.tolist(), "Перемещение не совпадает")


