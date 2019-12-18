from unittest import TestCase

from fixed_part_data import FixedPartData


class TestFixedPartData(TestCase):
    """Тест для неподвижной части антенны"""
    def setUp(self) -> None:
        """Собственные данные обзора без ошибок

        :return: None
        """
        self.fixed_part_data = FixedPartData()

    def test___init__(self) -> None:
        """Тест для __init__ без ошибок

        :return: None
        """
        # Проверка для истинной матрицы поворота
        transform_matrix = self.fixed_part_data.transform_matrix.tolist()
        real_transform_matrix = [[1., 0., 0.],
                                 [0., 1., 0.],
                                 [0., 0., 1.]]
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота установлена неверно")

        # Проверка для расчитанной матрицы поворота
        corrupted_transform_matrix = self.fixed_part_data.corrupted_transform_matrix.tolist()
        real_corrupted_transform_matrix = [[1., 0., 0.],
                                           [0., 1., 0.],
                                           [0., 0., 1.]]
        self.assertEqual(real_corrupted_transform_matrix, corrupted_transform_matrix, "Матрица опредлена неверно")

    def test___init___with_errors(self) -> None:
        """Тест для __init__ с ошибками

        :return: None
        """
        corrupted_fixed_part_data = FixedPartData(error_beta_north=30)

        # Проверка для истинной матрицы поворота
        transform_matrix = corrupted_fixed_part_data.transform_matrix.tolist()
        real_transform_matrix = [[1., 0., 0.],
                                 [0., 1., 0.],
                                 [0., 0., 1.]]
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота установлена неверно")

        # Проверка для расчитанной матрицы поворота
        corrupted_transform_matrix = corrupted_fixed_part_data.corrupted_transform_matrix.round(5).tolist()
        real_corrupted_transform_matrix = [[0.99996, 0.0, 0.00873],
                                           [0.0, 1.0, 0.0],
                                           [-0.00873, 0.0, 0.99996]]
        self.assertEqual(real_corrupted_transform_matrix, corrupted_transform_matrix, "Матрица определена неверно")
