from estimator_one_bearing_and_other_not_bearing_traces import EstimatorOneBearingAndOtherNotBearingTraces
from estimator_only_head_source_trace import EstimatorOnlyHeadSourceTrace
from estimator_two_bearing_traces import EstimatorTwoBearingTraces
from estimator_two_not_bearing_traces import EstimatorTwoNotBearingTraces
from source_trace import SourceTrace


class EstimatorsFabric:
    """
    Фабрика для оценивателей координат, скоростей и ковариационной матрицы трассы ЕМТ
    """
    @classmethod
    def generate(cls, source_trace_list: list):
        """
        :param source_trace_list: Список со всеми трассами источника по трассе ЕМТ

        :return: Оцениватель координат, скоростей и ковариационной матрицы
        """
        head_trace, *other_traces = source_trace_list
        head_trace: SourceTrace
        # Если дополнительных трасс нет
        if not other_traces:
            estimator = EstimatorOnlyHeadSourceTrace(head_trace)
        else:
            add_trace: SourceTrace = other_traces[0]
            # Выбор оценивателя исходя из признака пеленга у каждой трассы
            if head_trace.is_bearing and add_trace.is_bearing:
                estimator = EstimatorTwoBearingTraces(head_trace, add_trace)
            elif not head_trace.is_bearing and not add_trace.is_bearing:
                estimator = EstimatorTwoNotBearingTraces(head_trace, add_trace)
            else:
                estimator = EstimatorOneBearingAndOtherNotBearingTraces(head_trace, add_trace)
        return estimator
