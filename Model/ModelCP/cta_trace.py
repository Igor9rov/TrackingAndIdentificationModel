import numpy as np

from calc_covariance_matrix import elements_of_covariance_matrix
from estimators_fabric import EstimatorsFabric
from source_trace import SourceTrace


class CTATrace:
    """Класс, описывающий трассу ЕМТ"""
    __slots__ = ("number",
                 "ticks",
                 "coordinates",
                 "velocities",
                 "type",
                 "coordinate_covariance_matrix",
                 "head_source_trace",
                 "additional_source_trace_array")

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

    @property
    def registration(self):
        """Регистрируем номер, координаты, скорость, элементы ковариационной матрицы, количество источников по трассе ЕМТ

        :return: Региструриуемые величины в виде одномерного массива
        """
        return [self.number, *self.coordinates.tolist(), *self.velocities.tolist(),
                *elements_of_covariance_matrix(self.coordinate_covariance_matrix), len(self.all_source_traces)]

    @property
    def all_source_traces(self):
        """
        :return: Список всех трасс источников
        """
        return [self.head_source_trace] + self.additional_source_trace_array

    def must_identify_with_source_trace(self, trace: SourceTrace):
        """Проверяет нужно ли отождествление с этой трассой источника
        Проверка идёт по номером МФР: от одного МФР не отождествляем

        :param trace: Трасса источника - кандидат для отождествления

        :return: Признак нужно ли отождествление (bool)
        """
        return not any(trace.mfr_number == source_trace.mfr_number for source_trace in self.all_source_traces)

    def must_identify_with_cta_trace(self, cta_trace):
        """Проверяет нужно ли отождествление с этой трассой ЕМТ
        Проверка идёт по номером МФР: от одного МФР не отождествляем

        :param cta_trace: Трасса ЕМТ - кандидат на отождествление

        :return: Признак нужно ли отожедствление
        """
        cta_trace: CTATrace
        return not any(self_source_trace.mfr_number == cta_trace_source_trace.mfr_number
                       for self_source_trace in self.all_source_traces
                       for cta_trace_source_trace in cta_trace.all_source_traces)

    def add_new_source_trace(self, source_trace: SourceTrace):
        """Добавление наиболее близкой трассы из всех отождествившихся в массив дополнительных трасс ЕМТ

        :param source_trace: Новый источник по трассе ЕМТ

        :return: None
        """
        # Добавляем информацию от трассе ЕМТ в трассу источника
        source_trace.append_cta_info_and_number(num=self.number, is_head=False)
        # Добавляем трассу источника как дополнительную
        self.additional_source_trace_array.append(source_trace)

    def del_additional_source_trace(self, source_trace: SourceTrace):
        """Удаление дополнительного источника трассы

        :param source_trace: Дополнительная трасса, от которой нужно избавиться

        :return: None
        """
        # Убираем информацию о трассе ЕМТ и номере в трассе источника
        source_trace.delete_cta_info_and_number()
        # Удаляем трассу истояника из состава ЕМТ
        self.additional_source_trace_array.remove(source_trace)

    def sort_sources(self):
        """Сортировка источников трасс, корректировка признаков, головного и дополнительных источников

        :return: None
        """
        # Сначала сортируем по признаку пеленга, потом по АС, далее по времени оценки координат
        all_sorted_source_traces = sorted(self.all_source_traces, key=self.sort_key_function, reverse=True)
        # Запоминаем головную трассу и дополнительные источники
        self.head_source_trace, *self.additional_source_trace_array = all_sorted_source_traces
        # Выставляем признаки головного источника
        self.head_source_trace.is_head_source = True
        for source_trace in self.additional_source_trace_array:
            source_trace.is_head_source = False

    @staticmethod
    def sort_key_function(trace: SourceTrace):
        """Функция для сортировки трасс источников, применяется к каждой трассе истчоника, входящей в трассу ЕМТ

        :param trace: Трасса источника

        :return: В порядке важности признаки сортировки: признак АШП, признак АС, время оценки координат
        """
        return not trace.is_bearing, trace.is_auto_tracking, trace.estimate_tick

    def delete_sources_traces(self):
        """Удаление трасс источников

        :return: None
        """
        for source_trace in self.all_source_traces:
            source_trace.delete_cta_info_and_number()
        self.head_source_trace = None
        self.additional_source_trace_array = []

    def change_numbers(self, num: int):
        """Изменение номера трассы ЕМТ и связанных номеров трасс источников

        :param num: Номер трассы ЕМТ

        :return: None
        """
        self.number = num
        for source_trace in self.all_source_traces:
            source_trace.cta_number = self.number

    def calculate_self_data(self):
        """Получение итоговой оценки координат, скорости и ковариационной матрицы

        :return: None
        """
        estimator = EstimatorsFabric.generate(self.all_source_traces)
        self.coordinates = estimator.coordinates
        self.velocities = estimator.velocities
        self.coordinate_covariance_matrix = estimator.coordinates_covariance_matrix
