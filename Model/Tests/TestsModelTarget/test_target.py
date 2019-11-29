from unittest import TestCase

import numpy as np

from target import Target


class TestTarget(TestCase):
    def setUp(self):
        """Сохраняем ссылку на цель"""
        self.target = Target(coordinates=np.array([100_000., 5_000., 30_000.]),
                             velocities=np.array([-100., -100., 100.]))

    def test___init__(self):
        """Проверяет правильность установки значений по-умолчанию

        :return: None
        """
        target = Target()
        self.assertEqual(0, target.ticks, "Начальное значение времени не ноль")
        self.assertEqual({0: False}, target.is_auto_tracking, "По-умолчанию выставлен не правильный словарь")
        self.assertEqual({0: False}, target.is_anj, "По-умолчанию выставлен не правильный словарь")

    def test_operate(self):
        """Тест для основноого алгоритма работы

        :return: None
        """
        # Прошло столько тиков
        ticks = 100
        # Реальные координаты после стольки тиков
        real_coordinate = np.array([99_500., 4_500., 30_500.])
        # Вызов operate
        for tick in range(ticks):
            self.target.operate(tick)

        self.assertEqual(ticks, self.target.ticks + 1, "Не совпадают временные тики")
        self.assertEqual(real_coordinate.tolist(), self.target.coordinates.tolist(), "Перемещение не совпадает")

    def test_registration(self):
        """Проверка регистрируемых величин

        :return: None
        """
        x, y, z = self.target.coordinates.tolist()
        vx, vy, vz = self.target.velocities.tolist()
        self.assertEqual([x, y, z, vx, vy, vz], self.target.registration, "Не совпала регистрация")
