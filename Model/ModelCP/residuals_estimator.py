import numpy as np

from coordinate_system_math import dec2sph


class ResidualsEstimator:
    def __init__(self, mfr_number_pairs: list):

        self._ref_num, self._adj_num = mfr_number_pairs

        self._starting_count = 5
        self._max_len = 35

        self._common_residuals_dict = {}
        self._calculation_ready = False
        self._residuals = np.zeros(3)
        self._traces = {}

    def operate(self, source_traces: list):
        self._create_traces_dict_from(source_traces)
        if not self._calculation_ready:
            self._calculate_residuals()
        return self._calculation_ready

    @property
    def residuals(self):
        return self._residuals

    def _create_traces_dict_from(self, source_traces: list):
        for num in [self._ref_num, self._adj_num]:
            self._traces[num] = {trace.target_number: trace for trace in source_traces if trace.mfr_number == num}

    def _calculate_residuals(self):
        common_numbers = set(self._traces[self._ref_num].keys()) & set(self._traces[self._adj_num].keys())
        # Для всех общих номеров для пары МФР
        for target_num in common_numbers:
            # Поиск ссылок на трассы от эталлоного и юстируемого МФР
            reference_trace = self._traces[self._ref_num][target_num]
            adjustable_trace = self._traces[self._adj_num][target_num]

            reference_coordinates = dec2sph(reference_trace.coordinates - adjustable_trace.mfr_position)
            adjustable_coordinates = dec2sph(adjustable_trace.coordinates - adjustable_trace.mfr_position)

            diffirence = adjustable_coordinates - reference_coordinates
            try:
                difference_array = self._common_residuals_dict[target_num]
                difference_array.append(diffirence)
                if len(difference_array) >= self._max_len:
                    self._residuals = np.mean(difference_array[self._starting_count:], axis=0)
                    self._calculation_ready = True
                    break
            except KeyError:
                self._common_residuals_dict[target_num] = [diffirence]
