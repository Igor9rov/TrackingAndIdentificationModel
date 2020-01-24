from unittest import TestCase

from estimator_one_bearing_and_other_not_bearing_traces import EstimatorOneBearingAndOtherNotBearingTraces
from estimator_only_head_source_trace import EstimatorOnlyHeadSourceTrace
from estimator_two_bearing_traces import EstimatorTwoBearingTraces
from estimator_two_not_bearing_traces import EstimatorTwoNotBearingTraces
from estimators_fabric import EstimatorsFabric
from source_trace import SourceTrace


class TestEstimatorsFabric(TestCase):
    def setUp(self) -> None:
        """Сохраним ссылку на фабрику, чтобы не плодить кучу лишних объектов

        :return: None
        """
        self.fabric = EstimatorsFabric()

    def test_generate(self) -> None:
        """Тест для генерации нужного типа оценивателя для всех 4 случаев

        :return: None
        """
        # Проверка для случая, когда есть только трасса головного источника
        estimator = self.generate_estimator_only_head_source_trace()
        self.assertEqual(EstimatorOnlyHeadSourceTrace, type(estimator), "Тип оценивателя неверен")

        # Проверка для случая, когда две чистые трассы
        estimator = self.generate_estimator_two_not_bearing_traces()
        self.assertEqual(EstimatorTwoNotBearingTraces, type(estimator), "Тип оценивателя неверен")

        # Проверка для случая, когда две трассы по постановщикам АШП
        estimator = self.generate_estimator_two_bearing_traces()
        self.assertEqual(EstimatorTwoBearingTraces, type(estimator), "Тип оценивателя неверен")

        # Проверка для случая, когда одна трасса по постановщику АШП, а вторая по чистой цели
        estimator = self.generate_estimator_one_bearing_and_other_not_bearing()
        self.assertEqual(EstimatorOneBearingAndOtherNotBearingTraces, type(estimator), "Тип оценивателя неверен")

    def generate_estimator_only_head_source_trace(self) -> EstimatorOnlyHeadSourceTrace:
        """Конструирует оценивателя для случая, когда есть только один источник

        :return: Оцениватель
        :rtype: EstimatorOnlyHeadSourceTrace
        """
        source_trace_list = [SourceTrace()]
        return self.fabric.generate(source_trace_list)

    def generate_estimator_two_not_bearing_traces(self) -> EstimatorTwoNotBearingTraces:
        """Конструирует оценивателя для случая, когда есть две трассы по постановщику АШП

        :return: Оцениватель
        :rtype: EstimatorTwoNotBearingTraces
        """
        source_trace_list = [SourceTrace(), SourceTrace()]
        return self.fabric.generate(source_trace_list)

    def generate_estimator_two_bearing_traces(self) -> EstimatorTwoBearingTraces:
        """Конструирует оценивателя для случая, когда есть две трассы чистой цели

        :return: Оцениватель
        :rtype: EstimatorTwoBearingTraces
        """
        first_trace = SourceTrace()
        second_trace = SourceTrace()

        first_trace.is_bearing = second_trace.is_bearing = True

        source_trace_list = [first_trace, second_trace]
        return self.fabric.generate(source_trace_list)

    def generate_estimator_one_bearing_and_other_not_bearing(self) -> EstimatorOneBearingAndOtherNotBearingTraces:
        """Конструирует оценивателя для случая, когда есть две трассы: одна по постановщику АШП, другая по чистой цели

        :return: Оцениватель
        :rtype: EstimatorOneBearingAndOtherNotBearingTraces
        """
        first_trace = SourceTrace()
        second_trace = SourceTrace()

        first_trace.is_bearing = False
        second_trace.is_bearing = True

        source_trace_list = [first_trace, second_trace]
        return self.fabric.generate(source_trace_list)
