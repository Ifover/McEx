from fastapi import FastAPI
import requests
from xml.etree import ElementTree


app = FastAPI()


@app.get('/test/a={a}/b={b}')
def calculate(a: int = None, b: int = None):
    c = a + b
    res = {"res": c}
    return res


@app.get('/mcex/card')
def card(a: int = None, b: int = None):
    r = requests.get('https://appimg.qq.com/card/mk/card_info_v3.xml')
    str = r.text
    str = str.replace('&', '&amp;')  # 替换"&"为转义的字符

    root = ElementTree.XML(str)

    themes = root.findall("theme")

    cardsList = {}
    cards = root.findall("card")

    for card in cards:
        cardsList[card.attrib["id"]] = {
            "id":  card.attrib["id"],
            "themeId":  card.attrib["theme_id"],
            "name":  card.attrib["name"],
            "price":  card.attrib["price"],
        }


    return cardsList

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8080, workers=1)
