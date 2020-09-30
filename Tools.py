import requests
import requests.cookies
import gol
from http import cookiejar

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

    # def __init__(self):

    #     isLogined = False
    #     cookies = {}
    #

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
