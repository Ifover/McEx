from xml.etree import ElementTree
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *  # Qt, QPropertyAnimation
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *
import json
import threading
import time
import requests
# import execjs


class Gifts(object):

    def __init__(self):
        self.giftList = []

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.tabGifts = kwargs['tabGifts']
        self.labelStatusStr = kwargs['labelStatusStr']
        self.uin = kwargs['uin']

        self.createSendGifts()

        self.createInfo()

        self.createPre()

        self.btnSendGift = QtWidgets.QPushButton("开送", self.gBoxGifts)
        self.btnSendGift.setGeometry(QtCore.QRect(230, 315, 175, 40))
        self.btnSendGift.clicked.connect(self.handleStartSend)

        self.gBoxGet = QtWidgets.QGroupBox("收到礼物", self.tabGifts)
        self.gBoxGet.setGeometry(QtCore.QRect(425, 10, 360, 240))

        self.gBoxLog = QtWidgets.QGroupBox("日志", self.tabGifts)
        self.gBoxLog.setGeometry(QtCore.QRect(425, 250, 360, 120))

        self.tBrowLog = QtWidgets.QTextBrowser(self.gBoxLog)
        self.tBrowLog.setGeometry(QtCore.QRect(5, 20, 350, 95))

    # 创建 - 赠送礼物 列表
    def createSendGifts(self):
        self.gBoxGifts = QtWidgets.QGroupBox('赠送礼物', self.tabGifts)
        self.gBoxGifts.setGeometry(QtCore.QRect(10, 10, 410, 360))

        self.imgs = []

        configRes = requests.get('http://qzs.qq.com/appimg/free_gift/365/config.js')
        configRes.encoding = 'utf-8'
        res = json.loads(configRes.text.strip('var freeGiftConfig='))

        self.lWGift = QListWidget(self.gBoxGifts)
        self.lWGift.setGeometry(QtCore.QRect(5, 20, 400, 210))
        self.lWGift.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.lWGift.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lWGift.setAutoScroll(True)
        self.lWGift.setIconSize(QtCore.QSize(68, 68))
        self.lWGift.setViewMode(QtWidgets.QListView.IconMode)
        self.lWGift.setResizeMode(QtWidgets.QListView.Adjust)
        self.lWGift.setItemAlignment(QtCore.Qt.AlignCenter)
        self.lWGift.itemSelectionChanged.connect(self.handleCardSelect)

        for item in res:

            if item['show'] == 1:
                self.giftList.append(item)

                imgRes = requests.get(item['asset_url_freegift'])
                img = QImage.fromData(imgRes.content)
                lWItem = QtWidgets.QListWidgetItem()
                lWItem.setSizeHint(QSize(94, 102))
                lWItem.setText(item['name'])
                lWItem.setIcon(QIcon(QPixmap.fromImage(img)))

                self.lWGift.addItem(lWItem)

    # 创建 - 用户信息
    def createInfo(self):
        self.gBoxInfo = QtWidgets.QGroupBox("信息", self.gBoxGifts)
        self.gBoxInfo.setGeometry(QtCore.QRect(230, 235, 175, 75))

        self.fLayInfo = QFormLayout(self.gBoxInfo)
        self.fLayInfo.setGeometry(QtCore.QRect(5, 20, 165, 50))
        self.fLayInfo.setLabelAlignment(Qt.AlignRight)

        self.labTimes = QLabel()  # 次数

        self.fLayInfo.addRow("剩余次数", self.labTimes)

    def loadInfo(self):
        params = {
            "g_tk": 912350831,
            "appid": 365,
            "uin": self.uin
        }
        freeGift = self.tool.get('http://hydra.qzone.qq.com/cgi-bin/freegift/freegift_get_frds', params)
        self.labTimes.setText(f"{freeGift['quota_num']}/50")


    # 创建 - 优先赠送
    def createPre(self):
        self.gBoxPre = QtWidgets.QGroupBox("优先赠送", self.gBoxGifts)
        self.gBoxPre.setGeometry(QtCore.QRect(5, 235, 220, 120))
        self.gBoxPre.setEnabled(False)

        self.tEditPre = QtWidgets.QPlainTextEdit(self.gBoxPre)
        self.tEditPre.setGeometry(QtCore.QRect(5, 20, 160, 95))
        self.tEditPre.setToolTip('啊，好。还没做呢')

        self.btnPreSave = QtWidgets.QPushButton("保存", self.gBoxPre)
        self.btnPreSave.setGeometry(QtCore.QRect(170, 85, 45, 30))
        self.btnPreSave.setToolTip('啊，好。还没做呢')

    # 选择卡片
    def handleCardSelect(self):
        selectedItems = self.lWGift.selectedItems()

        # self.btnSearch.setEnabled(False)
        # self.selectCardList = []
        for i in list(selectedItems):
            print(self.giftList[self.lWGift.row(i)])
        #     self.selectCardList.append(self.currentCards[]['id'])
        # if len(self.selectCardList) > 0:
        #     self.btnSearch.setEnabled(True)

    # 开始赠送
    def handleStartSend(self):
        th = threading.Thread(target=self.loadInfo)
        th.start()

        # print(1)
