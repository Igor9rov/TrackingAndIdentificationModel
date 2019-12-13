from collections import namedtuple

from structure_of_variant import KeyMFRError

SurveillanceErrors = namedtuple(typename="SurveillanceErrors",
                                field_names=[KeyMFRError.beta_north, KeyMFRError.beta])
"""Класс описывает ошибки в параметрах обзора МФР, пока для простоты ошибки присутсвуют только в двух параметрах: 
азимутах подвижной и неподвижной части антенны"""
