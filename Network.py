#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import requests
import os.path


class NetworkException(Exception):
    pass


class Network:

    FOLDER = 'data'
    MAX_LINE_SIZE = 8000

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
        # return resp.json()['target_id']  Расскоментировать для получения номера цели

    @staticmethod
    def get_data(url):
        """
        получает информацию с сервера по url, и пишет в файл
        информация вида
        {'target_id':'12', 'info':[{"timestamp":"2017-08-28T15:17:13.157970","x":"571","y":"571","z":"621"}]}
        обязательные поля target_id, info, timestamp
        :param url: dns или ip сервера
        """
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
        filename = os.path.join(Network.FOLDER, filename)
        last_timestamp = ''
        # with open(filename, 'r') as f:
        #     f.seek(0, 2)
        #     fsize = f.tell()
        #     f.seek(max(fsize-Network.MAX_LINE_SIZE, 0), 0)
        #     last_line = f.readlines()[-1]
        #     last_timestamp = json.loads(last_line)['timestamp']
        with open(filename, 'a') as f:
            f.write(json.dumps(resp.json()) + '\n')
            # ## Должен быть лист в поле info
            # list_info = resp.json()['info']
            # for info in list_info:
            #     if last_timestamp != '' and last_timestamp < info['timestamp']:
            #         f.write(json.dumps(info) + '\n')


if __name__ == "__main__":
    Network.get_data('https://httpbin.org/get')