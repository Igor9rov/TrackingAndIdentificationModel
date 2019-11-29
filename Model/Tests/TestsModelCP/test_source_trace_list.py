from unittest import TestCase

import numpy as np

from source_trace import SourceTrace
from source_trace_list import SourceTraceList


# Тест для класса массива трасс источников
class TestSourceTraceList(TestCase):
    def setUp(self) -> None:
        mfr_position = np.array([1100., 20., 800])
        self.source_trace = SourceTrace(mfr_number=4, mfr_position=mfr_position)
        initial_list = [self.source_trace]
        self.source_trace_list = SourceTraceList(initial_list)

    def test_update(self):
        self.source_trace.coordinates = np.array([20., 40., 12.])
        self.source_trace.velocities = np.array([2., -8., 9.])
        self.source_trace.estimate_tick = 20
        extrapolate_tick = 30
        coordinates = np.array([21., 36., 16.5])

        self.source_trace_list.update(extrapolate_tick)

        self.assertEqual(coordinates.tolist(), self.source_trace_list[0].coordinates.tolist())

    def test_formation(self):
        extrapolate_tick = 30
        initial_list = [self.source_trace]

        self.source_trace_list.formation(initial_list, extrapolate_tick)

        self.assertEqual(self.source_trace, self.source_trace_list[0])
        self.assertEqual(len(initial_list), len(self.source_trace_list))
