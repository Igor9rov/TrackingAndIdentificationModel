"""Файл предназначен для профилирования процесса моделирования, объекты генерим на ходу"""

import numpy as np

from command_post import CommandPost
from multi_functional_radar import MultiFunctionalRadar
from target import Target

if __name__ == "__main__":
    # Цель
    target = Target(number=0,
                    coordinates=np.array([50_000., 5_000., 0.]),
                    velocities=np.array([-100., 0., 0.]),
                    target_type="Aerodynamic",
                    is_auto_tracking={0: True},
                    is_anj={0: False})

    # МФР
    multifunctional_radar = MultiFunctionalRadar(target_list=[target],
                                                 stable_point=np.array([1_000., 0., 0.]),
                                                 mfr_number=0)

    # ПБУ
    command_post = CommandPost(mfr_list=[multifunctional_radar])

    # Время моделирования в секундах
    modelling_time = 2_000

    # Моделирование (цикл по времени)
    for time in range(20 * modelling_time):
        target.operate(time)
        multifunctional_radar.operate(time)
        command_post.operate(time)
