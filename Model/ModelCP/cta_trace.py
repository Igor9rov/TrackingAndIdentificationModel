import numpy as np
from numpy import linalg

from source_trace import SourceTrace


# TODO: Hint: Когда делаешь метод, функцию, etc, старайся добавить тест, так проще отлаживать
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

    # TODO: реализация постобработки, учитывая данные источников
    #  результатом работы этой функции должно быть заполнение полей coordinates, velocities (надо подумать)
    # Получение итоговой оценки координат и скорости для нескольких трасс head и additional
    def calculate_self_data(self):
        if not self.additional_source_trace_array:
            self.common_point_for_one_trace()
        elif len(self.additional_source_trace_array) == 1:
            self.common_point_for_two_traces()
        elif len(self.additional_source_trace_array) == 2:
            pass

    # Расчёт итоговых координат цели для одной точки (head_source_trace)
    def calculate_common_point_for_one_trace(self):
        self.coordinates = self.head_source_trace.coordinates
        self.velocities = self.head_source_trace.velocities

    # Расчёт итоговых координат цели для двух точек
    def calculate_common_point_for_two_traces(self):
        # Введение обозначений для удобства
        trace_1 = self.head_source_trace
        trace_2 = self.additional_source_trace_array[0]
        # Считаем координаты общей точки
        self.coordinates = trace_1.calculate_common_point(trace_2)

    # Поиск триангуляционной точки при одном пеленге
    def calculate_triangular_point_for_jammer_and_target(self):
        # Определяем, какая из трасс трассы ЕМТ есть АШП
        # TODO: Серъёзно?? Смысл сравнивать с булевым выражением булево выражение в блоке if?)
        if self.head_source_trace.is_bearing == False:
            trace_jammer = self.additional_source_trace_array[0]
            trace_target = self.head_source_trace
        else:
            trace_target = self.additional_source_trace_array[0]
            trace_jammer = self.head_source_trace
        # Получаем ковариационная матрица координат чистой цели
        trg_cov_matrix = trace_target.coordinate_covariance_matrix
        # Получаем ковариационная матрица координат АШП
        anj_cov_matrix = trace_jammer.calc_anj_cov_matrix(trace_target)
        # Получаем ковариационная матрица между координатами первой и второй целей
        anj_trg_cov_matrix = trace_jammer.calc_anj_trg_cov_matrix(trace_target)
        # Получаем матрицы коэффициентов для точек положения целей от разных МФР
        # TODO: PyCharm сам подчёркивает "косяки"
        A, B = self.calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, anj_trg_cov_matrix)
        # Расчёт координат и ковариационой маитрицы АШП в случае АШП и чистой цели
        est_anj_coords, est_anj_cov_matrix = trace_jammer.calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(
            trace_target)
        # Расчёт оценки координат триангуляционной точки (мб скорости)
        common_point = A @ est_anj_coords + B @ trace_target.coordinates
        return common_point

    # Расчёт матриц коэффициентов триангуляционной точки
    # TODO: Декоратор статического метода в помощь
    def calculate_coefficient_matrix(self, anj_cov_matrix, trg_cov_matrix, anj_trg_cov_matrix):
        # Ковариационная матрица между координатами второй и первой цели
        trg_anj_cov_matrix = anj_trg_cov_matrix.transpose()
        # Вспомогательные матрицы
        cov_matrix = anj_cov_matrix + trg_cov_matrix - anj_trg_cov_matrix - trg_anj_cov_matrix
        anj_g_matrix = anj_cov_matrix - (trg_anj_cov_matrix + anj_trg_cov_matrix) / 2
        trg_g_matrix = trg_cov_matrix - (trg_anj_cov_matrix + anj_trg_cov_matrix) / 2
        cov_matrix_ = linalg.inv(cov_matrix)
        # Матрица коэффициентов для цели первого МФР
        A = cov_matrix_ @ trg_g_matrix
        # Матрица коэффициентов для цели второго МФР
        B = cov_matrix_ @ anj_g_matrix
        return A, B

    # Расчёт ковариационной матрицы триангуляционной точки
    def calculate_cov_matrix_of_triangular_point_for_jammer_and_target(self):
        # Определяем, какая из трасс трассы ЕМТ есть АШП
        # TODO: Ага..
        if self.head_source_trace.is_bearing == False:
            trace_jammer = self.additional_source_trace_array[0]
            trace_target = self.head_source_trace
        else:
            trace_target = self.additional_source_trace_array[0]
            trace_jammer = self.head_source_trace
        # Получаем ковариационная матрица координат чистой цели
        trg_cov_matrix = trace_target.coordinate_covariance_matrix
        # Получаем ковариационная матрица координат АШП
        anj_cov_matrix = trace_jammer.calc_anj_cov_matrix(trace_target)
        # Получаем ковариационная матрица между координатами первой и второй целей
        ang_trg_cov_matrix = trace_jammer.calc_anj_trg_cov_matrix(trace_target)
        # Получаем матрицы коэффициентов для точек положения целей от разных МФР
        # TODO: PyCharm сам подчёркивает "косяки"
        A, B = self.calculate_coefficient_matrix(anj_cov_matrix, trg_cov_matrix, ang_trg_cov_matrix)
        A_t = A.transpose()
        B_t = B.transpose()
        # Ковариационная матрица триангуляционной точки
        # TODO: Кравивый перенос
        triang_cov_matrix = A @ anj_cov_matrix @ A_t + B @ trg_cov_matrix @ B_t + A @ ang_trg_cov_matrix @ B_t + \
                            (A @ ang_trg_cov_matrix @ B_t).transpose()
        return triang_cov_matrix
