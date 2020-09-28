import requests
import requests.cookies
from http import cookiejar

session = requests.session()

# load_cookieJar = cookiejar.LWPCookieJar()
# load_cookieJar.load('cookies.txt', ignore_discard=True, ignore_expires=True)
# load_cookies = requests.utils.dict_from_cookiejar(load_cookieJar)
# session.cookies = requests.utils.cookiejar_from_dict(load_cookies)

# new_cookie_jar = cookiejar.LWPCookieJar('cookie.txt')
# requests.utils.cookiejar_from_dict({c.name: c.value for c in session.cookies}, new_cookie_jar)
# new_cookie_jar.save('cookies.txt', ignore_discard=True, ignore_expires=True)


baseUrl = 'https://mfkp.qq.com/cardshow'

cookies = {
    "uin": "o1224842990",
    "skey": "@kTPOlzgVW",
}


def post(url=baseUrl, data={}, params={}):
    try:
        r = requests.post(url=url, data=data, params=params, cookies=cookies)
        r.keep_alive = False
        return r
    except ConnectionError:
        print(ConnectionError)


def get(url=baseUrl, data={}, params={}):
    try:
        r = requests.get(url=url, data=data, params=params, cookies=cookies)
        r.keep_alive = False
        return r
    except ConnectionError:
        print(ConnectionError)
