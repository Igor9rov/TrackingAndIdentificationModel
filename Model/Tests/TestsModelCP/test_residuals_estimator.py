from unittest import TestCase

from residuals_estimator import ResidualsEstimator
from source_trace import SourceTrace


class TestResidualsEstimator(TestCase):
    """Тест для класса , выполняющего расчёт поправок для пары МФР"""
    def setUp(self) -> None:
        """Создаёт ссылки на оцениватель и номера эталонных и юстируемых локаторов

        :return: None
        """
        self.reference_mfr_number = 1
        self.adjustment_mfr_number = 2
        self.estimator = ResidualsEstimator([self.reference_mfr_number, self.adjustment_mfr_number])

    def test__init__(self) -> None:
        """Проверяет начальные значения в инициализаторе

        :return: None
        """
        # Проверка для номера эталонного локатора
        real_reference_mfr_number = self.reference_mfr_number
        reference_mfr_number = self.estimator._ref_num
        self.assertEqual(real_reference_mfr_number, reference_mfr_number, "Номер эталонного локатора задан неверно")

        # Проверка для номера юстируемого локатора
        real_adjustment_mfr_number = self.adjustment_mfr_number
        adjustment_mfr_number = self.estimator._adj_num
        self.assertEqual(real_adjustment_mfr_number, adjustment_mfr_number, "Номер юстируемого локатора задан неверно")

        # Проверка для индекса левой границы массива
        real_starting_count = 5
        starting_count = self.estimator._starting_count
        self.assertEqual(real_starting_count, starting_count, "Индекс левой границы задан неверно")

        # Проверка для индекса правой границы массива
        real_max_len = 35
        max_len = self.estimator._max_len
        self.assertEqual(real_max_len, max_len, "Индекс правой границы массива задан неверно")

        # Проверка для словаря поправок для цели
        real_common_residuals_dict = {}
        common_residuals_dict = self.estimator._common_residuals_dict
        self.assertDictEqual(real_common_residuals_dict, common_residuals_dict, "Словарь с поправками задан неверно")

        # Проверка для признака готовности вычислений
        calculation_ready = self.estimator._calculation_ready
        self.assertFalse(calculation_ready, "Признак готовности вычислений задан неверно")

        # Проверка для поправок
        real_residuals = [0, 0, 0]
        residuals = self.estimator._residuals.tolist()
        self.assertEqual(real_residuals, residuals, "Начальные поправки ненулевые")

        # Проверка для словаря с трассами
        real_traces = {}
        traces = self.estimator._traces
        self.assertDictEqual(real_traces, traces, "Словарь с трассами задан неверно")

    # TODO: Запилить тест
    def test_operate(self) -> None:
        """Тест для основного алгоритма работы

        :return: None
        """
        pass

    def test__create_traces_dict_from(self) -> None:
        """Проверяет правильность построения словаря

        :return: None
        """
        # Определим нужные данные для функции
        trace_from_ref_mfr = SourceTrace(mfr_number=self.reference_mfr_number)
        trace_from_ref_mfr.target_number = 25

        first_trace_from_adj_mfr = SourceTrace(mfr_number=self.adjustment_mfr_number)
        first_trace_from_adj_mfr.target_number = 78

        second_trace_from_adj_mfr = SourceTrace(mfr_number=self.adjustment_mfr_number)
        second_trace_from_adj_mfr.target_number = 58

        not_needed_trace = SourceTrace(mfr_number=3)
        not_needed_trace.target_number = 46

        source_trace_list = [trace_from_ref_mfr, first_trace_from_adj_mfr, second_trace_from_adj_mfr, not_needed_trace]

        # Определим словарь функцией
        self.estimator._create_traces_dict_from(source_trace_list)
        traces = self.estimator._traces

        # Создадим словарь вручную
        real_traces = {self.reference_mfr_number: {trace_from_ref_mfr.target_number: trace_from_ref_mfr},
                       self.adjustment_mfr_number: {first_trace_from_adj_mfr.target_number: first_trace_from_adj_mfr,
                                                    second_trace_from_adj_mfr.target_number: second_trace_from_adj_mfr}}

        # Проверка
        self.assertDictEqual(real_traces, traces, "Словарь определен неверно")

    # TODO: Запилить тест
    def test__calculate_residuals(self) -> None:
        """Проверка для вычисления поправок

        :return: None
        """
        pass
