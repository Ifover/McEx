from xml.etree import ElementTree
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  # Qt, QPropertyAnimation
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *
import json
import threading


class Spirite(object):
    def __init__(self):
        self.items = {}
        self.spiriteInfo = {}
        self.currentExplore = {}

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.tabSpirite = kwargs['tabSpirite']
        self.labelStatusStr = kwargs['labelStatusStr']
        self.uin = kwargs['uin']
        res = self.tool.get("http://appimg2.qq.com/card/swf/resource/resource_v_1649.xml")
        xmlStr = res.content.decode()
        root = ElementTree.XML(xmlStr)
        propItems = root.find("propItems")
        for item in propItems:
            self.items[f"{item.attrib['type']}_{item.attrib['id']}"] = {
                "value": f"{item.attrib['type']}_{item.attrib['id']}",
                "type": item.attrib['type'],
                "id": item.attrib['id'],
                "name": item.attrib['name'],
            }

        self.createSpirite()
        self.createSpiriteInfo()

    def createSpirite(self):
        self.loadSpiriteInfo()

        self.gBoxSpirite = QtWidgets.QGroupBox(self.tabSpirite)
        self.gBoxSpirite.setGeometry(QtCore.QRect(5, 5, 775, 360))
        self.gBoxSpirite.setTitle('灵宠探险')
        self.treeSpirite = QtWidgets.QTreeWidget(self.gBoxSpirite)

        self.treeSpirite.setGeometry(QtCore.QRect(5, 20, 550, 330))
        self.treeSpirite.setHeaderLabels(['地图', '提示'])
        self.treeSpirite.setColumnWidth(0, 130)
        self.treeSpirite.itemClicked.connect(self.handleTreeItemChange)

        res = self.tool.get("http://appimg2.qq.com/card/mk/soul_elf_v_51.xml")
        xmlStr = res.content.decode()
        root = ElementTree.XML(xmlStr)
        # data = root.find("data")
        cAcross = root.find("c_across")
        chapters = cAcross.findall('chapter')

        for chapter in chapters:
            treeChapter = QTreeWidgetItem(self.treeSpirite)
            treeChapter.setText(0, chapter.attrib['name'])
            treeChapter.setText(1, chapter.attrib['tips'])
            treeChapter.setToolTip(1, chapter.attrib['tips'])

            if (self.spiriteInfo['pass_id'] < int(chapter.attrib['id'])):
                treeChapter.setText(1, '条件不足')
                treeChapter.setToolTip(1, '条件不足')
                treeChapter.setDisabled(True)

            sections = chapter.findall('section')
            for section in sections:
                child = QTreeWidgetItem()
                child.setText(0, section.attrib['name'])
                child.setCheckState(0, Qt.Unchecked)
                child.setText(1, '探索奖励：' + section.attrib['award'])
                child.setText(2,
                              json.dumps({"id": int(section.attrib['open_c']), "subId": int(section.attrib['open_s'])}))

                child.setToolTip(1, '探索奖励：\n' + "\n".join(section.attrib['award'].split('|')))

                noLv = True
                for item in self.spiriteInfo['spirites']:
                    if item['lv'] >= int(section.attrib['elf_lv']):
                        noLv = False
                        break

                if (self.spiriteInfo['pass_id'] < int(section.attrib['open_c'])) or \
                        (self.spiriteInfo['section_id'] < int(section.attrib['open_s'])) or \
                        (len(self.spiriteInfo['spirites']) < int(section.attrib['elf_num'])) or \
                        noLv:
                    child.setText(1, '条件不足')
                    child.setToolTip(1, '条件不足')
                    child.setDisabled(True)

                treeChapter.addChild(child)

            # self.items[f"{item.attrib['name']}_{item.attrib['id']}"] = {
            #     "value": f"{item.attrib['type']}_{item.attrib['id']}",
            #     "type": item.attrib['type'],
            #     "id": item.attrib['id'],
            #     "name": item.attrib['name'],
            # }
        self.treeSpirite.expandAll()

        self.btnExplore = QPushButton(self.gBoxSpirite)
        self.btnExplore.setGeometry(QtCore.QRect(560, 310, 210, 40))
        self.btnExplore.setText("开始探索")
        self.btnExplore.clicked.connect(self.handleExplore)
        self.btnExplore.setEnabled(True)

    def createSpiriteInfo(self):
        self.gBoxSpiriteInfo = QtWidgets.QGroupBox(self.gBoxSpirite)
        self.gBoxSpiriteInfo.setTitle('信息')
        self.gBoxSpiriteInfo.setGeometry(QtCore.QRect(560, 15, 210, 290))

        self.fLaySpirite = QFormLayout(self.gBoxSpiriteInfo)
        self.fLaySpirite.setGeometry(QtCore.QRect(5, 300, 200, 300))

        self.fLaySpirite.setLabelAlignment(Qt.AlignRight)

        self.labTreasureMap = QLabel()  # 藏宝图
        self.labGoldKey = QLabel()  # 金钥匙
        self.labGoldFen = QLabel()  # 金粉
        self.labColorStone = QLabel()  # 五彩石
        self.labMoney = QLabel()  # 金币
        self.labPower = QLabel()  # 灵力点
        self.labYinDing = QLabel()  # 银锭
        self.labBaiBianDan = QLabel()  # 百变丹
        self.labExploreCnt = QLabel()  # 穿越丛林次数

        self.fLaySpirite.addRow("藏宝图", self.labTreasureMap)
        self.fLaySpirite.addRow("金钥匙", self.labGoldKey)
        self.fLaySpirite.addRow("金粉", self.labGoldFen)
        self.fLaySpirite.addRow("五彩石", self.labColorStone)
        self.fLaySpirite.addRow("金币", self.labMoney)
        self.fLaySpirite.addRow("灵力点", self.labPower)
        self.fLaySpirite.addRow("银锭", self.labYinDing)
        self.fLaySpirite.addRow("百变丹", self.labBaiBianDan)
        self.fLaySpirite.addRow("穿越丛林", self.labExploreCnt)

        self.refreshSpiriteInfo()

    def handleTreeItemChange(self, item):
        iterator = QTreeWidgetItemIterator(self.treeSpirite)

        while iterator.value():
            it = iterator.value()
            if it.text(2) and it != item:
                it.setCheckState(0, 0)
            elif it.text(2):
                self.currentExplore = json.loads(it.text(2))
                # print(self.currentExplore)

            iterator.__iadd__(1)

    def loadSpiriteInfo(self):
        data = {
            "act": 1,
            "opuin": self.uin
        }
        res = self.tool.post(url="https://card.qzone.qq.com/cgi-bin/card_user_spirite", data=data)
        self.spiriteInfo = res.json()

        data = {
            "uin": self.uin
        }
        res = self.tool.post(url="https://card.qzone.qq.com/cgi-bin/card_user_mainpage", data=data)

        xmlStr = res.content.decode()
        root = ElementTree.XML(xmlStr)
        newData = root.find("new_data")
        user = root.find("user")
        self.spiriteInfo['goldFen'] = newData.attrib['gold_fen']
        self.spiriteInfo['colorStone'] = newData.attrib['color_stone']
        self.spiriteInfo['money'] = user.attrib['money']

    def refreshSpiriteInfo(self):
        self.labTreasureMap.setText(str(self.spiriteInfo['treasure_map']))
        self.labGoldKey.setText(str(self.spiriteInfo['gold_key']))
        self.labGoldFen.setText(str(self.spiriteInfo['goldFen']))
        self.labColorStone.setText(str(self.spiriteInfo['colorStone']))
        self.labMoney.setText(str(self.spiriteInfo['money']))
        self.labPower.setText(str(self.spiriteInfo['power']))
        self.labYinDing.setText(str(self.spiriteInfo['yinding']))
        self.labBaiBianDan.setText(str(self.spiriteInfo['baibiandan']))
        self.labExploreCnt.setText(str(f"{10 - self.spiriteInfo['torrid_zone_explore_cnt']} / 10"))

    # def businessExplore(self):

    def handleExplore(self):
        # print(self.businessExplore)
        # self.threadExplore = QThread()
        # self.threadExplore.started.connect(self.businessExplore)
        # # self.threadExplore = threading.Thread(target=self.businessExplore)
        self.threadExplore = self.businessExplore(
            tool=self.tool,
            currentExplore=self.currentExplore,
        )
        self.threadExplore.start()
        # self.threadExplore.join()

    class businessExplore(QThread):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.currentExplore = kwargs['currentExplore']
            self.tool = kwargs['tool']

        def run(self):
            # print(self.items['73_0'])
            #
            data = {
                # "cnt": 1,
                "id": self.currentExplore['id'],
                "act": 11,
                "sub_id": self.currentExplore['subId']
            }
            # print(data)
            times = 10
            while times > 0:
                spiriteRes = self.tool.post(url="https://card.qzone.qq.com/cgi-bin/card_user_spirite", data=data)
                # spiriteData = spiriteRes.text
                spiriteData = spiriteRes.json()
                print(spiriteData)
                times -= 1
                if 'content' in spiriteData:
                    contents = spiriteData['content'].split(',')
                    for content in contents:
                        arr = content.split('_')
                        value = arr[0] + '_' + arr[1]
                        # print(value)
                        print(self.items[value]['name'] + 'x' + str(arr[2]))
