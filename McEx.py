# -*- coding: utf-8 -*-
# import sys
# import time

from xml.etree import ElementTree

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  # Qt, QPropertyAnimation
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound

from SearchUser import SearchUser
import gol


class McEx(object):
    def __init__(self):
        # super(self).__init__(parent)
        self.isStart = False
        self.cardsMine = []
        self.selectCardList = []
        self.cardsFriend = []
        self.slotMine = []
        self.slotFriend = []
        self.rootCardDict = {}
        self.rootThemeDict = {}
        self.opuin = ''
        self.uin = ""
        self.isExch = False
        self.searchThemeName = ''

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.tabMcEx = kwargs['tabMcEx']
        self.labelStatusStr = kwargs['labelStatusStr']

        self.init(gol.get_value('cookies')['uin'][1:])

    def init(self, uin):

        self.labelStatusStr.setText("登录成功，正在初始化数据")

        self.uin = uin

        # region 初始化字典
        cardInfoV3 = self.tool.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
        xmlStr = cardInfoV3.content.decode()
        xmlStr = xmlStr.replace("&", "&amp;")
        root = ElementTree.XML(xmlStr)

        self.cards = root.findall("card")
        self.themes = root.findall("theme")
        for card in self.cards:
            self.rootCardDict[card.attrib["id"]] = {
                "id": card.attrib["id"],
                "themeId": card.attrib["theme_id"],
                "cardName": card.attrib["name"],
                "price": card.attrib["price"],
            }

        for theme in self.themes:
            self.rootThemeDict[theme.attrib["id"]] = {
                "id": int(theme.attrib["id"]),
                "themeName": theme.attrib["name"],
                "diff": int(theme.attrib["diff"]),
                "type": int(theme.attrib["type"]),
                "time": int(theme.attrib["time"]),
            }
        # endregion

        self.createThemeBox()  # 绘制 - 套卡容器
        self.createCardBox()  # 绘制 - 卡片容器

        self.createMineBox()  # 绘制 - 我的卡箱
        self.createFriendBox()  # 绘制 - 卡友的换卡箱

        self.gBoxTheme.raise_()

        self.labelStatusStr.setText("初始化成功~")

    # 绘制 - 套卡容器
    def createThemeBox(self):
        self.gBoxTheme = QGroupBox(self.tabMcEx)
        self.gBoxTheme.setGeometry(QtCore.QRect(-165, 5, 210, 360))
        self.gBoxTheme.setAutoFillBackground(True)
        self.gBoxTheme.setStyleSheet(".QGroupBox{background-color:#fff}")
        self.gBoxTheme.setTitle("选择套卡")

        self.listViewThemeBox = QPropertyAnimation(self.gBoxTheme, b"geometry")
        self.btnSelectTheme = QtWidgets.QPushButton(self.gBoxTheme)
        self.btnSelectTheme.setGeometry(QtCore.QRect(170, 19, 30, 336))
        self.btnSelectTheme.setText(">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
        self.btnSelectTheme.setCheckable(True)
        self.btnSelectTheme.clicked.connect(self.btnSelectThemeChange)

        self.textbox = QLineEdit(self.gBoxTheme)
        self.textbox.setGeometry(QtCore.QRect(5, 20, 160, 24))
        self.textbox.setPlaceholderText("输入套卡名称")
        self.textbox.textChanged.connect(self.handleEditChange)

        self.tabWidget = QtWidgets.QTabWidget(self.gBoxTheme)
        self.tabWidget.setGeometry(QtCore.QRect(5, 50, 160, 20))

        self.themesList = [
            {"id": 1, "label": "发行", "type": [0, 2]},
            {"id": 2, "label": "下架", "type": [1, 5]},
            {"id": 3, "label": "闪卡", "type": [9]},
        ]

        self.currentTheme = self.themesList[0]

        for i in range(len(self.themesList)):
            tab = QWidget()
            self.tabWidget.addTab(tab, self.themesList[i]["label"])
            # self.tab1.addTab(i, self.themesList[i]["label"])

        self.treeThemeList = QTreeWidget(self.gBoxTheme)
        self.treeThemeList.setGeometry(QtCore.QRect(5, 70, 160, 284))
        self.treeThemeList.setHeaderLabels(['套卡名称'])
        self.treeThemeList.clicked.connect(self.handleThemeSelect)
        self.tabWidget.currentChanged.connect(self.handleTbThemeListClicked)
        self.createThemeList()

    # 绘制 - 套卡列表
    def createThemeList(self):
        self.treeThemeList.clear()

        data = {
            "uin": self.uin,
        }
        res = self.tool.post(url="https://card.qzone.qq.com/cgi-bin/card_mini_get", data=data)
        etXml = ElementTree.XML(res.text)
        Nodes = etXml.findall("Node")
        getThemeList = []
        for node in Nodes:
            getThemeList.append(node.attrib['theme_id'])

        self.treeThemeList.invisibleRootItem()
        for index in range(1, 6):
            root = QTreeWidgetItem(self.treeThemeList)
            root.setText(0, "难度系数：" + ('★' * index))
            # 设置子节点1
            for theme in self.themes:
                if theme.attrib['diff'] == str(index) and \
                        (int(theme.attrib['type']) in self.currentTheme["type"]) and \
                        theme.attrib["new_type"] == "0" and \
                        theme.attrib["gift"] != "" and \
                        theme.attrib['name'].find(self.searchThemeName) >= 0:
                    child = QTreeWidgetItem()
                    child.setText(0, theme.attrib['name'])
                    child.setText(1, theme.attrib['id'])
                    if theme.attrib['id'] in getThemeList:
                        child.setForeground(0, QBrush(QColor("#124c6f")))
                        child.setBackground(0, QBrush(QColor("#9ad033")))
                    else:
                        child.setForeground(0, QBrush(QColor("#955935")))

                    root.insertChild(0, child)

    # 绘制 - 卡片容器
    def createCardBox(self):
        self.gBoxCard = QtWidgets.QGroupBox(self.tabMcEx)
        self.gBoxCard.setGeometry(QtCore.QRect(50, 5, 180, 360))
        self.gBoxCard.setMinimumSize(QtCore.QSize(0, 0))
        self.gBoxCard.setAutoFillBackground(False)
        self.gBoxCard.setTitle("选择卡片")

        self.lBoxCardList = QListWidget(self.gBoxCard)
        self.lBoxCardList.setGeometry(QtCore.QRect(5, 20, 170, 310))
        self.lBoxCardList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.lBoxCardList.addItem('请选择套卡~~')
        self.lBoxCardList.setEnabled(False)
        self.lBoxCardList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lBoxCardList.itemSelectionChanged.connect(self.handleCardSelect)

        self.layWCardBox = QtWidgets.QWidget(self.gBoxCard)
        self.layWCardBox.setGeometry(QtCore.QRect(5, 330, 170, 30))

        self.hLCardBox = QtWidgets.QHBoxLayout(self.layWCardBox)
        self.hLCardBox.setContentsMargins(0, 0, 0, 0)

        self.cBoxExch = QtWidgets.QCheckBox(self.layWCardBox)
        self.cBoxExch.setText("跳过")
        self.cBoxExch.setToolTip("跳过那些有换卡要求的B崽子")
        self.cBoxExch.setEnabled(False)
        self.cBoxExch.stateChanged.connect(self.handleCheckChange)
        self.hLCardBox.addWidget(self.cBoxExch)

        self.btnSearch = QtWidgets.QPushButton(self.layWCardBox)
        self.btnSearch.setText("搜")
        self.btnSearch.setCheckable(True)
        self.btnSearch.setEnabled(False)
        self.btnSearch.clicked.connect(self.handleSearch)
        self.hLCardBox.addWidget(self.btnSearch)

        self.btnReloadCardList = QtWidgets.QPushButton(self.layWCardBox)
        self.btnReloadCardList.setText("刷")
        self.btnReloadCardList.setEnabled(False)
        self.btnReloadCardList.clicked.connect(lambda: self.handleThemeSelect('reload'))
        self.hLCardBox.addWidget(self.btnReloadCardList)

    # 绘制 - 我的卡箱
    def createMineBox(self):
        self.gBoxMine = QGroupBox(self.tabMcEx)
        self.gBoxMine.setGeometry(QtCore.QRect(240, 5, 270, 360))
        self.gBoxMine.setAutoFillBackground(False)
        self.gBoxMine.setTitle("****.卡箱")
        # self.gBoxMine.setCheckable(False)
        self.gBoxMine.clicked.connect(self.loadMineBox)

        self.treeMineBox = QTreeWidget(self.gBoxMine)
        self.treeMineBox.setGeometry(QtCore.QRect(5, 20, 260, 310))
        self.treeMineBox.setHeaderLabels(['卡名', '价格', '套卡'])

        self.treeMineBox.setColumnWidth(0, 130)
        self.treeMineBox.setColumnWidth(1, 40)
        self.treeMineBox.setColumnWidth(2, 70)
        self.treeMineBox.clicked.connect(self.treeMineBoxClick)
        self.treeMineBox.setRootIsDecorated(False)  # 隐藏箭头

        self.layWMineBox = QtWidgets.QWidget(self.gBoxMine)
        self.layWMineBox.setGeometry(QtCore.QRect(5, 330, 260, 30))

        self.hLMineBox = QtWidgets.QHBoxLayout(self.layWMineBox)
        self.hLMineBox.setContentsMargins(0, 0, 0, 0)

        self.btnMineBuy = QPushButton(self.layWMineBox)
        self.btnMineBuy.setText("买")
        self.btnMineBuy.setEnabled(False)
        self.btnMineBuy.setToolTip('还没弄，嘻嘻')
        self.hLMineBox.addWidget(self.btnMineBuy)

        self.btnMineSell = QPushButton(self.layWMineBox)
        self.btnMineSell.setText("卖")
        self.btnMineSell.setEnabled(False)
        self.btnMineSell.setToolTip('还没弄，嘻嘻')
        self.btnMineSell.clicked.connect(self.handleMineSell)
        self.hLMineBox.addWidget(self.btnMineSell)

        self.btnMineExChange = QPushButton(self.layWMineBox)
        self.btnMineExChange.setText("换")
        self.btnMineExChange.setEnabled(False)
        self.btnMineExChange.setToolTip("快换，不换就被换走了")
        self.btnMineExChange.clicked.connect(self.handleExchange)
        self.hLMineBox.addWidget(self.btnMineExChange)

        self.btnMineReload = QPushButton(self.layWMineBox)
        self.btnMineReload.setText("刷")
        self.btnMineReload.setToolTip("这还要看？刷就是刷新啊 啊吼")
        self.btnMineReload.clicked.connect(self.loadMineBox)
        self.hLMineBox.addWidget(self.btnMineReload)

        self.loadMineBox()

    # 绘制 - 卡友卡箱
    def createFriendBox(self):
        self.gBoxFriend = QGroupBox(self.tabMcEx)
        self.gBoxFriend.setGeometry(QtCore.QRect(515, 5, 270, 360))
        self.gBoxFriend.setAutoFillBackground(False)

        self.treeFriendBox = QTreeWidget(self.gBoxFriend)
        self.treeFriendBox.setGeometry(QtCore.QRect(5, 20, 260, 310))
        self.treeFriendBox.setHeaderLabels(['卡名', '价格', '套卡'])

        self.treeFriendBox.setColumnWidth(0, 130)
        self.treeFriendBox.setColumnWidth(1, 40)
        self.treeFriendBox.setColumnWidth(2, 70)
        self.treeFriendBox.clicked.connect(self.treeFriendBoxClick)
        self.treeFriendBox.setRootIsDecorated(False)

        self.layWFrientBox = QWidget(self.gBoxFriend)
        self.layWFrientBox.setGeometry(QtCore.QRect(5, 330, 260, 30))

        self.hLFrientBox = QtWidgets.QHBoxLayout(self.layWFrientBox)
        self.hLFrientBox.setContentsMargins(0, 0, 0, 0)

        self.btnFriendOpen = QPushButton(self.layWFrientBox)
        self.btnFriendOpen.setText("开")
        self.btnFriendOpen.setToolTip("用网页版打开该卡友的页面")
        self.btnFriendOpen.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("http://appimg2.qq.com/card/index_v3.html#opuin=" + self.opuin)))
        self.hLFrientBox.addWidget(self.btnFriendOpen)

        self.btnFriendExChange = QPushButton(self.layWFrientBox)
        self.btnFriendExChange.setText("换")
        self.btnFriendExChange.setToolTip("快换，不换就被换走了")
        self.btnFriendExChange.clicked.connect(self.handleExchange)
        self.hLFrientBox.addWidget(self.btnFriendExChange)

        self.btnFriendReload = QPushButton(self.layWFrientBox)
        self.btnFriendReload.setText("刷")
        self.btnFriendReload.setToolTip("这还要看？刷就是刷新啊 啊吼")
        self.btnFriendReload.clicked.connect(self.loadFriendBox)
        self.hLFrientBox.addWidget(self.btnFriendReload)

        self.initFrientBox()

    # 初始化 - 卡友卡箱
    def initFrientBox(self):
        self.gBoxFriend.setTitle("- - - の 卡箱")
        self.treeFriendBox.clear()

        child = QTreeWidgetItem(self.treeFriendBox)
        child.setText(0, "请先找到卡友")
        child.setText(1, "再")
        child.setText(2, "进行操作")

        self.btnFriendOpen.setEnabled(False)
        self.btnFriendExChange.setEnabled(False)
        self.btnFriendReload.setEnabled(False)

        self.treeFriendBox.setEnabled(False)

    # Load - 我的
    def loadMineBox(self):
        self.treeMineBox.clear()
        params = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }
        data = {
            "uin": self.uin,
        }
        userInfoRes = self.tool.post(params=params, data=data)
        etXml = ElementTree.XML(userInfoRes.text)

        userInfo = etXml.find("user")
        userName = userInfo.attrib["nick"] if userInfo.attrib["nick"] != '' else userInfo.attrib["uin"]

        self.gBoxMine.setTitle(userName + " の 卡箱")

        # region --换卡箱 Start--
        changeBox = etXml.find("changebox")
        changeBoxsCards = changeBox.findall("card")
        root = QTreeWidgetItem(self.treeMineBox)
        changeBoxsCardsList = self.disposeCardList(changeBox)

        root.setText(0, "-换卡箱- [{currentNum}/{maxNum}]".format(currentNum=len(changeBoxsCardsList),
                                                               maxNum=changeBox.attrib["cur"]))
        for cbCard in changeBoxsCardsList:
            child = QTreeWidgetItem()
            child.setText(0,
                          "{lock}{name}".format(lock='' if cbCard['unlock'] == '0' else '[锁]', name=cbCard['cardName']))
            child.setText(1, str(cbCard['price']))
            child.setText(2, cbCard['themeName'])
            child.setText(3, cbCard['cardId'] + '_' + cbCard['slot'] + '_0')
            child.setCheckState(0, Qt.Unchecked)
            child.setToolTip(0, cbCard['cardName'])
            child.setToolTip(2, cbCard['themeName'])

            root.insertChild(0, child)
        # endregion
        # region --保险箱 Start--
        storeboxBox = etXml.find("storebox")
        storeboxBoxCards = storeboxBox.findall("card")
        root = QTreeWidgetItem(self.treeMineBox)
        storeboxBoxCardsList = self.disposeCardList(storeboxBox)
        root.setText(0, "-保险箱- [{currentNum}/{maxNum}]".format(currentNum=len(storeboxBoxCards),
                                                               maxNum=storeboxBox.attrib["cur"]))

        for cbCard in storeboxBoxCardsList:
            child = QTreeWidgetItem()
            child.setText(0, cbCard['cardName'])
            child.setText(1, str(cbCard['price']))
            child.setText(2, cbCard['themeName'])
            child.setText(3, cbCard['cardId'] + '_' + cbCard['slot'] + '_1')
            child.setCheckState(0, Qt.Unchecked)
            child.setToolTip(0, cbCard['cardName'])
            child.setToolTip(2, cbCard['themeName'])

            root.insertChild(0, child)
        # endregion
        self.treeMineBox.expandAll()

        # self.statusBar.showMessage('刷新成功')

    # Load - 卡友
    def loadFriendBox(self):
        self.treeFriendBox.clear()
        params = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }
        data = {
            "uin": self.uin,
            "opuin": self.opuin
        }
        userInfoRes = self.tool.post(params=params, data=data)

        etXml = ElementTree.XML(userInfoRes.text)

        userInfo = etXml.find("user")
        userName = userInfo.attrib["nick"] if userInfo.attrib["nick"] != '' else userInfo.attrib["uin"]
        self.gBoxFriend.setTitle(userName + " の 换卡箱")

        changeBox = etXml.find("changebox")
        changeBoxsCards = changeBox.findall("card")

        changeBoxsCardsList = []
        for cbCard in changeBoxsCards:
            id = cbCard.attrib["id"]
            if int(id) > 0:  # 跳过一些莫名其妙的卡
                changeBoxsCardsList.append({
                    "cardId": id,
                    "cardName": self.rootCardDict[id]['cardName'],
                    "price": self.rootCardDict[id]['price'],
                    "themeName": self.rootThemeDict[self.rootCardDict[id]['themeId']]['themeName'],
                    "slot": cbCard.attrib["slot"],
                    "unlock": cbCard.attrib["unlock"],
                    "status": cbCard.attrib["status"],
                    "type": cbCard.attrib["type"]
                })

        changeBoxsCardsList.sort(key=lambda x: x["price"])
        for cbCard in changeBoxsCardsList:
            child = QTreeWidgetItem(self.treeFriendBox)

            child.setText(0,
                          "{lock}{name}".format(lock='' if cbCard['unlock'] == '0' else '[锁]', name=cbCard['cardName']))
            child.setText(1, cbCard['price'])
            child.setText(2, cbCard['themeName'])
            child.setText(3, cbCard['cardId'] + '_' + cbCard['slot'] + '_0')
            child.setCheckState(0, Qt.Unchecked)
            if cbCard['cardId'] in self.selectCardList and cbCard['unlock'] == '0':
                child.setBackground(0, QColor(102, 255, 102))
                child.setBackground(1, QColor(102, 255, 102))
                child.setBackground(2, QColor(102, 255, 102))
            child.setDisabled(cbCard['unlock'] != '0')

        self.treeFriendBox.expandAll()

    # 处理 - 卡片
    def disposeCardList(self, list):
        newList = []
        for item in list:
            id = item.attrib["id"]
            if int(id) > 0:  # 跳过一些莫名其妙的卡
                newList.append({
                    "cardId": id,
                    "themeId": self.rootCardDict[id]['themeId'],
                    "cardName": self.rootCardDict[id]['cardName'],
                    "price": int(self.rootCardDict[id]['price']),
                    "themeName": self.rootThemeDict[self.rootCardDict[id]['themeId']]['themeName'],
                    "slot": item.attrib["slot"],
                    "unlock": item.attrib["unlock"] if "unlock" in item.attrib.keys() else 0,
                    "status": item.attrib["status"],
                    "type": item.attrib["type"]
                })
        newList.sort(key=lambda x: x["price"])
        # newList.sort(key=lambda x: x["themeId"])
        return newList

    # 搜索框 - 输入
    def handleEditChange(self, val):
        self.searchThemeName = val
        self.createThemeList()
        if val != '':
            self.treeThemeList.expandAll()

    # 选择卡片
    def handleCardSelect(self):
        selectedItems = self.lBoxCardList.selectedItems()
        self.btnSearch.setEnabled(False)
        self.selectCardList = []
        for i in list(selectedItems):
            self.selectCardList.append(self.currentCards[self.lBoxCardList.row(i)]['id'])
        if len(self.selectCardList) > 0:
            self.btnSearch.setEnabled(True)

    def handleCheckChange(self, status):
        self.isExch = status == 2

    def handleMineSell(self):
        print(self.cardsMine)

    # 开始搜索
    def handleSearch(self):
        # TODO:如果再次搜索提醒是否丢弃当前卡友的状态
        print(self.opuin)
        if not self.isStart:
            self.isStart = True
            self.opuin = ''
            self.btnSearch.setText("停")
            self.btnReloadCardList.setEnabled(False)
            self.cBoxExch.setEnabled(False)
            self.lBoxCardList.setEnabled(False)
            self.initFrientBox()  # 初始化 - 卡友卡箱

            self.thread = SearchUser(themeId=self.themeId,
                                     selectCardList=self.selectCardList,
                                     tool=self.tool,
                                     isExch=self.isExch,
                                     rootThemeDict=self.rootThemeDict)

            self.thread.sec_changed_signal.connect(self.updateStatusBar)
            self.thread.theCardIsSearched.connect(self.cardSearched)
            self.thread.start()
            self.thread.exec()
        else:
            self.thread.setFlag()
            # self.thread.stop()
            self.btnSearch.setText("搜")
            self.cBoxExch.setEnabled(True)
            self.btnReloadCardList.setEnabled(True)
            self.lBoxCardList.setEnabled(True)
            # self.thread.exitFlag = True
            self.isStart = False

    # 找到卡了
    def cardSearched(self, opuin):
        self.opuin = opuin
        self.exitFlag = False
        self.isStart = False
        self.btnSearch.toggle()
        self.btnSearch.setText("搜")
        self.labelStatusStr.setText("找到了!!!")
        self.cBoxExch.setEnabled(True)  # 卡片容器 - 跳过按钮
        self.btnReloadCardList.setEnabled(True)  # 卡片容器 - 刷新按钮
        self.lBoxCardList.setEnabled(True)  # 卡片容器 - 卡片列表
        self.treeFriendBox.setEnabled(True)  # 卡友容器 - 卡片列表
        self.btnFriendReload.setEnabled(True)  # 卡友容器 - 刷新按钮
        self.btnFriendOpen.setEnabled(True)  # 卡友容器 - 打开网站

        self.loadFriendBox()
        self.sound = QSound('./sound/find.wav')
        self.sound.play()

    # 换卡 - 请求
    def handleExchange(self):
        params = {
            "cmd": "card_user_exchangecard",
            "h5ver": 1,
        }
        data = {
            "cmd": 1,
            "dst": '|'.join(self.slotFriend),
            "src": '|'.join(self.slotMine),
            "isFriend": 1,
            "uin": self.uin,
            "frnd": self.opuin
        }
        r = self.tool.post(params=params, data=data)
        etXml = ElementTree.XML(r.text)
        code = etXml.attrib['code']
        w = QWidget()
        if code == '0':
            self.labelStatusStr.setStyleSheet("QWidget{color: #28a745}")  # success
            self.labelStatusStr.setText('交换成功~')
            self.sound = QSound('./sound/success.wav')
        else:
            self.labelStatusStr.setStyleSheet("QWidget{color: #dc3545}")  # error
            self.labelStatusStr.setText(etXml.attrib['message'])
            self.sound = QSound('./sound/fail.wav')

        self.sound.play()
        self.btnFriendExChange.setEnabled(False)
        self.btnMineExChange.setEnabled(False)
        self.loadMineBox()
        self.loadFriendBox()

    # 计算 双方已选择卡片
    def componendNumPrise(self):
        if self.opuin:
            str = "已选择{l1}张，共{l2}面值的卡片 已选择{r1}张，共{r2}面值的卡片".format(
                l1=len(self.cardsMine),
                l2=sum(self.cardsMine),
                r1=len(self.cardsFriend),
                r2=sum(self.cardsFriend),
            )

            if len(self.cardsMine) + len(self.cardsFriend) >= 2 and \
                    len(self.cardsMine) == len(self.cardsFriend) and \
                    sum(self.cardsMine) == sum(self.cardsFriend):
                # 这恒河里
                self.labelStatusStr.setStyleSheet("QWidget{color: #28a745}")
                self.btnFriendExChange.setEnabled(True)
                self.btnMineExChange.setEnabled(True)
            else:
                # 这布河里
                self.labelStatusStr.setStyleSheet("QWidget{color: #dc3545}")
                self.btnFriendExChange.setEnabled(False)
                self.btnMineExChange.setEnabled(False)

            self.labelStatusStr.setText(str)

    # 我的卡箱 - 点击
    def treeMineBoxClick(self):
        self.cardsMine = []
        self.slotMine = []

        iterator = QTreeWidgetItemIterator(self.treeMineBox)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                self.cardsMine.append(int(item.text(1)))
                self.slotMine.append(item.text(3))
            iterator.__iadd__(1)
        self.componendNumPrise()

    # 卡友卡箱 - 点击
    def treeFriendBoxClick(self):
        self.cardsFriend = []
        self.slotFriend = []

        iterator = QTreeWidgetItemIterator(self.treeFriendBox)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                self.cardsFriend.append(int(item.text(1)))
                self.slotFriend.append(item.text(3))

            iterator.__iadd__(1)
        self.componendNumPrise()

    # 状态栏 - 搜索中[更新]
    def updateStatusBar(self, num):
        self.labelStatusStr.setText('搜索中... [{0}]'.format(num))
        self.labelStatusStr.setStyleSheet("QWidget{color: #333333}")

    # 选择套卡 - 确定
    def handleThemeSelect(self, flag):
        i = self.treeThemeList.currentItem()

        if i.text(1):  # 获取选择套卡的themeId
            self.themeId = i.text(1)
            self.currentCards = []

            self.gBoxCard.setTitle(i.text(0))

            self.cBoxExch.setEnabled(True)
            self.cBoxExch.setCheckState(False)
            self.isExch = False

            # 根据选择的套卡类型 自动勾选是否跳过有要求的卡友
            if self.rootThemeDict[self.themeId]['type'] in [0, 9]:
                self.cBoxExch.setCheckState(2)
                self.isExch = True

            for card in self.cards:
                if card.attrib['theme_id'] == i.text(1):
                    self.currentCards.append({
                        "id": card.attrib['id'],
                        "themeId": card.attrib['theme_id'],
                        "name": str.strip(card.attrib['name']),
                        "price": int(card.attrib['price']),
                    })

            self.currentCards.sort(key=lambda x: x["price"])
            self.lBoxCardList.clear()
            params = {
                "cmd": "card_user_mainpage",
                "h5ver": 1,
            }
            data = {
                "uin": self.uin,
            }
            userInfoRes = self.tool.post(params=params, data=data)
            etXml = ElementTree.XML(userInfoRes.text)

            changeBox = etXml.find("changebox")
            changeBoxsCards = changeBox.findall("card")

            storeboxBox = etXml.find("storebox")
            storeboxBoxCards = storeboxBox.findall("card")

            newList = []
            for item in changeBoxsCards:
                id = item.attrib["id"]
                if int(id) > 0:  # 跳过一些莫名其妙的卡
                    newList.append(id)
            for item in storeboxBoxCards:
                id = item.attrib["id"]
                if int(id) > 0:  # 跳过一些莫名其妙的卡
                    newList.append(id)
            for item in self.currentCards:
                num = "【{i}】".format(i=newList.count(item["id"]))
                itemStr = num + item['name'] + "[" + str(item['price']) + "]"
                self.item = QListWidgetItem(itemStr)
                self.item.setToolTip(itemStr)
                self.item.setSelected(True)
                self.lBoxCardList.addItem(self.item)
                # self.listBox.insertItem(0, self.item)

                # selectedItems = self.listBox.selectedItems()
                # self.btnSearch.setEnabled(False)
                # self.selectCardList = []
                # for i in list(selectedItems):
                #     self.selectCardList.append(self.currentCards[self.listBox.row(i)]['id'])
                # if len(self.selectCardList) > 0:
                #     self.btnSearch.setEnabled(True)
            # for i in range(self.listBox.count()):
            self.lBoxCardList.setEnabled(True)
            self.btnReloadCardList.setEnabled(True)

            if flag != 'reload':
                self.selectThemeHide()
                self.btnSelectTheme.toggle()
            else:
                self.labelStatusStr.setText('卡片列表已刷新~')

    # 选择套卡 - 隐藏&显示
    def btnSelectThemeChange(self):
        self.btnSelectTheme.setEnabled(False)
        if self.btnSelectTheme.isChecked():
            self.selectThemeShow()
        else:
            self.selectThemeHide()
        self.btnSelectTheme.setEnabled(True)

    # 隐藏选择套卡模块
    def selectThemeHide(self):
        self.btnSelectTheme.setText(">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
        self.listViewThemeBox.setDuration(300)
        self.listViewThemeBox.setStartValue(QtCore.QRect(10, 5, 210, 360))
        self.listViewThemeBox.setEndValue(QtCore.QRect(-165, 5, 210, 360))
        self.listViewThemeBox.start()

    # 显示选择套卡模块
    def selectThemeShow(self):
        self.btnSelectTheme.setText("<\n<\n<\n<\n<\n<\n<\n收\n起\n选\n择\n<\n<\n<\n<\n<\n<\n<")
        self.listViewThemeBox.setDuration(300)
        self.listViewThemeBox.setStartValue(QtCore.QRect(-165, 5, 210, 360))
        self.listViewThemeBox.setEndValue(QtCore.QRect(10, 5, 210, 360))
        self.listViewThemeBox.start()

    # 切换套卡类型
    def handleTbThemeListClicked(self, i):
        self.currentTheme = self.themesList[i]
        self.createThemeList()
