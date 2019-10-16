from math import exp, sqrt, log10, fabs, pi, e

import numpy as np


# Класс для фильтрации биконических координат
class FilterAB:
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

    # Основной алгоритм работы
    def operate(self):
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

    # Вычисление относительной интенсивности манёвра
    def calc_manoeuvre_level(self):
        # Ускорение свободного падения
        g_earth = 9.80665
        # Относительная интенсивность манёвра
        manoeuvre_level = 2 * self.manoeuvre_overload * g_earth * self.frame_time ** 2 / pi
        # Дальность до цели
        target_range = self.current_data.measure_coordinates[0]
        # Вычисление интенсивности манёвра по каждой координате
        manoeuvre_level_r = manoeuvre_level / self.current_data.sigma_bcs[0]
        manoeuvre_level_phi_v = manoeuvre_level / (self.current_data.sigma_bcs[1] * target_range)
        manoeuvre_level_phi_n = manoeuvre_level / (self.current_data.sigma_bcs[2] * target_range)
        self.manoeuvre_level_array = np.array([manoeuvre_level_r, manoeuvre_level_phi_v, manoeuvre_level_phi_n])

    # Вычисление коэффициентов alpha, beta для каждого такта фильтрации
    def calc_alpha_beta(self):
        # Если фильтр только начал работу (нет скорости и экстраполированных значений с пред. такта)
        if self.counter < 2:
            self.alpha_array = np.array([1, 1, 1])
            self.beta_array = np.array([1, 1, 1])
        else:
            # По всем интенсивностям манёвра в биконических координатах формируем коэфф. alpha и beta
            alpha_list = []
            beta_list = []
            for manoeuvre_level in self.manoeuvre_level_array:
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
                # Добавление результата в вектор по каждой биконической координате
                alpha_list.append(alpha)
                beta_list.append(beta)
            # Формировать так numpy массив быстрее, чем np.append
            self.alpha_array = np.array(alpha_list)
            self.beta_array = np.array(beta_list)

    # Alpha-Beta фильтрация координат и производных
    def filtrate_coord_and_vel(self):
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

    # Экстраполяция координат и скорости на следующий шаг
    def extrapolate_coord_and_vel(self):
        # Оценка координат на текущий шаг
        est_coord = self.current_data.estimate_coordinates
        # Оценка скорости на текущий шаг
        est_vel = self.current_data.estimate_velocities
        # Экстраполяция координат на след. шаг
        self.prolong_data.extrapolate_coordinates = est_coord + self.frame_time * est_vel
        # Эктсраполяция скорости на след. шаг
        self.prolong_data.extrapolate_velocities = est_vel

    # Вычисление ошибок фильтра
    def calculate_sigma(self):
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

    # Завершение текущего шага работы фильтра
    def increment_filter(self):
        self.increment_data()
        self.increment_counter()

    # Смещение данных фильтра
    def increment_data(self):
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

    # Инкремент шага фильтра
    def increment_counter(self):
        self.counter += 1


# Класс описывающий данные по трассе цели на предыдущий шаг
class PreviousTrackData:
    __slots__ = ("covariance_est_coord_vel",
                 "variance_estimate_velocities")

    def __init__(self):
        # Ковариация оценок координат и скорости
        self.covariance_est_coord_vel = np.zeros(3)
        # Дисперсии оценки скоростей
        self.variance_estimate_velocities = np.zeros(3)


# Класс описывающий данные по цели на текущий шаг
class CurrentTrackData:
    __slots__ = ("measure_coordinates",
                 "estimate_coordinates",
                 "estimate_velocities",
                 "extrapolate_coordinates",
                 "extrapolate_velocities",
                 "sigma_bcs",
                 "variance_estimate_coordinates",
                 "variance_extrapolate_coordinates",
                 "covariance_est_coord_vel",
                 "variance_estimate_velocities")

    def __init__(self):
        # Измеренные координаты
        self.measure_coordinates = np.zeros(3)
        # Оцененные координаты
        self.estimate_coordinates = np.zeros(3)
        # Оцененные скорости
        self.estimate_velocities = np.zeros(3)
        # Эктсраполированные координаты
        self.extrapolate_coordinates = np.zeros(3)
        # Экстраполирвоанные скорости
        self.extrapolate_velocities = np.zeros(3)
        # Вектор СКО измерений
        self.sigma_bcs = np.zeros(3)
        # Дисперсии оценки координат
        self.variance_estimate_coordinates = np.zeros(3)
        # Дисперсии экстраполированных координат
        self.variance_extrapolate_coordinates = np.zeros(3)
        # Ковариация оценок координат и скорости
        self.covariance_est_coord_vel = np.zeros(3)
        # Дисперсии оценки скоростей
        self.variance_estimate_velocities = np.zeros(3)


# Класс, содержащий данные по цели на следующий шаг
class ProlongTrackData:
    __slots__ = ("extrapolate_coordinates",
                 "extrapolate_velocities",
                 "variance_extrapolate_coordinates")

    def __init__(self):
        # Экстраполированные координаты
        self.extrapolate_coordinates = np.zeros(3)
        # Эктстраполированная скорость
        self.extrapolate_velocities = np.zeros(3)
        # Дисперсия экстраполированных координат
        self.variance_extrapolate_coordinates = np.zeros(3)
