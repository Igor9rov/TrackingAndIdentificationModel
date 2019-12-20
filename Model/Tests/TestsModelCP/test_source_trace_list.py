from unittest import TestCase

import numpy as np

from source_trace import SourceTrace
from source_trace_list import SourceTraceList


class TestSourceTraceList(TestCase):
    """Тест для класса массива трасс источников"""
    def setUp(self) -> None:
        """Сохраняет ссылку на объекты, откатывавет их после каждого теста

        :return: None
        """
        mfr_position = np.array([1100., 20., 800])
        self.source_trace = SourceTrace(mfr_number=4, mfr_position=mfr_position)
        initial_list = [self.source_trace]
        self.source_trace_list = SourceTraceList(initial_list)

    def test_update(self) -> None:
        """Тест для обновления массива трасс

        :return: None
        """
        # Подготовка данных для функции
        self.source_trace.coordinates = np.array([20., 40., 12.])
        self.source_trace.velocities = np.array([2., -8., 9.])
        self.source_trace.estimate_tick = 20

        # Вызов тестируемой функции
        self.source_trace_list.update(tick=30)

        # Проверка для координат
        coordinates = self.source_trace.coordinates.tolist()
        real_coordinates = [21., 36., 16.5]
        self.assertEqual(real_coordinates, coordinates)

    def test_formation(self) -> None:
        """Тест для формирования массива трасс источников

        :return: None
        """
        # Подготовка данных для функции
        initial_list = [self.source_trace]

        # Вызов тестируемой функции
        self.source_trace_list.formation(init_list=initial_list, tick=30)

        # Проверка для расположения трассы в МТИ
        is_trace_in_source_trace_list = self.source_trace in self.source_trace_list
        self.assertTrue(is_trace_in_source_trace_list, "Трасса не в составе МТИ")

        # Проверка для длины массива трасс источников
        len_source_trace_list = len(self.source_trace_list)
        real_len_source_trace_list = len(initial_list)
        self.assertEqual(real_len_source_trace_list, len_source_trace_list, "Длина МТИ неверна")

    # TODO: Реализация теста для совместной юстировки
    def test_adjustment(self) -> None:
        """Тестирование совместной юстировки

        :return: None
        """
        pass
