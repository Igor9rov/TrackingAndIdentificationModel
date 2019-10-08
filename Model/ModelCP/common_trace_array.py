from cta_trace import CTATrace
from source_trace import SourceTrace
from source_trace_list import SourceTraceList


# Класс, описывающий работу ЕМТ, наследуется от обычного списка
class CommonTraceArray(list):
    # Инициализация обычным списком
    def __init__(self, initial_list):
        super().__init__(initial_list)

    # Формирование единого массива трасс
    def formation(self, source_trace_list: SourceTraceList):
        # Отождествление трасс источников
        self.identification(source_trace_list)
        # Сортировка источников в трассах ЕМТ
        self.sort_sources_in_cta_traces()
        # Исключение дублирующихся трасс
        self.replicate_trace_excluding()
        # Формирование оценок в трассах ЕМТ
        self.calculate_data_in_cta_traces()

    # Отождествление трасс источников с трассами ЕМТ
    def identification(self, source_trace_list: SourceTraceList):
        # Проходимся по всем трассам в массиве источников трасс
        for source_trace in source_trace_list:
            # Если трасса не присутствует в ЕМТ, то отождествляем её со всеми остальными трассами ЕМТ
            if not source_trace.is_in_common_trace_array:
                self.identification_with_others_cta_traces_for_new_source_trace(source_trace)
            # Если трасса дополнительного источника, то отождествляем её с головным по той же трассе ЕМТ
            elif not source_trace.is_head_source:
                self.identification_with_head_source_trace_for_additional_source_trace(source_trace)

    # Отождествление новой трассы источника с остальными трассами ЕМТ
    def identification_with_others_cta_traces_for_new_source_trace(self, new_source_trace: SourceTrace):
        # Очищаем вспомогательный словарь для хранения трасс ЕМТ, с которыми отождествились
        new_source_trace.clear_identified_number_cta_trace_dict()
        for cta_trace in self:
            # Если нужно отождествить, то отождествляем
            if cta_trace.must_identify_with_source_trace(new_source_trace):
                new_source_trace.identification_with_trace(cta_trace.head_source_trace)
        # Если трасса отождествилась хотя бы с одной трассой ЕМТ
        if new_source_trace.identified_number_cta_trace_dict:
            # Добавление в трассу ЕМТ дополнительного иоточника
            self.append_new_additional_source_trace_in_cta_trace(new_source_trace)
        # Если ни с какой трассой из ЕМТ не отождествилось, то добавляем трассу как новую трассу ЕМТ
        else:
            # Добавляем трассу в ЕМТ
            self.append(new_source_trace)

    # Добавление в трассу ЕМТ дополнительного источника
    def append_new_additional_source_trace_in_cta_trace(self, new_additional_source_trace: SourceTrace):
        # Индекс трассы ЕМТ с минимальным расстоянием
        index_min_range = new_additional_source_trace.num_cta_trace_with_min_distance
        # Трасса ЕМТ с минимальным расстоянием
        min_distance_cta_trace = self[index_min_range]
        # Добавление наиболее близкой трассы из всех отождествившихся в массив дополнительных трасс ЕМТ
        min_distance_cta_trace.add_new_source_trace(new_additional_source_trace)

    # Отождествление трассы дополнительного источника с трассой головного источника по той же трассе ЕМТ
    def identification_with_head_source_trace_for_additional_source_trace(self, additional_source_trace: SourceTrace):
        # Очищаем вспомогательный словарь для хранения трасс ЕМТ, с которыми отождествились
        additional_source_trace.clear_identified_number_cta_trace_dict()
        # Трасса ЕМТ, с которой работает эта трасса источника
        cta_trace: CTATrace = self[additional_source_trace.cta_number]
        additional_source_trace.identification_with_trace(cta_trace.head_source_trace)
        # Если если трасса дополнительного источника не отождествилась с трассой головного источника
        if not additional_source_trace.identified_number_cta_trace_dict:
            # Удаляем трассу этого источника из дополнительных
            cta_trace.del_additional_source_trace(additional_source_trace)
            # Добавляем трассу в ЕМТ
            self.append(additional_source_trace)

    # Сортировка источников в трассах ЕМТ
    def sort_sources_in_cta_traces(self):
        for cta_trace in self:
            cta_trace.sort_sources()

    # Исключение дублирующихся трасс
    def replicate_trace_excluding(self):
        # Цикл по всем трассам в ЕМТ
        for cta_trace in self:
            self.identification_with_others_cta_traces_for_cta_trace(cta_trace)

    # Отождествление трассы ЕМТ с другими трассами ЕМТ
    def identification_with_others_cta_traces_for_cta_trace(self, identifying_cta_trace: CTATrace):
        # Трасса головного источника отождествляемой трассы ЕМТ
        identifying_head_source_trace: SourceTrace = identifying_cta_trace.head_source_trace
        # Вспомогательный массив для хранения трасс ЕМТ, с которыми отождествились
        identifying_head_source_trace.clear_identified_number_cta_trace_dict()
        for cta_trace in self:
            if cta_trace.must_identify_with_cta_trace(identifying_cta_trace):
                identifying_head_source_trace.identification_with_trace(cta_trace.head_source_trace)
        # Создаём список номеров трасс, с которыми отождествились
        identified_traces_numbers = identifying_head_source_trace.identified_cta_trace_numbers
        # Если список номеров не пуст
        if identified_traces_numbers:
            # Добавляем в этот список номер трассы ЕМТ, с которой отождествлялись все остальные
            identified_traces_numbers.append(identifying_cta_trace.number)
            # Удаление из ЕМТ всех менее точных трасс по указанным номерам
            self.remove_less_accuracy_cta_traces_with_numbers(identified_traces_numbers)

    # Удаление менее точных трасс ЕМТ с указаннами номерами
    def remove_less_accuracy_cta_traces_with_numbers(self, identified_traces_numbers: list):
        # Объединение в один лист всех трасс ЕМТ с указанными номерами
        identified_traces = [self[number] for number in identified_traces_numbers]
        # Сортировка трасс ЕМТ
        sorted_identified_traces = self.get_sorted_traces(identified_traces)
        # Удаление всех менее точных трасс из ЕМТ
        self.remove_all_less_accuracy_traces(sorted_identified_traces)

    # Сортировка трасс: сначала по пеленгу, потом по АС/ТС, далее по времени оценки координат
    @staticmethod
    def get_sorted_traces(traces: list):
        # Функция для сортировки
        def sort_func(cta_trace: CTATrace):
            head_trace: SourceTrace = cta_trace.head_source_trace
            return not head_trace.is_bearing, head_trace.is_auto_tracking, head_trace.estimate_tick
        # Сортируем список трасс по точности
        return sorted(traces, key=sort_func, reverse=True)

    # Удаление всех менее точных трасс из ЕМТ
    def remove_all_less_accuracy_traces(self, identified_traces: list):
        for cta_trace in identified_traces[1:]:
            self.remove(cta_trace)

    # Вычисление данных в трассах ЕМТ (координаты и скорость, мб что-то ещё)
    def calculate_data_in_cta_traces(self):
        for cta_trace in self:
            cta_trace.calculate_self_data()

    # Обновление номеров трасс ЕМТ
    def update_numbers_in_cta_traces(self):
        # Изменение номера трасс в ЕМТ и у всех трасс источников на индекс трассы ЕМТ
        for cta_trace in self:
            cta_trace.change_numbers(self.index(cta_trace))

    # Добавление трассы в ЕМТ
    def append(self, trace: SourceTrace):
        # Создаём новую трассу ЕМТ
        new_cta_trace = CTATrace(head_source_trace=trace)
        # Добавляем в ЕМТ
        super().append(new_cta_trace)
        # Даём новой трассе новый номер
        new_cta_trace.number = self.index(new_cta_trace)
        # Добавляем информацию и номер трассы ЕМТ в трассу источника
        trace.append_cta_info_and_number(num=new_cta_trace.number, is_head=True)

    # Удаление трассы из ЕМТ
    def remove(self, cta_trace: CTATrace):
        # Удаляем все признаки присутствия в ЕМТ у трасс источников
        cta_trace.delete_sources_traces()
        # Удаляем трассу из ЕМТ
        super().remove(cta_trace)
        # Обновление номеров всех оставшихся трасс
        self.update_numbers_in_cta_traces()
