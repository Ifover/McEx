from xml.dom.minidom import parse
from xml.etree import ElementTree

import requests
import time
import re


res = requests.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
# res = requests.get("./card_info_v3.xml")
xmlStr = res.content.decode()
xmlStr = xmlStr.replace("&", "&amp;")
root = ElementTree.XML(xmlStr)

cards = root.findall("card")
themes = root.findall("theme")

# startTime = int(time.time() * 1000)
# for card in cards:
#     if card.attrib['id'] == '6036':
#         print(card.attrib['name'])
#         break
    # print(card.attrib['id'])


# endTime = int(time.time() * 1000)

# print(cardInfos)
# for theme in themes:
#   if theme.attrib['id'] == '333':
#     print(theme.attrib['name'])
#     break
#   print(theme.attrib['id'])


# print("用时:" + str(endTime - startTime))


def getCardInfo(cardId):
    for card in cards:
        if card.attrib['id'] == str(cardId):
            return {
                "cardId": card.attrib['id'],
                "cardName": card.attrib['name']
            }
