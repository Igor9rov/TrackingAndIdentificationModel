from copy import deepcopy

import numpy as np

from command_post import CommandPost
from multi_functional_radar import MultiFunctionalRadar
from structure_of_variant import KeyTarget, KeyMFRForTarget, KeyVariant, KeyMFR, KeyTime
from target import Target


class GeneratedVariant:
    """Класс для создания объектов для моделирования, параметров моделирования"""
    def __init__(self, json_variant: dict):
        """Порядок генерации объектов важен, сначала цели, потом МФР, далее ПБУ.

        :param json_variant: Словарь словарей из json файла
        """
        self.modelling_time = json_variant[KeyVariant.time][KeyTime.modelling]
        self.repeating_time = json_variant[KeyVariant.time][KeyTime.repeating]
        self._target_list = self._generate_target_list(json_variant[KeyVariant.target])
        self._mfr_list = self._generate_mfr_list(json_variant)
        self._command_post = self._generate_command_post()

    @property
    def objects(self):
        """
        :return: Возвращает кортеж из сгенерированных объектов
        """
        return deepcopy((self._target_list, self._mfr_list, self._command_post))

    def _generate_target_list(self, json_variant) -> list:
        """Конструирует список целей

        :param json_variant: словарь словарей с параметрами

        :return: Список целей
        """
        target_list = []
        for target_number, parameters in json_variant.items():
            is_auto_tracking, is_anj = self._generate_mfr_parameters_for_target(parameters[KeyTarget.mfr])
            target = Target(number=target_number,
                            coordinates=np.array(parameters[KeyTarget.coordinates]),
                            velocities=np.array(parameters[KeyTarget.velocities]),
                            target_type=parameters[KeyTarget.type],
                            is_auto_tracking=is_auto_tracking,
                            is_anj=is_anj)
            target_list.append(target)
        return target_list

    @staticmethod
    def _generate_mfr_parameters_for_target(mfr_parameters: dict) -> tuple:
        """
        :param mfr_parameters: Словарь словарей с параметрами

        :return: Параметры МФР для цели (автоспровождение и признак помехи)
        """
        mfr_numbers = []
        is_auto_tracking = []
        is_anj = []
        for mfr_number, parameter in mfr_parameters.items():
            mfr_numbers.append(mfr_number)
            is_auto_tracking.append(parameter[KeyMFRForTarget.is_auto_tracking])
            is_anj.append(parameter[KeyMFRForTarget.is_anj])
        return dict(zip(mfr_numbers, is_auto_tracking)), dict(zip(mfr_numbers, is_anj))

    def _generate_mfr_list(self, json_variant) -> list:
        """
        :param json_variant: Словарь словарей с параметрами

        :return: Список МФР
        """
        mfr_list = []
        for mfr_number, parameter in json_variant[KeyVariant.mfr].items():
            target_list = self._generate_target_list_for_mfr(mfr_number, json_variant)
            mfr = MultiFunctionalRadar(stable_point=np.array(parameter[KeyMFR.coordinates]),
                                       mfr_number=mfr_number,
                                       target_list=target_list)
            mfr_list.append(mfr)
        return mfr_list

    def _generate_target_list_for_mfr(self, mfr_num, json_variant) -> list:
        """
        :param mfr_num: Номер МФР

        :param json_variant: Словарь словарей с параметрами

        :return: Список целей для определённого МФР
        """
        return [target for target in self._target_list
                if json_variant[KeyVariant.target][f"{target.number}"][KeyTarget.mfr][f"{mfr_num}"][KeyMFRForTarget.tracked]]

    def _generate_command_post(self):
        """
        :return: Объект ПБУ
        """
        return CommandPost(mfr_list=self._mfr_list)
