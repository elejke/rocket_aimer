#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from Point import Point
from scipy.misc import imread
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


class Trajectory(object):
    """
    1. Метод, который кушает одну приходящую точку (x, y, z, v_x=np.nan, v_y=np.nan, v_z=np.nan, a_x=np.nan, a_y=np.nan, a_z=np.nan),
    если тестовый режим работы - зашумляем, если присутствуют только координаты, *считает* скорости, ускорения и сохраняет это в self.x_list, self...
    2. Внутренний методы просчёта, фильтрации и аппроксимации траекторий.
    3. Метод для тестового зашумления данных и тд
    4.
    """

    def __init__(self, target="Target_0", map_ = 'data/map.jpg'):
        # Название и характеристики цели (на данный момент - строка):
        self.target = target
        # Координаты, скорости, ускорения и таймстампы точек траектории
        self.trajectory = []
        # Значения точек траектории, полученные после её обработки одним
        # или несколькими последовательно примененными алгоритмами фильтрации
        # и интерполяции
        self.filtered_trajectory = []
        self.__map__ = None
        self.__img__ = imread(map_)

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
        self._filter_trajectory(filtring_type="l1_filtering")
        # self._recompute_speed()
        # self._recompute_accelerations()
        return self

    def _filter_trajectory(self, filtring_type=None):

        import copy
        """
        Фильтрация и сглаживание траектории одним из способов:
        Нужно минимум window точек
        """


        def savgol(arr, window=15, order=5, deriv=0, rate=1):
            # window >= order + 2

            from math import factorial

            if len(arr) < window:
                window = len(arr)
                if window < order + 2:
                    order = window - 2

            y = np.asarray(arr[:])
            order_range = range(order + 1)
            half_window = (window - 1) // 2
            b = np.mat([[k ** i for i in order_range] for k in range(-half_window, half_window + 1)])
            m = np.linalg.pinv(b).A[deriv] * rate ** deriv * factorial(deriv)
            firstvals = y[0] - np.abs(y[1:half_window + 1][::-1] - y[0])
            lastvals = y[-1] + np.abs(y[-half_window - 1:-1][::-1] - y[-1])
            y = np.concatenate((firstvals, y, lastvals))
            return np.convolve(m[::-1], y, mode='valid')

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

    def get_map(self):
        mplfigure = Figure()
        ax = mplfigure.add_subplot(111)
        ax.plot([self.filtered_trajectory[i].x for i in range(len(self.filtered_trajectory))],
                 [self.filtered_trajectory[i].y for i in range(len(self.filtered_trajectory))])
        ax.legend()
        ax.imshow(self.__img__, extent=[0, self.__img__.shape[1], 0, self.__img__.shape[0]])
        canvas = FigureCanvas(mplfigure)
        canvas.set_size_request(400, 400)
        return canvas

if __name__ == "__main__":
    test = Trajectory()
    sig = 1.3
    a = 30
    b = 20
    trajectory = np.asarray([[i + np.random.randn() / sig, i + np.random.randn() / sig] for i in range(a)] + [
        [a + i + np.random.randn() / sig, a + np.random.randn() / sig] for i in range(b)] + [
                                [a + b + i + np.random.randn() / sig, a + i + np.random.randn() / sig] for i in
                                range(20)])
    pure_traj = np.asarray(
        [[i, i] for i in range(a)] + [[a + i, a] for i in range(b)] + [[a + b + i, a + i] for i in range(20)])
    for i in range(len(trajectory)):
        test.add_point_by_coordinates(0.1, trajectory[i][0], trajectory[i][1], 0.1)

    plt.close()
    # img = imread('data/map.jpg')
    # plt.plot([test.trajectory[i].x for i in range(len(test.trajectory))],
    #          [test.trajectory[i].y for i in range(len(test.trajectory))], '.')
    test.get_map()