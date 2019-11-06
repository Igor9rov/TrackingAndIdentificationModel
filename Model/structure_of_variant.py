"""
Файл определят ключи для словаря с вариантом моделирования
Если легко можно было сделать из json словаря словарей namedtuple namedtupl-ов, то воспользовались бы им.
"""


class KeyVariant:
    """Ключи в словаре для варианта моделирования"""
    time = "Time Parameters"
    mfr = "MFR Parameters"
    target = "Target Parameters"


class KeyTime:
    """Ключи в словаре для параметров времени"""
    modelling = "Modelling Time"
    repeating = "Repeating Time"


class KeyMFR:
    """Ключи в словаре для параметров одного МФР"""
    coordinates = "Coordinates"


class KeyTarget:
    """Ключи в словаре для параметров одной цели"""
    coordinates = "Coordinates"
    velocities = "Velocities"
    type = "Type"
    mfr = "MFR Parameters"


class KeyMFRForTarget:
    """Ключи в словаре для параметров цели, связанной с одним МФР"""
    tracked = "Tracked"
    is_anj = "IsAnj"
    is_auto_tracking = "IsAutoTracking"
