import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor, QPixmap
from PyQt5.QtCore import Qt
from xml.dom.minidom import parse
from xml.etree import ElementTree

import requests
import time
import re

res = requests.get("http://appimg2.qq.com/card/mk/card_info_v3.xml")
# res = requests.get("./card_info_v3.xml")
xmlStr = res.content.decode()
xmlStr = xmlStr.replace("&", "&amp;")
root = ElementTree.XML(xmlStr)

# cards = root.findall("card")
themes = root.findall("theme")


class TreeWidgetDemo(QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidgetDemo, TabDemo, self).__init__(parent)
        self.setWindowTitle('TreeWidget 例子')

        # super(TabDemo, self).__init__(parent)

        # 创建3个选项卡小控件窗口
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")

        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        self.tree.setHeaderLabels(['套卡名称', '套卡等级'])

        diffList = [
            {"diff": 1},
            {"diff": 2},
            {"diff": 3},
            {"diff": 4},
            {"diff": 5},
        ]
        # 设置根节点
        for diff in diffList:
            root1 = QTreeWidgetItem(self.tree)
            root1.setText(0, '★' * diff['diff'])
            # 设置子节点1
            for theme in themes:
                if theme.attrib['diff'] == str(diff['diff']):
                    child = QTreeWidgetItem()
                    child.setText(0, theme.attrib['name'])
                    root1.addChild(child)
            # root1.setText(0, theme.attrib['name'])
            # root2 = QTreeWidgetItem(self.tree)

        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 150)

    def onClicked(self, qmodeLindex):
        item = self.tree.currentItem()
        print('Key=%s,value=%s' % (item.text(0), item.text(1)))


class TabDemo(QTabWidget):
    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)

        # 创建3个选项卡小控件窗口
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
        self.addTab(self.tab3, "Tab 3")

        # 每个选项卡自定义的内容
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab1UI(self):
        # 表单布局
        layout = QFormLayout()
        # 添加姓名，地址的单行文本输入框
        layout.addRow('姓名', QLineEdit())
        layout.addRow('地址', QLineEdit())
        # 设置选项卡的小标题与布局方式
        self.setTabText(0, '联系方式')
        self.tab1.setLayout(layout)

    def tab2UI(self):
        # zhu表单布局，次水平布局
        layout = QFormLayout()
        sex = QHBoxLayout()

        # 水平布局添加单选按钮
        sex.addWidget(QRadioButton('男'))
        sex.addWidget(QRadioButton('女'))

        # 表单布局添加控件
        layout.addRow(QLabel('性别'), sex)
        layout.addRow('生日', QLineEdit())

        # 设置标题与布局
        self.setTabText(1, '个人详细信息')
        self.tab2.setLayout(layout)

    def tab3UI(self):
        # 水平布局
        layout = QHBoxLayout()

        # 添加控件到布局中
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))

        # 设置小标题与布局方式
        self.setTabText(2, '教育程度')
        self.tab3.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeWidgetDemo()
    tree.show()
    # sys.exit(app.exec_())

    # app=QApplication(sys.argv)
    # demo = TabDemo()
    # demo.show()
    sys.exit(app.exec_())
