#!/usr/bin/python
# -*- coding: utf-8 -*-

import gi
import threading
from gi.repository import Gtk, GObject
from datetime import datetime


import FolderSearcher
from PointerRocket import PointerRocket
from Map import Map
from Point import Point
from ModelObject import Rocket, Target, Satelight
from Check import Check, CheckException
from Network import Network
from dialogs import error_dialog
gi.require_version('Gtk', '3.0')

TIME_UPDATE_MAP = 1000
NO_INFORMATION = "Нет информации"


class Main:
    """
    Класс отвечающий за управлеие приложением, работой с визуальной частью
    """
    def __init__(self, ui='ui/main.glade'):
        # Объект карта которая будет отображаться
        self.map = Map()
        # Объект отвечающий за наводку ракеты
        self.pointer_rocket = PointerRocket()
        # Объект отвечающий за соотношние объектов из файла с шиблоном из приложения glade
        self.builder = Gtk.Builder()  #
        # подгружаем информацию из файла glade
        self.builder.add_from_file(ui)  #
        # получаю объект с id = 'window' в приложении glade
        self.window = self.builder.get_object('window')
        # далее данный метод будет получать другие объекты аналогично
        # Добавляем обработчик закрытия главного окна, завершаем gtk поток
        # а с ним и все приложение
        self.window.connect('destroy', self.close)
        self.server_address = self.builder.get_object('server_address')
        # Вставляем по дефолту текст в поле адреса сервера
        # (данный метод вставляет текст в поля объектов у которых он вызывается)
        self.server_address.set_text('http://')

        self.map_box = self.builder.get_object('map_box')
        btn_connect_to_server = self.builder.get_object('btn_connect')
        # Подписываемся на обработку
        # события нажатия клавиши "Подключиться"
        # метод connect подписывает на события. Событие clicked нажатие на кнопку
        btn_connect_to_server.connect('clicked', self.btn_connect_clicked)

        self.view_map = self.builder.get_object('view_map')
        self.default_axes = self.builder.get_object('default_axes')
        self.default_axes.connect('clicked', self.default_axes_clicked)
        # Метод set_sensitive устанавливает доступен ли объект для редактирования, True - доступен, False - нет
        self.builder.get_object('axes').set_sensitive(False)
        self.current_map = self.builder.get_object("current_map")
        # Создание фильтра для файлов
        filter_png = Gtk.FileFilter()
        # Имя фильтра
        filter_png.set_name("PNG files")
        # Задаем разрешение доступных файлов .png
        filter_png.add_pattern("*.png")
        # Добавляем в диалог выбора файлов
        self.current_map.add_filter(filter_png)

        save_settings = self.builder.get_object('save_settings')
        save_settings.connect('clicked', self.save_settings_clicked)
        self.left_x = self.builder.get_object('left_x')
        self.left_y = self.builder.get_object('left_y')
        self.right_x = self.builder.get_object('right_x')
        self.right_y = self.builder.get_object('right_y')

        self.target_combobox = self.builder.get_object('target_combobox')
        # Создаем дерево в виде листа из строк, который будет
        # содержать информацию для выпадающего списка(combobox)
        target_model = Gtk.ListStore(str)
        # Объект клетки который отображается в combobox
        renderer_text = Gtk.CellRendererText()
        # Добавляем в combobox клетку
        self.target_combobox.pack_start(renderer_text, True)
        # сопоставляем клетку с первым элементом из модели
        self.target_combobox.add_attribute(renderer_text, "text", 0)
        # Сопоставляем liststore с comboboxom
        self.target_combobox.set_model(target_model)
        # Подписываемся на событие изменения выбранного объекта в выпадающем списке
        self.target_combobox.connect('changed', self.target_combobox_changed)
        FolderSearcher.connect(FolderSearcher.NEW_FILE, self.add_target_in_combobox)
        FolderSearcher.run()
        self.choose_target_id = None
        self.builder.get_object('start_rocket').connect('clicked', self.btn_start_rocket_clicked)

        """
        Задаем фэйковые объекты
        """
        rocket_ = Rocket([0, 0, 600], rocket_id="ID000", rocket_type="C300-missle")
        rocket_2 = Rocket([0, 0, 10], rocket_id="ID001", rocket_type="C300-missle")
        rocket_3 = Rocket([0, 0, 400], rocket_id="ID002", rocket_type="C300-missle")

        rocket_.fake_trajectory()
        rocket_2.fake_trajectory()
        rocket_3.fake_trajectory()

        satelight_ = Satelight([300, 300, 300], "RLS1", "1")
        satelight_1 = Satelight([500, 500, 300], "RLS2", "2")
        satelight_2 = Satelight([700, 400, 300], "RLS3", "3")
        satelight_3 = Satelight([900, 100, 300], "RLS4", "4")

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
        """
        Добавляет цель в выпадающий список
        :param target: Строка содержащая id цели
        """
        self.target_combobox.get_model().append([str(target)])

    def remove_target_in_combobox(self, target):
        """
        Удаляет цель из выпадающего списка по его id
        :param target: Строка содержащая id цели
        :return:
        """
        list_target = self.target_combobox.get_model()
        for row in list_target:
            if row[0] == str(target):
                list_target.remove(row.iter)

    def target_combobox_changed(self, combobox):
        """
        Обработчик события изменения выбранной цели в списке
        :param combobox: Объект выпадающего списка(combobox)
        """
        target_model = combobox.get_model()
        number_row = combobox.get_active()
        self.choose_target_id = target_model[number_row][0]
        self.__change_info()

    def save_settings_clicked(self, btn):
        """
        Обработчик yажатия кнопки сохранить
        :param btn: кнопка
        :return:
        """
        """"
        Проверяем корректность введенных данных
        """
        # Выставлена ли голчка использовать разметку по умолчанию
        try:
            if not self.default_axes.get_active():
                # Если нет то переходим на проверку данных
                Check.check_float(self.left_x)
                Check.check_float(self.left_y)
                Check.check_float(self.right_x)
                Check.check_float(self.right_y)
        except CheckException:
            return False
        # Считываем выбранный файл карты
        filename = self.current_map.get_filename()
        """
        В зависимости от того задаются значения по умолчанию координатных прямых или нет задаем разные параметры
        """
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
        # Применяем изменения карты
        self.__change_map()

    def default_axes_clicked(self, btn):
        """
        Обработчик постановки и снятия галочки использования разметки координат по умолчанию
        :param btn:
        :return:
        """
        axes = self.builder.get_object('axes')
        axes.set_sensitive(not btn.get_active())

    def run(self):
        """
        Запуск приложения
        :return:
        """
        # Отрисовка главного окна
        self.window.show_all()
        # Добавление потока который каждые определенный промежуток времени вызывает метод update_all
        GObject.timeout_add(TIME_UPDATE_MAP, self.update_all)

    def close(self, window=None):
        """
        Закрытие приложения
        :param window: Объект окна
        """
        FolderSearcher.stop()
        Gtk.main_quit()

    def __change_map(self):
        """
        Обновляет карту
        :return:
        """
        # Удаляем старую из приложения
        self.view_map.remove(self.map_image)
        # Запрашиваем новую карту
        self.map_image = self.map.get_map()
        # вставляем ее в приложение
        self.view_map.add(self.map_image)
        # показываем ее
        self.view_map.show_all()

    def __change_info(self):
        """
        Обновляет информацию о цели
        :return:
        """
        def format_value(val):
            """
            Округляет значение val до двух знаков после запятой и переводит в строку число
            :param val: число с плавающей запятой тип float
            :return: преобразованное значение
            """
            return str(round(val, 2))

        info = self.map.get_target_info(self.choose_target_id)
        # Проверяем есть ли информация о данной цели
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
        else:
            self.builder.get_object('target_z').set_text(NO_INFORMATION)
            self.builder.get_object('speed_x').set_text(NO_INFORMATION)
            self.builder.get_object('speed_y').set_text(NO_INFORMATION)
            self.builder.get_object('speed_z').set_text(NO_INFORMATION)
            self.builder.get_object('speed_abs').set_text(NO_INFORMATION)
            self.builder.get_object('acceleration').set_text(NO_INFORMATION)

    def update_all(self):
        """
        Обновляет всю информацию о цели, карту, вычисление траектории ракеты
        :return:
        """
        self.pointer_rocket.__calculate_trajectory__()
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
        self.pointer_rocket.set_rocket_target(rocket, choose_target)


if __name__ == "__main__":
    Main().run()
    Gtk.main()

