# -*- coding: utf-8 -*-

import sys
import time
from xml.dom.minidom import parse
from xml.etree import ElementTree

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtWidgets import *

import threading
import search

res = requests.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
# res = requests.get("./card_info_v3.xml")
xmlStr = res.content.decode()
xmlStr = xmlStr.replace("&", "&amp;")
root = ElementTree.XML(xmlStr)

cookies = {
    "uin": "o1224842990",
    "skey": "@G92uIc33c",
}

cards = root.findall("card")
themes = root.findall("theme")

baseUrl = 'https://mfkp.qq.com/cardshow'
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
# print(dict.items(rootCardDict))

    # print(num)


def post(url, data={}, params={}):
    r = requests.post(url=url, data=data, params=params, cookies=cookies)
    r.keep_alive = False
    return r


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
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

        self.treeWidget = QTreeWidget(MainWindow)
        self.treeWidget.setGeometry(QtCore.QRect(300, 75, 240, 265))
        self.treeWidget.setHeaderLabels(['卡名', '价格', '套卡'])
        # self.treeWidget.setIndentation(0)
        self.treeWidget.setColumnWidth(0, 110)
        self.treeWidget.setColumnWidth(1, 40)
        self.treeWidget.setColumnWidth(2, 70)

        # self.treeWidget.clicked.connect(self.onClicked)

        userInfoRes = post(url=baseUrl, params=mCardUserMainPage,
                           data=mCardUserMainPageData)

        etXml = ElementTree.XML(userInfoRes.text)
        changeBox = etXml.find("changebox")
        changeBoxsCards = changeBox.findall("card")
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, "--换卡箱--")

        for cbCard in changeBoxsCards:
            child = QTreeWidgetItem()
            if int(cbCard.attrib["id"]) > 0:  # 跳过一些莫名其妙的卡
                child.setText(0, rootCardDict[cbCard.attrib["id"]]['cardName'])
                child.setText(1, rootCardDict[cbCard.attrib["id"]]['price'])
                child.setText(2, rootCardDict[cbCard.attrib["id"]]['themeId'])
                root.insertChild(0, child)

        storeboxBox = etXml.find("storebox")
        storeboxBoxCards = storeboxBox.findall("card")
        root = QTreeWidgetItem(self.treeWidget)
        root.setText(0, "--保险箱--")

        for cbCard in storeboxBox:
            child = QTreeWidgetItem()
            if int(cbCard.attrib["id"]) > 0:  # 跳过一些莫名其妙的卡
                child.setText(0, rootCardDict[cbCard.attrib["id"]]['cardName'])
                child.setText(1, rootCardDict[cbCard.attrib["id"]]['price'])
                child.setText(2, rootCardDict[cbCard.attrib["id"]]['themeId'])
                root.insertChild(0, child)

        self.listBox = QListWidget(self.groupBox2)
        self.listBox.setGeometry(QRect(5, 18, 170, 280))
        self.listBox.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)
        self.listBox.clicked.connect(self.handleListChanged)

        self.btnSearch = QtWidgets.QPushButton(self.groupBox2)
        self.btnSearch.setGeometry(QtCore.QRect(5, 302, 170, 40))
        self.btnSearch.setText("开始搜索")
        self.btnSearch.clicked.connect(self.btnStartSearch)

        self.listView_Anim = QPropertyAnimation(self.groupBox, b"geometry")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(170, 10, 30, 331))
        self.pushButton.setObjectName("pushButton")
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
        self.treeWidget.clicked.connect(self.onClicked)
        self.showTreeWidget()
        self.comboBox.currentIndexChanged.connect(self.onTabWidgetClicked)
        self.groupBox.raise_()

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menuIfover = QtWidgets.QMenu(self.menuBar)
        self.menuIfover.setTitle("Ifover")
        MainWindow.setMenuBar(self.menuBar)
        self.menuBar.addAction(self.menuIfover.menuAction())

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def componendNum(self, num):
        # self.statusBar.showMessage('rsearching...' + str(num), 5000)
        print('\rsearching... Times:{0}'.format(num), end='')

    def handleListChanged(self, currentRow):
        # if (currentRow >= 0):
        # print(currentRow.row())

        text_list = self.listBox.selectedItems()
        # text = [i.text() for i in list(text_list)]
        for i in list(text_list):
            print(self.currentCards[self.listBox.row(i)])
        # text = '_'.join(text)  # text即多选项并以_隔开
        # print(text)

        # for target_list in self.listBox.selectedItems():
        #     print(target_list.text())
        # for target_list in self.listBox.selectedItems():
        #     print(target_list.text())

    def btnStartSearch(self):
        # th = threading.Thread(target="search.startSearch")
        # th.start()
        print(search.startSearch())

    def showTreeWidget(self):
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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def btnSelectThemeShowHide(self):
        if self.pushButton.isChecked():
            self.selectThemeShow()
        else:
            self.selectThemeHide()

    def onClicked(self, index):
        i = self.treeWidget.currentItem()
        if i.text(1):  # 获取选择套卡的themeId
            # print(i.text(0), i.text(1))
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

            # print(self.currentCards)
        # print('key=%s,value=%s' % (i.text(0), i.text(1)))

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
        self.showTreeWidget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
