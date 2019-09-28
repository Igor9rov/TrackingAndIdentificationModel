from numpy import ndarray

from surveillance_data import SurveillanceData
from target import Target
from trace import Trace


# Класс, описывающий работу МФР
class MultiFunctionalRadar:
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

    # Основной алгоритм работы
    def operate(self, ticks: int):
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

    # Алгоритм обновления массива трасс
    # Удаляет трассы по тем целям, которые нельзя сопровождать
    # Добавляет трассы по целям, которые можно сопровождать, если трассы не было
    def update_trace_list(self):
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

    # Добавление трассы по цели, по которой не было трассы
    def append_trace_for_target(self, target: Target):
        # Если не было трассы по такой цели
        if not any(target is trace.target for trace in self.trace_list):
            # то добавить трассу
            self.trace_list.append(Trace(target, self.number, self.stable_point))

    # Удаление трассы по цели
    def remove_trace_for_target(self, target: Target):
        self.trace_list = list(filter(lambda trace: trace.target is not target, self.trace_list))

    # Алгоритм сопровождения
    def tracking(self):
        for trace in self.trace_list:
            # В зависимости от темпа сопровождения
            if not self.tick % trace.frame_tick:
                # Измерение
                self.create_measurement(trace)
                # Фильтрация
                trace.filtrate()
                # Пересчёт в декартовые координаты
                self.calculate_trace_to_dec(trace)

    # Измерение координат целей
    def create_measurement(self, trace: Trace):
        # Пересчёт координат и производных реального положения цели
        real_target_coordinates = trace.target.coordinates - self.stable_point
        # Выбор функции для пересчёта
        dec2bcs = self.surveillance_data.position_antenna_data.dec2bcs
        real_coord_bcs, real_velocity_bcs = dec2bcs(real_target_coordinates, trace.target.velocities)
        # Измерение координат цели как нормально распредлённая величина с СКО, заданным МФР
        trace.measure(real_coord_bcs, self.surveillance_data.sigma_bcs)

    # Пересчёт координат и ковариационных матриц в МЗСК МФР
    def calculate_trace_to_dec(self, trace: Trace):
        # Выбор функции для пересчёта координат и скоростей
        bcs2dec = self.surveillance_data.position_antenna_data.bcs2dec
        # Расчёт координат, скоростей в МЗСК МФР
        trace.calculate_dec_coord_and_vel(bcs2dec)
        # Выбор функциия для пересчёта ковариационных матриц
        calc_dec_matrix = self.surveillance_data.position_antenna_data.calc_dec_covariance_matrix_from_bcs
        # Расчёт ковариационных матриц в МЗСК МФР
        trace.calculate_dec_covariance_matrix(calc_dec_matrix)

    def update_source_traces(self):
        for trace in self.trace_list:
            trace.update_source_trace()
