from copy import deepcopy

import numpy as np

from command_post import CommandPost
from errors_namedtuple import SurveillanceErrors
from multi_functional_radar import MultiFunctionalRadar
from structure_of_variant import KeyTarget, KeyMFRForTarget, KeyVariant, KeyMFR, KeyTime, KeyMFRError
from target import Target


class GeneratedVariant:
    """Класс для создания объектов для моделирования, параметров моделирования"""
    def __init__(self, json_variant: dict) -> None:
        """Порядок генерации объектов важен, сначала цели, потом МФР, далее ПБУ.

        :param json_variant: Словарь словарей из json файла
        :type json_variant: dict
        """
        self.modelling_time = json_variant[KeyVariant.time][KeyTime.modelling]
        self.repeating_time = json_variant[KeyVariant.time][KeyTime.repeating]
        self._target_list = self._generate_target_list(json_variant[KeyVariant.target])
        self._mfr_list = self._generate_mfr_list(json_variant)
        self._command_post = self._generate_command_post()

    @property
    def objects(self) -> tuple:
        """Нужна глубокая копия, чтобы при изменении объектов при моделировании они не влияли на объекты в этом классе

        :return: Глубокая копия кортежа из сгенерированных объектов
        :rtype: tuple
        """
        return deepcopy((self._target_list, self._mfr_list, self._command_post))

    def _generate_target_list(self, json_variant: dict) -> list:
        """Конструирует список целей

        :param json_variant: словарь словарей с параметрами
        :type json_variant: dict

        :return: Список целей
        :rtype: list
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
        """Конструирует кортеж с параметрами цели, связанных с МФР

        :param mfr_parameters: Словарь словарей с параметрами
        :type mfr_parameters: dict

        :return: Параметры МФР для цели (автоспровождение и признак помехи)
        :rtype: tuple
        """
        mfr_numbers = []
        is_auto_tracking = []
        is_anj = []
        for mfr_number, parameter in mfr_parameters.items():
            mfr_numbers.append(mfr_number)
            is_auto_tracking.append(parameter[KeyMFRForTarget.is_auto_tracking])
            is_anj.append(parameter[KeyMFRForTarget.is_anj])
        return dict(zip(mfr_numbers, is_auto_tracking)), dict(zip(mfr_numbers, is_anj))

    def _generate_mfr_list(self, json_variant: dict) -> list:
        """Конструирует список с МФР

        :param json_variant: Словарь словарей с параметрами
        :type json_variant: dict

        :return: Список МФР
        :rtype: list
        """
        mfr_list = []
        for mfr_number, parameter in json_variant[KeyVariant.mfr].items():
            target_list = self._generate_target_list_for_mfr(mfr_number, json_variant)
            mfr = MultiFunctionalRadar(target_list=target_list,
                                       stable_point=np.array(parameter[KeyMFR.coordinates]),
                                       mfr_number=mfr_number,
                                       errors=SurveillanceErrors(parameter[KeyMFR.errors][KeyMFRError.beta_north],
                                                                 parameter[KeyMFR.errors][KeyMFRError.beta]))
            mfr_list.append(mfr)
        return mfr_list

    def _generate_target_list_for_mfr(self, mfr_num: int, json_variant: dict) -> list:
        """Конструирует список целей для одного МФР

        :param mfr_num: Номер МФР
        :type mfr_num: int
        :param json_variant: Словарь словарей с параметрами
        :type json_variant: dict

        :return: Список целей для определённого МФР
        :rtype: list
        """
        return [target for target in self._target_list
                if json_variant[KeyVariant.target][target.number][KeyTarget.mfr][mfr_num][KeyMFRForTarget.tracked]]

    def _generate_command_post(self) -> CommandPost:
        """Конструирует ПБУ

        :return: Объект ПБУ
        :rtype: CommandPost
        """
        return CommandPost(mfr_list=self._mfr_list)
