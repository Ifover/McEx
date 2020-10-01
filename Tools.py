import requests
import requests.cookies
import gol
import os
from http import cookiejar
from xml.etree import ElementTree

session = requests.session()


# load_cookieJar = cookiejar.LWPCookieJar()
# load_cookieJar.load('cookies.txt', ignore_discard=True, ignore_expires=True)
# load_cookies = requests.utils.dict_from_cookiejar(load_cookieJar)
# session.cookies = requests.utils.cookiejar_from_dict(load_cookies)

# new_cookie_jar = cookiejar.LWPCookieJar('cookie.txt')
# requests.utils.cookiejar_from_dict({c.name: c.value for c in session.cookies}, new_cookie_jar)
# new_cookie_jar.save('cookies.txt', ignore_discard=True, ignore_expires=True)

class Tools:
    baseUrl = 'https://mfkp.qq.com/cardshow'
    uin = ''

    def __init__(self):
        self.path = os.getenv("APPDATA") + r'\McEx\cookie.txt'
        if not os.path.exists(self.path):
            file = open(self.path, 'w')
            file.write('')
            file.close()
            gol.set_value('isLogined', False)
        else:
            self.loadCookie()
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
            print('Token有效')
            gol.set_value('isLogined', True)

    def saveCookie(self):
        cookies = gol.get_value('cookies')
        new_cookie_jar = cookiejar.LWPCookieJar(self.path)
        requests.utils.cookiejar_from_dict({c: str(cookies[c]) for c in cookies}, new_cookie_jar)
        new_cookie_jar.save(self.path, ignore_discard=True, ignore_expires=True)

        print('保存成功')

    def post(self, url=None, data={}, params={}):
        url = url if url else self.baseUrl
        cookies = gol.get_value("cookies")
        # print(self.baseUrl)
        # print(cookies)

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
