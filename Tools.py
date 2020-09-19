import requests


baseUrl = 'https://mfkp.qq.com/cardshow'
mCardUserMainPage = {
    "cmd": "card_user_mainpage",
    "h5ver": 1,
}
mCardUserMainPageData = {
    "uin": 1224842990,
}

cookies = {
    "uin": "o1224842990",
    "skey": "@YZN6r2xbW",
}


def post(url=baseUrl, data={}, params={}):
    r = requests.post(url=url, data=data, params=params, cookies=cookies)
    r.keep_alive = False
    return r
