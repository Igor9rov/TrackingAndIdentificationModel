import numpy as np

from estimators_fabric import EstimatorsFabric
from source_trace import SourceTrace


# Класс, описывающий трассу ЕМТ, и её методы
class CTATrace:
    def __init__(self, head_source_trace: SourceTrace):
        # Номер трассы
        self.number = 0
        # Текущее время
        self.ticks = 0
        # Координаты
        self.coordinates = np.zeros(3)
        # Скорость
        self.velocities = np.zeros(3)
        # Тип трассы
        self.type = None
        # Ковариационная матрица координат
        self.coordinate_covariance_matrix = np.eye(3)
        # Трасса головного источника
        self.head_source_trace = head_source_trace
        # Массив трасс дополнительных источников
        self.additional_source_trace_array = []

    # Получение списка всех трасс источников
    @property
    def all_source_traces(self):
        return self.additional_source_trace_array + [self.head_source_trace]

    # Проверяет нужно ли отождествление с этой трассой источника
    def must_identify_with_source_trace(self, trace: SourceTrace):
        return not any(trace.mfr_number == source_trace.mfr_number for source_trace in self.all_source_traces)

    # Проверяет нужно ли отождествление с этой трассой ЕМТ
    def must_identify_with_cta_trace(self, cta_trace):
        return not any(self_source_trace.mfr_number == cta_trace_source_trace.mfr_number
                       for self_source_trace in self.all_source_traces
                       for cta_trace_source_trace in cta_trace.all_source_traces)

    # Добавление наиболее близкой трассы из всех отождествившихся в массив дополнительных трасс ЕМТ
    def add_new_source_trace(self, source_trace: SourceTrace):
        # Добавляем информацию от трассе ЕМТ в трассу источника
        source_trace.append_cta_info_and_number(num=self.number, is_head=False)
        # Добавляем трассу источника как дополнительную
        self.additional_source_trace_array.append(source_trace)

    # Удаление дополнительного источника трассы
    def del_additional_source_trace(self, source_trace: SourceTrace):
        # Убираем информацию о трассе ЕМТ и номере в трассе источника
        source_trace.delete_cta_info_and_number()
        # Удаляем трассу истояника из состава ЕМТ
        self.additional_source_trace_array.remove(source_trace)

    # Сортировка источников трасс
    def sort_sources(self):
        # Функция для сортировки
        def sort_func(trace: SourceTrace):
            return not trace.is_bearing, trace.is_auto_tracking, trace.estimate_tick
        # Сначала сортируем по признаку пеленга, потом по АС, далее по времени оценки координат
        all_sorted_source_traces = sorted(self.all_source_traces, key=sort_func, reverse=True)
        # Запоминаем головную трассу и дополнительные источники
        self.head_source_trace, *self.additional_source_trace_array = all_sorted_source_traces
        # Выставляем признаки головного источника
        self.head_source_trace.is_head_source = True
        for source_trace in self.additional_source_trace_array:
            source_trace.is_head_source = False

    # Удаление трасс источников
    def delete_sources_traces(self):
        for source_trace in self.all_source_traces:
            source_trace.delete_cta_info_and_number()
        self.head_source_trace = None
        self.additional_source_trace_array = []

    # Изменение номера трассы ЕМТ и связанных номеров трасс источников
    def change_numbers(self, num):
        self.number = num
        for source_trace in self.all_source_traces:
            source_trace.cta_number = self.number

    # Получение итоговой оценки координат и скорости
    def calculate_self_data(self):
        estimator = EstimatorsFabric.generate(self.all_source_traces)
        self.coordinates = estimator.coordinates
        self.velocities = estimator.velocities
        self.coordinate_covariance_matrix = estimator.coordinates_covariance_matrix
