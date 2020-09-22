import queue
import winsound
from PyQt5.QtCore import *
from SearchCard import SearchCard
import Tools
from xml.dom.minidom import parse
from xml.etree import ElementTree


baseUrl = 'https://mfkp.qq.com/cardshow'


class SearchUser(QThread):

    sec_changed_signal = pyqtSignal(int)  # 信号类型：int
    theCardIsSearched = pyqtSignal(str)  # 信号类型：str

    def __init__(self, *args):
        super().__init__()
        self.opuinStr = ""
        self.times = 0
        self.exitFlag = False  # 找到了就会变成True
        self.isExch = False   # 跳过有要求的卡友
        self.tid = args[0]
        self.findCards = args[1]  # 要找寻的卡片ID
        print(args[1])

    def run(self):
        while (not self.exitFlag):
            try:
                mCardUserThemeList = {
                    "cmd": "card_user_theme_list",
                    "h5ver": 1,
                    "uin": 1224842990,
                    "tid": int(self.tid),  # 卡友正在练的套卡ID
                }
                res = Tools.post(url=baseUrl, params=mCardUserThemeList)
                root = ElementTree.XML(res.text)
                nodeList = root.findall("node")
                usersList = []
                nameList = []

                for uin in nodeList:
                    uins = uin.attrib["uin"]
                    userList = uins.split('|')
                    userList = [i for i in userList if i != '']  # 去除空
                    self.times += len(userList)
                    usersList.append(userList)

                    # print(times)
                # print('\rsearching... Times:{0}'.format(self.times), end='')
                # print(usersList)

                self.sec_changed_signal.emit(self.times)
                workQueue = queue.Queue(len(usersList))

                threads = []
                threadID = 1
                # 填充队列
                for index in range(len(usersList)):
                    workQueue.put(index)
                # print(usersList)
                # 创建新线程
                for userList in usersList:
                    # print(userList)
                    # print(threadID, userList, workQueue)

                    thread = SearchCard(
                        self, threadID, userList, workQueue, self.findCards)
                    # thread = searchCard(self, threadID, userList, workQueue)
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
                # return opuinStr
                # print("退出主线程")
            except:
                pass
        
        if len(self.opuinStr) > 0:
            self.theCardIsSearched.emit(self.getOpuinStr())
        # print('\n' + self.getOpuinStr())

    def setFlag(self):
        # print(self.exitFlag)
        self.exitFlag = True


    def getOpuinStr(self):
        try:
            # print(self.opuinStr)

            return self.opuinStr
        except Exception:
            return None
