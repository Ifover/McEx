from fastapi import FastAPI, Header
from typing import List
import requests
from xml.etree import ElementTree
import sys
sys.path.append('.\\Tools')
import axios  # NOQA: E402

app = FastAPI()


@app.get('/test/a={a}/b={b}')
def calculate(a: int = None, b: int = None):
    c = a + b
    res = {"res": c}
    return res


@app.get('/mcex/getUserInfo')
def card(cookie: List[str] = Header(None)):

    print(cookie)
    baseUrl = 'https://mfkp.qq.com/cardshow'

    mCardUserMainPage = {
        "cmd": "card_user_mainpage",
        "h5ver": 1,
    }
    mCardUserMainPageData = {
        "uin": 1224842990,
        # "opuin": opuin
    }
    r = axios.post(url=baseUrl, params=mCardUserMainPage,
                   data=mCardUserMainPageData)
    root = ElementTree.XML(r.text)
    changebox = root.find("changebox")
    changeBoxCards = changebox.findall("card")
    arr = []
    for card in changeBoxCards:
        arr.append({
            "slot": card.attrib["slot"],
            "id": card.attrib["id"],
            "unlock": card.attrib["unlock"],
        })

    storebox = root.find("storebox")
    storeboxCards = changebox.findall("card")
    arr2 = []
    for card in storeboxCards:
        arr2.append({
            "slot": card.attrib["slot"],
            "id": card.attrib["id"],
            "unlock": card.attrib["unlock"],
        })
    return {
        "changebox": arr,
        "storebox": arr2
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8080, workers=1)
