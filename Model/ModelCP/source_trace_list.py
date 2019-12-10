from source_trace import SourceTrace


class SourceTraceList(list):
    """Класс, определяющий поведение массива трасс источников, наследуется от обычного списка"""
    def __init__(self, initial_list: list, adjustment_dict=None):
        """
        :param initial_list: Список трасс от всех источников
        :type initial_list: list
        """
        super().__init__(initial_list)
        if adjustment_dict is None:
            adjustment_dict = {}
        self.adjustment_dict = adjustment_dict

    def formation(self, init_list: list, tick: int):
        """Формирование массива трасс источников

        :param init_list: Cписок трасс ЕМТ
        :type init_list: list
        :param tick: Текущее время в тиках
        :type tick: int

        :return: None
        """
        # Удаление трасс, которых не осталось в списке трасс источников
        for trace in self:
            if trace not in init_list:
                self.remove(trace)

        # Добавление трасс, которых не было на предудыщий тик работы
        for trace in init_list:
            if trace not in self:
                self.append(trace)

        self.update(tick)
        self.adjustment(init_list)

    def update(self, tick: int):
        """Обновление данных трасс иоточников, а именно экстраполяция до единого времени

        :param tick: Текущее время в тиках
        :type tick: int

        :return: None
        """
        for source_trace in self:
            source_trace: SourceTrace
            # Экстраполяция координат
            source_trace.extrapolate_coordinates_to_tick(tick)

    def adjustment(self, traces_list):
        """Совместная юстировка МФР

        :return: None
        """
        for dict_for_pair in self.adjustment_dict.values():
            if not dict_for_pair["ready"]:
                estimator = dict_for_pair["estimator"]
                is_ready = estimator.operate(traces_list)
                if is_ready:
                    dict_for_pair["ready"] = True
                    dict_for_pair["residuals"] = estimator.residuals
