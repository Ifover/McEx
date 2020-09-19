# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Python\McEx\McEx.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from xml.dom.minidom import parse
from xml.etree import ElementTree
import requests
import time
import re

startTime = int(time.time() * 1000)


res = requests.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
# res = requests.get("./card_info_v3.xml")
xmlStr = res.content.decode()
xmlStr = xmlStr.replace("&", "&amp;")
root = ElementTree.XML(xmlStr)

cards = root.findall("card")
themes = root.findall("theme")

cookies = {
    "uin": "o1224842990",
    "skey": "@S8a4ZRBIF",
}


def post(url, data={}, params={}):
    r = requests.post(url=url, data=data, params=params, cookies=cookies)
    r.keep_alive = False
    return r


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(-165, 10, 210, 530))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("选择套卡")

        self.listView_Anim = QPropertyAnimation(self.groupBox, b"geometry")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(170, 10, 30, 515))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(
            ">\n>\n>\n>\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>")
        self.pushButton.setCheckable(True)
        self.pushButton.clicked.connect(self.btnClick)

        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setGeometry(QtCore.QRect(5, 50, 160, 475))
        self.tabWidget.setObjectName("tabWidget")

        themesList = [
            {"id": 1, "label": "发行", "type": [0, 2]},
            {"id": 2, "label": "下架", "type": [1, 5]},
            {"id": 3, "label": "闪卡", "type": [9]},
        ]
        cardMiniGetRes = post("https://card.qzone.qq.com/cgi-bin/card_mini_get",
                              data={"uin": 1224842990})

        cardMiniGetRoot = ElementTree.XML(cardMiniGetRes.text)
        cardMiniGet = []
        for target_list in cardMiniGetRoot.findall("Node"):
            cardMiniGet.append(int(target_list.attrib["theme_id"]))

        for item in themesList:
            self.tab = QtWidgets.QWidget()
            self.tab.setEnabled(True)
            # self.tab.setObjectName("tab_" + str(item["id"]))
            self.treeWidget = QtWidgets.QTreeWidget(self.tab)
            self.treeWidget.clicked.connect(self.onClicked)

            self.treeWidget.setGeometry(QtCore.QRect(0, 0, 153, 450))
            self.treeWidget.setObjectName("treeWidget" + str(item["id"]))
            self.treeWidget.setHeaderLabels(['套卡名称'])

            # sum = 0
            # for theme in themes:
            #     if int(theme.attrib['type']) in item["type"] and theme.attrib["new_type"] == "0" and theme.attrib["gift"] != "":
            #         sum += 1

            self.tabWidget.addTab(self.tab, item["label"])   # + str(sum)

            # 设置根节点
            for index in range(1, 6):
                root = QTreeWidgetItem(self.treeWidget)
                root.setText(0, '★' * index)

                # 设置子节点1
                for theme in themes:
                    if theme.attrib['diff'] == str(index) and (int(theme.attrib['type']) in item["type"]) and theme.attrib["new_type"] == "0" and theme.attrib["gift"] != "":
                        child = QTreeWidgetItem()
                        child.setText(0, theme.attrib['name'])

                        if int(theme.attrib['id']) in cardMiniGet:
                            child.setBackground(0, QBrush(QColor("#98d22e")))

                        root.insertChild(0, child)

        self.treeWidget.addTopLevelItem(root)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

        endTime = int(time.time() * 1000)
        print("用时:" + str(endTime - startTime))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.menu.setTitle(_translate("MainWindow", "文件"))

    def btnClick(self):
        if self.pushButton.isChecked():
            self.pushButton.setText(
                "<\n<\n<\n<\n<\n<\n<\n<\n<\n<\n收\n起\n选\n择\n<\n<\n<\n<\n<\n<\n<\n<\n<\n<")
            self.listView_Anim.setDuration(300)
            self.listView_Anim.setStartValue(QtCore.QRect(-165, 10, 210, 530))
            self.listView_Anim.setEndValue(QtCore.QRect(10, 10, 210, 530))
            self.listView_Anim.start()
        else:
            self.pushButton.setText(
                ">\n>\n>\n>\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>")
            self.listView_Anim.setDuration(300)
            self.listView_Anim.setStartValue(QtCore.QRect(10, 10, 210, 530))
            self.listView_Anim.setEndValue(QtCore.QRect(-165, 10, 210, 530))
            self.listView_Anim.start()

    def onClicked(self, index):
        item = self.treeWidget.currentItem()
        # print('Key=%s,value=%s'%(item.text(0)))
        print(self.treeWidget.__dict__, index.__dict__)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
