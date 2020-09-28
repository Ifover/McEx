# -*- coding: utf-8 -*-
import sys
import time
from xml.dom.minidom import parse
from xml.etree import ElementTree
from selenium import webdriver
import time
# import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * #Qt, QPropertyAnimation
from PyQt5.QtGui import * #QPropertyAnimation
from PyQt5.QtWidgets import  *
# QMainWindow, QApplication, QMenuBar, QGroupBox, QTreeWidget, QWidget, QGridLayout, \
#     QPushButton, QTreeWidgetItem, QListWidget, QAbstractItemView, QComboBox, QListWidgetItem, QTreeWidgetItemIterator, \
#     QMessageBox

import Tools
from SearchUser import SearchUser


class Ui_MainWindow(object):
    def __init__(self):
        self.isStart = False
        self.cardsMine = []
        self.cardsFriend = []
        self.slotMine = []
        self.slotFriend = []
        self.opuin = ''
        self.uin = "1224842990"
        self.isExch = True
        # super().__init__()

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setWindowTitle("MainWindow")
        # MainWindow.setWindowFlags(QtGui.QtWindowStaysOnTopHint)
        MainWindow.resize(515, 400)
        MainWindow.setFixedSize(515, 400)

        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 20))

        bar1 = self.menuBar.addMenu('File')
        bar1.addAction('New')

        bar2 = self.menuBar.addMenu('设置')
        zd = bar2.addAction('置顶')
        zd.setCheckable(True)
        zd.triggered.connect(self.windowOnTop)

        # zd = QAction("置顶", self)
        # zd.setCheckable(True)
        # bar2.addAction(zd)

        MainWindow.setMenuBar(self.menuBar)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)

        self.groupBox = QGroupBox(MainWindow)
        self.groupBox.setGeometry(QtCore.QRect(-165, 28, 210, 345))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setTitle("选择套卡")

        self.groupBox2 = QGroupBox(MainWindow)
        self.groupBox2.setGeometry(QtCore.QRect(50, 28, 180, 345))
        self.groupBox2.setAutoFillBackground(True)
        self.groupBox2.setTitle("选择卡片")

        self.setMineBox()  # 绘制我的卡箱
        self.setFriendBox()  # 绘制卡友的换卡箱
        self.setBtnStartSearch()  # 开始搜索

        self.listBox = QListWidget(self.groupBox2)
        self.listBox.setGeometry(QtCore.QRect(5, 18, 170, 280))
        self.listBox.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.listBox.itemClicked.connect(self.handleCardSelect)
        self.listBox.itemSelectionChanged.connect(self.handleCardSelect)
        # self.listBox.currentItemChanged.connect(self.handleCardSelect)

        self.listView_Anim = QPropertyAnimation(self.groupBox, b"geometry")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(170, 10, 30, 331))
        self.pushButton.setText(">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
        self.pushButton.setCheckable(True)
        self.pushButton.clicked.connect(self.btnSelectThemeShowHide)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(5, 50, 160, 20))

        self.themesList = [
            {"id": 1, "label": "发行", "type": [0, 2]},
            {"id": 2, "label": "下架", "type": [1, 5]},
            {"id": 3, "label": "闪卡", "type": [9]},
        ]
        self.currentTheme = self.themesList[0]

        for item in self.themesList:
            self.comboBox.addItem(item["label"])

        self.treeWidget = QTreeWidget(self.groupBox)
        self.treeWidget.setGeometry(QtCore.QRect(5, 75, 160, 265))
        self.treeWidget.setHeaderLabels(['套卡名称'])
        self.treeWidget.clicked.connect(self.handleThemeSelect)
        self.setThemeList()
        self.comboBox.currentIndexChanged.connect(self.onTabWidgetClicked)
        self.groupBox.raise_()
        self.menuBar.raise_()

        # self.menuIfover = QMenu(self.menuBar)
        # self.menuIfover.setTitle("Ifover")
        #
        # self.cb1 = QCheckBox('全选')
        # # self.check_1.setTitle('置顶')
        #
        #
        # self.menuBar.addAction(self.menuIfover.menuAction())
        # self.menuBar.addAction(self.cb1)

        self.statusBar.showMessage("ready!")
        MainWindow.setStatusBar(self.statusBar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # 绘制 - 我的卡箱
    def setMineBox(self):
        self.groupMineBox = QGroupBox(MainWindow)
        self.groupMineBox.setGeometry(QtCore.QRect(240, 28, 270, 345))
        self.groupMineBox.setAutoFillBackground(True)
        self.groupMineBox.setTitle("****.卡箱")
        # self.groupMineBox.setCheckable(False)
        self.groupMineBox.clicked.connect(self.loadMineBox)

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

        self.layoutWidget = QWidget(self.groupMineBox)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 305, 271, 34))
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(5, 10, 5, 5)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")

        self.btnMineBuy = QPushButton(self.layoutWidget)
        self.btnMineBuy.setText("买")
        self.btnMineBuy.setEnabled(False)
        self.btnMineBuy.setMinimumSize(QtCore.QSize(32, 24))
        self.gridLayout.addWidget(self.btnMineBuy, 0, 0, 1, 1)

        self.btnMineSell = QPushButton(self.layoutWidget)
        self.btnMineSell.setText("卖")
        self.btnMineSell.setEnabled(False)
        self.btnMineSell.setMinimumSize(QtCore.QSize(32, 24))
        self.gridLayout.addWidget(self.btnMineSell, 0, 1, 1, 1)

        self.btnMineReload = QPushButton(self.layoutWidget)
        self.btnMineReload.setText("刷")
        self.btnMineReload.setMinimumSize(QtCore.QSize(32, 24))
        self.btnMineReload.clicked.connect(self.loadMineBox)
        self.gridLayout.addWidget(self.btnMineReload, 0, 3, 1, 1)

        self.loadMineBox()

    # 绘制 - 卡友卡箱
    def setFriendBox(self):
        self.groupFriendBox = QGroupBox(MainWindow)
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
        userInfoRes = Tools.post(url=baseUrl, params=mCardUserMainPage,
                                 data=mCardUserMainPageData)
        etXml = ElementTree.XML(userInfoRes.text)

        userInfo = etXml.find("user")
        userName = userInfo.attrib["nick"] if userInfo.attrib["nick"] != '' else userInfo.attrib["uin"]
        self.groupMineBox.setTitle(userName + " の 卡箱")

        # --换卡箱 Start--
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

        # --保险箱 Start--
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

        self.treeMineBox.expandAll()

        self.statusBar.showMessage('刷新成功')

    # Load - 卡友
    def loadFriendBox(self):
        self.treeFriendBox.clear()
        data = {
            "uin": 1224842990,
            "opuin": self.opuin
        }
        userInfoRes = Tools.post(url=baseUrl, params=mCardUserMainPage,
                                 data=data)

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
                    "cardName": rootCardDict[id]['cardName'],
                    "price": rootCardDict[id]['price'],
                    "themeName": rootThemeDict[rootCardDict[id]['themeId']]['themeName'],
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
                    "themeId": rootCardDict[id]['themeId'],
                    "cardName": rootCardDict[id]['cardName'],
                    "price": int(rootCardDict[id]['price']),
                    "themeName": rootThemeDict[rootCardDict[id]['themeId']]['themeName'],
                    "slot": item.attrib["slot"],
                    "unlock": item.attrib["unlock"] if "unlock" in item.attrib.keys() else 0,
                    "status": item.attrib["status"],
                    "type": item.attrib["type"]
                })
        newList.sort(key=lambda x: x["price"])
        # newList.sort(key=lambda x: x["themeId"])
        return newList

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
        self.btnSearch = QtWidgets.QPushButton(self.groupBox2)
        self.btnSearch.setGeometry(QtCore.QRect(5, 302, 170, 40))
        self.btnSearch.setText("搜")
        self.btnSearch.setCheckable(True)
        self.btnSearch.setEnabled(False)

        self.btnSearch.clicked.connect(self.btnStartSearch)
        # self.btnSearch.clicked.connect(lambda: self.btnStartSearch)
        # self.btnSearch.clicked.connect(lambda: thread.start())

    # 开始搜索
    def btnStartSearch(self):
        # print(self.isStart)
        if not self.isStart:
            self.isStart = True
            self.btnSearch.setText("停")
            MainWindow.resize(515, 400)
            MainWindow.setFixedSize(515, 400)
            self.thread = SearchUser(self.themeId, self.selectCardList)
            self.thread.sec_changed_signal.connect(self.updateStatusBar)
            self.thread.theCardIsSearched.connect(self.cardSearched)
            self.thread.start()
            self.thread.exec()
        else:
            self.thread.setFlag()
            # self.thread.stop()
            self.btnSearch.setText("搜")
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
            "uin": 1224842990,
            "frnd": self.opuin
        }
        r = Tools.post(params=params, data=data)
        print(r.text)
        etXml = ElementTree.XML(r.text)
        code = etXml.attrib['code']
        w = QWidget()
        if code == '0':
            QMessageBox.information(w, "提示", "交换成功~", QMessageBox.Yes)
            # self.statusBar.setStyleSheet("QWidget{color: #28a745}")  # success
            # self.statusBar.showMessage('交换成功~')
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle('错误')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(etXml.attrib['message'])
            msgBox.setStandardButtons(QMessageBox.Yes)
            reply = msgBox.exec()
            # QMessageBox.ctitical(w, "错误", "message", QMessageBox.Retry)
            # QMessageBox.warning(w, "消息框标题", "这是一条警告。", QMessageBox.Yes | QMessageBox.No)
            # self.statusBar.setStyleSheet("QWidget{color: #dc3545}")  # error
            # print(etXml.attrib['message'])
            # self.statusBar.showMessage(etXml.attrib['message'])

        self.btnFriendExChange.setEnabled(False)
        self.loadMineBox()
        self.loadFriendBox()

    # 计算 双方已选择卡片
    def componendNumPrise(self):
        # print(len(self.cardsMine), sum(self.cardsMine))
        # print(len(self.cardsFriend), sum(self.cardsFriend))
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
        self.statusBar.showMessage(str)

    # 我的卡箱 - 点击
    def treeMineBoxClick(self):
        self.cardsMine = []
        self.slotMine = []

        iterator = QTreeWidgetItemIterator(self.treeMineBox)
        # print(iterator.value())
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                self.cardsMine.append(int(item.text(1)))
                self.slotMine.append(item.text(3))
            iterator.__iadd__(1)
        self.componendNumPrise()
        # print("cardsMine", self.cardsMine)

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
        # print("cardsFriend", self.cardsFriend)

    # 找到卡了
    def cardSearched(self, opuin):
        self.opuin = opuin
        self.exitFlag = False
        self.isStart = False
        self.btnSearch.toggle()
        MainWindow.resize(800, 400)
        MainWindow.setFixedSize(800, 400)
        # self.btnSearch.setEnabled(True)
        self.btnSearch.setText("搜")
        self.statusBar.showMessage('找到了!!!')
        self.loadFriendBox()

    # 状态栏 - 搜索中[更新]
    def updateStatusBar(self, num):
        self.statusBar.showMessage('搜索中... [{0}]'.format(num))
        self.statusBar.setStyleSheet("QWidget{color: #333333}")
        # print('\rsearching... Times:{0}'.format(num), end='')

    # 绘制 - 套卡容器
    def setThemeList(self):
        data = {
            "uin": self.uin,
        }
        res = Tools.post(url="https://card.qzone.qq.com/cgi-bin/card_mini_get", data=data)
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
            for theme in themes:
                if theme.attrib['diff'] == str(index) and (int(theme.attrib['type']) in self.currentTheme["type"]) and \
                        theme.attrib["new_type"] == "0" and theme.attrib["gift"] != "":
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
    def handleThemeSelect(self, index):
        i = self.treeWidget.currentItem()
        if i.text(1):  # 获取选择套卡的themeId
            self.themeId = i.text(1)
            self.currentCards = []
            for card in cards:
                if card.attrib['theme_id'] == i.text(1):
                    self.currentCards.append({
                        "id": card.attrib['id'],
                        "themeId": card.attrib['theme_id'],
                        "name": str.strip(card.attrib['name']),
                        "price": int(card.attrib['price']),
                    })

            self.currentCards.sort(key=lambda x: x["price"])
            self.listBox.clear()
            for item in self.currentCards:
                self.item = QListWidgetItem(item['name'] + "[" + str(item['price']) + "]")
                self.listBox.addItem(self.item)
                # self.listBox.insertItem(0, self.item)
            self.selectThemeHide()
            self.pushButton.toggle()

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
        # print(self.comboBox.currentText(), i)
        self.currentTheme = self.themesList[i]
        self.treeWidget.clear()
        self.setThemeList()

    def windowOnTop(self, checked):
        print(checked)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # if checked:
        #     self.setWindowFlags(
        #         self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        # else:
        #     self.setWindowFlags(
        #         self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        # self.show()


baseUrl = 'https://mfkp.qq.com/cardshow'

mCardUserMainPage = {
    "cmd": "card_user_mainpage",
    "h5ver": 1,
}
mCardUserMainPageData = {
    "uin": 1224842990,
}

rootCardDict = {}
rootThemeDict = {}

if __name__ == '__main__':
    r = Tools.post(params=mCardUserMainPage, data=mCardUserMainPageData)

    if r.text.find('code="0"') > 0:
        # region 初始化字典
        cardInfoV3 = Tools.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
        xmlStr = cardInfoV3.content.decode()
        xmlStr = xmlStr.replace("&", "&amp;")
        root = ElementTree.XML(xmlStr)

        cards = root.findall("card")
        themes = root.findall("theme")
        for card in cards:
            rootCardDict[card.attrib["id"]] = {
                "id": card.attrib["id"],
                "themeId": card.attrib["theme_id"],
                "cardName": card.attrib["name"],
                "price": card.attrib["price"],
            }

        for theme in themes:
            rootThemeDict[theme.attrib["id"]] = {
                "id": theme.attrib["id"],
                "themeName": theme.attrib["name"],
                "diff": theme.attrib["diff"],
            }
        # endregion

        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    else:
        print('error')
        # from WebLogin import LoginWeb

        # app2 = QApplication(sys.argv)
        # w = LoginWeb()
        # w.show()
        # sys.exit(app2.exec_())
        driver = webdriver.Ie()
        # driver = webdriver.PhantomJS()
        driver.set_window_size(800, 600)
        # driver.implicitly_wait(8)

        driver.get("https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=1600000084&s_url=http%3A%2F%2Fappimg2.qq.com%2Fcard%2Findex_v3.html")
        # driver.quit()
        time.sleep(5)
        # driver.refresh()
        c = driver.get_cookies()
        # print(c)
        cookies = {}
        # 获取cookie中的name和value,转化成requests可以使用的形式
        for cookie in c:
            cookies[cookie['name']] = cookie['value']
        print(cookies)
        # https://zhuanlan.zhihu.com/p/38900589
