import execjs
import requests
from xml.etree import ElementTree
import threading
import queue
import winsound
import mcInfo


def searchCard(id, userList, q):
    global exitFlag
    # 魔卡师信息
    mCardUserMainPage = {
        "cmd": "card_user_mainpage",
        "h5ver": 1,
    }

    for opuin in userList:
        if not exitFlag:
            mCardUserMainPageData = {
                "uin": 1224842990,
                "opuin": opuin
            }

            r = post(url=baseUrl, params=mCardUserMainPage,
                     data=mCardUserMainPageData)
            root = ElementTree.XML(r.text)
            # 有时候可能会请求失败
            if root.attrib["code"] != '0':
                continue
            changebox = root.find("changebox")
            # 针对那些有换卡要求的
            if isExch:
                if changebox.attrib["exch"] != '0,0,0,0':
                    continue

            changeBoxsCards = changebox.findall("card")

            for card in changeBoxsCards:
                # print(card)
                # if(card.attrib["id"] != '0' and card.attrib["id"] != '-1'):
                if(int(card.attrib["id"]) in findCards and card.attrib["unlock"] == '0'):
                    # print(card.attrib["unlock"])

                    exitFlag = 1
                    print("\n【{cardName}[{id}]】==> http://appimg2.qq.com/card/index_v3.html#opuin={opuin}".format(
                        cardName=mcInfo.getCardInfo(card.attrib["id"])['cardName'], id=card.attrib["id"], opuin=opuin))
                    winsound.Beep(600, 700)
                    break  # 卡友可能有多张该卡,避免没必要的输出


def post(url, data={}, params={}):
    r = requests.post(url=url, data=data, params=params, cookies=cookies)
    r.keep_alive = False
    return r


class myThread (threading.Thread):
    def __init__(self, threadID, userList, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.userList = userList
        self.q = q

    def run(self):
        # print("开启线程：" + str(len(self.userList)))
        searchCard(self.threadID, self.userList, self.q)
        # print("退出线程：" + str(len(self.userList)))


requests.adapters.DEFAULT_RETRIES = 3
exitFlag = 0
baseUrl = 'https://mfkp.qq.com/cardshow'
mCardUserThemeList = {
    "cmd": "card_user_theme_list",
    "h5ver": 1,
    "uin": 1224842990,
    "tid": 984,  # 卡友正在练的套卡ID
}

cookies = {
    "uin": "o1224842990",
    "skey": "@IwID4Asg7",
}

isExch = False  # 跳过有要求的卡友

# 要找寻的卡片ID
# findCards = [12137, 12138, 12139, 12141, 12143, 12144]
findCards = [
 15024
]

if __name__ == "__main__":
    times = 0
    isFind = False  # 找到了就会变成True
    while (not exitFlag):
        # print(isFind)
        try:
            res = post(url=baseUrl, params=mCardUserThemeList)
            root = ElementTree.XML(res.text)
            nodeList = root.findall("node")
            usersList = []
            nameList = []
            for uin in nodeList:
                uins = uin.attrib["uin"]
                # userList = userList + uins.split('|')
                userList = uins.split('|')
                userList = [i for i in userList if i != '']
                times = times + len(userList)
                usersList.append(userList)

            print('\rsearching... Times:{0}'.format(times), end='')

            workQueue = queue.Queue(len(usersList))
            threads = []
            threadID = 1
            # 填充队列
            for index in range(len(usersList)):
                workQueue.put(index)
            # print(usersList)
            # 创建新线程
            for userList in usersList:
                thread = myThread(threadID, userList, workQueue)
                thread.start()
                threads.append(thread)
                threadID += 1
            # 等待队列清空
            # while not workQueue.empty():
            #     pass

            # 通知线程是时候退出
            # exitFlag = 1
            # 等待所有线程完成
            for t in threads:
                t.join()
            # print("退出主线程")
        except:
            pass
