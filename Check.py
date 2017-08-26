#!/usr/bin/python
# -*- coding: utf-8

import re
from gi.repository import Gtk, Gdk
from dialogs import error_dialog

class CheckException(Exception):
    pass


class Check:
    REGEX_IP = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    REGEX_URL = '^(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F])))$'

    def __init__(self):
        pass

    @staticmethod
    def error(entry, title='Недопустимый формат', message=''):
        entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0, 1.0))
        error_dialog(title=title, message=message)
        entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 0.0, 1.0))
        raise CheckException("Error Format")

    @staticmethod
    def check_float(entry):
        string = entry.get_text().strip()
        if re.match("^(\-?\d+\.\d+)|(\d+)$", string) is None:
            Check.error(entry, message= "Неправильно введенное значение числа с плавающей точкой либо поле не заполнено."
                                                          "\nПример: 3.14")
        else:
            return True

    @staticmethod
    def check_digital(entry):
        string = entry.get_text().strip()
        if re.match("^\-?\d+$", string) is None:
            Check.error(entry, message="Неправильно введенное целое число либо поле не заполнено."
                                       "\nПример: 3")
        else:
            return True

    @staticmethod
    def check_url(entry):
        string = entry.get_text().strip()
        if re.match(Check.REGEX_URL[:-1] + '|' + Check.REGEX_IP[1:], string) is None:
            Check.error(entry, message="Неправильно введенный url-адрес или ip сервера."
                                       "\nПример: http://google.com или 192.168.124.12")
        else:
            return True