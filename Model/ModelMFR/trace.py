import numpy as np
import numpy.random as rand
from numpy import ndarray

from filter_alpha_beta import FilterAB
from model_time import time_in_tick
from source_trace import SourceTrace
from target import Target


# Класс для хранения данных по трассе одной цели
# ПБУ работает с членом этого класса source_trace
class Trace:
    def __init__(self, target: Target, mfr_number: int, mfr_stable_point: ndarray):
        # Текущее время в тиках
        self.estimate_tick = 0.
        # Цель
        self.target = target
        # Признак пеленга
        self.is_bearing = target.is_anj[mfr_number]
        # Тип сопровождения
        self.is_auto_tracking = target.is_auto_tracking[mfr_number]
        # Априорная дальность (для постановщика АШП)
        self.default_range = 50000.
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

    def measure(self, real_coord_bcs: ndarray, sig_meas_bcs: ndarray):
        # Время измерения координат целей
        self.estimate_tick = self.target.ticks
        # Обновление информации о ошибках измерения
        self.variance_bcs_data.update_errors_measure_data(sig_meas_bcs)
        # Измерение координат цели как нормально распредлённая величина с СКО, заданным МФР
        self.coordinates_data.measure_coordinates_bcs = rand.normal(real_coord_bcs, sig_meas_bcs)
        # Если пеленг, то измерение дальности невозможно: вместо него априорная дальность
        if self.is_bearing:
            self.coordinates_data.measure_coordinates_bcs[0] = self.default_range

    # Алгоритм работы с собственным фильтром трассы
    def filtrate(self):
        # Обновление информации в фильтре
        self.update_filter_data()
        # Запуск работы фильтра
        self.run_filter()
        # Обновление данных трассы результатами работы фильтра
        self.update_self_data()

    # Обновление информации в фильтре
    def update_filter_data(self):
        # Обновление информации о текущем измерении трассы
        self.filter.current_data.measure_coordinates = self.coordinates_data.measure_coordinates_bcs
        # Обновление информации о СКО единичных измерений
        self.filter.current_data.sigma_bcs = self.variance_bcs_data.sigma_measure_coordinates

    # Запуск работы фильтра
    def run_filter(self):
        self.filter.operate()

    # Обновление данных трассы результатами работы фильтра
    def update_self_data(self):
        # Координаты
        self.coordinates_data.measure_coordinates_bcs = self.filter.current_data.measure_coordinates
        self.coordinates_data.estimate_coordinates_bcs = self.filter.current_data.estimate_coordinates
        self.coordinates_data.extrapolate_coordinates_bcs = self.filter.current_data.extrapolate_coordinates
        # Скорость
        self.velocities_data.extrapolate_velocities_bcs = self.filter.current_data.extrapolate_velocities
        # Дисперсии
        self.variance_bcs_data.variance_estimate_coordinates = self.filter.current_data.variance_estimate_coordinates
        self.variance_bcs_data.variance_extrapolate_coordinates = self.filter.current_data.variance_extrapolate_coordinates

    # Рассчёт координат и скоростей в МЗСК МФР
    def calculate_dec_coord_and_vel(self, calc_func):
        # Вычисление координат
        meas_coord, ext_vel = calc_func(self.coordinates_data.measure_coordinates_bcs,
                                        self.velocities_data.extrapolate_velocities_bcs)
        est_coord, _ = calc_func(self.coordinates_data.estimate_coordinates_bcs,
                                 self.velocities_data.extrapolate_velocities_bcs)
        ext_coord, _ = calc_func(self.coordinates_data.extrapolate_coordinates_bcs,
                                 self.velocities_data.extrapolate_velocities_bcs)
        # Запись полученных значений
        self.coordinates_data.measure_coordinates_dec = meas_coord
        self.coordinates_data.estimate_coordinates_dec = est_coord
        self.coordinates_data.extrapolate_coordinates_dec = ext_coord
        self.velocities_data.extrapolate_velocities_dec = ext_vel

    # Расчёт ковариационных матриц в МЗСК МФР
    def calculate_dec_covariance_matrix(self, calc_func):
        # Вычисление ковариационных матриц
        measure_covariance_matrix = calc_func(np.diag(self.variance_bcs_data.variance_measure_coordinates),
                                              self.coordinates_data.measure_coordinates_bcs)
        estimate_covariance_matrix = calc_func(np.diag(self.variance_bcs_data.variance_estimate_coordinates),
                                               self.coordinates_data.estimate_coordinates_bcs)
        extrapolate_covariance_matrix = calc_func(np.diag(self.variance_bcs_data.variance_extrapolate_coordinates),
                                                  self.coordinates_data.extrapolate_coordinates_bcs)
        # Запись полученных значений
        self.covariance_matrix_data.measure_covariance_matrix = measure_covariance_matrix
        self.covariance_matrix_data.estimate_covariance_matrix = estimate_covariance_matrix
        self.covariance_matrix_data.extrapolate_covariance_matrix = extrapolate_covariance_matrix

    # Обновление данных трассы источника (для использования ПБУ)
    def update_source_trace(self):
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


# Класс для хранения данных по координатам
class TraceCoordinatesData:
    def __init__(self):
        # Измеренные координаты цели
        self.measure_coordinates_bcs = np.zeros(3)
        self.measure_coordinates_dec = np.zeros(3)
        # Оценка координат цели
        self.estimate_coordinates_bcs = np.zeros(3)
        self.estimate_coordinates_dec = np.zeros(3)
        # Экстраполированные координаты цели
        self.extrapolate_coordinates_bcs = np.zeros(3)
        self.extrapolate_coordinates_dec = np.zeros(3)


# Класс для хранения данных по скоростям
class TraceVelocitiesData:
    def __init__(self):
        # Экстраполированная скорость цели
        self.extrapolate_velocities_bcs = np.zeros(3)
        self.extrapolate_velocities_dec = np.zeros(3)


# Класс для хранения дисперсий в биконическиой системе координат
class TraceVarianceBCSData:
    def __init__(self):
        # Вектор СКО измеренных координат
        self.sigma_measure_coordinates = np.zeros(3)
        # Вектор дисперсий измеренных координат
        self.variance_measure_coordinates = np.zeros(3)
        # Вектор дисперсий оцененных координат
        self.variance_estimate_coordinates = np.zeros(3)
        # Вектор дисперсий экстраполированных координат
        self.variance_extrapolate_coordinates = np.zeros(3)

    def update_errors_measure_data(self, sigma_meas_bcs):
        self.sigma_measure_coordinates = sigma_meas_bcs
        self.variance_measure_coordinates = sigma_meas_bcs ** 2


# Класс для хранения данных по ковариационным матрицам в декартовых координатах МФР
class TraceCovarianceMatrixData:
    def __init__(self):
        # Ковариационная матрица измеренных координат
        self.measure_covariance_matrix = np.zeros((3, 3))
        # Ковариационная матрица оценки координат
        self.estimate_covariance_matrix = np.zeros((3, 3))
        # Ковариационная матрица экстраполированных координат
        self.extrapolate_covariance_matrix = np.zeros((3, 3))
