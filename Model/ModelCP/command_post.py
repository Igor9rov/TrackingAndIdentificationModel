from common_trace_array import CommonTraceArray
from source_trace_list import SourceTraceList


class CommandPost:
    """
    Класс, описывающий работу ПБУ
    """
    __slots__ = ("start_tick",
                 "tick",
                 "tick_period",
                 "mfr_list",
                 "source_trace_list",
                 "common_trace_array")

    def __init__(self, mfr_list: list):
        # Время начала работы ПБУ
        self.start_tick = 0
        # Собственное время в тиках
        self.tick = 0
        # Период работы ПБУ (20 тиков = 1 секунда)
        self.tick_period = 20
        # Массив МФР
        self.mfr_list = mfr_list
        # Массив трасс источников
        self.source_trace_list = SourceTraceList([])
        # Единый массив трасс
        self.common_trace_array = CommonTraceArray([])

    def operate(self, tick: int):
        """
         Основной алгоритм работы
        :param tick: Время в тиках
        :return: None
        """
        # Определение собственного времени
        self.tick = tick - self.start_tick
        # Признак разрешения работы ПБУ (время неотрицательно, темп работы при этом 1 секунда)
        can_operate = not self.tick % self.tick_period and self.tick >= 0
        # Если можно, то ПБУ работает
        if can_operate:
            # Формирование массива трасс источников
            self.formation_source_trace_list()
            # Формирование единого массива трасс
            self.formation_common_trace_array()

    def formation_source_trace_list(self):
        """
        Формирование массива трасс источников
        :return: None
        """
        initial_list = [trace.source_trace for mfr in self.mfr_list for trace in mfr.trace_list]
        self.source_trace_list.formation(initial_list, self.tick)

    def formation_common_trace_array(self):
        """
        Формирование единого массива трасс
        :return: None
        """
        self.common_trace_array.formation(self.source_trace_list)
