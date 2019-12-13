from unittest import TestCase

import numpy as np

from source_trace import SourceTrace


class TestSourceTrace(TestCase):
    """Тест для класса SourceTrace"""
    def setUp(self) -> None:
        """Создадим трассу ЕМТ с данными по-умолчанию

        :return: None
        """
        self.source_trace = SourceTrace()

    def test_registration(self):
        """Проверка записи регисрации

        :return: None
        """
        # Определим нужные для функции данные
        self.source_trace.target_number = 34
        self.source_trace.coordinates = np.array([34_840, 23_000, 2_013])
        self.source_trace.velocities = np.array([230, 435, 544])
        self.source_trace.coordinate_covariance_matrix = np.array([[34_000, 45, 34],
                                                                   [45, 45_665, 2300],
                                                                   [34, 2300, 74_990]])
        self.source_trace.is_bearing = True
        self.source_trace.cta_number = 2
        self.source_trace.probability_measure = 2.98

        # Регистрация вычисленная вручную
        real_registration = [34,
                             34_840, 23_000, 2_013,
                             230, 435, 544,
                             34_000, 45_665, 74_990, 45, 34, 2_300,
                             True,
                             2,
                             2.98]

        # Расчет регистрации через свойство
        registration = self.source_trace.registration

        # Проверка
        self.assertEqual(real_registration, registration, "Регистрация записывается неверно")

    def test_identified_cta_trace_numbers(self):
        """Проверка получения номера трасс с которыми отождествилась трасса

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.identified_number_cta_trace_dict = dict(zip([1.25, 8.65], [5, 2]))

        # Получение номеров трасс ЕМТ вручную
        real_cta_numbers = [5, 2]

        # Получаем номеров трасс ЕМТ через свойство
        cta_numbers = self.source_trace.identified_cta_trace_numbers

        # Проверка
        self.assertEqual(real_cta_numbers, cta_numbers, "Номера трасс ЕМТ определены неверно")

    def test_clear_identified_number_cta_trace_dict(self):
        """Тестирует обнуление словаря

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.identified_number_cta_trace_dict = dict(zip([1.25, 8.65], [5, 2]))

        # Очистим словарь функцией
        self.source_trace.clear_identified_number_cta_trace_dict()
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Пустой словарь
        real_dictionary = {}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь не очистился")

    def test_num_cta_trace_with_min_distance(self):
        """Тестирование получения номера трассы ЕМТ с минимальным расстоянием

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.identified_number_cta_trace_dict = dict(zip([5.78, 1.25, 8.65], [3, 5, 2]))

        # Получение номера трассы ЕМТ с минимальным расстоянием через свойство
        number = self.source_trace.num_cta_trace_with_min_distance

        # Номер трассы ЕМТ с минимальным расстоянием оцененный вручную
        real_number = 5

        # Проверка
        self.assertEqual(real_number, number, "Номер трассы ЕМТ оценен неверно")

    def test_append_cta_info_and_number(self):
        """Тестирование добавления информации и номера трассы ЕМТ

        :return: None
        """
        self._test_append_cta_info_and_number_when_source_is_head()
        self._test_append_cta_info_and_number_when_source_is_additional()

    def _test_append_cta_info_and_number_when_source_is_head(self):
        """Тестирование добавления информации и номера трассы ЕМТ в случае, когда источник головной

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.identified_number_cta_trace_dict = {1.23: 10, 4.87: 32}

        # Добавим информацию функцией
        self.source_trace.append_cta_info_and_number(num=10, is_head=True)
        number_cta_trace = self.source_trace.cta_number
        is_head_source = self.source_trace.is_head_source
        is_in_common_trace_array = self.source_trace.is_in_common_trace_array
        probability_measure = self.source_trace.probability_measure

        # Оценим её сами
        real_number_cta_trace = 10
        real_probability_measure = 0

        # Проверка
        self.assertEqual(real_number_cta_trace, number_cta_trace, "Номер трассы ЕМТ определён неверно")
        self.assertTrue(is_head_source, "Неверно выставлен признак головного источника")
        self.assertTrue(is_in_common_trace_array, "Неверно выставлен признак наличия трассы источника в ЕМТ")
        self.assertEqual(real_probability_measure, probability_measure, "Обобщённое расстояние указано неверно")

    def _test_append_cta_info_and_number_when_source_is_additional(self):
        """Тестирование добавления информации и номера трассы ЕМТ в случае, когда источник дополнительный

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.identified_number_cta_trace_dict = {1.23: 10, 4.87: 32}

        # Добавим информацию функцией
        self.source_trace.append_cta_info_and_number(num=10, is_head=False)
        number_cta_trace = self.source_trace.cta_number
        is_head_source = self.source_trace.is_head_source
        is_in_common_trace_array = self.source_trace.is_in_common_trace_array
        probability_measure = self.source_trace.probability_measure

        # Оценим её сами
        real_number_cta_trace = 10
        real_probability_measure = 1.23

        # Проверка
        self.assertEqual(real_number_cta_trace, number_cta_trace, "Номер трассы ЕМТ определён неверно")
        self.assertFalse(is_head_source, "Неверно выставлен признак головного источника")
        self.assertTrue(is_in_common_trace_array, "Неверно выставлен признак наличия трассы источника в ЕМТ")
        self.assertEqual(real_probability_measure, probability_measure, "Обобщённое расстояние указано неверно")

    def test_delete_cta_info_and_number(self):
        """Тестирование удаления информации и номера трассы ЕМТ

        :return: None
        """
        # Определим нужные данные для функции
        self.source_trace.cta_number = 89
        self.source_trace.is_head_source = True
        self.source_trace.is_in_common_trace_array = True
        self.source_trace.probability_measure = 3.47

        # Удаление информации тестируемой функцией
        self.source_trace.delete_cta_info_and_number()
        cta_number = self.source_trace.cta_number
        probability_measure = self.source_trace.probability_measure
        is_in_common_trace_array = self.source_trace.is_in_common_trace_array
        is_head_source = self.source_trace.is_head_source

        # После удаления информации должны быть такие переменные
        real_cta_number = -1
        real_probability_measure = 0

        # Проверка
        self.assertEqual(real_cta_number, cta_number, "Номер трассы ЕМТ удален неверно")
        self.assertFalse(is_head_source, "Неверно удален признак головного источника")
        self.assertFalse(is_in_common_trace_array, "Неверно удален признак наличия трассы источника в ЕМТ")
        self.assertEqual(real_probability_measure, probability_measure, "Обобщённое расстояние удалено неверно")

    def test_extrapolate_coordinates_to_tick(self):
        """Тестирование экстраполяции координат на заданное время

        :return: None
        """
        # Определим нужные для функции данные
        self.source_trace.estimate_tick = 20
        self.source_trace.coordinates = np.array([20., 40., 12.])
        self.source_trace.velocities = np.array([2., -8., 9.])

        # Эктраполируем координаты функцией
        self.source_trace.extrapolate_coordinates_to_tick(tick=30)
        coordinates = self.source_trace.coordinates.tolist()

        # Экстраполируем координаты вручную
        real_coordinates = [21., 36., 16.5]

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Координаты экстраполированы неверно")

    def test_true_identification_jammer_and_target(self):
        """Проверка отождествления постановщика АШП и чистой цели, в случае, когда это одна цель

        :return: None
        """
        # Определим необходимые данные
        # Пусть сохраненная трасса будет трассой чистой цели
        self.source_trace.coordinates = np.array([0., 0., 1_100.])
        self.source_trace.is_bearing = False
        self.source_trace.coordinate_covariance_matrix = np.diag([22_443., 258., 3_344.])
        # А трасса с которой происходит отождествление - трасса постановщика АШП
        trace = SourceTrace()
        trace.cta_number = 4
        trace.coordinates = np.array([0., 0, 550.])
        trace.is_bearing = True
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        # Отождестлвяем функцией
        self.source_trace.identification_jammer_and_target(trace)
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Трассы должны были отождествиться, поэтому словарь такой
        real_dictionary = {0.: 4}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь с отождествившимися трассами определён неверно")

    def test_false_identification_jammer_and_target(self):
        """Проверка отождествления постановщика АШП и чистой цели, в случае, когда это разные цели

        :return: None
        """
        # Определим необходимые данные
        # Пусть сохраненная трасса будет трассой чистой цели
        self.source_trace.coordinates = np.array([0., 0., 1_100.])
        self.source_trace.is_bearing = False
        self.source_trace.coordinate_covariance_matrix = np.diag([22_443., 258., 3_344.])
        # А трасса с которой происходит отождествление - трасса постановщика АШП
        trace = SourceTrace()
        trace.cta_number = 4
        trace.coordinates = np.array([4_540., 3_330, 53_450.])
        trace.is_bearing = True
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        # Отождестлвяем функцией
        self.source_trace.identification_jammer_and_target(trace)
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Трассы не должны были отождествиться, поэтому словарь пустой
        real_dictionary = {}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь с отождествившимися трассами не пуст")

    def test_true_identification_target_and_target(self):
        """Тестирование отождествления двух трасс по одной чистой цели

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.coordinates = np.array([0., 0., 1_100.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22_443., 258., 3_344.])
        # Трасса, с которой будет проводиться отождествление
        trace = SourceTrace()
        trace.cta_number = 4
        trace.coordinates = np.array([0., 0, 1_100.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        # Отождествляем функцией
        self.source_trace.identification_target_and_target(trace)
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Трассы должны были отождествиться, поэтому словарь такой
        real_dictionary = {0.: 4}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь с отождествившимися трассами определён неверно")

    def test_false_identification_target_and_target(self):
        """Тестирование отождествления двух трасс по двум разным чистым целям

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.coordinates = np.array([0., 0., 1_100.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22_443., 258., 3_344.])
        # Трасса, с которой будет проводиться отождествление
        trace = SourceTrace()
        trace.cta_number = 4
        trace.coordinates = np.array([45_860., 0, 1_100.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        # Отождествляем функцией
        self.source_trace.identification_target_and_target(trace)
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Трассы не должны были отождествиться, поэтому словарь пустой
        real_dictionary = {}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь с отождествившимися трассами не пуст")

    def test_true_identification_jammer_and_jammer(self):
        """Проверка отождествления двух трасс по одному и тому же постановщику АШП

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.mfr_position = np.array([1_100., 0., 0.])
        self.source_trace.coordinates = np.array([550., 0., 5_500.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22_443., 258., 3_344.])
        # Трасса, с которой будет проводиться отождествление
        trace = SourceTrace(mfr_position=np.array([-1_100., 0., 0.]))
        trace.cta_number = 4
        trace.coordinates = np.array([-550., 0, 550.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        # Отождествляем функцией
        self.source_trace.identification_jammer_and_jammer(trace)
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Трассы должны были отождествиться, поэтому словарь такой
        real_dictionary = {0.: 4}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь с отождествившимися трассами определён неверно")

    def test_false_identification_jammer_and_jammer(self):
        """Проверка отождествления двух трасс по двум разным постановщикам АШП

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.mfr_position = np.array([1_100., 0., 0.])
        self.source_trace.coordinates = np.array([550., 0., 5_500.])
        self.source_trace.coordinate_covariance_matrix = np.diag([22_443., 258., 3_344.])
        # Трасса, с которой будет проводиться отождествление
        trace = SourceTrace(mfr_position=np.array([-1_100., 0., 0.]))
        trace.cta_number = 4
        trace.coordinates = np.array([-34_550., 43_430, -43_550.])
        trace.coordinate_covariance_matrix = np.diag([243., 659., 496])

        # Отождествляем функцией
        self.source_trace.identification_jammer_and_jammer(trace)
        dictionary = self.source_trace.identified_number_cta_trace_dict

        # Трассы не должны были отождествиться, поэтому словарь такой
        real_dictionary = {}

        # Проверка
        self.assertDictEqual(real_dictionary, dictionary, "Словарь с отождествившимися трассами не пуст")

    def test_calculate_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(self):
        """Проверка вычисления координат и ковариационной матрциы ближайшей точки на пеленге
        при отождествлении двух трасс постановщиков АШП

        :return: None
        """
        # Определим нужные для функции параметры
        self.source_trace.coordinates = np.array([1., 0., 0.])
        self.source_trace.mfr_position = np.ones(3)
        self.source_trace.coordinate_covariance_matrix = np.diag([1., 1., 0.])
        # Вторая трасса по постановщику АШП
        trace = SourceTrace(mfr_position=np.zeros(3))
        trace.coordinates = np.array([0., 0., 1.])
        trace.coordinate_covariance_matrix = np.diag([1., 0., 1])

        # Расчет тестируемой функцией
        coordinates, cov_matrix = self.source_trace.calc_est_anj_coords_and_cov_matrix_for_jammer_and_jammer(trace)
        coordinates = coordinates.tolist()
        cov_matrix = cov_matrix.tolist()

        # Расчет вручную
        real_coordinates = [1, 0, 0]
        real_cov_matrix = [[1., 0., 0.],
                           [0., 1., 0.],
                           [0., 0., 0.]]

        # Проверка
        self.assertEqual(real_coordinates, coordinates, "Расчет координат неверный")
        self.assertEqual(real_cov_matrix, cov_matrix, "Расчет ковариационной матрицы неверный")

    def test_calculate_est_anj_coords_and_cov_matrix_for_jammer_and_target(self):
        """Расчет координат и ковариационной матрицы в случае отождествления чистой трассы и постановщика АШП

        :return: None
        """
        # Определим необходимые для функции данные
        self.source_trace.coordinates = np.array([1., 0., 0.])
        self.source_trace.mfr_position = np.ones(3)
        self.source_trace.coordinate_covariance_matrix = np.diag([1., 1., 0.])
        # Трасса постановщика АШП
        trace = SourceTrace()
        trace.coordinates = np.array([0., 0, 1.])
        trace.coordinate_covariance_matrix = np.diag([1., 0., 1])

        # Расчет тестируемой функцией
        coordinates, cov_matrix = self.source_trace.calc_est_anj_coords_and_cov_matrix_for_jammer_and_target(trace)
        coordinates = coordinates.tolist()
        cov_matrix = cov_matrix.tolist()

        # Расчет вручную
        real_coordinates = [1., 0.5, 0.5]
        real_cov_matrix = [[0.25, 0.0, 0.0],
                           [0.0, 0.25, 0.0],
                           [0.0, 0.0, 0.0]]

        # Проверка
        self.assertEqual(coordinates, real_coordinates, "Расчет координат неверный")
        self.assertEqual(cov_matrix, real_cov_matrix, "Расчет ковариационной матрицы неверный")

    def test_calculate_generalized_distance(self):
        """Проверка вычисления обобщённого расстояния

        :return:
        """
        # Определение входных параметров для функции
        covariance_matrix = np.diag([25, 1, 0.01])
        distance = np.array([9, 3, 1])

        # Расчет обобщённого рассстояния тестируемой функцией
        generalized_distance = SourceTrace.calculate_generalized_distance(covariance_matrix, distance)

        # Обобщённое расстояние опредленное вручную
        real_generalized_distance = 112.24

        # Проверка
        self.assertEqual(real_generalized_distance, generalized_distance, "Обобщённое расстояние оценено неверно")
