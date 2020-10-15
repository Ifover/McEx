# -*- coding: utf-8 -*-
import sys
import time
from xml.dom.minidom import parse
from xml.etree import ElementTree

# import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  # Qt, QPropertyAnimation
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QSound

# QMainWindow, QApplication, QMenuBar, QGroupBox, QTreeWidget, QWidget, QGridLayout, \
#     QPushButton, QTreeWidgetItem, QListWidget, QAbstractItemView, QComboBox, QListWidgetItem, QTreeWidgetItemIterator, \
#     QMessageBox
# from WebLogin import LoginWeb

import resource
from SearchUser import SearchUser
import gol
import win32gui
import win32con


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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

        # super().__init__()

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.setWindowTitle("Super McEx")
        self.setWindowIcon(QIcon(':/icon.ico'))
        self.resize(515, 400)
        self.setFixedSize(515, 400)

        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 20))

        self.labelStatusStr = QLabel("xxxx")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.addPermanentWidget(self.labelStatusStr, stretch=4)
        #
        self.setStatusBar(self.statusBar)
        QtCore.QMetaObject.connectSlotsByName(self)

        # self.isLogined()
        # self.init()
        self.init({
            "code": 0,
            "data": {
                "cookies": gol.get_value('cookies'),
                "uin": gol.get_value('cookies')['uin'][1:]
            }
        })

    # def isLogined(self):

    def init(self, data):

        if data["code"] == 0:
            self.labelStatusStr.setText("登录成功，正在初始化数据")

            # gol.set_value("cookies", data['data']['cookies'])
            # gol.set_value("uin", data['data']['uin'])
            # self.tool.saveCookie()

            self.uin = data['data']['uin']
            # self.tool.uin = data['data']['uin']
            # self.tool.cookies = data['data']['cookies']
            self.createMenu()
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

            self.groupBox = QGroupBox(self)
            self.groupBox.setGeometry(QtCore.QRect(-165, 28, 210, 345))
            self.groupBox.setAutoFillBackground(True)
            self.groupBox.setTitle("选择套卡")
            self.groupBox.show()

            self.groupBox2 = QGroupBox(self)
            self.groupBox2.setGeometry(QtCore.QRect(50, 28, 180, 345))
            self.groupBox2.setAutoFillBackground(True)
            self.groupBox2.setTitle("选择卡片")
            self.groupBox2.show()

            self.listBox = QListWidget(self.groupBox2)
            self.listBox.setGeometry(QtCore.QRect(5, 18, 170, 280))
            self.listBox.setSelectionMode(QAbstractItemView.MultiSelection)
            self.listBox.addItem('请选择套卡~~')
            self.listBox.setEnabled(False)
            self.listBox.itemSelectionChanged.connect(self.handleCardSelect)
            self.listBox.show()

            self.listView_Anim = QPropertyAnimation(self.groupBox, b"geometry")
            self.pushButton = QtWidgets.QPushButton(self.groupBox)
            self.pushButton.setGeometry(QtCore.QRect(170, 10, 30, 331))
            self.pushButton.setText(">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
            self.pushButton.setCheckable(True)
            self.pushButton.clicked.connect(self.btnSelectThemeShowHide)
            self.pushButton.show()

            self.setThemeTypeTab()  # 绘制 - 套卡类型

            self.setBtnStartSearch()  # 开始搜索

            self.setMineBox()  # 绘制我的卡箱
            self.setFriendBox()  # 绘制卡友的换卡箱
            self.setThemeList()

            self.groupBox.raise_()
            self.menuBar.raise_()

            self.labelStatusStr.setText("初始化成功~")

    def handleLogin(self):
        self.labelStatusStr.setText("正在加载登录窗口~")
        # s = SecondWindow()
        from FormLogin import FormLogin

        # self.viewShow = QDialog()
        self.uui = FormLogin()
        self.uui.setupUi(tool=self.tool)
        self.close()
        self.uui.show()

    def createMenu(self):
        self.setMenuBar(self.menuBar)
        self.menuBar.clear()
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

        bar1 = self.menuBar.addMenu(userName)
        logout = bar1.addAction('注销')
        logout.triggered.connect(self.handleLogin)

        bar2 = self.menuBar.addMenu('设置')
        zd = bar2.addAction('置顶')
        zd.setCheckable(True)
        zd.triggered.connect(self.windowOnTop)

        # zd = QAction("置顶", self)
        # zd.setCheckable(True)
        # bar2.addAction(zd)

    # 绘制 - 我的卡箱
    def setMineBox(self):

        self.groupMineBox = QGroupBox(self)
        self.groupMineBox.setGeometry(QtCore.QRect(240, 28, 270, 345))
        self.groupMineBox.setAutoFillBackground(True)
        self.groupMineBox.setTitle("****.卡箱")
        # self.groupMineBox.setCheckable(False)
        self.groupMineBox.clicked.connect(self.loadMineBox)
        self.groupMineBox.show()

        self.treeMineBox = QTreeWidget(self.groupMineBox)
        self.treeMineBox.setGeometry(QtCore.QRect(5, 18, 260, 295))
        self.treeMineBox.setHeaderLabels(['卡名', '价格', '套卡'])

        # self.treeWidget.setIndentation(0)
        self.treeMineBox.setColumnWidth(0, 130)
        self.treeMineBox.setColumnWidth(1, 40)
        self.treeMineBox.setColumnWidth(2, 70)
        self.treeMineBox.clicked.connect(self.treeMineBoxClick)
        # self.treeMineBox.itemChanged.connect(self.handleChanged)
        self.treeMineBox.setRootIsDecorated(False)  # 隐藏箭头
        self.treeMineBox.show()

        self.layoutWidget = QWidget(self.groupMineBox)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 305, 271, 34))
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.show()

        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(5, 10, 5, 5)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")

        self.btnMineBuy = QPushButton(self.layoutWidget)
        self.btnMineBuy.setText("买")
        self.btnMineBuy.setEnabled(False)
        self.btnMineBuy.setToolTip('还没弄，嘻嘻')
        self.btnMineBuy.setMinimumSize(QtCore.QSize(32, 24))
        self.btnMineBuy.show()
        self.gridLayout.addWidget(self.btnMineBuy, 0, 0, 1, 1)

        self.btnMineSell = QPushButton(self.layoutWidget)
        self.btnMineSell.setText("卖")
        self.btnMineSell.setEnabled(False)
        self.btnMineSell.setToolTip('还没弄，嘻嘻')
        self.btnMineSell.clicked.connect(self.handleMineSell)
        self.btnMineSell.setMinimumSize(QtCore.QSize(32, 24))
        self.btnMineSell.show()
        self.gridLayout.addWidget(self.btnMineSell, 0, 1, 1, 1)

        self.btnMineReload = QPushButton(self.layoutWidget)
        self.btnMineReload.setText("刷")
        self.btnMineReload.setMinimumSize(QtCore.QSize(32, 24))
        self.btnMineReload.clicked.connect(self.loadMineBox)
        self.btnMineReload.show()
        self.gridLayout.addWidget(self.btnMineReload, 0, 3, 1, 1)
        # self.gridLayout.show()

        self.loadMineBox()

    # 绘制 - 卡友卡箱
    def setFriendBox(self):
        self.groupFriendBox = QGroupBox(self)
        self.groupFriendBox.setGeometry(QtCore.QRect(525, 28, 270, 345))
        self.groupFriendBox.setAutoFillBackground(True)
        self.groupFriendBox.setTitle("xxxxx.卡箱")

        self.treeFriendBox = QTreeWidget(self.groupFriendBox)
        self.treeFriendBox.setGeometry(QtCore.QRect(5, 18, 260, 295))
        self.treeFriendBox.setHeaderLabels(['卡名', '价格', '套卡'])
        # self.treeWidget.setIndentation(0)
        self.treeFriendBox.setColumnWidth(0, 130)
        self.treeFriendBox.setColumnWidth(1, 40)
        self.treeFriendBox.setColumnWidth(2, 70)
        self.treeFriendBox.clicked.connect(self.treeFriendBoxClick)
        self.treeFriendBox.setRootIsDecorated(False)

        self.layoutWidget2 = QWidget(self.groupFriendBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 305, 271, 34))

        self.gridLayout = QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(5, 10, 5, 5)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setVerticalSpacing(3)

        self.btnFriendOpen = QPushButton(self.layoutWidget2)
        self.btnFriendOpen.setText("开")
        # self.btnFriendOpen.setEnabled(False)
        self.btnFriendOpen.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("http://appimg2.qq.com/card/index_v3.html#opuin=" + self.opuin)))
        self.btnFriendOpen.setMinimumSize(QtCore.QSize(32, 24))
        self.gridLayout.addWidget(self.btnFriendOpen, 0, 0, 1, 1)

        self.btnFriendExChange = QPushButton(self.layoutWidget2)
        self.btnFriendExChange.setText("换")
        self.btnFriendExChange.setEnabled(False)
        self.btnFriendExChange.clicked.connect(self.handleExchange)
        self.btnFriendExChange.setMinimumSize(QtCore.QSize(32, 24))
        self.gridLayout.addWidget(self.btnFriendExChange, 0, 2, 1, 1)

        self.btnFriendReload = QPushButton(self.layoutWidget2)
        self.btnFriendReload.setText("刷")
        self.btnFriendReload.setMinimumSize(QtCore.QSize(32, 24))
        self.btnFriendReload.clicked.connect(self.loadFriendBox)
        self.gridLayout.addWidget(self.btnFriendReload, 0, 3, 1, 1)

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

        self.groupMineBox.setTitle(userName + " の 卡箱")

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
        self.groupFriendBox.setTitle(userName + " の 换卡箱")

        changeBox = etXml.find("changebox")
        changeBoxsCards = changeBox.findall("card")

        # root = QTreeWidgetItem(self.treeFriendBox)
        # root.setText(0, "-换卡箱-")

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
            # child.setData(0, Qt.CheckStateRole, QVariant())
            child.setDisabled(cbCard['unlock'] != '0')

            # self.treeFriendBox.insertChild(0, child)

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

    # 绘制 - 套卡类型
    def setThemeTypeTab(self):
        self.textbox = QLineEdit(self.groupBox)
        self.textbox.setGeometry(QtCore.QRect(5, 20, 160, 24))
        self.textbox.setPlaceholderText("输入套卡名称")
        self.textbox.textChanged.connect(self.handleEditChange)
        self.textbox.show()

        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setGeometry(QtCore.QRect(5, 50, 160, 20))
        self.tabWidget.show()

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

        self.treeWidget = QTreeWidget(self.groupBox)
        self.treeWidget.setGeometry(QtCore.QRect(5, 70, 160, 265))
        self.treeWidget.setHeaderLabels(['套卡名称'])
        self.treeWidget.clicked.connect(self.handleThemeSelect)
        self.treeWidget.show()
        self.tabWidget.currentChanged.connect(self.onTabWidgetClicked)

    # 搜索框 - 输入
    def handleEditChange(self, val):
        self.searchThemeName = val
        self.setThemeList()
        if val != '':
            self.treeWidget.expandAll()

    # 选择卡片
    def handleCardSelect(self):
        selectedItems = self.listBox.selectedItems()
        self.btnSearch.setEnabled(False)
        self.selectCardList = []
        for i in list(selectedItems):
            self.selectCardList.append(self.currentCards[self.listBox.row(i)]['id'])
        if len(self.selectCardList) > 0:
            self.btnSearch.setEnabled(True)

    # 绘制 - 按钮[开始搜索]
    def setBtnStartSearch(self):

        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(5, 302, 170, 40))

        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        self.checkExch = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkExch.setText('跳过要求')
        self.checkExch.setEnabled(False)
        self.checkExch.stateChanged.connect(self.handleCheckChange)
        self.checkExch.show()

        self.gridLayout_2.addWidget(self.checkExch, 0, 0, 1, 1)

        # self.checkTop = QtWidgets.QCheckBox(self.gridLayoutWidget)
        # self.checkTop.setText('窗口置顶')
        # self.checkTop.stateChanged.connect(self.windowOnTop)
        # self.gridLayout_2.addWidget(self.checkTop, 1, 0, 1, 1)
        #
        self.btnReloadCardList = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnReloadCardList.setText('刷新列表')
        self.btnReloadCardList.setMinimumSize(QtCore.QSize(0, 18))
        self.btnReloadCardList.setStyleSheet("font-size:10px;")
        self.btnReloadCardList.setEnabled(False)
        self.btnReloadCardList.show()
        self.btnReloadCardList.clicked.connect(lambda: self.handleThemeSelect('reload'))
        self.gridLayout_2.addWidget(self.btnReloadCardList, 1, 0, 1, 1)

        self.btnSearch = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnSearch.setMinimumSize(QtCore.QSize(0, 40))
        self.btnSearch.setText("搜")
        self.btnSearch.setCheckable(True)
        self.btnSearch.setEnabled(False)
        self.btnSearch.clicked.connect(self.btnStartSearch)
        self.btnSearch.show()
        self.gridLayout_2.addWidget(self.btnSearch, 0, 1, 1, 1)

    def handleCheckChange(self, status):
        self.isExch = status == 2

    def handleMineSell(self):
        print(self.cardsMine)

    # 开始搜索
    def btnStartSearch(self):
        if not self.isStart:
            self.isStart = True
            self.opuin = ''
            self.btnSearch.setText("停")
            self.resize(515, 400)
            self.setFixedSize(515, 400)
            self.btnReloadCardList.setEnabled(False)
            self.checkExch.setEnabled(False)
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
            self.checkExch.setEnabled(True)
            self.btnReloadCardList.setEnabled(True)
            # self.thread.exitFlag = True
            self.isStart = False

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
            self.statusBar.setStyleSheet("QWidget{color: #28a745}")  # success
            self.labelStatusStr.setText('交换成功~')
            self.sound = QSound('./sound/success.wav')
        else:
            self.statusBar.setStyleSheet("QWidget{color: #dc3545}")  # error
            self.labelStatusStr.setText(etXml.attrib['message'])
            self.sound = QSound('./sound/fail.wav')

        self.sound.play()
        self.btnFriendExChange.setEnabled(False)
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
                self.statusBar.setStyleSheet("QWidget{color: #28a745}")
                self.btnFriendExChange.setEnabled(True)
            else:
                # 这布河里
                self.statusBar.setStyleSheet("QWidget{color: #dc3545}")
                self.btnFriendExChange.setEnabled(False)

            self.labelStatusStr.setText(str)
            # self.statusBar.showMessage(str)

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

    # 找到卡了
    def cardSearched(self, opuin):
        self.opuin = opuin
        self.exitFlag = False
        self.isStart = False
        self.btnSearch.toggle()
        self.resize(800, 400)
        self.setFixedSize(800, 400)
        # self.btnSearch.setEnabled(True)

        # playsound('./sound/find.wav')

        # os.system('mpg123' + './sound/find.wav')
        self.btnSearch.setText("搜")
        self.statusBar.showMessage('找到了!!!')
        self.btnReloadCardList.setEnabled(True)
        self.checkExch.setEnabled(True)
        self.loadFriendBox()
        self.sound = QSound('./sound/find.wav')
        self.sound.play()

    # 状态栏 - 搜索中[更新]
    def updateStatusBar(self, num):
        self.labelStatusStr.setText('搜索中... [{0}]'.format(num))
        self.statusBar.setStyleSheet("QWidget{color: #333333}")

    # 绘制 - 套卡容器
    def setThemeList(self):
        self.treeWidget.clear()

        data = {
            "uin": self.uin,
        }
        res = self.tool.post(url="https://card.qzone.qq.com/cgi-bin/card_mini_get", data=data)
        etXml = ElementTree.XML(res.text)
        Nodes = etXml.findall("Node")
        getThemeList = []
        for node in Nodes:
            getThemeList.append(node.attrib['theme_id'])

        self.treeWidget.invisibleRootItem()
        for index in range(1, 6):
            root = QTreeWidgetItem(self.treeWidget)
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

    # 选择套卡 - 确定
    def handleThemeSelect(self, flag):
        i = self.treeWidget.currentItem()
        if i.text(1):  # 获取选择套卡的themeId
            self.themeId = i.text(1)
            self.currentCards = []

            self.checkExch.setEnabled(True)
            self.checkExch.setCheckState(False)
            self.isExch = False

            # 根据选择的套卡类型 自动勾选是否跳过有要求的卡友
            if self.rootThemeDict[self.themeId]['type'] in [0, 9]:
                self.checkExch.setCheckState(2)
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
            self.listBox.clear()
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
                self.item = QListWidgetItem(num + item['name'] + "[" + str(item['price']) + "]")
                # self.item.setSelected( item['id'] in self.selectCardList)
                self.item.setSelected(True)
                self.listBox.addItem(self.item)
                # self.listBox.insertItem(0, self.item)

                # selectedItems = self.listBox.selectedItems()
                # self.btnSearch.setEnabled(False)
                # self.selectCardList = []
                # for i in list(selectedItems):
                #     self.selectCardList.append(self.currentCards[self.listBox.row(i)]['id'])
                # if len(self.selectCardList) > 0:
                #     self.btnSearch.setEnabled(True)
            # for i in range(self.listBox.count()):
            self.listBox.setEnabled(True)
            self.btnReloadCardList.setEnabled(True)

            if flag != 'reload':
                self.selectThemeHide()
                self.pushButton.toggle()
            else:
                self.labelStatusStr.setText('卡片列表已刷新~')

    # 选择套卡 - 隐藏&显示
    def btnSelectThemeShowHide(self):
        self.pushButton.setEnabled(False)
        if self.pushButton.isChecked():
            self.selectThemeShow()
        else:
            self.selectThemeHide()
        self.pushButton.setEnabled(True)

    # 隐藏选择套卡模块
    def selectThemeHide(self):
        self.pushButton.setText(">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
        self.listView_Anim.setDuration(300)
        self.listView_Anim.setStartValue(QtCore.QRect(10, 28, 210, 345))
        self.listView_Anim.setEndValue(QtCore.QRect(-165, 28, 210, 345))
        self.listView_Anim.start()

    # 显示选择套卡模块
    def selectThemeShow(self):
        self.pushButton.setText("<\n<\n<\n<\n<\n<\n<\n收\n起\n选\n择\n<\n<\n<\n<\n<\n<\n<")
        self.listView_Anim.setDuration(300)
        self.listView_Anim.setStartValue(QtCore.QRect(-165, 28, 210, 345))
        self.listView_Anim.setEndValue(QtCore.QRect(10, 28, 210, 345))
        self.listView_Anim.start()

    # 切换套卡类型
    def onTabWidgetClicked(self, i):
        self.currentTheme = self.themesList[i]
        self.setThemeList()

    def windowOnTop(self, checked):
        hwnd = win32gui.GetForegroundWindow()

        if not checked:
            # 取消置顶
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)
        else:
            # 设置置顶
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW)

        win32gui.SetForegroundWindow(hwnd)
        self.show()
