#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


class Point(object):
    """
    Класс, отвечающий за хранение информации о координатах, скоростях и ускорениях цели в
    заданной точке и в заданный момент времени.

    Аргументы:
        timestamp: str: строка с датой и временем в в одном из используемых форматов даты.
        x, y, z: floats:  целые числа или числа с плавающей точкой, отвечающие за
        координаты цели в данный момент времени.
        v_x, v_y, v_z: floats:  целые числа или числа с плавающей точкой, отвечающие
        за скорость цели в данный момент времени.
        x,_a a_y, a_z: floats:  целые числа или числа с плавающей точкой, отвечающие
        за ускорения цели в данный момент времени.
    """

    def __init__(self, timestamp=np.nan,
                 x=np.nan, y=np.nan, z=np.nan,
                 v_x=np.nan, v_y=np.nan, v_z=np.nan,
                 a_x=np.nan, a_y=np.nan, a_z=np.nan):
        # время, в которое цель находилась в точке (x, y, z)
        self.timestamp = timestamp
        # координаты по трём осям
        self.x = x
        self.y = y
        self.z = z
        # скорости
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        # ускорения
        self.a_x = a_x
        self.a_y = a_y
        self.a_z = a_z
        # модуль скорости
        self.v = np.sum(np.array([self.v_x, self.v_y, self.v_z]) ** 2)
        # модуль ускорения
        self.a = np.sum(np.array([self.a_x, self.a_y, self.a_z]) ** 2)

    def set_coordinates(self, timestamp, x, y, z,
                        v_x=np.nan, v_y=np.nan, v_z=np.nan,
                        a_x=np.nan, a_y=np.nan, a_z=np.nan):
        """
        Добавление координат к инициализированной точке.
        Обязательные атрибуты - время и (x, y, z)
        """
        self.timestamps = timestamp
        self.x, self.y, self.z = x, y, z
        return self

    def set_speed(self, v_x, v_y, v_z):
        """
        Добавление скоростей к инициализированной точке.
        Атрибуты - время и скорости по осям (x, y, z)
        """
        self.v_x, self.v_y, self.v_z = v_x, v_y, v_z
        # модуль скорости
        self.v = np.sum(np.array([self.v_x, self.v_y, self.v_z]) ** 2)
        return self

    def set_acceleration(self, a_x, a_y, a_z):
        """
        Добавление ускорений к инициализированной точке.
        Атрибуты - время и ускорения по осям (x, y, z)
        """
        self.a_x, self.a_y, self.a_z = a_x, a_y, a_z
        # модуль ускорения
        self.a = np.sum(np.array([self.a_x, self.a_y, self.a_z]) ** 2)
        return self

    def get_coordinates(self):
        """
        Функция выдаёт координаты в формате (x, y, z)
        """
        return np.array([self.x, self.y, self.z])

    def get_speed(self):
        """
        Функция выдаёт скорость в формате (v_x, v_y, v_z)
        """
        return np.array([self.v_x, self.v_y, self.v_z])

    def get_acceleration(self):
        """
        Функция выдаёт ускорения в формате (a_x, a_y, a_z)
        """
        return np.array([self.a_x, self.a_y, self.a_z])

    def get_speed_value(self):
        """
        Функция модуль скорости
        """
        return self.v

    def get_acceleration_value(self):
        """
        Функция выдаёт модуль ускорения
        """
        return self.a