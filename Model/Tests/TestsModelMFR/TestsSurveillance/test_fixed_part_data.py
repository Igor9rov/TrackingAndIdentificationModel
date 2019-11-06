from unittest import TestCase

import numpy as np

from fixed_part_data import FixedPartData


class TestFixedPartData(TestCase):
    def setUp(self):
        # Собственные данные обзора
        self.fixed_part_data = FixedPartData()

    # TODO: Проверить не только при значениях по умолчанию!!!
    def test_calculate_transform_matrix(self):
        # При текущих значениях по умолчанию, должна получиться единичная матрица
        self.assertEqual(self.fixed_part_data.transform_matrix.tolist(), np.eye(3).tolist())
