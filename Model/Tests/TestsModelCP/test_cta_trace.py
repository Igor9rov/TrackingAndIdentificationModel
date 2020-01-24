from unittest import TestCase

import numpy as np

from cta_trace import CTATrace
from source_trace import SourceTrace


class TestCTATrace(TestCase):
    """Тест для класса трассы ЕМТ"""
    def setUp(self) -> None:
        """Сохраняет ссылки на нужные объекты, откатывает их после каждого теста

        :return: None
        """
        self.head_source_trace = SourceTrace(mfr_number=1)
        self.cta_trace = CTATrace(self.head_source_trace)

    def test_get_all_sources_trace(self) -> None:
        """Тест для получения всех трасс источников

        :return: None
        """
        # Подготовка данных для функции
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        # Вызов тестируемой функции
        all_source_traces = self.cta_trace.all_source_traces

        # Проверка для нахождения трассы головного источника в списке
        is_head_source_trace_in_list = self.cta_trace.head_source_trace in all_source_traces
        self.assertTrue(is_head_source_trace_in_list, "Трасса головного источника не в списке")

        # Проверка для нахождения трассы дополнительного источника в списке
        is_add_source_trace_in_list = add_source_trace in all_source_traces
        self.assertTrue(is_add_source_trace_in_list, "Трасса дополнительного источника не в списке")

        # Проверка для длины возващаемого функцией массива
        len_all_source_traces = len(all_source_traces)
        real_len_all_source_traces = 2
        self.assertEqual(real_len_all_source_traces, len_all_source_traces, "Длина списка определена неверно")

    def test_successful_must_identify_with_source_trace(self) -> None:
        """Проверка для возможности отождествления с трассой источника
        Должны получить True для трассы с номером МФР, от которого в трассе ЕМТ нет трассы источника

        :return: None
        """
        # Подготовка данных для функции
        source_trace = SourceTrace(mfr_number=3)

        # Вызов тестируемой функции
        must_identify = self.cta_trace.must_identify_with_source_trace(source_trace)

        # Проверка для необходимости отождествления
        self.assertTrue(must_identify, "Должны были отождествить")

    def test_unsuccessful_must_identify_with_source_trace(self) -> None:
        """Проверка для возможности отождествления с трассой источника
        Должны получить True для трассы с номером МФР, от которого в трассе ЕМТ есть трасса источника

        :return: None
        """
        # Подготовка данных для функции, по такому номеру МФР есть трасса головного источника
        source_trace = SourceTrace(mfr_number=1)

        # Вызов тестируемой функции
        must_identify = self.cta_trace.must_identify_with_source_trace(source_trace)

        # Проверка для необходимости отождествления
        self.assertFalse(must_identify, "Не должны были отождествлять")
        # ______________________________________________________________________________________________________________
        # Проверим, что влияет и наличие дополнительного источника:
        # если в трассе ЕМТ от МФР с таким номером есть трасса, то отождествления происходить не должно
        add_source_trace = SourceTrace(mfr_number=2)
        self.cta_trace.additional_source_trace_array.append(add_source_trace)
        another_source_trace = SourceTrace(mfr_number=2)

        # Вызов тестируемой функции
        must_identify = self.cta_trace.must_identify_with_source_trace(another_source_trace)

        # Проверка для необходимости отождествления
        self.assertFalse(must_identify, "Не должны были отождествлять")

    def test_unsuccessful_must_identify_with_cta_trace(self) -> None:
        """Проверяет возможность отождествления с трассой ЕМТ

        :return: None
        """
        # Подготовка данных для функций
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        identifying_head_source_trace = SourceTrace(mfr_number=4)
        identifying_cta_trace = CTATrace(identifying_head_source_trace)
        identifying_add_source_trace = SourceTrace(mfr_number=1)
        identifying_cta_trace.additional_source_trace_array.append(identifying_add_source_trace)

        # Не должны отождествлять (номера мфр)
        must_identify = self.cta_trace.must_identify_with_cta_trace(identifying_cta_trace)

        # Проверка для возможности отождествления
        self.assertFalse(must_identify)

        identifying_head_source_trace = SourceTrace(mfr_number=4)
        identifying_cta_trace = CTATrace(identifying_head_source_trace)
        identifying_add_source_trace = SourceTrace(mfr_number=3)
        identifying_cta_trace.additional_source_trace_array.append(identifying_add_source_trace)

        # Должны отождествлять
        must_identify = self.cta_trace.must_identify_with_cta_trace(identifying_cta_trace)
        self.assertTrue(must_identify)

    def test_add_new_source_trace(self) -> None:
        """

        :return: None
        """
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        add_source_trace.identified_number_cta_trace_dict = {0.: self.cta_trace.number}

        self.cta_trace.add_new_source_trace(add_source_trace)

        self.assertEqual(1, len(self.cta_trace.additional_source_trace_array))
        self.assertTrue(add_source_trace in self.cta_trace.additional_source_trace_array)

    def test_del_additional_source_trace(self) -> None:
        """

        :return: None
        """
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        self.cta_trace.del_additional_source_trace(add_source_trace)

        self.assertEqual(0, len(self.cta_trace.additional_source_trace_array))
        self.assertFalse(add_source_trace in self.cta_trace.additional_source_trace_array)

    def test_sort_sources(self) -> None:
        """

        :return: None
        """
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        add_source_trace.is_auto_tracking = True
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        # Дполнительный и головной иоточник должны поменяться местами (у доп. АС - он точнее)
        self.cta_trace.sort_sources()

        self.assertTrue(add_source_trace is self.cta_trace.head_source_trace)
        self.assertTrue(self.head_source_trace in self.cta_trace.additional_source_trace_array)

    def test_delete_sources_traces(self) -> None:
        """

        :return: None
        """
        add_source_trace = SourceTrace(mfr_number=2, mfr_position=np.array([100., 34., 43.]))
        self.cta_trace.additional_source_trace_array.append(add_source_trace)

        self.cta_trace.delete_sources_traces()

        self.assertEqual([], self.cta_trace.additional_source_trace_array)
        self.assertIsNone(self.cta_trace.head_source_trace)

    def test_change_numbers(self) -> None:
        """

        :return: None
        """
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
