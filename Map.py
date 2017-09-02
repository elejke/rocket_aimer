#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

from PIL import Image
from scipy.misc import imread

import FolderSearcher
from ModelObject import Target

class Map(object):
    
    def __init__(self, map_path="data/map.jpg"):
        """
        Класс карты, содержит в себе объекты целей, ракет и РЛС, которые отрисовываются в режиме онлайн в приложении.
        :param map_path: путь к карте
        """
        # списки объектов целей, ракет и РЛС
        self.targets = []
        self.rockets = []
        self.satelights = []
        # объекты карты (картинка_) с нанесенными на неё объектами и без.
        self.__map__ = None
        self.__img__ = imread(map_path)
        # путь до изображения карты подложки
        self.map_path = map_path
        # координаты, которые содержатся в левом верхнем и правом нижнем углу карты (по дефолту заполняются размерами
        # изображения от 0 до img.shape
        self.__img_left_x = 0
        self.__img_right_x = self.__img__.shape[1]
        self.__img_down_y = 0
        self.__img_up_y = self.__img__.shape[0]
        self.img_height = self.__img_up_y - self.__img_down_y
        FolderSearcher.connect(FolderSearcher.NEW_FILE, self.new_target_from_file)
        FolderSearcher.connect(FolderSearcher.NEW_LINE, self.new_trajectory_target)



    def set_image_map(self, map_path="data/map.jpg", 
                      img_left_x=None, 
                      img_right_x=None,
                      img_down_y=None,
                      img_up_y=None):
        """
        Функция загрузки карты и установления координат левого верхнего и правого нижнего угла изображения

        :param map_path: Путь до изображения карты
        :param img_left_x: Координаты левого x
        :param img_right_x: ...
        :param img_down_y: ...
        :param img_up_y: ...
        :return:
        """
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

            :param x: координата, которую необходимо пересчитать для изображения на решейпнутой карте по оси х
            :param y: координата, которую необходимо пересчитать для изображения на решейпнутой карте по оси у
            :param img_shape: изначальные раземеры изобрежния
            :param new_min_x: новые размеры изображения (новый х левого верхнего угла)
            :param new_min_y: новые размеры изображения (новый у правого нижнего угла)
            :param new_max_x: новые размеры изображения (новый х ...)
            :param new_max_y: новые размеры изображения (новый у ... )
            :return:
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
            Функция отрисовки одного объекта класса Trajectory() или унаследованного от него и его траектории полёта.

            :param object_: объект класса
            :param object_init_size: начальный размер изображения объекта в пикселях
            :param object_color: цвет траектории объекта
            :return:
            """
            # получение изображения объекта
            pic_object = object_.__pic__.copy()
            # получение координат объекта (последняя точка траектории)
            object_x, object_y, object_z = object_.filtered_trajectory[-1].get_coordinates()
            # получение скоростей объекта (последняя точка траектории)
            object_speed_x, object_speed_y, object_speed_z = object_.filtered_trajectory[-1].get_speed()
            # поворот объекта в зависимости от направления его вектора скорости (для двумерного изображения в осях (ху))
            rotation_angle = 270 * (object_speed_y < 0) + 90 * (object_speed_y >= 0)
            phi = np.arctan(object_speed_x / object_speed_y)
            # поворот и сжатие изображения объекта
            pic_object = pic_object.rotate(np.nan_to_num([rotation_angle - phi / np.pi * 180])[0], expand=True)
            pic_object = pic_object.resize(object_init_size * 2, Image.ANTIALIAS)
            # пересчёт координат объекта в зависимости от сжатия подложки
            object_x, object_y = _coordinates_reshape(object_x, object_y,
                                                      self.__img__.shape,
                                                      self.__img_left_x,
                                                      self.__img_down_y,
                                                      self.__img_right_x,
                                                      self.__img_up_y)
            # пересчёт сдвига от верхнего левого угла по оси у (делается из-за изменеия координат при задании
            # собственных от левого нижнего угла
            _, reshape_factor = _coordinates_reshape(0, self.img_height + self.__img_down_y,
                                                     self.__img__.shape,
                                                     self.__img_left_x,
                                                     self.__img_down_y,
                                                     self.__img_right_x,
                                                     self.__img_up_y)
            # вычисление координат объекта на окончательной карте
            object_x, object_y = (int(object_x - object_init_size[0]),
                                  int(reshape_factor - object_y - object_init_size[1]))
            # добавление объекта на карту
            map_.paste(pic_object, (object_x, object_y), pic_object)
            # добавление траектории на карту
            object_trajectory_x, object_trajectory_y = (object_.get_coordinates_list()[1],
                                                        object_.get_coordinates_list()[2])
            ax.plot(object_trajectory_x, object_trajectory_y, c=object_color)

        # поворот изображений самолётов в зависимости от вектора их скорости:
        # отрисовка их траекторий и изображений на карте
        for target in self.targets:
            print(target)
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
        # отрисовка подложки (карты) и задание соответствующих координат в углах изображения
        ax.imshow(np.array(map_), extent=[self.__img_left_x, self.__img_right_x,
                                          self.__img_down_y, self.__img_up_y])
        
        # Для отображения в jupyter notebook:
        # display.clear_output(wait=True)
        # display.display(plt.gcf())
        # time.sleep(0.7)
        # объект подложки для изображения
        canvas = FigureCanvas(mpl_figure)
        canvas.set_size_request(400, 400)
        return canvas
        # для выдачи объекта изображения в формате plt.plot()
        # return ax

    def new_target_from_file(self, target_id):
        target = Target('name', target_id=target_id)
        file_path = os.path.join(FolderSearcher.path, target_id)
        target.load_trajectory(file_path)
        self.add_target(target)

    def new_trajectory_target(self, target_id):
        file_path = os.path.join(FolderSearcher.path, target_id)
        for target in self.targets:
            if target.target_id == target_id:
                target.load_trajectory(file_path)

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
        """
        Функция выдачи информации о цели
        :param target_id: id цели
        :return:
        """
        for target in self.targets:
            if target.target_id == target_id:
                return target.get_info_object()
        return None

    def get_rocket_info(self, rocket_id):
        """
        Функция выдачи информации о ракете
        :param rocket_id: id ракеты
        :return:
        """
        for rocket in self.rockets:
            if rocket.rocket_id == rocket_id:
                return rocket.get_info_object()
        return None

    def get_target_by_id(self, target_id):
        """
        Функция выдачи цели по id
        :param target_id: id цели
        :return:
        """
        for target in self.targets:
            if target.target_id == target_id:
                return target
        return None
