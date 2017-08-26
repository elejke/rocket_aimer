#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from datetime import datetime
from Point import Point
from ModelObject import Rocket, Target


class AimerRocket:
    def __init__(self, rocket = None, target= None):
        self.MAX_SPEED_AXES = 10
        self.TIME = 10
        if isinstance(rocket, Rocket):
            self.__rocket__ = rocket
        else:
            self.__rocket__ = None
        if isinstance(target, Target):
            self.__target__ = target
        else:
            self.__target__ = None

    def __calculate_trajectory__(self):
        """
        Метод реализации способа наведения
        :return:
        """
        if isinstance(self.__rocket__, type(None)):
            return
        info = self.__rocket__.get_info_object()
        coordinate_rocket, speed_rocket, a_rocket = info

        if isinstance(speed_rocket, type(None)):
            point = self.__rocket__.get_coordinates_list()[-1]
            point.set_speed(100, 100, 100)
        else:
            [speed_rocket_x, speed_rocket_y, speed_rocket_z], speed_rocket_abs = speed_rocket
        if not isinstance(a_rocket, type(None)):
            [a_rocket_x, a_rocket_y, a_rocket_z], a_rocket_abs = a_rocket
        coordinate_target, speed_target, a_target = self.__target__.get_info_object()
        distance = coordinate_target - coordinate_rocket
        coef = distance / np.max(distance)
        speed = coef * self.MAX_SPEED_AXES
        new_coordinate = coordinate_rocket + speed * self.TIME
        new_point = Point(timestamp=datetime.now().isoformat(),
                          x=new_coordinate[0],
                          y=new_coordinate[1],
                          z=new_coordinate[2],
                          v_x=speed[0],
                          v_y=speed[1],
                          v_z=speed[2])
        self.__rocket__.add_point(new_point)

    def set_rocket_target(self, rocket, target):
        if isinstance(rocket, Rocket):
            self.__rocket__ = rocket
        else:
            self.__rocket__ = None
        if isinstance(target, Target):
            self.__target__ = target
        else:
            self.__target__ = None
