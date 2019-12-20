from unittest import TestCase

import numpy as np

from common_trace_array import CommonTraceArray
from cta_trace import CTATrace
from source_trace import SourceTrace
from source_trace_list import SourceTraceList


class TestCommandTraceArray(TestCase):
    """Тест для класса ЕМТ"""
    def setUp(self) -> None:
        """Сохраняет ссылки на объекты и откатывет их к начальному сосотоянию

        :return: None
        """
        # Собственный ЕМТ
        self.common_trace_array = CommonTraceArray([])
        # Сообщение об ошибке
        self.failure_message = "Что-то пошло не так"

    def test_formation(self) -> None:
        """Тест формирования ЕМТ

        :return: None
        """
        # Подготовка нужных для функции данных
        head_source_trace = SourceTrace()
        source_trace_list = SourceTraceList([head_source_trace])

        # Выполнение тестируемой функции
        try:
            self.common_trace_array.formation(source_trace_list)
        except AttributeError:
            self.fail(self.failure_message)

    def test_identification(self) -> None:
        """Тест отождествления трасс источников с трассами ЕМТ

        :return: None
        """
        # Подготовка нужных для функции данных
        first_source_trace = SourceTrace(mfr_number=0)
        self.common_trace_array.append(first_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]

        # (дополнительный источник по той же трассе ЕМТ, произойдёт успешное отожедствление с головным)
        second_source_trace = SourceTrace(mfr_number=1)
        second_source_trace.identified_number_cta_trace_dict = {2.74: 0}
        first_cta_trace.add_new_source_trace(second_source_trace)

        # Третья трасса источника (её нет в ЕМТ, не отождествится ни с чем (из-за номера))
        third_source_trace = SourceTrace(mfr_number=1)

        # Объединение в один список
        source_trace_list = SourceTraceList([first_source_trace, second_source_trace, third_source_trace])

        # ______________________________________________________________________________________________________________
        # Выполнение тестируемой функции
        self.common_trace_array.identification(source_trace_list)
        # ______________________________________________________________________________________________________________
        # После отождествление в ЕМТ две трассы, первая с доп. источником, вторая по третьей трассе
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Проверка для длины ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 2
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ опредлена неверно")

        # Проверка для нахождения второй трассы источника в массиве доп. трасс
        second_trace_in_additional_array = second_source_trace in first_cta_trace.additional_source_trace_array
        self.assertTrue(second_trace_in_additional_array, "Вторая трасса источника не была добавлена в ЕМТ")

        # Проверка для длины массива трасс от доп. источников
        len_additional_array = len(first_cta_trace.additional_source_trace_array)
        real_len_additional_array = 1
        self.assertEqual(real_len_additional_array, len_additional_array, "Длина массива трасс от доп. неверна")

        # Проверка того, что головной трассой по второй трассе ЕМТ стала третья трасса истчочника
        is_third_source_trace_head = third_source_trace == second_cta_trace.head_source_trace
        self.assertTrue(is_third_source_trace_head, "Третья трасса источника не стала головной по второй трассе ЕМТ")

        # Проверка что у второй трассы нет дополнительных источников
        additional_array = second_cta_trace.additional_source_trace_array
        real_additional_array = []
        self.assertEqual(real_additional_array, additional_array, "У второй трассы ЕМТ есть доп. источник")

    def test_successful_identify_with_others_cta_traces_for_new_trace(self) -> None:
        """Тест отождествления с другими трассам ЕМТ для новой трассы источника

        :return: None
        """
        # Подготовка данных для функции
        self.common_trace_array.append(SourceTrace(mfr_number=1))
        another_source_trace = SourceTrace(mfr_number=2)

        # Выполнение ототждествления тестируемой функцией
        self.common_trace_array.identification_with_others_cta_traces_for_new_source_trace(another_source_trace)

        # Проверка для признака наличия трассы источника в списке доп. источников трассы ЕМТ
        cta_trace: CTATrace = self.common_trace_array[0]
        is_in_additional_array = another_source_trace in cta_trace.additional_source_trace_array
        self.assertTrue(is_in_additional_array, "Трасса источника в массиве доп. источников")

        # Проверка для длины ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 1
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ определена неверно")

    def test_unsuccessful_identify_with_others_cta_traces_for_new_trace_with_number(self) -> None:
        """Тест неуспешного отождествления из-за номера МФР

        :return: None
        """
        # Подготовка данных для функции
        self.common_trace_array.append(SourceTrace(mfr_number=1))
        another_source_trace = SourceTrace(mfr_number=1)

        # Выполнение ототждествления тестируемой функцией
        self.common_trace_array.identification_with_others_cta_traces_for_new_source_trace(another_source_trace)

        # Проверка для длины ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 2
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ определена неверно")

    def test_unsuccessful_identify_with_others_cta_traces_for_new_trace_with_coordinates(self) -> None:
        """Тест неуспешного отождествления из-за координат

        :return: None
        """
        # Подготовка данных для функции
        self.common_trace_array.append(SourceTrace(mfr_number=1))
        another_source_trace = SourceTrace(mfr_number=2)
        another_source_trace.coordinates = np.array([40., 3535., 42246.])

        # Выполнение ототждествления тестируемой функцией
        self.common_trace_array.identification_with_others_cta_traces_for_new_source_trace(another_source_trace)

        # Проверка для длины ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 2
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ определена неверно")

    def test_append_new_additional_source_trace_in_cta_trace(self) -> None:
        """Тест добавления нового дополнительного источника

        :return: None
        """
        # Подготовка данных для функции
        # Первая трасса ЕМТ
        head_source_trace = SourceTrace(mfr_number=0)
        self.common_trace_array.append(head_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]
        # Вторая трасса ЕМТ
        head_source_trace = SourceTrace(mfr_number=1)
        self.common_trace_array.append(head_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]
        # Добавление трассы дополнительного источника, которая успешно отождествлится с двумя трассами ЕМТ
        new_source_trace = SourceTrace(mfr_number=2)
        # Отождествление c двумя трассами ЕМТ
        new_source_trace.identified_number_cta_trace_dict = {5.87: 1, 0.: 0}

        # Выполнение тестируемой функции
        self.common_trace_array.append_new_additional_source_trace_in_cta_trace(new_source_trace)

        # Проверим, что у первой трассы появился новый доп. источник
        new_source_in_first_cta_trace = new_source_trace in first_cta_trace.additional_source_trace_array
        self.assertTrue(new_source_in_first_cta_trace)

        # Проверка, что у второй трассы такого источника нет
        self.assertFalse(new_source_trace in second_cta_trace.additional_source_trace_array)

    def test_successful_identification_with_head_source_trace_for_additional_source_trace(self) -> None:
        """Тест удачного отождествления с головной трассой источника для трассы дополнительного источника

        :return: None
        """
        # Подготовка данных для функции
        head_source_trace = SourceTrace(mfr_number=0)
        another_source_trace = SourceTrace(mfr_number=1)

        self.common_trace_array.append(head_source_trace)
        cta_trace: CTATrace = self.common_trace_array[0]
        cta_trace.additional_source_trace_array.append(another_source_trace)

        # Вызов тестируемой функции
        self.common_trace_array.identification_with_head_source_trace_for_additional_source_trace(another_source_trace)

        # Проверка для признака наличия трассы в составе массива трасс от дполнительных источников
        is_in_source_array = another_source_trace in cta_trace.additional_source_trace_array
        self.assertTrue(is_in_source_array, "Трасса удалена из массива трасс от дополнительных источников")

    def test_unsuccessful_identification_with_head_source_trace_for_additional_source_trace(self) -> None:
        """Тест неудачного отождествления с головной трассой источника для трассы дополнительного источника

        :return: None
        """
        # Подготовка данных для функции
        head_source_trace = SourceTrace(mfr_number=0)
        another_source_trace = SourceTrace(mfr_number=1)
        another_source_trace.coordinates = np.array([232., 3554., 464.])

        self.common_trace_array.append(head_source_trace)
        cta_trace: CTATrace = self.common_trace_array[0]
        cta_trace.additional_source_trace_array.append(another_source_trace)

        # Вызов тестируемой функции
        self.common_trace_array.identification_with_head_source_trace_for_additional_source_trace(another_source_trace)

        # Проверка для признака наличия трассы в составе массива трасс источников
        is_in_source_array = another_source_trace in cta_trace.additional_source_trace_array
        self.assertFalse(is_in_source_array, "Трасса не была удалена из массива трасс от дополнительных источников")

    def test_successful_identification_with_others_cta_traces_for_cta_trace(self) -> None:
        """Тест успешного отождествления трассы ЕМТ с другими трассами ЕМТ

        :return: None
        """
        # Подготовка данных для функции
        # Подготовка первой трассы ЕМТ
        first_source_trace = SourceTrace(mfr_number=0)
        first_source_trace.is_auto_tracking = True
        self.common_trace_array.append(first_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]

        # Подготовка второй трассы ЕМТ
        second_source_trace = SourceTrace(mfr_number=1)
        second_source_trace.is_auto_tracking = False
        self.common_trace_array.append(second_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Вызов тестируемой функции
        self.common_trace_array.identification_with_others_cta_traces_for_cta_trace(first_cta_trace)
        # После вызова тестируемой функции, в ЕМТ должна была остаться только первая трасса,
        # так как трассы отождествлились,
        # и первая трасса имеет более высокий приоритет за счет признака автосопровождения

        # Проверка для наличия в ЕМТ первой трассы
        is_first_trace_in_cta = first_cta_trace in self.common_trace_array
        self.assertTrue(is_first_trace_in_cta, "Первая трасса ушла из ЕМТ")

        # Проверка для наличия в ЕМТ второй трассы
        is_second_trace_in_cta = second_cta_trace in self.common_trace_array
        self.assertFalse(is_second_trace_in_cta, "Вторая трасса ЕМТ не ушла из ЕМТ")

    def test_unsuccessful_identification_with_others_cta_traces_for_cta_trace(self) -> None:
        """Тест неудачного отождествления трассы ЕМТ с другими трассами ЕМТ

        :return: None
        """
        # Подготовка данных для функции
        # Подготовка первой трассы ЕМТ
        first_source_trace = SourceTrace(mfr_number=0)
        self.common_trace_array.append(first_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]

        # Подготовка второй трассы ЕМТ
        second_source_trace = SourceTrace(mfr_number=2)
        second_source_trace.coordinates = np.array([40., 3535., 42246.])
        self.common_trace_array.append(second_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Вызов тестируемой функции
        self.common_trace_array.identification_with_others_cta_traces_for_cta_trace(first_cta_trace)
        # После вызова тестируемой функции, в ЕМТ должны были остаться обе трассы,
        # так как трассы не отождествлились

        # Проверка для наличия в ЕМТ первой трассы ЕМТ
        is_first_trace_in_cta = first_cta_trace in self.common_trace_array
        self.assertTrue(is_first_trace_in_cta, "Первая трасса ушла из ЕМТ")

        # Проверка для наличия в ЕМТ второй трассы
        is_second_trace_in_cta = second_cta_trace in self.common_trace_array
        self.assertTrue(is_second_trace_in_cta, "Вторая трасса ушла из ЕМТ")

    def test_remove_less_accuracy_cta_traces_with_numbers(self) -> None:
        """Тест удаления наименее точных трасс с указаннами номерами

        :return: None
        """
        # Подготовка данных для функции
        # Первая трасса, самая точная
        num_first_trace_in_cta = 0
        first_head_source_trace = SourceTrace(mfr_number=1)
        first_head_source_trace.is_auto_tracking = True
        self.common_trace_array.append(first_head_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]

        # Вторая трасса, менее точная
        num_second_trace_in_cta = 1
        second_head_source_trace = SourceTrace(mfr_number=2)
        second_head_source_trace.is_auto_tracking = False
        self.common_trace_array.append(second_head_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Объединение в список
        cta_traces = [num_first_trace_in_cta, num_second_trace_in_cta]

        # Вызов тестируемой функции
        self.common_trace_array.remove_less_accuracy_cta_traces_with_numbers(cta_traces)

        # Проверка для нахождения первой трассы в ЕМТ
        is_first_trace_in_cta = first_cta_trace in self.common_trace_array
        self.assertTrue(is_first_trace_in_cta, "Первая трасса ушла из ЕМТ")

        # Проверка для нахождения второй трассы в ЕМТ
        is_second_trace_in_cta = second_cta_trace in self.common_trace_array
        self.assertFalse(is_second_trace_in_cta, "Вторая трасса не ушла из ЕМТ")

    def test_get_sorted_traces(self) -> None:
        """Тест для сортировки трасс источников по точности

        :return: None
        """
        # Подготовка данных для функции
        # Создание списка из трасс источников, в котором источника расположены в убывании по точности
        list_source_traces = [SourceTrace(1, np.zeros(3)) for _ in range(8)]
        for trace, index in zip(list_source_traces, range(len(list_source_traces))):
            trace.is_bearing = index <= 3
            trace.is_auto_tracking = index not in [0, 1, 4, 5]
            trace.estimate_tick = index % 2

        # На основвании такого списка создание списка трасс ЕМТ
        list_cta_traces = [CTATrace(source_trace) for source_trace in list_source_traces]

        # Вызов тестируемой функции для сортировки
        sorted_cta_traces = self.common_trace_array.get_sorted_traces(list_cta_traces)
        # В результате выполнения функции должен был получиться в этом случае инвертированный входной список

        # Проверка для результирующего списка
        real_sorted_cta_traces = list(reversed(list_cta_traces))
        self.assertEqual(real_sorted_cta_traces, sorted_cta_traces, "Результирующий список определён неверно")

    def test_remove_all_less_accuracy_traces(self) -> None:
        """Тест удаления всех менее точных трасс из списка

        :return: None
        """
        # Подготовка данных для функции
        first_source_trace = SourceTrace(mfr_number=1)
        self.common_trace_array.append(first_source_trace)
        first_cta_trace = self.common_trace_array[0]

        second_source_trace = SourceTrace(mfr_number=2)
        self.common_trace_array.append(second_source_trace)
        second_cta_trace = self.common_trace_array[1]

        # Объединение в список
        identified_traces = [first_cta_trace, second_cta_trace]

        # Вызов тестируемой функции
        self.common_trace_array.remove_all_less_accuracy_traces(identified_traces)

        # Проверка для длины  ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 1
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ определена неверно")

    def test_update_numbers_in_cta_traces(self) -> None:
        """Тест обновления номеров в трассах ЕМТ

        :return: None
        """
        # Подготвка данных для функции
        # Первая трасса ЕМТ
        first_head_source_trace = SourceTrace(mfr_number=1)
        self.common_trace_array.append(first_head_source_trace)
        first_cta_trace: CTATrace = self.common_trace_array[0]

        # Вторая трасса ЕМТ
        second_head_source_trace = SourceTrace(mfr_number=2)
        self.common_trace_array.append(second_head_source_trace)
        second_cta_trace: CTATrace = self.common_trace_array[1]

        # Вызов тестируемой функции
        self.common_trace_array.update_numbers_in_cta_traces()

        # Проверка для номера первой трассы ЕМТ
        first_cta_trace_num = first_cta_trace.number
        real_first_cta_trace_num = 0
        self.assertEqual(real_first_cta_trace_num, first_cta_trace_num, "Номер трассы ЕМТ неверный")

        # Проверка для номера трассы ЕМТ головного источника первой трассы ЕМТ
        first_cta_trace_num_in_source_trace = first_head_source_trace.cta_number
        self.assertEqual(real_first_cta_trace_num, first_cta_trace_num_in_source_trace, "Номер трассы ЕМТ неверный")

        # Проверка для номера второй трассы ЕМТ
        second_cta_trace_num = second_cta_trace.number
        real_second_cta_trace_num = 1
        self.assertEqual(real_second_cta_trace_num, second_cta_trace_num, "Номер трассы ЕМТ неверный")

        # Проверка для номера трассы ЕМТ головного источника второй трассы ЕМТ
        second_cta_trace_num_in_source_trace = second_head_source_trace.cta_number
        self.assertEqual(real_second_cta_trace_num, second_cta_trace_num_in_source_trace, "Номер трассы ЕМТ неверный")

    def test_append(self) -> None:
        """Тест добавления трассы источника как новой трассы ЕМТ

        :return: None
        """
        # Подготовка данных для функции
        source_trace = SourceTrace(mfr_number=1, mfr_position=np.zeros(3))

        # Вызов тестируемой функции
        self.common_trace_array.append(source_trace)

        appended_cta_trace = self.common_trace_array[0]

        # Проверка для типа добавленной трассы
        type_trace = type(appended_cta_trace)
        real_type_trace = CTATrace
        self.assertEqual(real_type_trace, type_trace, "Тип трассы установлен неверно")

        # Проверка для номера трассы ЕМТ
        num_cta_trace = appended_cta_trace.number
        real_num_cta_trace = 0
        self.assertEqual(real_num_cta_trace, num_cta_trace, "Номер трассы ЕМТ определен неверно")

        # Проверка для длины ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 1
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ определена неверно")

    def test_remove(self) -> None:
        """Тест удаления трассы ЕМТ из состава ЕМТ

        :return: None
        """
        # Подготовка данных для функции
        head_source_trace = SourceTrace(mfr_number=1)
        self.common_trace_array.append(head_source_trace)
        cta_trace: CTATrace = self.common_trace_array[0]

        # Вызов тестируемой функцией
        self.common_trace_array.remove(cta_trace)

        # Проверка для длины ЕМТ
        len_cta = len(self.common_trace_array)
        real_len_cta = 0
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ не ноль")
