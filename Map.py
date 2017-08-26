#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

from PIL import Image
from scipy.misc import imread


class Map(object):
    
    def __init__(self, map_path="data/map.jpg"):
        """
        Класс карты
        """
        self.targets = []
        self.rockets = []
        self.satelights = []
        self.__map__ = None
        self.__img__ = imread(map_path)
        self.map_path = map_path
        self.__img_left_x = 0
        self.__img_right_x = self.__img__.shape[1]
        self.__img_down_y = 0
        self.__img_up_y = self.__img__.shape[0]
        self.img_height = self.__img_up_y - self.__img_down_y

    def set_image_map(self, map_path="data/map.jpg", 
                      img_left_x=None, 
                      img_right_x=None,
                      img_down_y=None,
                      img_up_y=None):
        if not isinstance(map_path, type(None)):
            self.map_path = map_path
            self.__img__ = imread(map_path)
        if isinstance(img_left_x, type(None)):
            self.__img_left_x = 0
            self.__img_right_x = self.__img__.shape[1]
            self.__img_down_y = 0
            self.__img_up_y = self.__img__.shape[0]
        else:
            self.__img_left_x = float(img_left_x)
            self.__img_right_x = float(img_right_x)
            self.__img_down_y = float(img_down_y)
            self.__img_up_y = float(img_up_y)
    
    def get_map(self):
        """
        Генерация карты с траекториями полёта и изображениями ракет, самолётов и РЛС

        :return:
        """
        def _coordinates_reshape(x, y, img_shape, new_min_x, new_min_y, new_max_x, new_max_y):
            """
            Пересчёт координат целей, самолётов и РЛС для отрисовки на решейпнутой карте
            """
            new_x = (x - new_min_x) * img_shape[1] / (new_max_x - new_min_x)
            new_y = (y - new_min_y) * img_shape[0] / (new_max_y - new_min_y)
            return int(new_x), int(new_y)
            
        mpl_figure = Figure()
        ax = mpl_figure.add_subplot(111)
        # fig, ax = plt.subplots(figsize=[10, 10])
        map_ = Image.open(self.map_path)
        
        # задание относительных размеров изображений ракеты, цели и РЛС (костыль для наших конкретных картинок)
        rocket_init_size = np.array([40, 40])
        target_init_size = np.array([40, 40])
        satelight_init_size = np.array([20, 20])

        self.img_height = self.__img_up_y - self.__img_down_y

        def _plot_object_and_trajectory(object_, object_init_size=np.array([40, 40]), object_color="red"):
            """
            Функция отрисовки объекта класса Trajectory() и его траектории полёта.
            """
            pic_object = object_.__pic__.copy()
            object_x, object_y, object_z = object_.filtered_trajectory[-1].get_coordinates()
            object_speed_x, object_speed_y, object_speed_z = object_.filtered_trajectory[-1].get_speed()
            rotation_angle = 270 * (object_speed_y < 0) + 90 * (object_speed_y >= 0)
            phi = np.arctan(object_speed_x / object_speed_y)
            pic_object = pic_object.rotate(np.nan_to_num([rotation_angle - phi / np.pi * 180])[0], expand=True)
            pic_object = pic_object.resize(object_init_size * 2, Image.ANTIALIAS)

            object_x, object_y = _coordinates_reshape(object_x, object_y,
                                                      self.__img__.shape,
                                                      self.__img_left_x,
                                                      self.__img_down_y,
                                                      self.__img_right_x,
                                                      self.__img_up_y)

            _, reshape_factor = _coordinates_reshape(0, self.img_height + self.__img_down_y,
                                                     self.__img__.shape,
                                                     self.__img_left_x,
                                                     self.__img_down_y,
                                                     self.__img_right_x,
                                                     self.__img_up_y)

            object_x, object_y = (int(object_x - object_init_size[0]),
                                  int(reshape_factor - object_y - object_init_size[1]))

            map_.paste(pic_object, (object_x, object_y), pic_object)

            object_trajectory_x, object_trajectory_y = (object_.get_coordinates_list()[1],
                                                        object_.get_coordinates_list()[2])
            ax.plot(object_trajectory_x, object_trajectory_y, c=object_color)

        # поворот изображений самолётов в зависимости от вектора их скорости:
        # отрисовка их траекторий и изображений на карте
        for target in self.targets:
            _plot_object_and_trajectory(target, target_init_size, "red")
        # поворот изображений ракеты в зависимости от вектора их скорости:
        # отрисовка их траекторий и изображений на карте
        for rocket in self.rockets:
            _plot_object_and_trajectory(rocket, rocket_init_size, "green")
        # отрисовка РЛС:
        for satelight in self.satelights:
            pic_satelight = satelight.__pic__.copy()
            pic_satelight = pic_satelight.resize(satelight_init_size * 2, Image.ANTIALIAS)
            map_.paste(pic_satelight, (satelight.coordinates[0], satelight.coordinates[1]), pic_satelight)

        ax.imshow(np.array(map_), extent=[self.__img_left_x, self.__img_right_x,
                                          self.__img_down_y, self.__img_up_y])
        
        # Для отображения в jupyter notebook:
        # display.clear_output(wait=True)
        # display.display(plt.gcf())
        # time.sleep(0.7)

        canvas = FigureCanvas(mpl_figure)
        canvas.set_size_request(400, 400)
        return canvas
        # return ax
    
    def add_target(self, target):
        """
        Добавление целей в список отслеживаемых целей:
        
        Агурменты:
            target: Target(): объект класс Target.
        """
        self.targets.append(target)
        return self
        
    def add_rocket(self, rocket):
        """
        Добавление ракеты в список отслеживаемых ракет:
        
        Агурменты:
            rocket: Rocket(): объект класс Rocket.
        """
        self.rockets.append(rocket)
        return self

    def add_satelight(self, satelight):
        """
        Добавление ракеты в список отслеживаемых ракет:
        
        Агурменты:
            satelight: Satelight(): объект класс Satelight.
        """
        self.satelights.append(satelight)
        return self

    def get_target_info(self, target_id):
        for target in self.targets:
            if target.target_id == target_id:
                return target.get_info_object()
        return None

    def get_rocket_info(self, rocket_id):
        for rocket in self.rockets:
            if rocket.rocket_id == rocket_id:
                return rocket.get_info_object()
        return None

    def get_target_by_id(self, target_id):
        for target in self.targets:
            if target.target_id == target_id:
                return target
        return None
