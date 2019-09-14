from unittest import TestCase
from common_trace_array import CommonTraceArray
from cta_trace import CTATrace
from source_trace_list import SourceTraceList
from source_trace import SourceTrace
import numpy as np


# TODO: Комменты
# Тест для класса ЕМТ
class TestCommandTraceArray(TestCase):
    def setUp(self) -> None:
        # Собственный ЕМТ
        self.common_trace_array = CommonTraceArray([])
        # Сообщение об ошибке
        self.failure_message = "Что-то пошло не так"

    # Тест формирования ЕМТ
    def test_formation(self):
        # Трасса источника
        head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        # Массив трасс истчоников
        source_trace_list = SourceTraceList([head_source_trace])
        try:
            self.common_trace_array.formation(source_trace_list)
        except AttributeError:
            self.fail(self.failure_message)

    # Тест отождествления трасс источников с трассами ЕМТ
    def test_identification(self):
        # Первая трасса источника
        first_source_trace = SourceTrace(mfr_number=0, mfr_position=np.zeros(3))
        # Добавление её в ЕМТ
        self.common_trace_array.append(first_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]
        # Вторая трасса источника
        # (дополнительный источник по той же трассе ЕМТ, произойдёт успешное отожедствление с головным)
        second_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        second_source_trace.identified_number_cta_trace_dict = {2.74: 0}
        first_cta_trace.add_new_source_trace(second_source_trace)
        # Третья трасса источника (её нет в ЕМТ, не отождествится ни с чем (из-за номера))
        third_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        # Объединение в один список
        source_trace_list = SourceTraceList([first_source_trace, second_source_trace, third_source_trace])

        # После отождествление в ЕМТ две трассы, первая с доп. источником, вторая по третьей трассе
        self.common_trace_array.identification(source_trace_list)

        second_cta_trace: CTATrace = self.common_trace_array[1]

        self.assertEqual(2, len(self.common_trace_array))
        self.assertTrue(second_source_trace in first_cta_trace.additional_source_trace_array)
        self.assertEqual(1, len(first_cta_trace.additional_source_trace_array))
        self.assertTrue(third_source_trace == second_cta_trace.head_source_trace)
        self.assertEqual([], second_cta_trace.additional_source_trace_array)

    # Тест отождествления с другими трассам ЕМТ для новой трассы источника
    def test_identification_with_others_cta_traces_for_new_source_trace(self):
        # Добавляем трассу ЕМТ
        head_source_trace = SourceTrace(mfr_number=0, mfr_position=np.zeros(3))
        self.common_trace_array.append(head_source_trace)
        cta_trace: CTATrace = self.common_trace_array[0]

        # Первая трасса источника (отождествится с трассой ЕМТ)
        first_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))

        # Вторая трасса источника (не отождествится с трассой ЕМТ (один и тот же номер))
        second_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))

        # Третья трасса источника (не отождествится с трассами ЕМТ (по координатам))
        third_source_trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        third_source_trace.coordinates = np.array([40., 3535., 42246.])

        # Успешное отождествление: в трассе ЕМТ дополнительный источник
        self.common_trace_array.identification_with_others_cta_traces_for_new_source_trace(first_source_trace)
        self.assertTrue(first_source_trace in cta_trace.additional_source_trace_array)
        self.assertEqual(1, len(self.common_trace_array))

        # Отождествления не было, в ЕМТ две трассы
        self.common_trace_array.identification_with_others_cta_traces_for_new_source_trace(second_source_trace)
        self.assertEqual(2, len(self.common_trace_array))

        self.common_trace_array.identification_with_others_cta_traces_for_new_source_trace(third_source_trace)
        self.assertEqual(3, len(self.common_trace_array))

    # Тест добавления нового допольнительного источника
    def test_append_new_additional_source_trace_in_cta_trace(self):
        # Первая трасса ЕМТ
        head_source_trace = SourceTrace(mfr_number=0, mfr_position=np.zeros(3))
        self.common_trace_array.append(head_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]
        # Вторая трасса ЕМТ
        head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        self.common_trace_array.append(head_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Добавление трассы дополнительного источника, которая успешно отождествлится с двумя трассами ЕМТ
        added_source_trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        # Отождествление c двумя трассами ЕМТ
        added_source_trace.identified_number_cta_trace_dict = {5.87: 1, 0.: 0}

        self.common_trace_array.append_new_additional_source_trace_in_cta_trace(added_source_trace)

        # Проверим, что у первой трассы появился новый доп. источник
        self.assertTrue(added_source_trace in first_cta_trace.additional_source_trace_array)
        self.assertFalse(added_source_trace in second_cta_trace.additional_source_trace_array)

    # Тест отождествления с головной трассой источника для трассы дополнительного источника
    def test_identification_with_head_source_trace_for_additional_source_trace(self):
        # Трасса ЕМТ
        head_source_trace = SourceTrace(mfr_number=0, mfr_position=np.zeros(3))
        self.common_trace_array.append(head_source_trace)
        cta_trace: CTATrace = self.common_trace_array[0]
        # Добавление трассы дополнительного источника, с которой произойдёт отождествление
        added_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        cta_trace.additional_source_trace_array.append(added_source_trace)

        # Должно произойти успешное отождествление
        self.common_trace_array.identification_with_head_source_trace_for_additional_source_trace(added_source_trace)

        self.assertTrue(added_source_trace in cta_trace.additional_source_trace_array)

        # Добавление трассы дополнительного источника, с которой не произойдёт отождествление
        added_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        added_source_trace.coordinates = np.array([232., 3554., 464.])
        cta_trace.additional_source_trace_array.append(added_source_trace)

        # Не будет успешного отождествления
        self.common_trace_array.identification_with_head_source_trace_for_additional_source_trace(added_source_trace)

        self.assertFalse(added_source_trace in cta_trace.additional_source_trace_array)

    # Тест сортировки трасс иоточников во всех трассах ЕМТ, просто проверка что ничего не упало
    def test_sort_sources_in_cta_traces(self):
        try:
            self.common_trace_array.sort_sources_in_cta_traces()
        except AttributeError:
            self.fail(self.failure_message)

    # Тест исключения дублирующихся трасс, просто проверка что ничего не упало
    def test_replicate_trace_excluding(self):
        try:
            self.common_trace_array.replicate_trace_excluding()
        except AttributeError:
            self.fail(self.failure_message)

    # Тест отождествления трассы ЕМТ с другими трассами ЕМТ
    def test_identification_with_others_cta_traces_for_cta_trace(self):
        # Первая трасса ЕМТ
        first_head_source_trace = SourceTrace(mfr_number=0, mfr_position=np.zeros(3))
        first_head_source_trace.is_auto_tracking = True
        self.common_trace_array.append(first_head_source_trace)

        # Вторая трасса ЕМТ
        second_head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        second_head_source_trace.is_auto_tracking = False
        self.common_trace_array.append(second_head_source_trace)

        # Третья трасса ЕМТ
        third_head_source_trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        third_head_source_trace.coordinates = np.array([40., 3535., 42246.])
        self.common_trace_array.append(third_head_source_trace)

        first_cta_trace: CTATrace = self.common_trace_array[0]
        second_cta_trace: CTATrace = self.common_trace_array[1]
        third_cta_trace: CTATrace = self.common_trace_array[2]

        # Отождествление первой трассы ЕМТ с другими трассами ЕМТ
        self.common_trace_array.identification_with_others_cta_traces_for_cta_trace(first_cta_trace)

        # Должны были отождествиться первая и вторая трассы ЕМТ,
        # Первая и третья должны были остаться
        # Вторая трасса должна была уйти из состава ЕМТ
        self.assertTrue(first_cta_trace in self.common_trace_array)
        self.assertFalse(second_cta_trace in self.common_trace_array)
        self.assertTrue(third_cta_trace in self.common_trace_array)

    # Тест удаления наименее точных трасс с указаннами номерами
    def test_remove_less_accuracy_cta_traces_with_numbers(self):
        # Нулевая трасса, самая точная
        num_first_trace_in_cta = 0
        first_head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        first_head_source_trace.is_auto_tracking = True
        self.common_trace_array.append(first_head_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]

        # Первая трасса, менее точная
        num_second_trace_in_cta = 1
        second_head_source_trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        second_head_source_trace.is_auto_tracking = False
        self.common_trace_array.append(second_head_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Должна была удалиться первая трасса
        self.common_trace_array.remove_less_accuracy_cta_traces_with_numbers([num_first_trace_in_cta,
                                                                              num_second_trace_in_cta])

        self.assertTrue(first_cta_trace in self.common_trace_array)
        self.assertFalse(second_cta_trace in self.common_trace_array)

    def test_get_sorted_traces(self):
        list_source_traces = [SourceTrace(1, np.zeros(3)) for _ in range(8)]
        for trace, index in zip(list_source_traces, range(len(list_source_traces))):
            trace.is_bearing = index <= 3
            trace.is_auto_tracking = index not in [0, 1, 4, 5]
            trace.estimate_tick = index % 2

        list_cta_traces = [CTATrace(source_trace) for source_trace in list_source_traces]

        sorted_list_cta_traces = self.common_trace_array.get_sorted_traces(list_cta_traces)
        list_cta_traces.reverse()
        self.assertEqual(list_cta_traces, sorted_list_cta_traces)

    # Тест удаления всех менее точных трасс из списка
    def test_remove_all_less_accuracy_traces(self):
        # Создание трасс ЕМТ
        first_head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        self.common_trace_array.append(first_head_source_trace)

        second_head_source_trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        self.common_trace_array.append(second_head_source_trace)
        # Длина ЕМТ после удаления
        len_cta_after_remove = 1

        # Удаление всех менее точных трасс из ЕМТ
        identified_traces = list(self.common_trace_array)
        self.common_trace_array.remove_all_less_accuracy_traces(identified_traces)
        self.assertEqual(len_cta_after_remove, len(self.common_trace_array))

    # Тест расчёта данных в трассах ЕМТ, просто проверка, что ничего не упало
    def test_calculate_data_in_cta_traces(self):
        try:
            self.common_trace_array.calculate_data_in_cta_traces()
        except AttributeError:
            self.fail(self.failure_message)

    # Тест обновления номеров в трассах ЕМТ
    def test_update_numbers_in_cta_traces(self):
        # Нулевая трасса ЕМТ
        num_first_trace_in_cta = 0
        first_head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        self.common_trace_array.append(first_head_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]
        # Первая трасса ЕМТ
        num_second_trace_in_cta = 1
        second_head_source_trace = SourceTrace(mfr_number=2, mfr_position=np.zeros(3))
        self.common_trace_array.append(second_head_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Обновление номеров в трассах
        self.common_trace_array.update_numbers_in_cta_traces()

        self.assertEqual(num_first_trace_in_cta, first_cta_trace.number)
        self.assertEqual(num_first_trace_in_cta, first_head_source_trace.cta_number)

        self.assertEqual(num_second_trace_in_cta, second_cta_trace.number)
        self.assertEqual(num_second_trace_in_cta, second_head_source_trace.cta_number)

    # Тест добавления трассы источника как новой трассы ЕМТ
    def test_append(self):
        # Номер трассы ЕМТ
        num_trace_in_cta = 0
        head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        len_before_append = len(self.common_trace_array)

        # Добавление трассы источника как новой трассы ЕМТ
        self.common_trace_array.append(head_source_trace)

        append_counter = 1
        len_after_append = len(self.common_trace_array)
        appended_cta_trace = self.common_trace_array[0]

        self.assertEqual(type(appended_cta_trace), CTATrace)
        self.assertEqual(num_trace_in_cta, appended_cta_trace.number)
        self.assertEqual(append_counter, len_after_append - len_before_append)

    # Тест удаления трассы ЕМТ из состава ЕМТ
    def test_remove(self):
        # Сначала добавим её, чтобы было что удалять
        head_source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))
        self.common_trace_array.append(head_source_trace)
        cta_trace = self.common_trace_array[0]
        len_before_remove = len(self.common_trace_array)

        # Удаляем трассу из ЕМТ
        self.common_trace_array.remove(cta_trace)

        remove_counter = 1
        len_after_remove = len(self.common_trace_array)

        self.assertEqual(remove_counter, len_before_remove - len_after_remove)
