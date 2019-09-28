from unittest import TestCase

import numpy as np

from mobile_part_data import MobilePartData


class TestFixedPartData(TestCase):
    def setUp(self):
        # Собственные данные обзора
        self.fixed_part_data = MobilePartData()

    # TODO: Проверить не только при значениях по умолчанию!!!
    def test_calculate_transform_matrix(self):
        # При текущих значениях по умолчанию, должна получиться матрица
        result_matrix = np.array([[0.866025403, 0.5, 0], [-0.5, 0.866025403, 0], [0, 0, 1]])
        self.fixed_part_data.calculate_transform_matrix()
        self.assertEqual(self.fixed_part_data.transform_matrix.round(7).tolist(), result_matrix.round(7).tolist())
