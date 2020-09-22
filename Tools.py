import requests


baseUrl = 'https://mfkp.qq.com/cardshow'

cookies = {
    "uin": "o1224842990",
    "skey": "@woxi0nRHW",
}


def post(url=baseUrl, data={}, params={}):
    r = requests.post(url=url, data=data, params=params, cookies=cookies)
    r.keep_alive = False
    return r

def get(url=baseUrl, data={}, params={}):
    r = requests.get(url=url, data=data, params=params, cookies=cookies)
    r.keep_alive = False
    return r
