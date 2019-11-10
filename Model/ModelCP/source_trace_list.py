from source_trace import SourceTrace


class SourceTraceList(list):
    """Класс, определяющий поведение массива трасс источников, наследуется от обычного списка"""
    def __init__(self, initial_list: list):
        """
        :param initial_list: Список трасс от всех источников
        :type initial_list: list
        """
        super().__init__(initial_list)

    def formation(self, init_list: list, tick: int):
        """Формирование массива трасс источников

        :param init_list: Cписок трасс ЕМТ
        :type init_list: list
        :param tick: Текущее время в тиках
        :type tick: int

        :return: None
        """
        self.__init__(init_list)
        self.update(tick)

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
