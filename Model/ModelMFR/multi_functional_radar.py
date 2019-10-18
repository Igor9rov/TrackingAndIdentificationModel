from numpy import ndarray

from surveillance_data import SurveillanceData
from target import Target
from trace import Trace


class MultiFunctionalRadar:
    """
    Класс, описывающий работу МФР
    """
    __slots__ = ("start_tick",
                 "tick",
                 "number",
                 "stable_point",
                 "surveillance_data",
                 "target_list",
                 "trace_list",
                 "mfr_registration")

    def __init__(self, stable_point: ndarray, mfr_number: int, target_list: list):
        # Время начала работы МФР
        self.start_tick = 0.
        # Текущее время в тиках
        self.tick = 0.
        # Номер МФР
        self.number = mfr_number
        # Координаты МФР
        self.stable_point = stable_point
        # Параметры обзора
        self.surveillance_data = SurveillanceData()
        # Массив целей, которых пытается сопровождать МФР
        self.target_list = target_list
        # Массив трасс
        self.trace_list = [Trace(trg, self.number, self.stable_point) for trg in target_list]
        # Массив информации о каждой трассе этого МФР
        self.mfr_registration = []

    def operate(self, ticks: int):
        """
        Основной алгоритм работы
        :param ticks: Текущее время в тиках
        :return: None
        """
        # Текущее время в тиках
        self.tick = ticks - self.start_tick
        if self.tick >= 0:
            # Обновление параметров положения антенны, а именно матриц поворота
            self.surveillance_data.calculate_position_antenna_data()
            # Добавление или удаление трасс из состава трасс МФР
            self.update_trace_list()
            # Сопровождение целей: измерение, фильтрация, пересчёт в МЗСК МФР
            self.tracking()
            # Формирование сообщений на ПБУ
            self.update_source_traces()
            self.registration()

    def update_trace_list(self):
        """
        Алгоритм обновления массива трасс
        Удаляет трассы по тем целям, которые нельзя сопровождать
        Добавляет трассы по целям, которые можно сопровождать, если трассы не было
        :return: None
        """
        # Цикл по всем целям
        for target in self.target_list:
            # Проверка на возможность сопровождения
            # Координаты цели в системе координат МФР
            real_target_coordinates = target.coordinates - self.stable_point
            # Если можно сопровождать
            if self.surveillance_data.validate_tracking(real_target_coordinates):
                # то добавить трассу, если не было трассы по такой цели
                self.append_trace_for_target(target)
            else:
                # Если сопровождать нельзя, а трасса по такой цели есть, то удалить трассу
                self.remove_trace_for_target(target)

    def append_trace_for_target(self, target: Target):
        """
        Добавление трассы по цели, по которой не было трассы
        :param target: Цель, по которой хотим создать трассу
        :return: None
        """
        # Если не было трассы по такой цели
        if not any(target is trace.target for trace in self.trace_list):
            # то добавить трассу
            self.trace_list.append(Trace(target, self.number, self.stable_point))

    def remove_trace_for_target(self, target: Target):
        """
        Удаление трассы по цели
        :param target: Цель
        :return: None
        """
        self.trace_list = list(filter(lambda trace: trace.target is not target, self.trace_list))

    def tracking(self):
        """
        Алгоритм сопровождения
        :return: None
        """
        for trace in self.trace_list:
            # В зависимости от темпа сопровождения
            if not self.tick % trace.frame_tick:
                # Измерение
                self.create_measurement(trace)
                # Фильтрация
                trace.filtrate()
                # Пересчёт в декартовые координаты
                self.calculate_trace_to_dec(trace)

    def create_measurement(self, trace: Trace):
        """
        Измерение координат целей
        :param trace: Трасса цели
        :return: None
        """
        # Пересчёт координат и производных реального положения цели
        real_target_coordinates = trace.target.coordinates - self.stable_point
        # Выбор функции для пересчёта
        dec2bcs = self.surveillance_data.position_antenna_data.dec2bcs
        real_coord_bcs, real_velocity_bcs = dec2bcs(real_target_coordinates, trace.target.velocities)
        # Измерение координат цели как нормально распредлённая величина с СКО, заданным МФР
        trace.measure(real_coord_bcs, self.surveillance_data.sigma_bcs)

    def calculate_trace_to_dec(self, trace: Trace):
        """
        Пересчёт координат и ковариационных матриц в МЗСК МФР
        :param trace: Трасса цели
        :return: None
        """
        # Выбор функции для пересчёта координат и скоростей
        bcs2dec = self.surveillance_data.position_antenna_data.bcs2dec
        # Расчёт координат, скоростей в МЗСК МФР
        trace.calculate_dec_coord_and_vel(bcs2dec)
        # Выбор функциия для пересчёта ковариационных матриц
        calc_dec_matrix = self.surveillance_data.position_antenna_data.calc_dec_covariance_matrix_from_bcs
        # Расчёт ковариационных матриц в МЗСК МФР
        trace.calculate_dec_covariance_matrix(calc_dec_matrix)

    def update_source_traces(self):
        """
        Обновление данных трасс источника, которыми пользуется ПБУ
        :return: None
        """
        for trace in self.trace_list:
            # В зависимости от темпа сопровождения
            if not self.tick % trace.frame_tick:
                trace.update_source_trace()

    def registration(self):
        # Цикл по всем целям
        for trace in self.trace_list:
            # В зависимости от темпа сопровождения
            if not self.tick % trace.frame_tick:
                # TODO: Ну не target же..
                target = trace.source_trace
                # TODO: x, y, z = array.tolist()
                x, y, z = target.coordinates[0], target.coordinates[1], target.coordinates[2]
                v_x, v_y, v_z = target.velocities[0], target.velocities[1], target.velocities[2]
                var_x = target.coordinate_covariance_matrix[0][0]
                var_y = target.coordinate_covariance_matrix[1][1]
                var_z = target.coordinate_covariance_matrix[2][2]
                cov_xy = target.coordinate_covariance_matrix[0][1]
                cov_xz = target.coordinate_covariance_matrix[0][2]
                cov_yz = target.coordinate_covariance_matrix[1][2]
                # TODO: Выкинуть в отдельную переменную моссив для регистрации
                self.mfr_registration.append([self.tick, self.number, target.target_number, x, y, z, v_x, v_y, v_z,
                                              var_x, var_y, var_z, cov_xy, cov_xz, cov_yz, target.is_bearing])

