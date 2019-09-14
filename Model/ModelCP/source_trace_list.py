# Класс, определяющий поведение массива трасс источников, наследуется от обычного списка
class SourceTraceList(list):
    # Инициализация обычным списком
    def __init__(self, initial_list: list):
        super().__init__(initial_list)

    # Формирование массива трасс источников
    def formation(self, init_list: list, tick: int):
        self.__init__(init_list)
        self.update(tick)

    # Обновление данных трасс иоточников, а именно экстраполяция до единого времени
    def update(self, tick: int):
        for source_trace in self:
            # Экстраполяция координат
            source_trace.extrapolate_coordinates_to_tick(tick)
