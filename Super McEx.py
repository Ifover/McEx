from PyQt5.QtWidgets import *
import sys
from MainWindow import MainWindow
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
    else:
        ui = MainWindow()
        ui.setupUi(tool=tool)
        ui.show()

    sys.exit(app.exec_())
