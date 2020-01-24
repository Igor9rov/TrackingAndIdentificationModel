from unittest import TestCase

import numpy as np

from target import Target


class TestTarget(TestCase):
    def setUp(self) -> None:
        """Сохраняем ссылку на цель

        :return: None
        """
        self.target = Target()

    def test___init__without_arguments(self) -> None:
        """Проверяет правильность установки значений инициализатором без аргументов

        :return: None
        """
        # Вызов тестируемой функции
        target = Target()

        # Проверка для собственного времени
        ticks = target.ticks
        real_ticks = 0
        self.assertEqual(real_ticks, ticks, "Собственное время установлено неверно")

        # Проверка для номера цели
        number = target.number
        real_number = -1
        self.assertEqual(real_number, number, "Номер цели установлен неверно")

        # Проверка для координат цели
        coordinates = target.coordinates.tolist()
        real_coordinates = [0., 0., 0.]
        self.assertEqual(real_coordinates, coordinates, "Координаты установлены неверно")

        # Проверка для скоростей цели
        velocities = target.velocities.tolist()
        real_velocities = [0., 0., 0.]
        self.assertEqual(real_velocities, velocities, "Скорости установлены неверно")

        # Проверка для типа цели
        target_type = target.type
        real_target_type = "Aerodynamic"
        self.assertEqual(real_target_type, target_type, "Тип цели установлен неверно")

        # Проверка для признака АС цели
        is_auto_tracking = target.is_auto_tracking
        real_is_auto_tracking = {num: False for num in range(1, 4)}
        self.assertDictEqual(real_is_auto_tracking, is_auto_tracking, "Признак АС установлен неверно")

        # Проверка для признака помехи от цели
        is_anj = target.is_anj
        real_is_anj = {num: False for num in range(1, 4)}
        self.assertDictEqual(real_is_anj, is_anj, "Признак помехи установлен неверно")

    def test___init__with_arguments(self) -> None:
        """Проверяет правильность установки значений инициализатором с аргументами

        :return: None
        """
        # Вызов тестируемой функции
        target = Target(number=1,
                        coordinates=np.array([30_000., 2_000., -2_000.]),
                        velocities=np.array([200., 235., -20]),
                        target_type="Ballistic",
                        is_auto_tracking={1: True},
                        is_anj={1: False})

        # Проверка для собственного времени
        ticks = target.ticks
        real_ticks = 0
        self.assertEqual(real_ticks, ticks, "Собственное время установлено неверно")

        # Проверка для номера цели
        number = target.number
        real_number = 1
        self.assertEqual(real_number, number, "Номер цели установлен неверно")

        # Проверка для координат цели
        coordinates = target.coordinates.tolist()
        real_coordinates = [30_000., 2_000., -2_000.]
        self.assertEqual(real_coordinates, coordinates, "Координаты установлены неверно")

        # Проверка для скоростей цели
        velocities = target.velocities.tolist()
        real_velocities = [200., 235., -20]
        self.assertEqual(real_velocities, velocities, "Скорости установлены неверно")

        # Проверка для типа цели
        target_type = target.type
        real_target_type = "Ballistic"
        self.assertEqual(real_target_type, target_type, "Тип цели установлен неверно")

        # Проверка для признака АС цели
        is_auto_tracking = target.is_auto_tracking
        real_is_auto_tracking = {1: True}
        self.assertDictEqual(real_is_auto_tracking, is_auto_tracking, "Признак АС установлен неверно")

        # Проверка для признака помехи от цели
        is_anj = target.is_anj
        real_is_anj = {1: False}
        self.assertDictEqual(real_is_anj, is_anj, "Признак помехи установлен неверно")

    def test_operate(self) -> None:
        """Тест для основного алгоритма работы

        :return: None
        """
        # Определим нужные для функции данные
        ticks = 100
        self.target.coordinates = np.array([100_000., 5_000., 30_000.])
        self.target.velocities = np.array([-100., -100., 100.])

        # Вызов тестируемой функции
        for tick in range(ticks):
            self.target.operate(tick)

        # Проверка для координат
        coordinates = self.target.coordinates.tolist()
        real_coordinates = [99_500., 4_500., 30_500.]
        self.assertEqual(real_coordinates, coordinates, "Координаты цели не совпадают")

        # Проверка для временных тиков
        target_ticks = self.target.ticks
        real_target_ticks = 99
        self.assertEqual(real_target_ticks, target_ticks, "Не совпадают временные тики")

    def test_registration(self) -> None:
        """Проверка регистрируемых величин

        :return: None
        """
        # Определим нужные для функции данные
        self.target.coordinates = np.array([20_000., 1_000., 2_430.])
        self.target.velocities = np.array([100., 250., -50.])

        # Определение регистрации тестируемой функцией
        registration = self.target.registration

        # Определение регистрации вручную
        real_registration = [20_000., 1_000., 2_430., 100., 250., -50.]

        # Проверка
        self.assertEqual(real_registration, registration, "Не совпала регистрация")
