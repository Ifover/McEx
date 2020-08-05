
import requests
import execjs
from xml.etree import ElementTree


cookiess = "uin=o1224842990; skey=@PF6hMeQLV"

cookies = {}

for line in cookiess.split(";"):
    if line.find("=") != -1:
        name, value = line.strip().split("=")
        cookies[name] = value


url = 'http://appimg2.qq.com/card/mk/card_info_v3.js'
# url = 'https://mfkp.qq.com/cardshow?cmd=card_user_mainpage&h5ver=1&g_tk=1033445924&ishttps=1&mkfrom=mkqz&is_h5=1'
# url2 = 'https://mfkp.qq.com/cardshow?cmd=card_market_npc_buy&h5ver=1&g_tk=1033445924&ishttps=1&theme_id=929&card_id=14326'
r = requests.post(url=url, cookies=cookies)
# r.decode='GBK'
res = r.text
# print(res)

# res = r.text.replace(/\r\n/g, "");  encoding='gbk'

# with open(r".\list.js", 'r') as f:
#     res = f.read()

jsdoc = execjs.compile(res)
dr = jsdoc.eval('card_list')
cardsList = {}
for card in dr:
    cardsList[card[0]] = {
        "cardId": card[0],
        "themeId": card[1],
        "cardName": card[2]
    }
print(cardsList)




# r2 = requests.post(url=url2, cookies=cookies)
# print(r)
# root = ElementTree.XML(r.text)

# changebox = root.find("changebox")
# changeBoxsCards = changebox.findall("card")
# for card in changeBoxsCards:
#     print(card.attrib["id"])
