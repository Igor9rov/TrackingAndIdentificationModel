import numpy as np


class TraceVelocitiesData:
    """Класс для хранения данных по скоростям"""
    __slots__ = ("extrapolate_velocities_bcs",
                 "extrapolate_velocities_dec")

    def __init__(self) -> None:
        # Экстраполированная скорость цели
        self.extrapolate_velocities_bcs = np.zeros(3)
        self.extrapolate_velocities_dec = np.zeros(3)
