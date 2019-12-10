from common_trace_array import CommonTraceArray
from cta_trace import CTATrace
from multi_functional_radar import MultiFunctionalRadar
from residuals_estimator import ResidualsEstimator
from source_trace_list import SourceTraceList


class CommandPost:
    """Класс, описывающий работу ПБУ"""
    __slots__ = ("start_tick",
                 "tick",
                 "tick_period",
                 "mfr_list",
                 "adjustment_dict",
                 "source_trace_list",
                 "common_trace_array",
                 "registration")

    def __init__(self, mfr_list: list):
        # Время начала работы ПБУ
        self.start_tick = 0
        # Собственное время в тиках
        self.tick = 0
        # Период работы ПБУ (20 тиков = 1 секунда)
        self.tick_period = 20
        # Массив МФР
        self.mfr_list = mfr_list
        # Заполним словарь для юстировки
        self._generate_adjustment_dict()
        # Массив трасс источников
        self.source_trace_list = SourceTraceList([], self.adjustment_dict)
        # Единый массив трасс
        self.common_trace_array = CommonTraceArray([])
        # Массив информации о каждой трассе этого ПБУ
        self.registration = []

    def __repr__(self) -> str:
        return f"ПБУ. В подчинении {len(self.mfr_list)!r} МФР." \
               f"Всего трасс источников {len(self.source_trace_list)!r}, " \
               f"всего трасс ЕМТ {len(self.common_trace_array)!r}. " \
               f"Объект класса {self.__class__.__name__} по адресу в памяти {hex(id(self))}"

    def _generate_adjustment_dict(self):
        self.adjustment_dict = {}
        mfr_numbers = [mfr.number for mfr in self.mfr_list]
        if 1 in mfr_numbers and 2 in mfr_numbers:
            self.adjustment_dict[2] = {"estimator": ResidualsEstimator([1, 2]),
                                       "ready": False,
                                       "residuals": None}

        if 1 in mfr_numbers and 3 in mfr_numbers:
            self.adjustment_dict[3] = {"estimator": ResidualsEstimator([1, 3]),
                                       "ready": False,
                                       "residuals": None}

    def operate(self, tick: int):
        """Основной алгоритм работы

        :param tick: Время в тиках
        :type tick: int

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
            # Оценка поправок от юстировки
            self.analyze_adjustment()
            # Формирование единого массива трасс
            self.formation_common_trace_array()
            # Регистрация работы ПБУ
            self.register()

    def formation_source_trace_list(self):
        """Формирование массива трасс источников

        :return: None
        """
        initial_list = [trace.source_trace for mfr in self.mfr_list for trace in mfr.trace_list]
        self.source_trace_list.formation(initial_list, self.tick)

    def analyze_adjustment(self):
        """Для неотюстированных локаторов устанавливает, если посчитались, поправки

        :return: None
        """
        not_adjustment_mfr = [mfr for mfr in self.mfr_list if not mfr.is_adjustment]
        for mfr in not_adjustment_mfr:
            mfr: MultiFunctionalRadar
            try:
                if self.adjustment_dict[mfr.number]["ready"]:
                    mfr.is_adjustment = True
                    mfr.residuals = self.adjustment_dict[mfr.number]["residuals"]
            except KeyError:
                # Сюда завалимся, если в системе нет МФР №1, а это значит, что никакой юстировки быть не может
                pass

    def formation_common_trace_array(self):
        """Формирование единого массива трасс

        :return: None
        """
        self.common_trace_array.formation(self.source_trace_list)

    def register(self):
        """Регистрация работы ПБУ

        :return: None
        """
        # Цикл по всем трассам ЕМТ
        for cta_trace in self.common_trace_array:
            cta_trace: CTATrace
            # Хотим регистрировать следующее: текущее время и данные трассы ЕМТ
            registration_row = [self.tick, *cta_trace.registration]
            self.registration.append(registration_row)
