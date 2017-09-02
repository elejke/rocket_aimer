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
    REGEX_DIGITAL = '^[\-]?\d+$'
    REGEX_FLOAT = '^([\-]?\d+\.\d+)|(' + REGEX_DIGITAL[1:-1] + ')$'

    def __init__(self):
        pass

    @staticmethod
    def error(entry, title='Недопустимый формат', message=''):
        """
        Вызывается в случае не прохождения проверки
        :param entry: Объект поля ввода
        :param title: заголовок сообщения об ошибке
        :param message: текст ошибки
        """
        entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0, 1.0))
        error_dialog(title=title, message=message)
        entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 0.0, 1.0))
        raise CheckException("Error Format")

    @staticmethod
    def check_float(entry):
        """
        Провекра на правильность числа с плавающей запятой
        :param entry: Объект поля ввода
        """
        string = entry.get_text().strip()
        print(string)
        if re.match(Check.REGEX_FLOAT, string) is None:
            Check.error(entry, message= "Неправильно введенное значение числа с плавающей точкой либо поле не заполнено."
                                                          "\nПример: 3.14")
        else:
            return True

    @staticmethod
    def check_digital(entry):
        """
        Правильность на правильность целого числа
        :param entry: Объект поля ввода
        :return:
        """
        string = entry.get_text().strip()
        if re.match(Check.REGEX_DIGITAL , string) is None:
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