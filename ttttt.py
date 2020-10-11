from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# from haoP import Ui_nihao

# 第二界面
class Ui_nihao(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_nihao, self).__init__()
        self.setObjectName("nihao")
        self.resize(400, 300)
        self.setWindowTitle("消息")
        self.changeP = QtWidgets.QPushButton(self)
        self.changeP.setGeometry(QtCore.QRect(100, 80, 181, 91))
        self.changeP.setObjectName("pageb")
        self.changeP.setText("跳转pageb")
        self.changeP.clicked.connect(self.pageb)

    def pageb(self):
        self.haoN = Ui_PageB()
        self.haoN.show()
        print("bbbbb")
        self.close()
        # self.haoN.exec_()


# 第一界面
class Ui_PageB(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_PageB, self).__init__()
        self.setObjectName("nihao")
        self.resize(400, 300)
        self.setWindowTitle("消息")
        self.changeP = QtWidgets.QPushButton(self)
        self.changeP.setGeometry(QtCore.QRect(100, 100, 181, 71))
        self.changeP.setObjectName("changeP")
        self.changeP.setText("跳转nihao")
        self.changeP.clicked.connect(self.haoPa)

    def haoPa(self):
        self.haoN = Ui_nihao()
        self.haoN.show()
        print("nihao")
        self.close()
        # self.haoN.exec_()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = Ui_PageB()
    widget.show()
    sys.exit(app.exec_())