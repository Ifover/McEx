import sys
sys.path.append('.\\Tools')
import axios  # NOQA: E402
import execjs
from xml.etree import ElementTree
import threading
import queue
# 优先级队列模块


# url = 'http://appimg2.qq.com/card/mk/card_info_v3.js'
# cardInfo = axios.post(url=url)

# with open(r".\card_info_v3.js", 'r') as f:
#     cardInfo = f.read()

# jsdoc = execjs.compile(cardInfo)
# dr = jsdoc.eval('card_list')

# cardsList = {}
# for card in dr:
#     cardsList[str(card[0])] = {
#         "cardId": card[0],
#         "themeId": card[1],
#         "cardName": card[2]
#     }


# def searchUser():
#     global isFind
# print('第' + str(times) + '次搜搜开始')
# times += 1

# print(userList)
# _thread.start_new_thread(searchCard, (userList,))
# searchCard(userList)
# print("对%d个卡友进行搜索" % (len(userList)))


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

            r = axios.post(url=baseUrl, params=mCardUserMainPage,
                           data=mCardUserMainPageData)
            root = ElementTree.XML(r.text)
            # 有时候可能会请求失败
            if root.attrib["code"] != '0':
                continue
            changebox = root.find("changebox")
            # 针对那些有换卡要求的
            if changebox.attrib["exch"] != '0,0,0,0':
                continue

            changeBoxsCards = changebox.findall("card")

            for card in changeBoxsCards:
                # print(card)
                # if(card.attrib["id"] != '0' and card.attrib["id"] != '-1'):
                if(card.attrib["id"] == '10368' and card.attrib["unlock"] == '0'):
                    # print(card.attrib["unlock"])

                    exitFlag = 1
                    print(
                        '找到啦==>http://appimg2.qq.com/card/index_v3.html#opuin=' + opuin)
                    break  # 卡友可能有多张该卡,避免没必要的输出

                    # print(card.attrib["id"])
                    # print(cardsList[card.attrib["id"]]['cardName'])


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


baseUrl = 'https://mfkp.qq.com/cardshow'
mCardUserThemeList = {
    "cmd": "card_user_theme_list",
    "h5ver": 1,
    "uin": 1224842990,
    "tid": 648,
}

exitFlag = 0

if __name__ == "__main__":
    times = 0
    isFind = False  # 找到了就会变成True
    while (not exitFlag):
        # print(isFind)
        res = axios.post(url=baseUrl, params=mCardUserThemeList)
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
