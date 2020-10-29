from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *  # QPropertyAnimation
from PyQt5.QtWidgets import *

from xml.etree import ElementTree
from modules.McEx import McEx
from modules.Spirite import Spirite
from modules.Gifts import Gifts
import win32gui
import win32con
import gol
import time


class MainWindow(QMainWindow):

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.setWindowTitle("Super McEx")
        self.setWindowIcon(QIcon(':/icon.ico'))
        self.resize(800, 450)
        self.setFixedSize(800, 450)
        self.labelStatusStr = QLabel("xxxx")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.addPermanentWidget(self.labelStatusStr, stretch=4)

        self.setStatusBar(self.statusBar)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.createMenu()
        self.createTabBox()

    # 绘制 - 菜单栏
    def createMenu(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.setMenuBar(self.menuBar)
        self.menuBar.clear()
        params = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }
        data = {
            "uin": gol.get_value('cookies')['uin'][1:],
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

    # 绘制 - 主Tab页
    def createTabBox(self):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 5, 790, 395))
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 280))

        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabBarAutoHide(False)

        self.tabWidget.setStyleSheet('.QTabWidget{background-color:#f0f0f0}')

        timeStart = time.time()

        self.tabMcEx = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tabMcEx, "换卡")
        self.McEx = McEx()
        self.McEx.setupUi(
            tool=self.tool,
            tabMcEx=self.tabMcEx,
            labelStatusStr=self.labelStatusStr
        )

        self.tabSpirite = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tabSpirite, "灵宠")
        self.Spirite = Spirite()
        self.Spirite.setupUi(
            tool=self.tool,
            tabSpirite=self.tabSpirite,
            labelStatusStr=self.labelStatusStr,
            uin=gol.get_value('cookies')['uin'][1:]
        )

        self.tabGifts = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tabGifts, "礼物")
        self.Gifts = Gifts()
        self.Gifts.setupUi(
            tool=self.tool,
            tabGifts=self.tabGifts,
            labelStatusStr=self.labelStatusStr,
            uin=gol.get_value('cookies')['uin'][1:]
        )

        timeEnd = time.time()
        # print(timeEnd - timeStart)
        self.tabWidget.setCurrentIndex(2)

    def handleLogin(self):
        self.labelStatusStr.setText("正在加载登录窗口~")
        from FormLogin import FormLogin

        self.uui = FormLogin()
        self.uui.setupUi(tool=self.tool)
        self.close()
        self.uui.show()

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
