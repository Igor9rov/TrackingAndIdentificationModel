import numpy as np


class ProlongTrackData:
    """
    Класс, содержащий данные по цели на следующий шаг
    """
    __slots__ = ("extrapolate_coordinates",
                 "extrapolate_velocities",
                 "variance_extrapolate_coordinates")

    def __init__(self):
        # Экстраполированные координаты
        self.extrapolate_coordinates = np.zeros(3)
        # Эктстраполированная скорость
        self.extrapolate_velocities = np.zeros(3)
        # Дисперсия экстраполированных координат
        self.variance_extrapolate_coordinates = np.zeros(3)
