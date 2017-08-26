#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import os.path


class NetworkException(Exception):
    pass


class Network:

    FOLDER = 'data'

    def __init__(self, url='', filename=''):
        self.work = True
        self.url = url

    def set_url(self, url):
        self.url = url

    def start(self):
        self.work = True
        while True:
            if self.work:
                Network.get_data(self.url)
            else:
                break

    def stop(self):
        self.work = False

    @staticmethod
    def get_number_target(resp):
        pass
        return '12'
        # return resp.json()['target']  Расскоментировать для получения номера цели

    @staticmethod
    def get_data(url):
        try:
            resp = requests.get(url)
            if not resp.ok:
                raise requests.RequestException("Error connection")
        except requests.RequestException:
            raise NetworkException('Ошибка получения данных с сервера. Возможно указаны неверные данные.')
        filename = Network.get_number_target(resp)
        if not os.path.isdir(Network.FOLDER):
            if os.path.isfile(Network.FOLDER):
                os.remove(Network.FOLDER)
            os.mkdir(Network.FOLDER)
        with open(os.path.join(Network.FOLDER, filename), 'a') as f:
            f.write(str(resp.json()) + '\n')
            # f.write(str(resp.json()['info']))


if __name__ == "__main__":
    Network.get_data('https://httpbin.org/get')
