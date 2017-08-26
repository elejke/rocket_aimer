#!/usr/bin/python
# -*- coding: utf-8 -*-


from datetime import datetime

from Point import Point
from PIL import Image
from Trajectory import Trajectory


class Target(Trajectory):
    def __init__(self, target_name, target_id, pic_path="data/pics/airplane.png"):
        """
        Класс цели (объекта наведения)
        
        Аргументы:
            target_name: str: имя цели
            target_id: str: уникальный id цели
            airplane_picture: str: путь к изображению самолётика
        """
        super(Target, self).__init__()
        self.__pic__ = Image.open(pic_path)
        self.target_name = target_name
        self.target_id = target_id
        
    def fake_trajectory(self):
        """
        Генератор случайной траектории полета цели для тестового использования
        """
        x, y, z = [0, 0, 50]
        for i in range(600):
            self.add_point(Point(datetime.now().isoformat(), x + i, y + i, z + i))


class Satelight(object):
    def __init__(self, coordinates, satelight_type, satelight_id, pic_path="data/pics/satelight.png"):
        """
        Класс РЛС, коориданты, имя, тип рлс и её изображение на карте
        """
        self.coordinates = coordinates
        self.satelight_type = satelight_type
        self.satelight_id = satelight_id
        self.__pic__ = Image.open(pic_path)


class Rocket(Trajectory):
    def __init__(self, coordinates, rocket_id, rocket_type, pic_path="data/pics/rocket.png"):
        """
        Класс ракеты, запускаемой по какой-то цели
        
        Аргументы:
            cordinates: Point(): объект класса Point() - координаты точки запуска ракеты
            rocket_id: str: уникальный идентификатор ракеты (её имя)
            rocket_type: str: идентифиактор типа ракеты
            rocket_pic: str: путь к изображению, которое будет её изображением на карте
        """
        
        super(Rocket, self).__init__()
        self.rocket_id = rocket_id
        self.rocket_type = rocket_type
        self.coordinates = coordinates
        self.__pic__ = Image.open(pic_path).rotate(45, expand=True)
        self.target = None
        
    def start_rocket(self, target, time=None):
        """
        Метод, запускающий ракету из точки self.coordinates по цели target (обект класса Target)
        
        Аргументы:
            target: Target(): объект класса Target() - цель, по которой запущена ракета
            time: str: время в одном из пригодных 
        """
        self.target = target
        # здесь должна вызываться функция, которая в режиме реального времени реализовывает просчёт траектории
        # ракеты:
        # self._trajectory_computation()
        x, y, z = self.coordinates
        self.filtered_trajectory.set_point(Point().set_coordinates(time, x, y, z))
        return self
        
    def _trajectory_computation(self, method="method_name"):
        """
        Абстрактная функция, которая в режиме реального времени просчитывает траекторию ракеты по координатам цели
        
        Аргументы:
            method: str: название метода для вычисления траектории полёта.
        """
        pass
    
    def fake_trajectory(self):
        """
        Генератор случайной траектории ракеты для тестового использования (без алгоритма наведения и управления 
        ракетой)
        """
        x, y, z = self.coordinates
        for i in range(500):
            self.add_point(Point(datetime.now().isoformat(), x + i, y + i, z + i))
