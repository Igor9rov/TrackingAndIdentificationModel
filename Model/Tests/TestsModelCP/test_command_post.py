from unittest import TestCase

import numpy as np

from command_post import CommandPost
from cta_trace import CTATrace
from multi_functional_radar import MultiFunctionalRadar
from target import Target


# Тест для ПБУ
class TestCommandPost(TestCase):
    def setUp(self) -> None:
        # Две цели
        is_anj = {1: False, 2: False}
        is_auto_tracking = {1: False, 2: False}
        first_target_coordinates = np.array([100000, 1001, 30000.])
        first_target_velocities = np.array([-50., 0., -60.])
        first_target_type = "Aerodynamic"
        first_target = Target(1, first_target_coordinates, first_target_velocities, first_target_type,
                              is_anj, is_auto_tracking)

        second_target_coordinates = np.array([30000, 5001, 30000.])
        second_target_velocities = np.array([-50., 0., -60.])
        second_target_type = "Aerodynamic"
        second_target = Target(2, second_target_coordinates, second_target_velocities, second_target_type,
                               is_anj, is_auto_tracking)

        # Список целей
        self.target_list = [first_target, second_target]
        # Два локатора
        first_radar = MultiFunctionalRadar(np.array([1001, 0, -780]), 1, self.target_list)
        second_radar = MultiFunctionalRadar(np.array([-1000, 0, 780]), 2, self.target_list)
        # Список локаторов
        self.radar_list = [first_radar, second_radar]
        # Собственный ПБУ
        self.command_post = CommandPost(self.radar_list)
        self.failure_msg = "Что-то пошло не так"

    # Тест основного алгоритма работы
    def test_operate(self):
        # Запуск моделирования с двумя целями, двумя локаторами и ПБУ
        for time in range(1000):
            for target in self.target_list:
                target.operate(time)
            for radar in self.radar_list:
                radar.operate(time)
            try:
                self.command_post.operate(time)
            except AttributeError:
                self.fail(self.failure_msg)

        # Первая трасса ЕМТ
        first_cta_trace: CTATrace = self.command_post.common_trace_array[0]
        # Вторая трасса ЕМТ
        second_cta_trace: CTATrace = self.command_post.common_trace_array[1]

        self.assertEqual(2, len(self.command_post.common_trace_array))
        self.assertIsNotNone(first_cta_trace.additional_source_trace_array)
        self.assertIsNotNone(second_cta_trace.additional_source_trace_array)

    # Тест формирования массива трасс источника, просто проверка что ничего не упало
    def test_formation_source_trace_list(self):
        try:
            self.command_post.formation_source_trace_list()
        except AttributeError:
            self.fail(self.failure_msg)

    # Тест формирования ЕМТ, просто проверка что ничего не упало
    def test_formation_common_trace_array(self):
        try:
            self.command_post.formation_common_trace_array()
        except AttributeError:
            self.fail(self.failure_msg)
