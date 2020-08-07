import sys
sys.path.append('.\\Tools')
import axios  # NOQA: E402
import execjs
from xml.etree import ElementTree


# url = 'http://appimg2.qq.com/card/mk/card_info_v3.js'
# cardInfo = axios.post(url=url)

with open(r".\card_info_v3.js", 'r') as f:
    cardInfo = f.read()

jsdoc = execjs.compile(cardInfo)
dr = jsdoc.eval('card_list')

cardsList = {}
for card in dr:
    cardsList[str(card[0])] = {
        "cardId": card[0],
        "themeId": card[1],
        "cardName": card[2]
    }


baseUrl = 'https://mfkp.qq.com/cardshow'
mCardUserThemeList = {
    "cmd": "card_user_theme_list",
    "h5ver": 1,
    "uin": 1224842990,
    "tid": 964,
}
res = axios.post(url=baseUrl, params=mCardUserThemeList)
root = ElementTree.XML(res.text)

nodeList = root.findall("node")
userList = []
for uin in nodeList:
    uins = uin.attrib["uin"]

    userList = userList + uins.split('|')

userList = [i for i in userList if i != '']
# print(userList)


# 魔卡师信息
mCardUserMainPage = {
    "cmd": "card_user_mainpage",
    "h5ver": 1,
}
for opuin in userList:
    mCardUserMainPageData = {
        "uin": 1224842990,
        "opuin": opuin
    }
    r = axios.post(url=baseUrl, params=mCardUserMainPage,
                   data=mCardUserMainPageData)
    root = ElementTree.XML(r.text)

    changebox = root.find("changebox")
    changeBoxsCards = changebox.findall("card")

    for card in changeBoxsCards:
        # if(card.attrib["id"] != '0' and card.attrib["id"] != '-1'):
        if(card.attrib["id"] == '11265' and card.attrib["unlock"] == '0' ):
            # print(card.attrib["unlock"])
            print('找到啦==>http://appimg2.qq.com/card/index_v3.html#opuin=' + opuin)
            break       #卡友可能有多张该卡,避免没必要的输出
            # print(card.attrib["id"])
            # print(cardsList[card.attrib["id"]]['cardName'])
