import queue
import winsound
from PyQt5.QtCore import QThread, pyqtSignal
from SearchCard import SearchCard
from Tools import Tools
from xml.dom.minidom import parse
from xml.etree import ElementTree
import gol

class SearchUser(QThread):
    sec_changed_signal = pyqtSignal(int)  # 信号类型：int
    theCardIsSearched = pyqtSignal(str)  # 信号类型：str

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.opuinStr = ""
        self.times = 0
        self.exitFlag = False  # 找到了就会变成True
        self.tid = kwargs['themeId']
        self.findCards = kwargs['selectCardList']  # 要找寻的卡片ID
        self.tool = kwargs['tool']  # 要找寻的卡片ID
        self.isExch = kwargs['isExch']  # 跳过有要求的卡友

    def run(self):
        # tool = Tools()
        while not self.exitFlag:
            mCardUserThemeList = {
                "cmd": "card_user_theme_list",
                "h5ver": 1,
                "uin": gol.get_value('uin'),
                "tid": int(self.tid),  # 卡友正在练的套卡ID985
            }

            res = self.tool.post(params=mCardUserThemeList)
            root = ElementTree.XML(res.text)
            nodeList = root.findall("node")
            usersList = []

            for uin in nodeList:
                uins = uin.attrib["uin"]
                userList = uins.split('|')
                userList = [i for i in userList if i != '']  # 去除空
                self.times += len(userList)
                usersList.append(userList)

            self.sec_changed_signal.emit(self.times)
            workQueue = queue.Queue(len(usersList))

            threads = []
            threadID = 1
            # 填充队列
            for index in range(len(usersList)):
                workQueue.put(index)
            # 创建新线程
            for userList in usersList:
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

        if len(self.opuinStr) > 0:
            self.theCardIsSearched.emit(self.getOpuinStr())

    def setFlag(self):
        self.exitFlag = True

    def getOpuinStr(self):
        try:
            return self.opuinStr
        except Exception:
            return None
