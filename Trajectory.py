#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from Point import Point


class Trajectory(object):
    """
    1. Метод, который кушает одну приходящую точку (x, y, z, v_x=np.nan, v_y=np.nan, v_z=np.nan, a_x=np.nan,
     a_y=np.nan, a_z=np.nan),
    если тестовый режим работы - зашумляем, если присутствуют только координаты, *считает* скорости, ускорения и
     сохраняет это в self.x_list, self...
    2. Внутренний методы просчёта, фильтрации и аппроксимации траекторий.
    3. Метод для тестового зашумления данных и тд
    """

    def __init__(self):
        # Координаты, скорости, ускорения и таймстампы точек траектории
        self.trajectory = []
        # Значения точек траектории, полученные после её обработки одним
        # или несколькими последовательно примененными алгоритмами фильтрации
        # и интерполяции
        self.filtered_trajectory = []
        self.trajectory_id = None
        self.trajectory_type = None

    def add_point_by_coordinates(self, timestamp, x, y, z,
                                 v_x=np.nan, v_y=np.nan, v_z=np.nan,
                                 a_x=np.nan, a_y=np.nan, a_z=np.nan):
        self.add_point(Point(timestamp, x, y, z, v_x, v_y, v_z, a_x, a_y, a_z))
        return self

    def add_point(self, point):
        """
        Добавление новой точки:

        Аргументы:
            point: Point: объект класса Point,
        """
        self.trajectory.append(point)
        self.filtered_trajectory = self.trajectory
        # для пересчёта траектории с фильтрацией раскомментировать следующую строчку:
        # self._filter_trajectory(filtring_type="l1_filtering")

        if len(self.trajectory) > 1:
            self._recompute_speed()
        if len(self.trajectory) > 2:
            self._recompute_accelerations()
        return self

    def get_info_object(self):
        """
        Получает информацию об объекте в крайней точке
        :return: Лист с информацией
        """
        last_point = self.trajectory[-1]
        coordinate = last_point.get_coordinates()
        speed = last_point.get_speed(), last_point.get_speed_value()
        acceleration = last_point.get_acceleration(), last_point.get_acceleration_value()
        return coordinate, speed, acceleration

    def _recompute_speed(self):
        """
        Функция вычисления скорости по вновь пришедшей и предыдущей точке.
        """
        last_point = self.filtered_trajectory[-2]
        current_point = self.filtered_trajectory[-1]
        v = (current_point.get_coordinates() - last_point.get_coordinates() + len(self.trajectory) * 0.00000001) / \
            (current_point.timestamp - last_point.timestamp).total_seconds()
        current_point.set_speed(v[0], v[1], v[2])

    def _recompute_accelerations(self):
        """
        Функция вычисления ускорения по вновь пришедшей и предыдущей точке.
        """
        last_point = self.filtered_trajectory[-2]
        current_point = self.filtered_trajectory[-1]
        a_x, a_y, a_z = (current_point.get_speed() - last_point.get_speed()) / \
            (current_point.timestamp - last_point.timestamp).total_seconds()
        current_point.set_acceleration(a_x, a_y, a_z)

    def _filter_trajectory(self, filtring_type=None):

        import copy
        """
        Фильтрация и сглаживание траектории одним из способов:
        Нужно минимум window точек
        """

        def savgol(arr, window=15, order=5, deriv=0, rate=1):
            """
            Функция вычисления сглаживания Сав в окне

            :param arr: list-like: список точек
            :param window: int: окно, в котором происходит сглаживание
            :param order: int: порядок сглаживания
            :param deriv: int: порядок производной
            :param rate: int:
            :return:
            """
            # window >= order + 2
            from math import factorial

            if len(arr) < window:
                window = len(arr)
                if window < order + 2:
                    order = window - 2

            y = np.asarray(arr[:])
            order_range = range(order + 1)
            half_window = (window - 1) // 2
            b = np.mat([[k ** j for j in order_range] for k in range(-half_window, half_window + 1)])
            m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
            firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
            lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
            y = np.concatenate((firstvals, y, lastvals))
            return np.convolve(m[::-1], y, mode='valid')

        # вычисление сглаживания отдельно для каждой из координат:
        self.filtered_trajectory = copy.deepcopy(self.trajectory)
        if len(self.filtered_trajectory) > 2:
            filtered_coordinate = savgol([self.trajectory[i].x for i in range(len(self.trajectory))])
            for i in range(len(self.filtered_trajectory)):
                self.filtered_trajectory[i].x = filtered_coordinate[i]
            filtered_coordinate = savgol([self.trajectory[i].y for i in range(len(self.trajectory))])
            for i in range(len(self.filtered_trajectory)):
                self.filtered_trajectory[i].y = filtered_coordinate[i]
            filtered_coordinate = savgol([self.trajectory[i].z for i in range(len(self.trajectory))])
            for i in range(len(self.filtered_trajectory)):
                self.filtered_trajectory[i].z = filtered_coordinate[i]

        return self.filtered_trajectory

    def get_coordinates_list(self):
        """
        Метод, который выдаёт список координат в формате [[t_1, ..., t_n],
        [x_1, ..., x_n], [y_1, ..., y_n], [z_1, ..., z_n], ]
        """
        ts = [coord.timestamp for coord in self.filtered_trajectory]
        xs = [coord.x for coord in self.filtered_trajectory]
        ys = [coord.y for coord in self.filtered_trajectory]
        zs = [coord.z for coord in self.filtered_trajectory]

        return ts, xs, ys, zs

    def load_trajectory(self, filename="data/trajectories/ID001.json"):
        """
        Функция загрузки траектории из файла.

        :param filename: str: Строка, указывающая полный путь до файла траектории
        :return:
        """
        df = pd.read_json(filename, orient="records", lines=True)
        df = df.iloc[len(self.trajectory):]
        for point_ in df.iterrows():
            ts, xs, ys, zs = point_[1].values
            self.add_point_by_coordinates(ts, xs, ys, zs)

    def save_trajectory(self, filename="data/trajectories/ID001.json", ):
        """
        Функция сохранения траектории в файл.

        :param filename: str: Строка, указывающая полный путь до файла траектории
        :return:
        """

        ts, xs, ys, zs = self.get_coordinates_list()
        df = pd.DataFrame(np.array([[t.isoformat() for t in ts], xs, ys, zs]).T, columns=["timestamp", "x", "y", "z"])

        df.to_json(filename, orient="records", lines=True)
