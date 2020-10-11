from PyQt5.QtWidgets import *
import sys
from Ui_McEx2 import MainWindow
from FormLogin import FormLogin

import gol
from Tools import Tools

if __name__ == '__main__':
    gol._init()
    tool = Tools()
    app = QApplication(sys.argv)

    if not gol.get_value("isLogined"):
        uui = FormLogin()
        uui.setupUi(tool=tool)
        uui.show()
        # bar1 = self.menuBar.addAction('登录')
        # # bar1.addAction('New')
        # bar1.triggered.connect()
        #
        # self.setMenuBar(self.menuBar)
        #
        # self.labelStatusStr.setText("请先登录")
        # print(1)

        # self.handleLogin()
    else:
        ui = MainWindow()
        ui.setupUi(tool=tool)
        ui.show()

    sys.exit(app.exec_())
