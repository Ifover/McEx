import requests

# cookiess = "uin=o1224842990; skey=@PF6hMeQLV"


# class Axios:
#   def __init__(self):
#     self.cookies = {
#       "uin":"o1224842990",
#       "skey":"@PF6hMeQLV",
#     }

#   def post(self,url,data):
#     return requests.post(url=url, cookies=self.cookies)

# for line in cookiess.split(";"):
#     if line.find("=") != -1:
#         name, value = line.strip().split("=")
#         cookies[name] = value

# x = Axios()
# x.post()


cookies = {
    "uin": "o1224842990",
    "skey": "@IKNL9FdrN",
}


def post(url, data={}, params={}):
    return requests.post(url=url, data=data, params=params, cookies=cookies)
