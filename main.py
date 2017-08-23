#!/usr/bin/python
# -*- coding: utf-8 -*-
import gi
import numpy as np
from gi.repository import Gtk, GObject
gi.require_version('Gtk', '3.0')
from Trajectory import Trajectory


class Main:

    def __init__(self, ui='ui/main.glade'):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(ui)
        self.window = self.builder.get_object('window')
        self.window.connect('destroy', Gtk.main_quit)
        self.server_address = self.builder.get_object('server_address')
        self.map_box = self.builder.get_object('map_box')
        self.builder.get_object('btn_connect').connect('clicked', self.btn_connect_clicked)
        self.view_map = self.builder.get_object('view_map')
        default_axes = self.builder.get_object('default_axes')
        default_axes.connect('clicked', self.default_axes_clicked)
        self.builder.get_object('')
        self.test = Trajectory()
        sig = 1.3
        a = 30
        b = 20
        trajectory = np.asarray([[i + np.random.randn() / sig, i + np.random.randn() / sig] for i in range(a)] + [
            [a + i + np.random.randn() / sig, a + np.random.randn() / sig] for i in range(b)] + [
                                    [a + b + i + np.random.randn() / sig, a + i + np.random.randn() / sig] for i in
                                    range(20)])
        for i in range(len(trajectory)):
            self.test.add_point_by_coordinates(0.1, trajectory[i][0], trajectory[i][1], 0.1)
        self.map_ = self.test.get_map()
        self.view_map.add(self.map_)

    def default_axes_clicked(self, btn):
        axes = self.builder.get_object('axes')
        axes.set_sensitive(not btn.get_active())

    def run(self):
        self.window.show_all()
        GObject.timeout_add(1000, self.update_map)

    def update_map(self):
        self.view_map.remove(self.map_)
        self.map_ = self.test.get_map()
        self.view_map.add(self.map_)
        self.view_map.show_all()
        return True

    def btn_connect_clicked(self, btn):
        print 'clicked'

if __name__ == "__main__":
    Main().run()
    Gtk.main()

