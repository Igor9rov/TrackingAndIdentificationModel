from cta_trace import CTATrace
from source_trace import SourceTrace
from source_trace_list import SourceTraceList


class CommonTraceArray(list):
    """Класс, описывающий работу ЕМТ, наследуется от обычного списка"""
    def __init__(self, initial_list: list):
        """Инициализация обычным списком

        :param initial_list: Список ЕМТ трасс
        :type initial_list: list
        """
        super().__init__(initial_list)

    def formation(self, source_trace_list: SourceTraceList):
        """Формирование единого массива трасс

        :param source_trace_list: Массив трасс источников
        :type source_trace_list: SourceTraceList

        :return: None
        """
        # Отождествление трасс источников
        self.identification(source_trace_list)
        # Сортировка источников в трассах ЕМТ
        self.sort_sources_in_cta_traces()
        # Исключение дублирующихся трасс
        self.replicate_trace_excluding()
        # Формирование оценок в трассах ЕМТ
        self.calculate_data_in_cta_traces()

    def identification(self, source_trace_list: SourceTraceList):
        """Отождествление трасс источников с трассами ЕМТ

        :param source_trace_list: Массив трасс источников
        :type source_trace_list: SourceTraceList

        :return: None
        """
        # Проходимся по всем трассам в массиве источников трасс
        for source_trace in source_trace_list:
            source_trace: SourceTrace
            # Если трасса не присутствует в ЕМТ, то отождествляем её со всеми остальными трассами ЕМТ
            if not source_trace.is_in_common_trace_array:
                self.identification_with_others_cta_traces_for_new_source_trace(source_trace)
            # Если трасса дополнительного источника, то отождествляем её с головным по той же трассе ЕМТ
            elif not source_trace.is_head_source:
                self.identification_with_head_source_trace_for_additional_source_trace(source_trace)

    def identification_with_others_cta_traces_for_new_source_trace(self, new_source_trace: SourceTrace):
        """Отождествление новой трассы источника с остальными трассами ЕМТ

        :param new_source_trace: Новая трасса источника
        :type new_source_trace: SourceTrace

        :return: None
        """
        # Очищаем вспомогательный словарь для хранения трасс ЕМТ, с которыми отождествились
        new_source_trace.clear_identified_number_cta_trace_dict()
        for cta_trace in self:
            cta_trace: CTATrace
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

    def append_new_additional_source_trace_in_cta_trace(self, new_additional_source_trace: SourceTrace):
        """Добавление в трассу ЕМТ дополнительного источника

        :param new_additional_source_trace: Трасса нового дополнительного источника
        :type new_additional_source_trace: SourceTrace

        :return: None
        """
        # Индекс трассы ЕМТ с минимальным расстоянием
        index_min_range = new_additional_source_trace.num_cta_trace_with_min_distance
        # Трасса ЕМТ с минимальным расстоянием
        min_distance_cta_trace = self[index_min_range]
        # Добавление наиболее близкой трассы из всех отождествившихся в массив дополнительных трасс ЕМТ
        min_distance_cta_trace.add_new_source_trace(new_additional_source_trace)

    def identification_with_head_source_trace_for_additional_source_trace(self, additional_source_trace: SourceTrace):
        """Отождествление трассы дополнительного источника с трассой головного источника по той же трассе ЕМТ

        :param additional_source_trace: Трасса дополнительного источника
        :type additional_source_trace: SourceTrace

        :return: None
        """
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

    def sort_sources_in_cta_traces(self):
        """Сортировка источников в трассах ЕМТ

        :return: None
        """
        for cta_trace in self:
            cta_trace: CTATrace
            cta_trace.sort_sources()

    def replicate_trace_excluding(self):
        """Исключение дублирующихся трасс

        :return: None
        """
        # Цикл по всем трассам в ЕМТ
        for cta_trace in self:
            cta_trace: CTATrace
            self.identification_with_others_cta_traces_for_cta_trace(cta_trace)

    def identification_with_others_cta_traces_for_cta_trace(self, identifying_cta_trace: CTATrace):
        """Отождествление трассы ЕМТ с другими трассами ЕМТ

        :param identifying_cta_trace: Трасса ЕМТ, с которой будет отождествляться остальные трасса
        :type identifying_cta_trace: CTATrace

        :return: None
        """
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

    def remove_less_accuracy_cta_traces_with_numbers(self, identified_traces_numbers: list):
        """Удаление менее точных трасс ЕМТ с указаннами номерами

        :param identified_traces_numbers: Номера трасс, с которыми произошло отождествление
        :type identified_traces_numbers: list

        :return: None
        """
        # Объединение в один лист всех трасс ЕМТ с указанными номерами
        identified_traces = [self[number] for number in identified_traces_numbers]
        # Сортировка трасс ЕМТ
        sorted_identified_traces = self.get_sorted_traces(identified_traces)
        # Удаление всех менее точных трасс из ЕМТ
        self.remove_all_less_accuracy_traces(sorted_identified_traces)

    @staticmethod
    def get_sorted_traces(traces: list) -> list:
        """Сортировка трасс: сначала по пеленгу, потом по АС/ТС, далее по времени оценки координат

        :param traces: Список с трассами
        :type traces: list

        :return: Отсортированнная копия списка трасс ЕМТ
        :rtype: list
        """
        # Сортируем список трасс по точности
        return sorted(traces, key=CommonTraceArray.sort__key_function, reverse=True)

    @staticmethod
    def sort__key_function(cta_trace: CTATrace):
        """Функция для сортировки, применяется к каждой трассе ЕМТ, от неё нужна трасса головного источника

        :return: Признаки в порядке убывания важности: признак пеленга, признак АС, время оценки координат
        """
        head_trace: SourceTrace = cta_trace.head_source_trace
        return not head_trace.is_bearing, head_trace.is_auto_tracking, head_trace.estimate_tick

    def remove_all_less_accuracy_traces(self, identified_traces: list):
        """Удаление всех менее точных трасс из ЕМТ

        :param identified_traces: Список с отождествившимися трассами
        :type identified_traces: list

        :return: None
        """
        for cta_trace in identified_traces[1:]:
            self.remove(cta_trace)

    def calculate_data_in_cta_traces(self):
        """Вычисление данных в трассах ЕМТ (координаты и скорость, мб что-то ещё)

        :return: None
        """
        for cta_trace in self:
            cta_trace.calculate_self_data()

    def update_numbers_in_cta_traces(self):
        """Обновление номеров трасс ЕМТ
        Изменение номера трасс в ЕМТ и у всех трасс источников на индекс трассы ЕМТ

        :return: None
        """
        for cta_trace in self:
            cta_trace: CTATrace
            cta_trace.change_numbers(self.index(cta_trace))

    def append(self, trace: SourceTrace):
        """Добавление трассы в ЕМТ

        :param trace: Трасса ЕМТ, которую необходимо добавить
        :type trace: SourceTrace

        :return: None
        """
        # Создаём новую трассу ЕМТ
        new_cta_trace = CTATrace(head_source_trace=trace)
        # Добавляем в ЕМТ
        super().append(new_cta_trace)
        # Даём новой трассе новый номер
        new_cta_trace.number = self.index(new_cta_trace)
        # Добавляем информацию и номер трассы ЕМТ в трассу источника
        trace.append_cta_info_and_number(num=new_cta_trace.number, is_head=True)

    def remove(self, cta_trace: CTATrace):
        """Удаление трассы из ЕМТ

        :param cta_trace: Трасса ЕМТ, которую необходимо удалить
        :type cta_trace: CTATrace

        :return: None
        """
        # Удаляем все признаки присутствия в ЕМТ у трасс источников
        cta_trace.delete_sources_traces()
        # Удаляем трассу из ЕМТ
        super().remove(cta_trace)
        # Обновление номеров всех оставшихся трасс
        self.update_numbers_in_cta_traces()
