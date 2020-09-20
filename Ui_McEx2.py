# -*- coding: utf-8 -*-


import sys
import time
from xml.dom.minidom import parse
from xml.etree import ElementTree

# import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtWidgets import *

import Tools
from SearchUser import SearchUser
import threading


# import search
baseUrl = 'https://mfkp.qq.com/cardshow'

res = Tools.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
xmlStr = res.content.decode()
xmlStr = xmlStr.replace("&", "&amp;")
root = ElementTree.XML(xmlStr)

cards = root.findall("card")
themes = root.findall("theme")

mCardUserMainPage = {
    "cmd": "card_user_mainpage",
    "h5ver": 1,
}
mCardUserMainPageData = {
    "uin": 1224842990,
}

rootCardDict = {}
for card in cards:
    rootCardDict[card.attrib["id"]] = {
        "id": card.attrib["id"],
        "themeId": card.attrib["theme_id"],
        "cardName": card.attrib["name"],
        "price": card.attrib["price"],
    }

rootThemeDict = {}
for theme in themes:
    rootThemeDict[theme.attrib["id"]] = {
        "id": theme.attrib["id"],
        "themeName": theme.attrib["name"],
        "diff": theme.attrib["diff"],
    }


class Ui_MainWindow(object):
    def __init__(self):
        self.isStart = False
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(800, 400)
        MainWindow.setFixedSize(800, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.groupBox = QGroupBox(MainWindow)
        self.groupBox.setGeometry(QRect(-165, 28, 210, 345))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setTitle("选择套卡")

        self.groupBox2 = QGroupBox(MainWindow)
        self.groupBox2.setGeometry(QRect(50, 28, 180, 345))
        self.groupBox2.setAutoFillBackground(True)
        self.groupBox2.setTitle("选择卡片")

        self.setMineBox()  # 绘制我的卡箱
        self.setCardFriendBox()  # 绘制卡友的换卡箱
        self.setBtnStartSearch()  # 开始搜索

        self.btnExChange = QtWidgets.QPushButton(MainWindow)
        self.btnExChange.setGeometry(QtCore.QRect(495, 293, 45, 80))
        self.btnExChange.setText("交\n\n换")
        self.btnExChange.setCheckable(True)
        self.btnExChange.clicked.connect(self.getText)

        self.listBox = QListWidget(self.groupBox2)
        self.listBox.setGeometry(QRect(5, 18, 170, 280))
        self.listBox.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)
        # self.listBox.clicked.connect(self.handleCardSelect)
        self.listBox.currentItemChanged.connect(self.handleCardSelect)

        self.listView_Anim = QPropertyAnimation(self.groupBox, b"geometry")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(170, 10, 30, 331))
        self.pushButton.setText(
            ">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
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

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menuIfover = QtWidgets.QMenu(self.menuBar)
        self.menuIfover.setTitle("Ifover")
        MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menuIfover.menuAction())

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.showMessage("ready!")
        MainWindow.setStatusBar(self.statusBar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # 绘制 - 我的卡箱
    def setMineBox(self):
        userInfoRes = Tools.post(url=baseUrl, params=mCardUserMainPage,
                                 data=mCardUserMainPageData)

        etXml = ElementTree.XML(userInfoRes.text)
        changeBox = etXml.find("changebox")

        self.groupBox3 = QGroupBox(MainWindow)
        self.groupBox3.setGeometry(QRect(240, 28, 250, 345))
        self.groupBox3.setAutoFillBackground(True)
        self.groupBox3.setTitle("Ifover.卡箱")

        self.treeMineBox = QTreeWidget(self.groupBox3)
        self.treeMineBox.setGeometry(QtCore.QRect(5, 18, 240, 323))
        self.treeMineBox.setHeaderLabels(['卡名', '价格', '套卡'])
        # self.treeWidget.setIndentation(0)
        self.treeMineBox.setColumnWidth(0, 110)
        self.treeMineBox.setColumnWidth(1, 40)
        self.treeMineBox.setColumnWidth(2, 70)
        self.treeMineBox.clicked.connect(self.treeMineBoxClick)
        # self.treeMineBox.itemChanged.connect(self.handleChanged)

        self.treeMineBox.setRootIsDecorated(False)  # 隐藏箭头

        changeBox = etXml.find("changebox")
        changeBoxsCards = changeBox.findall("card")
        root = QTreeWidgetItem(self.treeMineBox)

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

        root.setText(
            0, "-换卡箱- [{currentNum}/{maxNum}]".format(currentNum=len(changeBoxsCardsList), maxNum=changeBox.attrib["cur"]))
        # root.setText(0, "-换卡箱- [" + changeBox.attrib["cur"] + "]")

        changeBoxsCardsList.sort(key=lambda x: x["price"])
        for cbCard in changeBoxsCardsList:
            child = QTreeWidgetItem()
            child.setText(0, "{lock}{name}".format(
                lock='' if cbCard['unlock'] == '0' else '[锁]', name=cbCard['cardName']))
            child.setText(1, cbCard['price'])
            child.setText(2, cbCard['themeName'])
            child.setText(3, cbCard['cardId'] + '_' + cbCard['slot'] + '_0')
            child.setCheckState(0, not Qt.CheckState)
            child.setToolTip(0, cbCard['cardName'])

            root.insertChild(0, child)

        storeboxBox = etXml.find("storebox")
        storeboxBoxCards = storeboxBox.findall("card")
        root = QTreeWidgetItem(self.treeMineBox)
        # root.setText(0, "--保险箱--")
        root.setText(
            0, "-保险箱- [{currentNum}/{maxNum}]".format(currentNum=len(storeboxBoxCards), maxNum=storeboxBox.attrib["cur"]))

        for cbCard in storeboxBox:
            child = QTreeWidgetItem()
            id = cbCard.attrib["id"]
            if int(id) > 0:  # 跳过一些莫名其妙的卡
                child.setText(0, rootCardDict[id]['cardName'])
                child.setText(1, rootCardDict[id]['price'])
                child.setText(
                    2, rootThemeDict[rootCardDict[id]['themeId']]['themeName'])
                child.setText(3, id + '_' + cbCard.attrib["slot"] + '_1')
                child.setCheckState(0, not Qt.CheckState)
                root.insertChild(0, child)

        self.treeMineBox.expandAll()

    # 绘制 - 卡友卡箱
    def setCardFriendBox(self):
        self.groupBox4 = QGroupBox(MainWindow)
        self.groupBox4.setGeometry(QRect(545, 28, 250, 345))
        self.groupBox4.setAutoFillBackground(True)
        self.groupBox4.setTitle("xxxxx.卡箱")

        self.treeFriendBox = QTreeWidget(self.groupBox4)
        self.treeFriendBox.setGeometry(QtCore.QRect(5, 18, 240, 323))
        self.treeFriendBox.setHeaderLabels(['卡名', '价格', '套卡'])
        # self.treeWidget.setIndentation(0)
        self.treeFriendBox.setColumnWidth(0, 110)
        self.treeFriendBox.setColumnWidth(1, 40)
        self.treeFriendBox.setColumnWidth(2, 70)
        self.treeFriendBox.clicked.connect(self.treeFriendBoxClick)

        self.treeFriendBox.setRootIsDecorated(False)

    # Load - 卡友
    def loadFriendBox(self):
        data = {
            "uin": 1224842990,
            "opuin": self.opuin
        }
        userInfoRes = Tools.post(url=baseUrl, params=mCardUserMainPage,
                                 data=data)

        etXml = ElementTree.XML(userInfoRes.text)
        changeBox = etXml.find("changebox")
        changeBoxsCards = changeBox.findall("card")
        root = QTreeWidgetItem(self.treeFriendBox)
        root.setText(0, "--换卡箱--")

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
            child = QTreeWidgetItem()
            child.setText(0, cbCard['cardName'])
            child.setText(1, cbCard['price'])
            child.setText(2, cbCard['themeName'])
            child.setText(3, cbCard['cardId'] + '_' + cbCard['slot'] + '_0')
            child.setCheckState(0, not Qt.CheckState)
            root.insertChild(0, child)

        self.treeFriendBox.expandAll()

    # 选择卡片
    def handleCardSelect(self):
        selectedItems = self.listBox.selectedItems()
        self.selectCardList = []
        for i in list(selectedItems):
            self.selectCardList.append(
                self.currentCards[self.listBox.row(i)]['id'])

    # 绘制 - 按钮[开始搜索]
    def setBtnStartSearch(self):
        self.btnSearch = QtWidgets.QPushButton(self.groupBox2)
        self.btnSearch.setGeometry(QtCore.QRect(5, 302, 170, 40))
        self.btnSearch.setText("开始搜索")
        self.btnSearch.setCheckable(True)

        self.btnSearch.clicked.connect(self.btnStartSearch)
        # self.btnSearch.clicked.connect(lambda: self.btnStartSearch)
        # self.btnSearch.clicked.connect(lambda: thread.start())

    # 开始搜索
    def btnStartSearch(self):
        # print(self.isStart)
        if not self.isStart:
            self.isStart = True
            self.btnSearch.setText("停止搜索")
            self.thread = SearchUser(self.themeId, self.selectCardList)
            self.thread.sec_changed_signal.connect(self.updateStatusBar)
            self.thread.theCardIsSearched.connect(self.cardSearched)
            self.thread.start()
            self.thread.exec()
        else:
            self.thread.setFlag()
            # self.thread.stop()
            self.btnSearch.setText("开始搜索")
            # self.thread.exitFlag = True
            self.isStart = False

        # if thread in self.keys():
        #     print(self.thread)
        # if self.btnSearch.isChecked():

        #     self.btnSearch.setText("停止搜索")
        # else:

        # self.btnSearch.setEnabled(False)

        # self.thread.start()
        # self.thread.exec()

    # def handleChanged(self, item, column):
        # 当check状态改变时得到他的状态。
        # if item.checkState(column) == Qt.Checked:
            # print("checked", item, item.text(column))
        # if item.checkState(column) == Qt.Unchecked:
            # print("unchecked", item, item.text(column))

    def getText(self):
        # print self.tree
        iterator = QTreeWidgetItemIterator(self.treeMineBox)
        # print(iterator.value())
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                print(item.text(3))

            iterator.__iadd__(1)

    def componendNumPrise(self):

        self.statusBar.showMessage('搜索中... [{0}]'.format(num))

    # 我的卡箱 - 点击
    def treeMineBoxClick(self):
        self.cardsMine = []
        iterator = QTreeWidgetItemIterator(self.treeMineBox)
        # print(iterator.value())
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                self.cardsMine.append(int(item.text(1)))
            iterator.__iadd__(1)
        print("cardsMine", self.cardsMine)
        self.componendNumPrise()
        

    # 卡友卡箱 - 点击
    def treeFriendBoxClick(self):
        self.cardsFriend = []
        iterator = QTreeWidgetItemIterator(self.treeFriendBox)
        while iterator.value():
            item = iterator.value()
            if item.checkState(0) == Qt.Checked:
                self.cardsFriend.append(int(item.text(1)))
            iterator.__iadd__(1)
        print("cardsFriend", self.cardsFriend)
        self.componendNumPrise()


    # 找到卡了

    def cardSearched(self, opuin):
        self.opuin = opuin
        self.exitFlag = False
        self.btnSearch.setEnabled(True)
        self.btnSearch.setText("开始搜索")
        self.loadFriendBox()

    def updateStatusBar(self, num):
        self.statusBar.showMessage('搜索中... [{0}]'.format(num))
        # print('\rsearching... Times:{0}'.format(num), end='')

    def setThemeList(self):
        self.treeWidget.invisibleRootItem()
        for index in range(1, 6):
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0, "难度系数：" + ('★' * index))
            # 设置子节点1
            for theme in themes:
                if theme.attrib['diff'] == str(index) and (int(theme.attrib['type']) in self.currentTheme["type"]) and theme.attrib["new_type"] == "0" and theme.attrib["gift"] != "":
                    child = QTreeWidgetItem()
                    child.setText(0, theme.attrib['name'])
                    child.setText(1, theme.attrib['id'])

                    root.insertChild(0, child)

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
                self.item = QListWidgetItem(
                    item['name'] + "[" + str(item['price']) + "]")
                self.listBox.addItem(self.item)
                # self.listBox.insertItem(0, self.item)
            self.selectThemeHide()
            self.pushButton.toggle()

            # print(self.currentCards)
        # print('key=%s,value=%s' % (i.text(0), i.text(1)))

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
        self.pushButton.setText(
            ">\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>")
        self.listView_Anim.setDuration(300)
        self.listView_Anim.setStartValue(QtCore.QRect(10, 28, 210, 345))
        self.listView_Anim.setEndValue(QtCore.QRect(-165, 28, 210, 345))
        self.listView_Anim.start()

    # 显示选择套卡模块
    def selectThemeShow(self):
        self.pushButton.setText(
            "<\n<\n<\n<\n<\n<\n<\n收\n起\n选\n择\n<\n<\n<\n<\n<\n<\n<")
        self.listView_Anim.setDuration(300)
        self.listView_Anim.setStartValue(QtCore.QRect(-165, 28, 210, 345))
        self.listView_Anim.setEndValue(QtCore.QRect(10, 28, 210, 345))
        self.listView_Anim.start()

    def onTabWidgetClicked(self, i):
        # print(self.comboBox.currentText(), i)
        self.currentTheme = self.themesList[i]
        self.treeWidget.clear()
        self.setThemeList()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
