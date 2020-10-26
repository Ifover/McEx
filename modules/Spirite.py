from xml.etree import ElementTree
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  # Qt, QPropertyAnimation
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *
import json
import threading
import time


class Spirite(object):
    def __init__(self):
        self.items = {}
        self.spiriteInfo = {}
        self.currentExplore = {}
        self.spiriteLogCss = '''<style>p{padding:0;margin:0;}.time{font-weight:700;}.error{color:#ef1f1f;} </style>'''
        self.spiriteLogText = ""

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
        self.createSpiriteLog()

    def createSpirite(self):
        self.loadSpiriteInfo()

        self.gBoxSpirite = QtWidgets.QGroupBox(self.tabSpirite)
        self.gBoxSpirite.setGeometry(QtCore.QRect(5, 5, 775, 360))
        self.gBoxSpirite.setTitle('灵宠探险')
        self.treeSpirite = QtWidgets.QTreeWidget(self.gBoxSpirite)

        self.treeSpirite.setGeometry(QtCore.QRect(5, 20, 350, 330))
        self.treeSpirite.setHeaderLabels(['地图', '提示'])
        self.treeSpirite.setColumnWidth(0, 130)
        self.treeSpirite.itemClicked.connect(self.handleTreeItemChange)

        res = self.tool.get("http://appimg2.qq.com/card/mk/soul_elf_v_51.xml")
        xmlStr = res.content.decode()
        root = ElementTree.XML(xmlStr)

        piecelist = root.find("card_piecelist")
        cardPieces = piecelist.findall("card_piece")
        for item in cardPieces:
            self.items[f"56_{item.attrib['id']}"] = {
                "value": f"56_{item.attrib['id']}",
                # "type": item.attrib['type'],
                "id": item.attrib['id'],
                "name": item.attrib['name'],
            }

        cAcross = root.find("c_across")
        chapters = cAcross.findall('chapter')

        id = 0
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

            subId = 0
            for section in sections:
                child = QTreeWidgetItem()
                child.setText(0, section.attrib['name'])
                child.setCheckState(0, Qt.Unchecked)
                child.setText(1, '探索奖励：' + section.attrib['award'])
                child.setText(2, json.dumps({
                    "id": id,
                    "subId": subId
                })
                              )

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
                subId += 1
            id += 1
            # self.items[f"{item.attrib['name']}_{item.attrib['id']}"] = {
            #     "value": f"{item.attrib['type']}_{item.attrib['id']}",
            #     "type": item.attrib['type'],
            #     "id": item.attrib['id'],
            #     "name": item.attrib['name'],
            # }

        self.treeSpirite.expandAll()

        self.btnExplore = QPushButton(self.gBoxSpirite)
        self.btnExplore.setGeometry(QtCore.QRect(360, 310, 150, 40))
        self.btnExplore.setText("开始探索")
        self.btnExplore.clicked.connect(self.handleExplore)
        self.btnExplore.setEnabled(True)

    def createSpiriteInfo(self):
        self.gBoxSpiriteInfo = QtWidgets.QGroupBox(self.gBoxSpirite)
        self.gBoxSpiriteInfo.setTitle('信息')
        self.gBoxSpiriteInfo.setGeometry(QtCore.QRect(360, 15, 150, 290))

        self.fLaySpirite = QFormLayout(self.gBoxSpiriteInfo)
        self.fLaySpirite.setGeometry(QtCore.QRect(5, 300, 140, 300))

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

    def createSpiriteLog(self):
        self.gBoxSpiriteLog = QtWidgets.QGroupBox(self.gBoxSpirite)
        self.gBoxSpiriteLog.setTitle('日志')
        self.gBoxSpiriteLog.setGeometry(QtCore.QRect(515, 15, 255, 335))

        self.tBrowSpiriteLog = QTextBrowser(self.gBoxSpiriteLog)
        self.tBrowSpiriteLog.setGeometry(QtCore.QRect(5, 20, 245, 310))

    def refreshSpiriteLog(self, spiriteData):
        if 'error' in spiriteData and spiriteData['error'] == 1:
            textHtml = f'''
                    <p>
                        <span class="time">[{time.strftime("%H:%M:%S")}]</span><span class="time error">[错误]</span><span>请先选择探险地图</span>
                    </p>
                '''
        else:

            if 'content' in spiriteData:
                contents = spiriteData['content'].split(',')
                for content in contents:
                    arr = content.split('_')
                    value = arr[0] + '_' + arr[1]
                    textHtml = f'''
                        <p>
                            <span class="time">[{time.strftime("%H:%M:%S")}]</span>
                            <span>获得 {self.items[value]['name']} x {str(arr[2])}</span>
                        </p>
                    '''
                    self.loadSpiriteInfo()
                    self.refreshSpiriteInfo()

            elif spiriteData['code'] == -4:
                textHtml = f'''
                        <p>
                            <span class="time">[{time.strftime("%H:%M:%S")}]</span><span class="time error">[错误]</span><span>探险次数不足</span>
                        </p>
                '''

            else:
                textHtml = f'''
                        <p>
                            <span class="time">[{time.strftime("%H:%M:%S")}]</span><span class="time error">[错误]</span><span>未知错误，反正报错了</span>
                        </p>
                '''

        self.spiriteLogText = textHtml + self.spiriteLogText
        self.tBrowSpiriteLog.setText(self.spiriteLogCss + self.spiriteLogText)

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

    # 获取 - 信息
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

    # 信息更新
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

    # 开始探险
    def handleExplore(self):
        self.threadExplore = self.businessExplore(
            tool=self.tool,
            currentExplore=self.currentExplore,
        )
        self.threadExplore.business_explored.connect(self.refreshSpiriteLog)
        self.threadExplore.start()

    class businessExplore(QThread):
        business_explored = pyqtSignal(object)

        def __init__(self, *args, **kwargs):
            super().__init__()
            self.currentExplore = kwargs['currentExplore']
            self.tool = kwargs['tool']

        def run(self):
            try:
                data = {
                    "cnt": 1,
                    "id": self.currentExplore['id'],
                    "act": 11,
                    "sub_id": self.currentExplore['subId']
                }

                times = 15
                while times > 0:
                    spiriteRes = self.tool.post(url="https://card.qzone.qq.com/cgi-bin/card_user_spirite", data=data)
                    spiriteData = spiriteRes.json()
                    print(spiriteData)
                    times -= 1
                    self.business_explored.emit(spiriteData)
                    if not ('content' in spiriteData):
                        times = 0
            except KeyError:
                self.business_explored.emit({"error": 1})
