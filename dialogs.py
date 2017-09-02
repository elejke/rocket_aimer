#!/usr/bin/python
# -*- coding: utf-8


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def info_dialog(type=Gtk.MessageType.INFO, title='', message=''):
    """
    Функция вызова окна информирования
    :param type:
    :param title:
    :param message:
    :return:
    """
    dialog = Gtk.MessageDialog(None, 0, type,
                               Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(message)
    dialog.run()
    dialog.destroy()


def error_dialog(type=Gtk.MessageType.ERROR, title='', message=''):
    """
    Функция вызова окна ошибки
    :param type:
    :param title:
    :param message:
    :return:
    """
    info_dialog(type, title, message)
