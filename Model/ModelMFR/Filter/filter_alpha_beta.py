from math import exp, sqrt, log10, fabs, pi, e

import numpy as np

from previous_track_data import PreviousTrackData
from prolong_track_data import ProlongTrackData
from сurrent_track_data import CurrentTrackData


class FilterAB:
    """
    Класс для фильтрации биконических координат
    """
    __slots__ = ("counter",
                 "frame_time",
                 "manoeuvre_overload",
                 "manoeuvre_level_array",
                 "alpha_array",
                 "beta_array",
                 "previous_data",
                 "current_data",
                 "prolong_data")

    def __init__(self, frame_time: int, manoeuvre_overload: float):
        # Счётчик фильтра
        self.counter = 0
        # Время между сопровождением в секундах
        self.frame_time = frame_time
        # Перегрузка при манёвре цели (длинный 0.4-0.2, короткий 9-4))
        self.manoeuvre_overload = manoeuvre_overload
        # Интенсивность манёвра
        self.manoeuvre_level_array = np.zeros(3)
        # Массив коэфф. alpha
        self.alpha_array = np.zeros(3)
        # Массив коэфф. beta
        self.beta_array = np.zeros(3)
        # Данные фильтра на предыдущий такт сопровождения
        self.previous_data = PreviousTrackData()
        # Данные фильтра на текущий такт сопровождения
        self.current_data = CurrentTrackData()
        # Данные фильтра на следующий такт сопровождения
        self.prolong_data = ProlongTrackData()

    def operate(self):
        """
        Основной алгоритм работы, порядок вызова функций важен
        :return: None
        """
        # Оценить интенсивность манёвра
        self.calc_manoeuvre_level()
        # Расчитать коэффициенты alpha и beta
        self.calc_alpha_beta()
        # Фильтрация координат и производных
        self.filtrate_coord_and_vel()
        # Экстраполяция координат и производных
        self.extrapolate_coord_and_vel()
        # Вычисление ошибок фильтра
        self.calculate_sigma()
        # Инкрементация состояния фильтра на следующий шаг
        self.increment_filter()

    def calc_manoeuvre_level(self):
        """
        Вычисление относительной интенсивности манёвра
        :return: None
        """
        # Ускорение свободного падения
        g_earth = 9.80665
        # Относительная интенсивность манёвра
        manoeuvre_level = 2 * self.manoeuvre_overload * g_earth * self.frame_time ** 2 / pi
        # Дальность до цели
        target_range = self.current_data.measure_coordinates[0]
        # Связь между индексами и биконическими кооррдинатами
        r, phi_v, phi_n = 0, 1, 2
        # Вычисление интенсивности манёвра по каждой координате
        self.manoeuvre_level_array[r] = manoeuvre_level / self.current_data.sigma_bcs[r]
        self.manoeuvre_level_array[phi_v] = manoeuvre_level / (self.current_data.sigma_bcs[phi_v] * target_range)
        self.manoeuvre_level_array[phi_n] = manoeuvre_level / (self.current_data.sigma_bcs[phi_n] * target_range)

    def calc_alpha_beta(self):
        """
        Вычисление коэффициентов alpha, beta для каждого такта фильтрации
        :return: None
        """
        # Если фильтр только начал работу (нет скорости и экстраполированных значений с пред. такта)
        if self.counter < 2:
            self.alpha_array = np.ones(3)
            self.beta_array = np.ones(3)
        else:
            # По всем интенсивностям манёвра в биконических координатах формируем коэфф. alpha и beta
            for index, manoeuvre_level in enumerate(self.manoeuvre_level_array):
                # Десятичный логарифм интенсивности манёвра
                lg_manoeuvre_level = log10(manoeuvre_level)
                if lg_manoeuvre_level <= 0.15:
                    alpha = 0.5 * exp(-fabs(lg_manoeuvre_level - 0.15) ** 1.7 / 3.53376)
                    beta = 2 * (1 - alpha - sqrt(1 - 2 * alpha))
                elif 0.15 < lg_manoeuvre_level <= 0.65:
                    alpha = 0.5 * exp(-fabs(lg_manoeuvre_level - 0.15) ** 1.9 / e)
                    beta = 2 * (1 - alpha + sqrt(1 - 2 * alpha))
                else:
                    # Сразу посчитано значение, оно константное
                    alpha = 0.45306574291791984
                    beta = 1.7066278932491654
                # Изменение коэффициента по каждой биконической координате
                self.alpha_array[index] = alpha
                self.beta_array[index] = beta

    def filtrate_coord_and_vel(self):
        """
        Alpha-Beta фильтрация координат и производных
        :return: None
        """
        # Измеренные координаты
        meas_coord = self.current_data.measure_coordinates
        # Экстраполированная оценка координат с прошлого шага
        ext_coord = self.current_data.extrapolate_coordinates
        # TODO: Временно, для обработки начального состояния фильтра, чтобы корректно считалась скорость
        ext_coord = meas_coord if ext_coord.tolist() == np.zeros(3).tolist() else ext_coord
        # Экстраполированная оценка координат с прошлого шага
        ext_vel = self.current_data.extrapolate_velocities
        # Коэффициент alpha
        alpha = self.alpha_array
        # Коэффициент beta
        beta = self.beta_array
        # Время в секундах между сопровождением
        dt = self.frame_time
        # Вычисление оценки координат
        self.current_data.estimate_coordinates = alpha * meas_coord + (1 - alpha) * ext_coord
        # Вычисление оценки скорости
        self.current_data.estimate_velocities = (beta / dt) * (meas_coord - ext_coord) + ext_vel

    def extrapolate_coord_and_vel(self):
        """
        Экстраполяция координат и скорости на следующий шаг
        :return: None
        """
        # Оценка координат на текущий шаг
        est_coord = self.current_data.estimate_coordinates
        # Оценка скорости на текущий шаг
        est_vel = self.current_data.estimate_velocities
        # Экстраполяция координат на след. шаг
        self.prolong_data.extrapolate_coordinates = est_coord + self.frame_time * est_vel
        # Эктсраполяция скорости на след. шаг
        self.prolong_data.extrapolate_velocities = est_vel

    def calculate_sigma(self):
        """
        Вычисление ошибок фильтра
        :return: None
        """
        # Обозначения для упрощения записи
        dt = self.frame_time
        alpha = self.alpha_array
        beta = self.beta_array
        prev_cov_est_coord_vel = self.previous_data.covariance_est_coord_vel
        prev_var_est_vel = self.previous_data.variance_estimate_velocities
        cur_var_ext_coord = self.current_data.variance_extrapolate_coordinates
        # Дисперсия текущего измерения
        cur_var_meas_coord = self.current_data.sigma_bcs ** 2
        # Ковариация экстраполированных на текущий такт координаты и оценки скорости с пред. шага
        cov_ext_coord_est_vel = prev_cov_est_coord_vel + prev_var_est_vel * dt
        # Ковариация оценки координат и скоростей на текущий шаг
        cur_cov_est_coord_vel = alpha * beta * cur_var_meas_coord / dt
        cur_cov_est_coord_vel -= (1-alpha) * beta * cur_var_ext_coord / dt
        cur_cov_est_coord_vel += (1 - alpha) * cov_ext_coord_est_vel
        # Дисперсия оценки оценки скорости на текущий шаг
        cur_var_est_vel = (beta / dt)**2 * (cur_var_meas_coord + cur_var_ext_coord)
        cur_var_est_vel -= 2 * beta * cov_ext_coord_est_vel / dt
        cur_var_est_vel += prev_var_est_vel
        # Дисперсия оценки координат на текущий шаг
        cur_var_est_coord = alpha**2 * cur_var_meas_coord + (1 - alpha)**2 * cur_var_ext_coord
        # Дисперсия экстраполированных координат на следующий такт
        prolong_var_ext_coord = cur_var_est_coord + 2 * cur_cov_est_coord_vel * dt + cur_var_est_vel * dt**2
        # Запись вычисленных значений в фильтр
        self.current_data.covariance_est_coord_vel = cur_cov_est_coord_vel
        self.current_data.variance_estimate_velocities = cur_var_est_vel
        self.current_data.variance_estimate_coordinates = cur_var_est_coord
        self.prolong_data.variance_extrapolate_coordinates = prolong_var_ext_coord

    def increment_filter(self):
        """
        Завершение текущего шага работы фильтра
        :return: None
        """
        self.increment_data()
        self.increment_counter()

    def increment_data(self):
        """
        Смещение данных фильтра
        :return: None
        """
        # Смещение экстраполированных координат со след. шага на текущий
        self.current_data.extrapolate_coordinates = self.prolong_data.extrapolate_coordinates
        # Смещение экстраполированной скорости со след. такта на текущий
        self.current_data.extrapolate_velocities = self.prolong_data.extrapolate_velocities
        # Смещение дисперсии экстраполированных координат со след. шага на текущий
        self.current_data.variance_extrapolate_coordinates = self.prolong_data.variance_extrapolate_coordinates
        # Смещение ковариации оценных координат и скоростей с текущего такта на предыдущий
        self.previous_data.covariance_est_coord_vel = self.current_data.covariance_est_coord_vel
        # Смещение дисперсии оценки скоростей с текущего такта на предыдущий
        self.previous_data.variance_estimate_velocities = self.current_data.variance_estimate_velocities

    def increment_counter(self):
        """
        Инкремент шага фильтра
        :return: None
        """
        self.counter += 1
