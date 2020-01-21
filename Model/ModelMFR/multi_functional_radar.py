import numpy as np
from numpy import ndarray

from errors_namedtuple import SurveillanceErrors
from surveillance_data import SurveillanceData
from target import Target
from trace_ import Trace


class MultiFunctionalRadar:
    """Класс, описывающий работу МФР"""
    __slots__ = ("start_tick",
                 "tick",
                 "number",
                 "stable_point",
                 "is_adjustment",
                 "residuals",
                 "surveillance_data",
                 "target_list",
                 "trace_list",
                 "registration")

    def __init__(self,
                 target_list: list,
                 stable_point: ndarray = np.zeros(3),
                 mfr_number: int = 1,
                 errors: SurveillanceErrors = SurveillanceErrors(0, 0)) -> None:
        # Время начала работы МФР
        self.start_tick = 0.
        # Текущее время в тиках
        self.tick = 0.
        # Номер МФР
        self.number = mfr_number
        # Точка стояния
        self.stable_point = stable_point
        # Признак юстированности
        self.is_adjustment = True if self.number == 1 else False
        # Вектор поправок
        self.residuals = None
        # Параметры обзора
        self.surveillance_data = SurveillanceData(errors)
        # Массив целей, которых пытается сопровождать МФР
        self.target_list = target_list
        # Массив трасс
        self.trace_list = [Trace(target=trg,
                                 mfr_number=self.number,
                                 mfr_stable_point=self.stable_point) for trg in target_list]
        # Массив информации о каждой трассе этого МФР
        self.registration = []

    def __repr__(self) -> str:
        return f"МФР c номером {self.number!r}, c точкой стояния {self.stable_point!r}. " \
               f"Объект класса {self.__class__.__name__} по адресу в памяти {hex(id(self))}"

    def operate(self, ticks: int) -> None:
        """Основной алгоритм работы

        :param ticks: Текущее время в тиках
        :type ticks: int

        :return: None
        """
        # Текущее время в тиках
        self.tick = ticks - self.start_tick
        if self.tick >= 0:
            # Добавление или удаление трасс из состава трасс МФР
            self.update_trace_list()
            # Сопровождение целей: измерение, фильтрация, пересчёт в МЗСК МФР
            self.tracking()
            # Формирование сообщений на ПБУ
            self.update_source_traces()
            # Регистрация нужных переменных
            self.register()

    def update_trace_list(self) -> None:
        """Алгоритм обновления массива трасс
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

    def append_trace_for_target(self, target: Target) -> None:
        """Добавление трассы по цели, по которой не было трассы

        :param target: Цель, по которой хотим создать трассу
        :type target: Target

        :return: None
        """
        # Если не было трассы по такой цели
        if not any(target is trace.target for trace in self.trace_list):
            # то добавить трассу
            self.trace_list.append(Trace(target=target,
                                         mfr_number=self.number,
                                         mfr_stable_point=self.stable_point))

    def remove_trace_for_target(self, target: Target) -> None:
        """Удаление трассы по цели

        :param target: Цель, по которой хотим удалить трассу
        :type target: Target

        :return: None
        """
        self.trace_list = list(filter(lambda trace: trace.target is not target, self.trace_list))

    def tracking(self) -> None:
        """Алгоритм сопровождения

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

    def create_measurement(self, trace: Trace) -> None:
        """Измерение координат целей

        :param trace: Трасса цели
        :type trace: Trace

        :return: None
        """
        # Пересчёт координат и производных реального положения цели в прямоугольную декартовую МЗСК МФР
        coordinates_dec = trace.target.coordinates - self.stable_point
        velocities_dec = trace.target.velocities

        # Пересчёт координат и производных реального положения цели в БСК МФР
        dec2bcs = self.surveillance_data.position_antenna_data.dec2bcs
        coordinates_bcs, velocities_bcs = dec2bcs(coordinates_dec, velocities_dec)

        # Выбор СКО для координат в БСК
        sigma_bcs = self.surveillance_data.sigma_bcs

        # Измерение биконических координат цели, каждая из которых - нормально распредлённая величина
        trace.measure(coordinates_bcs, sigma_bcs)

    def calculate_trace_to_dec(self, trace: Trace) -> None:
        """Пересчёт координат и ковариационных матриц в МЗСК МФР

        :param trace: Трасса цели
        :type trace: Trace

        :return: None
        """
        # Выбор функции для пересчёта координат и скоростей
        bcs2dec = self.surveillance_data.position_antenna_data.bcs2dec
        # Расчёт координат и скоростей в декартовой прямоугольной МЗСК МФР, c учетом поправок
        trace.calculate_dec_coord_and_vel(bcs2dec, self.residuals)

        # Выбор функциия для пересчёта ковариационных матриц
        bsc2dec_for_matrix = self.surveillance_data.position_antenna_data.calc_dec_covariance_matrix_from_bcs
        # Расчёт ковариационных матриц в декартовой прямоугольной МЗСК МФР
        trace.calculate_dec_covariance_matrix(bsc2dec_for_matrix)

    def update_source_traces(self) -> None:
        """Обновление данных трасс источника, которыми пользуется ПБУ

        :return: None
        """
        for trace in self.trace_list:
            # В зависимости от темпа сопровождения
            if not self.tick % trace.frame_tick:
                trace.update_source_trace()

    def register(self) -> None:
        """Регистрация работы МФР

        :return: None
        """
        # Цикл по всем трассам
        for trace in self.trace_list:
            # В зависимости от темпа сопровождения
            if not self.tick % trace.frame_tick:
                # Хотим регистрировать следующее:
                registration_row = [self.tick, self.number, self.is_adjustment, *trace.target.registration, *trace.source_trace.registration]
                self.registration.append(registration_row)
