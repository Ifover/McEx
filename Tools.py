import requests
import requests.cookies
import gol
import os
from http import cookiejar
from xml.etree import ElementTree
import configparser

session = requests.session()
session.keep_alive = False


class Tools:
    baseUrl = 'https://mfkp.qq.com/cardshow'
    uin = ''
    flag = False

    def __init__(self):
        if not Tools.flag:
            self.path = r'./config.ini'
            self.iniConfig = configparser.ConfigParser()  # 类实例化
            if not os.path.exists(self.path):
                self.iniConfig.add_section('config')  # 首先添加一个新的section
                self.iniConfig.set('config', 'uin', '')  # 写入数据
                self.iniConfig.set('config', 'skey', '')  # 写入数据
                self.iniConfig.write(open(self.path, 'a'))  # 保存数据
                self.loadCookie()
            else:
                self.loadCookie()
            Tools.flag = True

    def loadCookie(self):
        self.iniConfig.read(self.path)
        load_cookies = {
            "uin": 'o' + self.iniConfig['config']['uin'],
            "skey": '@' + self.iniConfig['config']['skey']
        }
        # print(load_cookies)
        gol.set_value('cookies', load_cookies)
        gol.set_value('uin', self.iniConfig['config']['uin'])
        params = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }
        data = {
            "uin": load_cookies['uin'][1:],
        }
        res = self.post(params=params, data=data)
        root = ElementTree.XML(res.text)
        # print(root.attrib["code"])
        if root.attrib["code"] == '0':
            gol.set_value('isLogined', True)

    def saveCookie(self):
        cookies = gol.get_value('cookies')
        new_cookie_jar = cookiejar.LWPCookieJar(self.path)
        requests.utils.cookiejar_from_dict({c: str(cookies[c]) for c in cookies}, new_cookie_jar)
        new_cookie_jar.save(self.path, ignore_discard=True, ignore_expires=True)

        # print('Token-保存成功')

    def post(self, url=None, data={}, params={}):
        url = url if url else self.baseUrl
        cookies = gol.get_value("cookies")
        # print(65, cookies)
        try:
            r = requests.post(url=url, data=data, params=params, cookies=cookies)
            r.keep_alive = False
            return r
        except ConnectionResetError:
            print(ConnectionResetError)

    def get(self, url=None, data={}, params={}):
        url = url if url else self.baseUrl
        cookies = gol.get_value("cookies")
        # print(cookies)
        try:
            r = requests.get(url=url, data=data, params=params, cookies=cookies)
            r.keep_alive = False
            return r
        except ConnectionError:
            print(ConnectionError)
