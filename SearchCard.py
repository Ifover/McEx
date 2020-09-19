from xml.etree import ElementTree
import threading
import Tools
import sys
import time


class SearchCard(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self._self = args[0]
        self.threadID = args[1]
        self.userList = args[2]
        self.q = args[3]

    def run(self):
        # print("开启线程：" + str(len(self.userList)))
        # self.searchCard(self.threadID, self.userList, self.q)
        # print("退出线程：" + str(len(self.userList)))
        mCardUserMainPage = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }

        for opuin in self.userList:
            if not self._self.exitFlag:
                mCardUserMainPageData = {
                    "uin": 1224842990,
                    "opuin": opuin
                }

                r = Tools.post(params=mCardUserMainPage,
                         data=mCardUserMainPageData)
                root = ElementTree.XML(r.text)
                # 有时候可能会请求失败
                if root.attrib["code"] != '0':
                    continue
                changebox = root.find("changebox")
                # 针对那些有换卡要求的
                if self._self.isExch:
                    if changebox.attrib["exch"] != '0,0,0,0':
                        continue

                changeBoxsCards = changebox.findall("card")

                for card in changeBoxsCards:

                    # if(card.attrib["id"] != '0' and card.attrib["id"] != '-1'):
                    if(int(card.attrib["id"]) in self._self.findCards and card.attrib["unlock"] == '0'):
                        # print(card.attrib["unlock"])
                        # print(opuin)

                        self._self.opuinStr = opuin
                        self._self.exitFlag = True
                        # print("\n【{cardName}[{id}]】==> http://appimg2.qq.com/card/index_v3.html#opuin={opuin}".format(
                        #     cardName=mcInfo.getCardInfo(card.attrib["id"])['cardName'], id=card.attrib["id"], opuin=opuin))
                        # winsound.Beep(600, 700)
                        break  # 卡友可能有多张该卡,避免没必要的输出
