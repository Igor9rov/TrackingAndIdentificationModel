from unittest import TestCase
from math import pi

from mobile_part_data import MobilePartData


class TestMobilePartData(TestCase):
    """Тест для подвижной части антенны"""
    def setUp(self):
        """Собственные данные обзора"""
        self.mobile_part_data = MobilePartData()

    def test___init__(self):
        """Проверка для __init__ без ошибок"""
        # При текущих значениях по умолчанию, должна получиться матрица
        real_transform_matrix = [[0.8660254, 0.5, 0], [-0.5, 0.8660254, 0], [0, 0, 1]]
        # Получилась такая матрица
        transform_matrix = self.mobile_part_data.transform_matrix.round(7).tolist()
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота определена неверно")

    def test___init__with_errors(self):
        """Проверка для __init__ с ошибками"""
        # Ошибка по азимуту в угловых минутах
        error_beta = 30
        corrupted_mobile_part_data = MobilePartData(error_beta=error_beta)
        # Должен получиться такой азимут с учётом ошибки
        real_beta = error_beta * pi / (180 * 60)
        # Получился такой азимут
        beta = corrupted_mobile_part_data.beta

        # Проверка
        self.assertEqual(real_beta, beta, "Азимут задан неверно")

    def test_calculate_transform_matrix(self):
        """Тест для расчёта матрицы поворота, пока нет реализации функции, то и тестить нечего"""
        pass
