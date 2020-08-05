import requests
from xml.etree import ElementTree

r = requests.get('https://appimg.qq.com/card/mk/card_info_v3.xml')
str = r.text
str = str.replace('&', '&amp;')  # 替换"&"为转义的字符

root = ElementTree.XML(str)

themes = root.findall("theme")
# for theme in themes:
# print(theme.attrib["name"],theme.attrib["gift"].split('|'))

cardsList = {}
cards = root.findall("card")

for card in cards:
    # print(card.attrib["id"])
    # cardsList.append({
    #     "id":  card.attrib["id"],
    #     "themeId":  card.attrib["theme_id"],
    #     "name":  card.attrib["name"],
    #     "price":  card.attrib["price"],
    # })
    
    cardsList[card.attrib["id"]] = {
        "id":  card.attrib["id"],
        "themeId":  card.attrib["theme_id"],
        "name":  card.attrib["name"],
        "price":  card.attrib["price"],
    }


print(cardsList)
