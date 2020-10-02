import requests
import requests.cookies
import gol
import os
from http import cookiejar
from xml.etree import ElementTree

session = requests.session()

class Tools:
    baseUrl = 'https://mfkp.qq.com/cardshow'
    uin = ''
    flag = False

    def __init__(self):
        if not Tools.flag:
            self.path = os.getenv("APPDATA") + r'\McEx\cookie.txt'
            if not os.path.exists(self.path):
                os.mkdir(os.getenv("APPDATA") + r'\McEx')
                with open(self.path, mode='w', encoding='utf-8') as fObject:
                    fObject.write("#LWP-Cookies-2.0\n")
                    fObject.write('Set-Cookie3: skey="@h"; path="/"; domain=""; path_spec; discard; HttpOnly=None; '
                                  'version=0\n')
                    fObject.write(
                        'Set-Cookie3: uin=o1; path="/"; domain=""; path_spec; discard; HttpOnly=None; version=0\n')
                gol.set_value('isLogined', False)
            else:
                self.loadCookie()
            Tools.flag = True

        # isLogined = False
        # cookies = {}

    def loadCookie(self):
        load_cookieJar = cookiejar.LWPCookieJar()
        load_cookieJar.load(self.path, ignore_discard=True, ignore_expires=True)
        load_cookies = requests.utils.dict_from_cookiejar(load_cookieJar)
        gol.set_value('cookies', load_cookies)
        params = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }
        data = {
            "uin": load_cookies['uin'][1:],
        }
        res = self.post(params=params, data=data)
        root = ElementTree.XML(res.text)
        if root.attrib["code"] == '0':
            print('Token-有效')
            gol.set_value('isLogined', True)

    def saveCookie(self):
        cookies = gol.get_value('cookies')
        new_cookie_jar = cookiejar.LWPCookieJar(self.path)
        requests.utils.cookiejar_from_dict({c: str(cookies[c]) for c in cookies}, new_cookie_jar)
        new_cookie_jar.save(self.path, ignore_discard=True, ignore_expires=True)

        print('Token-保存成功')

    def post(self, url=None, data={}, params={}):
        url = url if url else self.baseUrl
        cookies = gol.get_value("cookies")

        try:
            r = requests.post(url=url, data=data, params=params, cookies=cookies)
            r.keep_alive = False
            return r
        except ConnectionError:
            print(ConnectionError)

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
