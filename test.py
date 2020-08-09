import sys
sys.path.append('.\\Tools')
import axios  # NOQA: E402
import execjs
from xml.etree import ElementTree
import threading
import queue


baseUrl = 'https://mfkp.qq.com/cardshow'
mCardUserThemeList = {
    "cmd": "card_user_theme_list",
    "h5ver": 1,
    "uin": 1224842990,
    "tid": 648,
}

mCardUserMainPage = {
    "cmd": "card_user_mainpage",
    "h5ver": 1,
}

res = axios.post(url=baseUrl, params=mCardUserThemeList)
root = ElementTree.XML(res.text)
nodeList = root.findall("node")
userList = []
nameList = []
for uin in nodeList:
    uins = uin.attrib["uin"]
    # userList = userList + uins.split('|')
    userList += uins.split('|')
    userList = [i for i in userList if i != '']
    # usersList.append(userList)

for opuin in userList:
  mCardUserMainPageData = {
      "uin": 1224842990,
      "opuin": opuin
      }

  r = axios.post(url=baseUrl, params=mCardUserMainPage,
                  data=mCardUserMainPageData)
  root = ElementTree.XML(r.text)
  print(root.attrib["code"])

 # QQHOME = root.find("QQHOME")
    # if root.attrib["code"] != '0':
    #     continue
    # changebox = root.find("changebox")
    # # 针对那些有换卡要求的
    # if changebox.attrib["exch"] != '0,0,0,0':
    #     continue

    # changeBoxsCards = changebox.findall("card")

    # for card in changeBoxsCards:
    #     # print(card)
    #     # if(card.attrib["id"] != '0' and card.attrib["id"] != '-1'):
    #     if(card.attrib["id"] == '10368' and card.attrib["unlock"] == '0'):
    #         # print(card.attrib["unlock"])

    #         exitFlag = 1
    #         print(
    #             '找到啦==>http://appimg2.qq.com/card/index_v3.html#opuin=' + opuin)
    #         break  # 卡友可能有多张该卡,避免没必要的输出

    #         # print(card.attrib["id"])
    #         # print(cardsList[card.attrib["id"]]['cardName'])
