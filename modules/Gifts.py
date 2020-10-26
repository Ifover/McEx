from xml.etree import ElementTree
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  # Qt, QPropertyAnimation
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *
import json
import threading
import time
import requests
import execjs


class Gifts(object):

    def __init__(self):
        self.giftList = []

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.tabGifts = kwargs['tabGifts']
        self.labelStatusStr = kwargs['labelStatusStr']
        self.uin = kwargs['uin']

        self.imgs = []
        configRes = requests.get('http://qzs.qq.com/appimg/free_gift/365/config.js')
        configRes.encoding = 'utf-8'
        res = json.loads(configRes.text.strip('var freeGiftConfig='))

        # print(res)
        self.listWidget = QListWidget(self.tabGifts)
        self.listWidget.setGeometry(QtCore.QRect(5, 5, 400, 210))
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setAutoScroll(True)
        self.listWidget.setIconSize(QtCore.QSize(68, 68))
        self.listWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.listWidget.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidget.itemSelectionChanged.connect(self.handleCardSelect)

        for item in res:

            if item['show'] == 1:
                self.giftList.append(item)

                imgRes = requests.get(item['asset_url_freegift'])
                img = QImage.fromData(imgRes.content)
                listwidgetitem = QtWidgets.QListWidgetItem()
                listwidgetitem.setSizeHint(QSize(94, 102))
                listwidgetitem.setText(item['name'])
                listwidgetitem.setIcon(QIcon(QPixmap.fromImage(img)))

                self.listWidget.addItem(listwidgetitem)

    # 选择卡片
    def handleCardSelect(self):
        selectedItems = self.listWidget.selectedItems()

        # self.btnSearch.setEnabled(False)
        # self.selectCardList = []
        for i in list(selectedItems):
            print(self.giftList[self.listWidget.row(i)])
        #     self.selectCardList.append(self.currentCards[]['id'])
        # if len(self.selectCardList) > 0:
        #     self.btnSearch.setEnabled(True)
