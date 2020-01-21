from collections import defaultdict

import numpy as np
from numpy import mean, ndarray

from coordinate_system_math import dec2sph


class ResidualsEstimator:
    """Класс позволяет выполнить совместную юстировку для пары локаторов"""
    def __init__(self, mfr_number_pairs: list) -> None:

        self._ref_num, self._adj_num = mfr_number_pairs

        self._starting_count = 5
        self._max_len = 35

        self._common_residuals_dict = defaultdict(list)
        self._calculation_ready = False
        self._residuals = np.zeros(3)
        self._traces = {}

    def operate(self, source_traces: list) -> bool:
        """Основной алггоритм работы оценщика: формирует словарь, считает поправки, если оценка не готова
        и возращает признак готовности

        :param source_traces: Обычный список с трассами источника
        :type source_traces: list
        :return: Признак окончания работы
        :rtype: bool
        """
        self._create_traces_dict_from(source_traces)
        if not self._calculation_ready:
            self._calculate_residuals()
        return self._calculation_ready

    @property
    def residuals(self) -> ndarray:
        """Обеспечиавает read-only доступ к поправке извне

        :return: Вектор поправок в сферических координатах
        :rtype: ndarray
        """
        return self._residuals

    def _create_traces_dict_from(self, source_traces: list) -> None:
        """Записывает в атрибут _traces по ключу равным номеру МФР
        словарь с ключом равным номеру трассы и значением равным этой трассе

        :param source_traces: Обычный список с трассами источника
        :type source_traces: list
        :return: None
        """
        for num in [self._ref_num, self._adj_num]:
            self._traces[num] = {trace.target_number: trace for trace in source_traces if trace.mfr_number == num}

    def _calculate_residuals(self) -> None:
        """Вычисляет невязки в сферических координатах
        Для каждой общей трассы для эталонного и юстируемого МФР в словаре невязок заводится ключ с номером этой трассы
        По этому ключу находится массив разностей сферических координат.
        Как только длина одного из этих массивов превышает порог, то вычисления останавливаются,
        и в атрибут класса записывается вектор невязок равный МО разности сферических координат

        :return: None
        """
        common_numbers = set(self._traces[self._ref_num].keys()) & set(self._traces[self._adj_num].keys())
        # Для всех общих номеров для пары МФР
        for target_num in common_numbers:
            # Поиск ссылок на трассы от эталонного и юстируемого МФР
            reference_trace = self._traces[self._ref_num][target_num]
            adjustable_trace = self._traces[self._adj_num][target_num]

            reference_coordinates = dec2sph(reference_trace.coordinates - adjustable_trace.mfr_position)
            adjustable_coordinates = dec2sph(adjustable_trace.coordinates - adjustable_trace.mfr_position)

            difference = adjustable_coordinates - reference_coordinates

            difference_array = self._common_residuals_dict[target_num]
            difference_array.append(difference)
            if len(difference_array) >= self._max_len:
                self._residuals = mean(difference_array[self._starting_count:], axis=0)
                self._calculation_ready = True
                break
