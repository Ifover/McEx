from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QBrush, QColor
import sys
import time


class treechange(QWidget):
    def __init__(self):
        super(treechange, self).__init__()
        self.resize(800, 600)
        layout = QHBoxLayout()

        self.groupBox = QGroupBox()
        self.groupBox.setGeometry(QRect(10, 10, 210, 530))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("选择套卡")

        # self.treeWidget = QTreeWidget(self.groupBox)
        # self.treeWidget.setGeometry(QRect(0, 0, 180, 530))
        # self.treeWidget.setColumnCount(2)
        # self.treeWidget.setHeaderLabels(['套卡名称', '套卡名称'])
        # self.treeWidget.clicked.connect(self.onClicked)
        # root = QTreeWidgetItem(self.treeWidget)
        # root.setText(0, "root")
        # root.setText(1, "1")

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setGeometry(QRect(170, 10, 30, 515))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText(
            ">\n>\n>\n>\n>\n>\n>\n>\n>\n>\n选\n择\n套\n卡\n>\n>\n>\n>\n>\n>\n>\n>\n>\n>")
        self.pushButton.setCheckable(True)
        # self.pushButton.clicked.connect(self.btnClick)




        layout.addWidget(self.groupBox)
        layout1 = QVBoxLayout(self)
        layout1.addLayout(layout)
        layout1.addWidget(self.groupBox)
        # layout1.addWidget(self.treeWidget)
        self.setLayout(layout1)

    def onClicked(self, index):
        i = self.treeWidget.currentItem()
        print(index.row())
        print('key=%s,value=%s' % (i.text(0), i.text(1)))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ui = treechange()
    ui.show()
    sys.exit(app.exec_())
