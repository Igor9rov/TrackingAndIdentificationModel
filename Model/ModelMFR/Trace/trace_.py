import numpy as np
import numpy.random as rand
from numpy import ndarray

from coordinate_system_math import dec2sph, sph2dec
from filter_alpha_beta import FilterAB
from model_time import time_in_tick
from source_trace import SourceTrace
from target import Target
from trace_coordinates_data import TraceCoordinatesData
from trace_covariance_matrix_data import TraceCovarianceMatrixData
from trace_variance_bcs_data import TraceVarianceBCSData
from trace_velocities_data import TraceVelocitiesData


class Trace:
    """Класс для хранения данных по трассе одной цели"""
    __slots__ = ("estimate_tick",
                 "target",
                 "is_bearing",
                 "is_auto_tracking",
                 "default_range",
                 "frame_tick",
                 "filter",
                 "coordinates_data",
                 "velocities_data",
                 "variance_bcs_data",
                 "covariance_matrix_data",
                 "source_trace")

    def __init__(self, target: Target, mfr_number: int, mfr_stable_point: ndarray) -> None:
        # Текущее время в тиках
        self.estimate_tick = 0
        # Цель
        self.target = target
        # Признак пеленга
        self.is_bearing = target.is_anj[mfr_number]
        # Тип сопровождения
        self.is_auto_tracking = target.is_auto_tracking[mfr_number]
        # Априорная дальность (для постановщика АШП)
        self.default_range = 50_000.
        # Временных тиков между измерениями
        self.frame_tick = 2 if self.is_auto_tracking else 20
        frame_time = self.frame_tick * time_in_tick
        # Собственный фильтр
        self.filter = FilterAB(frame_time, manoeuvre_overload=4)
        # Данные по координатам
        self.coordinates_data = TraceCoordinatesData()
        # Данные по скоростям
        self.velocities_data = TraceVelocitiesData()
        # Данные по дисперсиям в БСК
        self.variance_bcs_data = TraceVarianceBCSData()
        # Данные по ковариационным матрицам
        self.covariance_matrix_data = TraceCovarianceMatrixData()
        # Трасса источника (для пользования ПБУ)
        self.source_trace = SourceTrace(mfr_number, mfr_stable_point, target.number)

    def __repr__(self) -> str:
        return f"Трасса по цели с номером {self.target.number!r}." \
               f"Объект класса {self.__class__.__name__} по адресу в памяти {hex(id(self))}"

    def measure(self, real_coord_bcs: ndarray, sig_meas_bcs: ndarray) -> None:
        """Производит измерение координат цели, как нормально распределённую величинус известным распредлением

        :param real_coord_bcs: Настоящие координаты цели в БСК
        :type real_coord_bcs: ndarray
        :param sig_meas_bcs: Сигмы измерений координат в БСК
        :type sig_meas_bcs: ndarray

        :return: None
        """
        # Время измерения координат целей
        self.estimate_tick = self.target.ticks
        # Обновление информации о ошибках измерения
        self.variance_bcs_data.update_errors_measure_data(sig_meas_bcs)
        # Измерение координат цели как нормально распредлённая величина с СКО, заданным МФР
        self.coordinates_data.measure_coordinates_bcs = rand.normal(real_coord_bcs, sig_meas_bcs)
        # Если пеленг, то измерение дальности невозможно: вместо него априорная дальность
        if self.is_bearing:
            self.coordinates_data.measure_coordinates_bcs[0] = self.default_range

    def filtrate(self) -> None:
        """Работа с собственным фильтром трассы

        :return: None
        """
        # Обновление информации в фильтре
        self.update_filter_data()
        # Запуск работы фильтра
        self.run_filter()
        # Обновление данных трассы результатами работы фильтра
        self.update_self_data()

    def update_filter_data(self) -> None:
        """Обновление информации в фильтре

        :return: None
        """
        # Обновление информации о текущем измерении трассы
        self.filter.current_data.measure_coordinates = self.coordinates_data.measure_coordinates_bcs
        # Обновление информации о СКО единичных измерений
        self.filter.current_data.sigma_bcs = self.variance_bcs_data.sigma_measure_coordinates

    def run_filter(self) -> None:
        """Запуск работы фильтра

        :return: None
        """
        self.filter.operate()

    def update_self_data(self) -> None:
        """Обновление данных трассы результатами работы фильтра

        :return: None
        """
        # Текущие данные от фильтра
        current_data = self.filter.current_data
        # Координаты
        self.coordinates_data.measure_coordinates_bcs = current_data.measure_coordinates
        self.coordinates_data.estimate_coordinates_bcs = current_data.estimate_coordinates
        self.coordinates_data.extrapolate_coordinates_bcs = current_data.extrapolate_coordinates
        # Скорость
        self.velocities_data.extrapolate_velocities_bcs = current_data.extrapolate_velocities
        # Дисперсии
        self.variance_bcs_data.variance_estimate_coordinates = current_data.variance_estimate_coordinates
        self.variance_bcs_data.variance_extrapolate_coordinates = current_data.variance_extrapolate_coordinates

    def calculate_dec_coord_and_vel(self, func, residuals: [None, ndarray]) -> None:
        """Расчёт координат и скоростей в МЗСК МФР

        :param func: Функция для пересчёта координат из БСК в декартовую прямоугольную СК
        :param residuals: Вектор поправок для сферических координат МФР, в начальный момент времени None,
        позже, после совместной юстировки принимает некоторое вычисленное в ПБУ значение
        :type residuals: ndarray

        :return: None
        """
        # Данные о координатах
        coordinates_data = self.coordinates_data
        # Экстраполированная скорость
        extrapolate_velocities_bcs = self.velocities_data.extrapolate_velocities_bcs
        # Вычисление координат
        meas_coord, ext_vel = func(coordinates_data.measure_coordinates_bcs, extrapolate_velocities_bcs)
        est_coord, _ = func(coordinates_data.estimate_coordinates_bcs, extrapolate_velocities_bcs)
        ext_coord, _ = func(coordinates_data.extrapolate_coordinates_bcs, extrapolate_velocities_bcs)

        # Запись полученных значений
        # Для координат в зависимости от наличия поправки
        coordinates_data.measure_coordinates_dec = self.calc_with_residuals(meas_coord, residuals)
        coordinates_data.estimate_coordinates_dec = self.calc_with_residuals(est_coord, residuals)
        coordinates_data.extrapolate_coordinates_dec = self.calc_with_residuals(ext_coord, residuals)
        # Скорость не зависит от поправок
        self.velocities_data.extrapolate_velocities_dec = ext_vel

    @staticmethod
    def calc_with_residuals(coord: ndarray, residuals: [None, ndarray]) -> ndarray:
        """Вычисляет координаты с учетом поправок в сферической СК МФР

        :param coord: Координаты в декартовой прямоугольной МЗСК МФР
        :type coord: ndarray
        :param residuals: Вектор поправок для сферических координат
        :type residuals: ndarray или None
        :return: Координаты в декартовой прямоугольной МЗСК МФР
        :rtype: ndarray
        """
        return coord if residuals is None else sph2dec(dec2sph(coord) - residuals)

    def calculate_dec_covariance_matrix(self, func):
        """Расчёт ковариационных матриц в МЗСК МФР

        :param func: Функция для перехода от ковариационной матрицы в БСК к матрице в декартовой прямоугольной СК

        :return: None
        """
        # Вычисление ковариационных матриц
        measure_covariance_matrix = func(np.diag(self.variance_bcs_data.variance_measure_coordinates),
                                         self.coordinates_data.measure_coordinates_bcs)
        estimate_covariance_matrix = func(np.diag(self.variance_bcs_data.variance_estimate_coordinates),
                                          self.coordinates_data.estimate_coordinates_bcs)
        extrapolate_covariance_matrix = func(np.diag(self.variance_bcs_data.variance_extrapolate_coordinates),
                                             self.coordinates_data.extrapolate_coordinates_bcs)
        # Запись полученных значений
        self.covariance_matrix_data.measure_covariance_matrix = measure_covariance_matrix
        self.covariance_matrix_data.estimate_covariance_matrix = estimate_covariance_matrix
        self.covariance_matrix_data.extrapolate_covariance_matrix = extrapolate_covariance_matrix

    def update_source_trace(self) -> None:
        """Обновление данных трассы источника (для использования ПБУ)

        :return: None
        """
        source_trace = self.source_trace
        # Признак АС
        source_trace.is_auto_tracking = self.is_auto_tracking
        # Координаты цели
        source_trace.coordinates = self.coordinates_data.estimate_coordinates_dec + self.source_trace.mfr_position
        # Скорость цели
        source_trace.velocities = self.velocities_data.extrapolate_velocities_dec
        # Время оценки данных трассы
        source_trace.estimate_tick = self.estimate_tick
        # Признак помехи
        source_trace.is_bearing = self.is_bearing
        # Ковариционная матрица координат
        source_trace.coordinate_covariance_matrix = self.covariance_matrix_data.extrapolate_covariance_matrix
