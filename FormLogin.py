# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from xml.etree import ElementTree
import configparser
import gol


class FormLogin(QDialog):
    def __init__(self):
        super(FormLogin, self).__init__()  # <---
        from MainWindow import MainWindow
        self.ui = MainWindow()
        self.path = r'./config.ini'
        self.iniConfig = configparser.ConfigParser()
        self.iniConfig.read(self.path)
        self.uin = self.iniConfig['config']['uin']
        self.skey = self.iniConfig['config']['skey']

    def setupUi(self, **kwargs):
        self.tool = kwargs['tool']
        self.resize(320, 200)
        self.setFixedSize(320, 200)
        self.setWindowTitle("登录")
        qfl = QFormLayout()
        qfl.setLabelAlignment(Qt.AlignRight)

        self.uinLineEdit = QLineEdit()
        self.sKeyLineEdit = QLineEdit()
        okPushButton = QPushButton('确定')
        okPushButton.clicked.connect(self.btnClick)

        bookMark = QLineEdit("javascript:alert(document.cookie.substr(document.cookie.indexOf('skey') + 5,10))")
        bookMark.setDragEnabled(True)
        qfl.addRow("QQ", self.uinLineEdit)
        qfl.addRow("sKey", self.sKeyLineEdit)
        qfl.addRow(okPushButton)
        qfl.addRow(bookMark)

        self.uinLineEdit.setPlaceholderText("请输入QQ号")
        self.sKeyLineEdit.setPlaceholderText("请输入sKey")
        self.uinLineEdit.setText(self.uin)
        self.sKeyLineEdit.setText(self.skey)

        self.setLayout(qfl)

    def btnClick(self):
        cookies = {
            "uin": 'o' + self.uinLineEdit.text(),
            "skey": '@' + self.sKeyLineEdit.text()
        }
        gol.set_value('cookies', cookies)
        params = {
            "cmd": "card_user_mainpage",
            "h5ver": 1,
        }
        data = {
            "uin": self.uinLineEdit.text(),
        }
        print(params, data)
        res = self.tool.post(params=params, data=data)
        root = ElementTree.XML(res.text)
        print(root.attrib["code"])
        if root.attrib["code"] == '0':
            # self.iniConfig = configparser.ConfigParser()
            # self.iniConfig.read(r'./config.ini')
            self.iniConfig.remove_option('config', 'uin')  # 删除一个配置
            self.iniConfig.remove_option('config', 'skey')  # 删除一个配置

            self.iniConfig.set('config', 'uin', self.uinLineEdit.text())  # 写入数据
            self.iniConfig.set('config', 'skey', self.sKeyLineEdit.text())  # 写入数据
            self.iniConfig.write(open(self.path, 'w'))  # 保存数据


            gol.set_value('isLogined', True)
            self.ui.setupUi(tool=self.tool)
            self.close()
            self.ui.show()
