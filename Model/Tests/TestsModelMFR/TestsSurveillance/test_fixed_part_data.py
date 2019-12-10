from math import pi
from unittest import TestCase

import numpy as np

from fixed_part_data import FixedPartData


class TestFixedPartData(TestCase):
    """Тест для неподвижной части антенны"""
    def setUp(self):
        """Собственные данные обзора без ошибок"""
        self.fixed_part_data = FixedPartData()

    def test___init__(self):
        """Тест для __init__ без ошибок"""
        # При текущих значениях по умолчанию, должна получиться единичная матрица
        real_transform_matrix = np.eye(3).tolist()
        # Получена такая матрица
        transform_matrix = self.fixed_part_data.transform_matrix.tolist()

        # Проверка
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота определена неверно")

    def test___init___with_errors(self):
        """Тест для __init__ с ошибками"""
        # Ошибка по азимуту в угловых минутах
        error_beta_north = 30
        corrupted_fixed_part_data = FixedPartData(error_beta_north=error_beta_north)
        # Должен получиться такой азимут с учётом ошибки
        real_beta_north = error_beta_north * pi / (180 * 60)
        # Получился такой азимут
        beta_north = corrupted_fixed_part_data.corrupted_beta_north

        # Проверка
        self.assertEqual(real_beta_north, beta_north, "Азимут задан неверно")
