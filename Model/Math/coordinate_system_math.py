# Модуль содержит математические функции для расчётов
import math
import numpy as np


# Функция для перехода от прямоугольных декартовых координат к сферическим координатам
def dec2sph(coordinate_dec):
    # Вводим обозначения для удобства записи
    x = coordinate_dec[0]
    y = coordinate_dec[1]
    z = coordinate_dec[2]

    # Вычисление элементов результирующего вектора
    r = math.sqrt(x**2+y**2+z**2)
    beta = math.atan2(z, x)
    eps = math.atan2(y, math.sqrt(x**2+z**2))
    # Результирующий вектор
    coordinate_sph = np.array([r, beta, eps])
    return coordinate_sph


# Функция для перехода от сферических координат к прямоугольным декартовым
def sph2dec(coordinate_sph):
    # Вводим обозначения для удобства записи
    r = coordinate_sph[0]
    beta = coordinate_sph[1]
    eps = coordinate_sph[2]

    # Результирующий вектор
    x = r*math.cos(beta)*math.cos(eps)
    y = r*math.sin(eps)
    z = r*math.sin(beta)*math.cos(eps)

    coordinate_dec = np.array([x, y, z])
    return coordinate_dec
