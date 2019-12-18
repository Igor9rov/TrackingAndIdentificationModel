from unittest import TestCase

from mobile_part_data import MobilePartData


class TestMobilePartData(TestCase):
    """Тест для подвижной части антенны"""
    def setUp(self) -> None:
        """Собственные данные обзора

        :return: None
        """
        self.mobile_part_data = MobilePartData()

    def test___init__(self) -> None:
        """Проверка для __init__ без ошибок

        :return: None
        """
        # Проверка для истинной матрицы поворота
        transform_matrix = self.mobile_part_data.transform_matrix.round(5).tolist()
        real_transform_matrix = [[0.86603, 0.5, 0.0],
                                 [-0.5, 0.86603, 0.0],
                                 [0.0, 0.0, 1.0]]
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота определена неверно")

        # Проверка для оцененной матрицы поворота
        transform_matrix = self.mobile_part_data.corrupted_transform_matrix.round(5).tolist()
        real_transform_matrix = [[0.86603, 0.5, 0.0],
                                 [-0.5, 0.86603, 0.0],
                                 [0.0, 0.0, 1.0]]
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота определена неверно")

    def test___init__with_errors(self) -> None:
        """Проверка для __init__ с ошибками

        :return: None
        """
        corrupted_mobile_part_data = MobilePartData(error_beta=30)

        # Проверка для истинной матрицы поворота
        transform_matrix = corrupted_mobile_part_data.transform_matrix.round(5).tolist()
        real_transform_matrix = [[0.86603, 0.5, 0.0],
                                 [-0.5, 0.86603, 0.0],
                                 [0.0, 0.0, 1.0]]
        self.assertEqual(real_transform_matrix, transform_matrix, "Матрица поворота установлена неверно")

        # Проверка для расчитанной матрицы поворота
        corrupted_transform_matrix = corrupted_mobile_part_data.corrupted_transform_matrix.round(5).tolist()
        real_corrupted_transform_matrix = [[0.86599, 0.5, 0.00756],
                                           [-0.49998, 0.86603, -0.00436],
                                           [-0.00873, 0.0, 0.99996]]
        self.assertEqual(real_corrupted_transform_matrix, corrupted_transform_matrix, "Матрица определена неверно")

