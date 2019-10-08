from unittest import TestCase

import numpy as np

from cta_trace import CTATrace
from source_trace import SourceTrace
from numpy import random


# TODO: Комменты
# Тест для класса трассы ЕМТ
class TestCTATrace(TestCase):
    def setUp(self) -> None:
        self.head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        self.cta_trace = CTATrace(self.head_source_trace)

    def test_get_all_sources_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        all_source_traces = self.cta_trace.all_source_traces

        self.assertTrue(self.cta_trace.head_source_trace in all_source_traces)
        self.assertTrue(add_source_trace in all_source_traces)
        self.assertEqual(2, len(all_source_traces))

    def test_must_identify_with_source_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        # Не должны отождествлять (номера мфр)
        another_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        must_identify = self.cta_trace.must_identify_with_source_trace(another_source_trace)
        self.assertFalse(must_identify)

        # Должны отождествлять
        another_source_trace = SourceTrace(mfr_number=3, mfr_position=np.zeros(3))
        must_identify = self.cta_trace.must_identify_with_source_trace(another_source_trace)
        self.assertTrue(must_identify)

    def test_must_identify_with_cta_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        identifying_head_source_trace = SourceTrace(mfr_number=4, mfr_position=np.zeros(3))
        identifying_cta_trace = CTATrace(identifying_head_source_trace)
        identifying_add_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        identifying_cta_trace.additional_source_trace_array.append(identifying_add_source_trace)

        # Не должны отождествлять (номера мфр)
        must_identify = self.cta_trace.must_identify_with_cta_trace(identifying_cta_trace)
        self.assertFalse(must_identify)

        identifying_head_source_trace = SourceTrace(mfr_number=4, mfr_position=np.zeros(3))
        identifying_cta_trace = CTATrace(identifying_head_source_trace)
        identifying_add_source_trace = SourceTrace(mfr_number=3, mfr_position=np.zeros(3))
        identifying_cta_trace.additional_source_trace_array.append(identifying_add_source_trace)

        # Должны отождествлять
        must_identify = self.cta_trace.must_identify_with_cta_trace(identifying_cta_trace)
        self.assertTrue(must_identify)

    def test_add_new_source_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        add_source_trace.identified_number_cta_trace_dict = {0.: self.cta_trace.number}

        self.cta_trace.add_new_source_trace(add_source_trace)

        self.assertEqual(1, len(self.cta_trace.additional_source_trace_array))
        self.assertTrue(add_source_trace in self.cta_trace.additional_source_trace_array)

    def test_del_additional_source_trace(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        self.cta_trace.del_additional_source_trace(add_source_trace)

        self.assertEqual(0, len(self.cta_trace.additional_source_trace_array))
        self.assertFalse(add_source_trace in self.cta_trace.additional_source_trace_array)

    def test_sort_sources(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        add_source_trace.is_auto_tracking = True
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        # Дполнительный и головной иоточник должны поменяться местами (у доп. АС - он точнее)
        self.cta_trace.sort_sources()

        self.assertTrue(add_source_trace is self.cta_trace.head_source_trace)
        self.assertTrue(self.head_source_trace in self.cta_trace.additional_source_trace_array)

    def test_delete_sources_traces(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        self.cta_trace.delete_sources_traces()

        self.assertEqual([], self.cta_trace.additional_source_trace_array)
        self.assertIsNone(self.cta_trace.head_source_trace)

    def test_change_numbers(self):
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)
        changed_num = 89

        self.cta_trace.change_numbers(changed_num)

        self.assertEqual(changed_num, self.cta_trace.number)
        self.assertEqual(changed_num, self.head_source_trace.cta_number)
        self.assertEqual(changed_num, add_source_trace.cta_number)

    # TODO: Добавление реализации теста для calculate_self_data
    def test_calculate_self_data(self):
        pass
