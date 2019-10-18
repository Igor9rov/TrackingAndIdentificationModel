from common_trace_array import CommonTraceArray
from source_trace_list import SourceTraceList


class CommandPost:
    """
    Класс, описывающий работу ПБУ
    """
    __slots__ = ("start_tick",
                 "tick",
                 "tick_period",
                 "mfr_list",
                 "source_trace_list",
                 "common_trace_array",
                 "mfr_registration")

    def __init__(self, mfr_list: list):
        # Время начала работы ПБУ
        self.start_tick = 0
        # Собственное время в тиках
        self.tick = 0
        # Период работы ПБУ (20 тиков = 1 секунда)
        self.tick_period = 20
        # Массив МФР
        self.mfr_list = mfr_list
        # Массив трасс источников
        self.source_trace_list = SourceTraceList([])
        # Единый массив трасс
        self.common_trace_array = CommonTraceArray([])
        # Массив информации о каждой трассе этого ПБУ
        # TODO: CP скорее всего, но лучше просто регистрация
        self.mfr_registration = []

    def operate(self, tick: int):
        """
         Основной алгоритм работы
        :param tick: Время в тиках
        :return: None
        """
        # Определение собственного времени
        self.tick = tick - self.start_tick
        # Признак разрешения работы ПБУ (время неотрицательно, темп работы при этом 1 секунда)
        can_operate = not self.tick % self.tick_period and self.tick >= 0
        # Если можно, то ПБУ работает
        if can_operate:
            # Формирование массива трасс источников
            self.formation_source_trace_list()
            # Формирование единого массива трасс
            self.formation_common_trace_array()
            self.registration()

    def formation_source_trace_list(self):
        """
        Формирование массива трасс источников
        :return: None
        """
        initial_list = [trace.source_trace for mfr in self.mfr_list for trace in mfr.trace_list]
        self.source_trace_list.formation(initial_list, self.tick)

    def formation_common_trace_array(self):
        """
        Формирование единого массива трасс
        :return: None
        """
        self.common_trace_array.formation(self.source_trace_list)

    # TODO: Название функции должно быть глаголом, а это имя лучше отдать атрибуту класса
    def registration(self):
        # Цикл по всем трассам ЕМТ
        for cta_trace in self.common_trace_array:
            # TODO: В одной строке реггистрации должна быть информация о трассе ЕМТ, а не о трассе источников,
            #  от трасс источников, в ней должны быть только номера целей и номер ПБУ
            for source_trace in cta_trace.all_source_traces:
                # TODO: Это условие лишнее, в ПБУ данные пишем раз в секунду
                # В зависимости от темпа сопровождения
                frame_tick = 2 if source_trace.is_auto_tracking else 20
                if not self.tick % frame_tick:
                    # TODO: x, y, z = array.tolist() приятнее читать, со скоростями аналогично
                    x, y, z = source_trace.coordinates[0], source_trace.coordinates[1], source_trace.coordinates[2]
                    v_x, v_y, v_z = source_trace.velocities[0], source_trace.velocities[1], source_trace.velocities[2]
                    var_x = source_trace.coordinate_covariance_matrix[0][0]
                    var_y = source_trace.coordinate_covariance_matrix[1][1]
                    var_z = source_trace.coordinate_covariance_matrix[2][2]
                    cov_xy = source_trace.coordinate_covariance_matrix[0][1]
                    cov_xz = source_trace.coordinate_covariance_matrix[0][2]
                    cov_yz = source_trace.coordinate_covariance_matrix[1][2]
                    # TODO: Раз уж избавляемся от упоминания трассы, то действуем до конца
                    # TODO: Регистрация в отдельную переменную
                    self.mfr_registration.append([self.tick, source_trace.mfr_number, source_trace.target_number, x, y, z, v_x, v_y, v_z,
                                                  var_x, var_y, var_z, cov_xy, cov_xz, cov_yz, source_trace.is_bearing])
