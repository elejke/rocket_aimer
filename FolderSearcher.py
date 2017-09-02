#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import sys
import threading

import time

from Singleton import Singleton


class FolderSearcherException(Exception):
    pass


# @Singleton
class _SingleFolderSearcher(object):
    def __init__(self, path="data/trajectories"):
        """
        Класс обработки папки с файлами

        :param path:
        """
        self.NEW_FILE = 'new_file'
        self.NEW_LINE = 'new_line'
        self.UPDATE_TIME = 20
        self.subscribes = {self.NEW_FILE: [],
                           self.NEW_LINE: []}
        self.path = path
        self.file_map = {}
        self.work = True

    def stop(self):
        self.work = False
        self.close_files()

    def run(self):
        def working():
            while self.work:
                self.update_filelist()
                time.sleep(self.UPDATE_TIME)
                # self.read_files()
        self.work = True
        t = threading.Thread(target=working)
        t.start()

    def connect(self, signals, func):
        """
        Подпись на событие
        :param signals: тип сигнала
        :param func: указатель на функцию
        """
        if signals in self.subscribes.keys():
            self.subscribes[signals].append(func)

    def disconnect(self, signals, func):
        """
        Отпись от события
        :param signals:
        :param func:
        """
        if signals in self.subscribes.keys():
            if func in self.subscribes[signals]:
                self.subscribes[signals].remove(func)

    def update_filelist(self):
        """
        Обновление файлов в папке
        """
        if not os.path.isdir(self.path):
            try:
                os.remove(self.path)
            except OSError:
                pass
            os.mkdir(self.path)
        list_file = os.listdir(self.path)
        for file_name in list_file:
            file_path = os.path.join(self.path, file_name) ##Путь к файлу
            if not file_name in self.file_map.keys():
                file_descriptor = open(file_path, 'r')
                self.file_map[file_name] = file_descriptor
                for func in self.subscribes[self.NEW_FILE]:
                    func(file_name)
            for file_path in self.file_map:
                lines = self.file_map[file_path].readlines()
                if lines:
                    for func in self.subscribes[self.NEW_LINE]:
                        func(file_name)

    def close_files(self):
        """
        Закрывает все открытые дескрипторы файлов
        """
        try:
            for file_name in self.file_map:
                self.file_map[file_name].close()
        except Exception:
            pass


cls = _SingleFolderSearcher()


class Wrapper(object):
    """
    Обертка для импортирования подменяет модуль на объект класса cls = _SingleFolderSearcher()
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, name):
        return getattr(self.wrapped.cls, name)


sys.modules[__name__] = Wrapper(sys.modules[__name__])
