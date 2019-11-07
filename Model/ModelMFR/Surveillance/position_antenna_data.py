from math import cos, sin, sqrt, asin

import numpy as np
from numpy import ndarray

from errors_namedtuple import SurveillanceErrors
from fixed_part_data import FixedPartData
from mobile_part_data import MobilePartData


class PositionAntennaData:
    """Класс, описывающий положение антенны, поддерживает пересчёт координат и ковариационных матриц"""
    __slots__ = ("height",
                 "mobile_part_data",
                 "fixed_part_data")

    def __init__(self, errors: SurveillanceErrors = SurveillanceErrors(0, 0)):
        # Высота антенного полотна
        self.height = 5.64
        # Данные по подвижной части антенны
        self.mobile_part_data = MobilePartData(errors.Beta)
        # Данные по неподвижной части антенны
        self.fixed_part_data = FixedPartData(errors.Beta_north)

    def calculate_data(self):
        """Вычисление матриц поворота

        :return: None
        """
        # TODO: Пока нет кругового режима, то ничего в этой функции не будет происходить
        self.mobile_part_data.calculate_transform_matrix()

    def dec2bcs(self, coordinates_dec: ndarray, velocities_dec: ndarray):
        """Расчёт координат и скоростей в БСК из МЗСК МФР

        :param coordinates_dec: Вектор координат в прямоугольной декартовой СК
        :param velocities_dec: Вектор скоростей в прямоугольной декартовой СК

        :return: Вектор координат, вектор скоростей в БСК
        """
        # Переход к АСК от декартовых
        coordinates_acs, velocities_acs = self.dec2acs(coordinates_dec, velocities_dec)
        # Переход к БСК от АСК
        coordinates_bcs, velocities_bcs = self.acs2bcs(coordinates_acs, velocities_acs)
        return coordinates_bcs, velocities_bcs

    def dec2acs(self, coordinates_dec: ndarray, velocities_dec: ndarray):
        """Расчёт скоростей и координат из МЗСК МФР к АСК МФР

        :param coordinates_dec: Вектор координат в прямоугольной декартовой СК
        :param velocities_dec: Вектор скоростей в прямоугольной декартовой СК

        :return: Вектор координат, вектор скоростей в АСК
        """
        # Обозначения для удобства записи
        matrix_a = self.fixed_part_data.transform_matrix
        matrix_b = self.mobile_part_data.transform_matrix
        height = self.height
        # Переход к прямоугольным координатам в АСК
        coordinate_acs = matrix_a @ (matrix_b @ coordinates_dec - np.array([0., height, 0.]))
        # Скорость в АСК
        velocity_acs = matrix_a @ matrix_b @ velocities_dec
        return coordinate_acs, velocity_acs

    @staticmethod
    def acs2bcs(coordinates_acs: ndarray, velocities_acs: ndarray):
        """Расчёт координат из декартовой АСК к БСК

        :param coordinates_acs: Вектор координат в АСК
        :param velocities_acs: Вектор скоростей в АСК

        :return: Вектор координат, вектор скоростей в БСК
        """
        # Координаты в АСК
        x, y, z = coordinates_acs.tolist()
        # Скорости в АСК
        vx, vy, vz = velocities_acs.tolist()
        # Расчёт координат в БСК
        r = sqrt(x ** 2 + y ** 2 + z ** 2)
        phi_v = asin(y / r)
        phi_n = asin(z / r)
        # Результат преобразований координат
        coordinate_bcs = np.array([r, phi_v, phi_n])
        # Расчёт скоростей в БСК
        vr = (x * vx + y * vy + z * vz) / r
        v_phi_v = (vy * r - y * vr) / (r * sqrt(r ** 2 - y ** 2))
        v_phi_n = (vz * r - z * vr) / (r * sqrt(r ** 2 - z ** 2))
        # Результат преобразований скоростей
        velocity_bcs = np.array([vr, v_phi_v, v_phi_n])
        return coordinate_bcs, velocity_bcs

    def acs2dec(self, coordinates_acs: ndarray, velocities_acs: ndarray):
        """Функция для перехода от АСК к МЗСК

        :param coordinates_acs: Вектор координат в АСК
        :param velocities_acs: Вектор скоростей в АСК

        :return: Веткор координат, вектор скоростей в прямоугольной декартовой СК
        """
        # Обозначения для удобства записи
        matrix_a = self.fixed_part_data.transform_matrix
        matrix_b = self.mobile_part_data.transform_matrix
        height = self.height
        # Переход от АСК к МЗСК для координат
        coordinate_dec = matrix_b.transpose() @ (matrix_a.transpose() @ coordinates_acs + np.array([0., height, 0.]))
        # Переход от АСК к МЗСК для скоростей
        velocity_dec = matrix_b.transpose() @ (matrix_a.transpose() @ velocities_acs)
        return coordinate_dec, velocity_dec

    def bcs2dec(self, coordinates_bcs: ndarray, velocities_bcs: ndarray):
        """Функция для расчёта координат и скоростей в МЗСК из БСК

        :param coordinates_bcs: Вектор координат в БСК
        :param velocities_bcs: Вектор скоростей в БСК

        :return: Вектор координат, вектор скоростей в прямоугольной декартовой СК
        """
        coordinates_acs, velocities_acs = self.bcs2acs(coordinates_bcs, velocities_bcs)
        coordinates_dec, velocities_dec = self.acs2dec(coordinates_acs, velocities_acs)
        return coordinates_dec, velocities_dec

    @staticmethod
    def bcs2acs(coordinates_bcs: ndarray, velocities_bcs: ndarray):
        """Функция для перехода от БСК к АСК

        :param coordinates_bcs: Вектор координат в БСК
        :param velocities_bcs: Вектор скоростей в БСК

        :return: Вектор координат, вектор скоростей в АСК
        """
        # Введём обозначения координат для упрощения записи
        r, theta_v, theta_n = coordinates_bcs.tolist()
        # Введём обознаечния скоростей для упрощения записи
        vr, v_theta_v, v_theta_n = velocities_bcs.tolist()
        # Переменные для удобства записи
        sin_n = sin(theta_n)
        sin_v = sin(theta_v)
        sin_2n = sin(2. * theta_n)
        sin_2v = sin(2. * theta_v)
        # Координаты в АСК
        x_acs = r * sqrt(1 - sin_n ** 2 - sin_v ** 2)
        y_acs = r * sin_v
        z_acs = r * sin_n
        # Скорость в АСК
        vx_acs = (vr * x_acs / r) - (r ** 2 * (sin_2n * v_theta_n + sin_2v * v_theta_v)) / (2. * x_acs)
        vy_acs = vr * sin_v + r * cos(theta_v) * v_theta_v
        vz_acs = vr * sin_n + r * cos(theta_n) * v_theta_n
        # Координаты в АСК
        coordinate_acs = np.array([x_acs, y_acs, z_acs])
        # Скорость в АСК
        velocity_acs = np.array([vx_acs, vy_acs, vz_acs])
        return coordinate_acs, velocity_acs

    def calc_dec_covariance_matrix_from_bcs(self, covariance_matrix_bcs: ndarray, coordinate_bcs: ndarray):
        """Расчёт ковариационной матрицы в декартовых координатах МФР из БСК

        :param covariance_matrix_bcs: Ковариационная матрица в БСК
        :param coordinate_bcs: Вектор координат в БСК

        :return: Ковариационная матрица в прямоугольной декартовой СК
        """
        # Ковариационная матрица в АСК
        covariance_matrix_acs = self.calc_acs_covariance_matrix_from_bcs(covariance_matrix_bcs, coordinate_bcs)
        # Ковариационная матрица в декартовых координатых МФР
        covariance_matrix_dec = self.calc_dec_covariance_matrix_from_acs(covariance_matrix_acs)
        return covariance_matrix_dec

    @staticmethod
    def calc_acs_covariance_matrix_from_bcs(covariance_matrix_bcs: ndarray, coordinates_bcs: ndarray):
        """Расчёт ковариационной матрицы в АСК МФР из БСК МФР

        :param covariance_matrix_bcs: Ковариационная матрица в БСК
        :param coordinates_bcs: Вектор координат в БСК

        :return: Ковариационная матрица в АСК
        """
        r, phi_v, phi_n = coordinates_bcs.tolist()
        # Формируем элементы матрицы производных
        derivative_matrix = np.zeros([3, 3])

        derivative_matrix[0][0] = sqrt(1 - sin(phi_n)**2 - sin(phi_v)**2)
        derivative_matrix[0][1] = -r * cos(phi_n) * sin(phi_n) / derivative_matrix[0][0]
        derivative_matrix[0][2] = -r * cos(phi_v) * sin(phi_v) / derivative_matrix[0][0]

        derivative_matrix[1][0] = sin(phi_v)
        derivative_matrix[1][1] = 0.
        derivative_matrix[1][2] = r * cos(phi_v)

        derivative_matrix[2][0] = sin(phi_n)
        derivative_matrix[2][1] = r * cos(phi_n)
        derivative_matrix[2][2] = 0.
        # Ковариационная матрица в АСК равна F*K_sph*F', где F - матрица производных
        covariance_matrix_acs = derivative_matrix @ covariance_matrix_bcs @ derivative_matrix.transpose()
        return covariance_matrix_acs

    def calc_dec_covariance_matrix_from_acs(self, covariance_matrix_acs: ndarray):
        """Расчёт ковариационной матрицы в декартовых координатах МФР из АСК МФР

        :param covariance_matrix_acs: Ковариационная матрица координат в АСК

        :return: Ковариационная матрица в прямоугольной декартовой СК
        """
        # Обозначения для удобства записи
        matrix_a = self.fixed_part_data.transform_matrix
        matrix_b = self.mobile_part_data.transform_matrix
        matrix_f = matrix_a.transpose() @ matrix_b.transpose()
        # Ковариационная матрица в декартовых координатах равна B'*A'*K_acs*A*B
        covariance_matrix_dec = matrix_f @ covariance_matrix_acs @ matrix_f.transpose()
        return covariance_matrix_dec
