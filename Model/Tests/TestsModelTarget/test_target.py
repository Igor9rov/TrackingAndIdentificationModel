from unittest import TestCase

import numpy as np

from target import Target, time_in_tick


class TestTarget(TestCase):
    def setUp(self):
        number = 1
        coordinate = np.array([100000., 5000., 30000.])
        velocity = np.array([-300., -30., 1000.])
        target_type = "Aerodynamic"
        is_anj = {0: False}
        is_autotracking = {0: False}
        self.target = Target(number, coordinate, velocity, target_type, is_autotracking, is_anj)

    # Тест для __init__
    def test___init__(self):
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


