from unittest import TestCase

import numpy as np

from command_post import CommandPost
from cta_trace import CTATrace
from multi_functional_radar import MultiFunctionalRadar
from source_trace import SourceTrace
from target import Target


class TestCommandPost(TestCase):
    """Тест для ПБУ"""
    def setUp(self) -> None:
        """Сохраняет ссылки на нужные объекты, откатывает их к первоначальному состоянию

        :return: None
        """
        # Две цели
        first_target = Target(number=1,
                              coordinates=np.array([100000, 1001, 30000.]),
                              velocities=np.array([-50., 0., -60.]))

        second_target = Target(number=2,
                               coordinates=np.array([30000, 5001, 30000.]),
                               velocities=np.array([-50., 0., -60.]))

        # Список целей
        self.target_list = [first_target, second_target]
        # Два локатора
        first_radar = MultiFunctionalRadar(target_list=self.target_list,
                                           stable_point=np.array([1001, 0, -780]),
                                           mfr_number=1)
        second_radar = MultiFunctionalRadar(target_list=self.target_list,
                                            stable_point=np.array([-1000, 0, 780]),
                                            mfr_number=2)
        # Список локаторов
        self.radar_list = [first_radar, second_radar]
        # Собственный ПБУ
        self.command_post = CommandPost(mfr_list=self.radar_list)
        self.failure_msg = "Что-то пошло не так"

    def test__generate_adjustment_dict(self) -> None:
        """Тест для генерации словаря для юстировок

        :return: None
        """
        # Вызов тестируемой функции
        self.command_post._generate_adjustment_dict()

        # Проверка для словаря с юстировками
        # (Словари напрямую не сравнить (объекты оценивателя не проходят сравнения,
        # так как они в разных участках памяти))
        len_adjustment_dict = len(self.command_post.adjustment_dict)
        real_len_adjustment_dict = 1
        self.assertEqual(real_len_adjustment_dict, len_adjustment_dict, "Словарь для юстировки неверный")

    def test_operate(self) -> None:
        """Тест основного алгоритма работы

        :return: None
        """
        # Запуск тестируемой функции с двумя целями, двумя локаторами и ПБУ
        for time in range(1000):
            for target in self.target_list:
                target.operate(time)
            for radar in self.radar_list:
                radar.operate(time)
            try:
                self.command_post.operate(time)
            except AttributeError:
                self.fail(self.failure_msg)

        # Проверка для длины ЕМТ
        len_cta = len(self.command_post.common_trace_array)
        real_len_cta = 2
        self.assertEqual(real_len_cta, len_cta, "Длина ЕМТ неверна")

        # Проверка для массива трасс дополнительных источников по первой трассе ЕМТ
        first_cta_trace: CTATrace = self.command_post.common_trace_array[0]
        self.assertIsNotNone(first_cta_trace.additional_source_trace_array)

        # Проверка для массива трасс дополнительных источников по второй трассе ЕМТ
        second_cta_trace: CTATrace = self.command_post.common_trace_array[1]
        self.assertIsNotNone(second_cta_trace.additional_source_trace_array)

    def test_analyze_adjustment_when_it_ready(self) -> None:
        """Тест для анализа юстировок, когда они готовы

        :return: None
        """
        # Подготовка нужных для функции данных
        adjustment_dict = self.command_post.adjustment_dict[2]
        adjustment_dict["ready"] = True
        adjustment_dict["residuals"] = np.array([2., 4., 2.])

        # Выполненение тестируемой функции
        self.command_post.analyze_adjustment()

        mfr = self.radar_list[1]

        # Проверка для призанка юстированности
        is_adjustment = mfr.is_adjustment
        self.assertTrue(is_adjustment, "Признак юстированности установлен неверно")

        # Проверка для поправок
        residuals = mfr.residuals.tolist()
        real_residuals = [2., 4., 2.]
        self.assertEqual(real_residuals, residuals, "Поправки установлены неверно")

    def test_analyze_adjustment_when_it_not_ready(self) -> None:
        """Тест для анализа юстировок, когда они не готовы

        :return: None
        """
        # Подготовка нужных для функции данных
        adjustment_dict = self.command_post.adjustment_dict[2]
        adjustment_dict["ready"] = False
        adjustment_dict["residuals"] = np.array([2., 4., 2.])

        # Выполненение тестируемой функции
        self.command_post.analyze_adjustment()

        mfr = self.radar_list[1]

        # Проверка для призанка юстированности
        is_adjustment = mfr.is_adjustment
        self.assertFalse(is_adjustment, "Признак юстированности установлен неверно")

        # Проверка для поправок
        residuals = mfr.residuals
        self.assertIsNone(residuals, "Поправки установлены неверно")

    def test_register(self) -> None:
        """Тест для регистрации ПБУ

        :return: None
        """
        # Определение нужной для функции данных
        self.command_post.tick = 23
        self.command_post.common_trace_array.append(SourceTrace())
        cta_trace: CTATrace = self.command_post.common_trace_array[0]
        cta_trace.number = 88
        cta_trace.coordinates = np.array([34., 323., -293.])
        cta_trace.velocities = np.array([200., 23., -21.])
        cta_trace.coordinate_covariance_matrix = np.diag([32., 34., 569.])

        # Выполненение тестируемой функции
        self.command_post.register()

        # Проверка для регистрации
        registration = self.command_post.registration
        real_registration = [[23, 88, 34.0, 323.0, -293.0, 200.0, 23.0, -21.0, 32.0, 34.0, 569.0, 0.0, 0.0, 0.0, 1]]
        self.assertEqual(real_registration, registration, "Регистрация посчитана неверно")
