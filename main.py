#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
import threading
from gi.repository import Gtk, GObject
gi.require_version('Gtk', '3.0')
from datetime import datetime

from AimerRocket import AimerRocket
from Map import Map
from Point import Point
from ModelObject import Rocket, Target, Satelight
from Check import Check, CheckException
from Network import Network
from dialogs import error_dialog


class Main:
    """
    Класс отвечающий за управлеие приложением, работой с визуальной частью
    """
    def __init__(self, ui='ui/main.glade'):
        self.map = Map() ##Объект карта которая будет отображаться
        self.aimer_rocket = AimerRocket()  ##Объект отвечающий за наводку ракеты
        self.builder = Gtk.Builder()  ## Объект отвечающий за соотношние объектов из файла с шиблоном из приложения glade
        self.builder.add_from_file(ui)  ## подгружаем информацию из файла glade
        self.window = self.builder.get_object('window') ## получаю объект с id = 'window' в приложении glade
                                                        ## далее данный метод будет получать другие объекты аналогично
        self.window.connect('destroy', Gtk.main_quit)  ## Добавляем обработчик закрытия главного окна, завершаем gtk поток
                                                        ## а с ним и все приложение
        self.server_address = self.builder.get_object('server_address')
        self.server_address.set_text('http://')  ## Добавл
        self.map_box = self.builder.get_object('map_box')
        self.builder.get_object('btn_connect').connect('clicked', self.btn_connect_clicked)
        self.view_map = self.builder.get_object('view_map')
        self.default_axes = self.builder.get_object('default_axes')
        self.default_axes.connect('clicked', self.default_axes_clicked)
        self.builder.get_object('axes').set_sensitive(False)

        self.current_map = self.builder.get_object("current_map")

        filter_png = Gtk.FileFilter()
        filter_png.set_name("PNG files")
        filter_png.add_pattern("*.png")
        self.current_map.add_filter(filter_png)

        save_settings = self.builder.get_object('save_settings')
        save_settings.connect('clicked', self.save_settings_clicked)
        self.left_x = self.builder.get_object('left_x')
        self.left_y = self.builder.get_object('left_y')
        self.right_x = self.builder.get_object('right_x')
        self.right_y = self.builder.get_object('right_y')


        self.target_combobox = self.builder.get_object('target_combobox')
        target_model = Gtk.ListStore(str)
        renderer_text = Gtk.CellRendererText()

        self.target_combobox.pack_start(renderer_text, True)
        self.target_combobox.add_attribute(renderer_text, "text", 0)
        self.target_combobox.set_model(target_model)
        self.target_combobox.connect('changed', self.target_combobox_changed)
        self.choose_target_id = None
        self.builder.get_object('start_rocket').connect('clicked', self.btn_start_rocket_clicked)

        target_model.append(['1'])
        target_model.append(['2'])
        target_model.append(['3'])
        self.remove_target_in_combobox('2')
        self.add_target_in_combobox('5')

        rocket_ = Rocket([0, 0, 600], rocket_id="ID000", rocket_type="C300-missle")
        rocket_2 = Rocket([0, 0, 10], rocket_id="ID001", rocket_type="C300-missle")
        rocket_3 = Rocket([0, 0, 400], rocket_id="ID002", rocket_type="C300-missle")

        rocket_.fake_trajectory()
        rocket_2.fake_trajectory()
        rocket_3.fake_trajectory()

        target_ = Target(target_name="F-16", target_id="1")

        target_.fake_trajectory()

        satelight_ = Satelight([300, 300, 300], "RLS1", "1")
        satelight_1 = Satelight([500, 500, 300], "RLS2", "2")
        satelight_2 = Satelight([700, 400, 300], "RLS3", "3")
        satelight_3 = Satelight([900, 100, 300], "RLS4", "4")

        self.map.add_target(target_)
        self.map.add_rocket(rocket_)
        self.map.add_rocket(rocket_2)
        self.map.add_rocket(rocket_3)
        self.map.add_satelight(satelight_)
        self.map.add_satelight(satelight_1)
        self.map.add_satelight(satelight_2)
        self.map.add_satelight(satelight_3)

        self.map_image = self.map.get_map()
        self.view_map.add(self.map_image)

        self.network = Network()

    def add_target_in_combobox(self, target):
        self.target_combobox.get_model().append([str(target)])

    def remove_target_in_combobox(self, target):
        list_target = self.target_combobox.get_model()
        for row in list_target:
            if row[0] == str(target):
                list_target.remove(row.iter)

    def target_combobox_changed(self, combobox):
        target_model = combobox.get_model()
        number_row = combobox.get_active()
        self.choose_target_id = target_model[number_row][0]
        self.__change_info()

    def save_settings_clicked(self, btn):
        try:
            if not self.default_axes.get_active():
                Check.check_float(self.left_x)
                Check.check_float(self.left_y)
                Check.check_float(self.right_x)
                Check.check_float(self.right_y)
        except CheckException:
            return False
        filename = self.current_map.get_filename()
        if self.default_axes.get_active():
            self.map.set_image_map(filename)
        else:
            left_x = float(self.left_x.get_text().strip())
            left_y = float(self.left_y.get_text().strip())
            right_x = float(self.right_x.get_text().strip())
            right_y = float(self.right_y.get_text().strip())
            if left_y <= right_y or right_x <= left_x:
                error_dialog(title='Ошибка в задании координат',
                             message='Проверьте правильность задания координат левой вернзней и\nправой нижней точек.')
                return False
            self.map.set_image_map(filename, left_x, right_x, right_y, left_y)
        self.__change_map()

    def default_axes_clicked(self, btn):
        axes = self.builder.get_object('axes')
        axes.set_sensitive(not btn.get_active())

    def run(self):
        self.window.show_all()
        GObject.timeout_add(1000, self.update_map)

    def __change_map(self):
        self.view_map.remove(self.map_image)
        self.map_image = self.map.get_map()
        self.view_map.add(self.map_image)
        self.view_map.show_all()

    def __change_info(self):
        def format_value(val):
            return str(round(val, 2))

        info = self.map.get_target_info(self.choose_target_id)
        if not isinstance(info, type(None)):
            coordinate, speed, acceleration = info
            x, y, z = coordinate

            self.builder.get_object('target_z').set_text(format_value(z))
            if not isinstance(speed, type(None)):
                [speed_x, speed_y, speed_z], speed_abs = speed
                self.builder.get_object('speed_x').set_text(format_value(speed_x))
                self.builder.get_object('speed_y').set_text(format_value(speed_y))
                self.builder.get_object('speed_z').set_text(format_value(speed_z))
                self.builder.get_object('speed_abs').set_text(format_value(speed_abs))
            if not isinstance(acceleration, type(None)):
                [a_x, a_y, a_z], a_abs = acceleration
                self.builder.get_object('acceleration').set_text(format_value(a_abs))

    def update_map(self):
        self.aimer_rocket.__calculate_trajectory__()
        self.__change_info()
        self.__change_map()
        return True

    def btn_connect_clicked(self, btn):
        """
        Обработчик нажатия клавиши подключения к серверу
        :param btn: Нажатая кнопка
        :return:
        """
        if self.server_address.get_sensitive():
            try:
                Check.check_url(self.server_address)
            except CheckException:
                return False
            btn.set_label("Отключиться")
            self.server_address.set_sensitive(False)
            self.network.set_url(self.server_address.get_text().strip())
            network = threading.Thread(target=self.network.start)
            network.start()
        else:
            btn.set_label("Подключиться")
            self.network.stop()
            self.server_address.set_sensitive(True)

    def btn_start_rocket_clicked(self, btn):
        """
        Обработчик нажатия кнопки запуска рокеты
        :param btn: Нажатая кнопка
        :return: None
        """
        entry_rocket_x = self.builder.get_object('rocket_x')
        entry_rocket_y = self.builder.get_object('rocket_y')
        try:
            Check.check_float(entry_rocket_x)
            Check.check_float(entry_rocket_y)
        except CheckException:
            return
        rocket_x = float(entry_rocket_x.get_text().strip())
        rocket_y = float(entry_rocket_y.get_text().strip())
        rocket_point = Point(timestamp=datetime.now().isoformat(),
                             x=rocket_x, y=rocket_y, z=0.)
        rocket = Rocket(rocket_point, rocket_id='1', rocket_type='t-40')
        rocket.add_point(rocket_point)
        if isinstance(self.choose_target_id, type(None)):
            error_dialog(title="Ошибка запуска ракеты",
                         message="Не задана цель ракеты.")
            return
        choose_target = self.map.get_target_by_id(self.choose_target_id)
        self.map.add_rocket(rocket)
        self.aimer_rocket.set_rocket_target(rocket, choose_target)


if __name__ == "__main__":
    Main().run()
    Gtk.main()

