# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Python\McEx\McEx.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 256, 331))
        self.listWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuIfover = QtWidgets.QMenu(self.menuBar)
        self.menuIfover.setObjectName("menuIfover")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuIfover.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.listWidget.setSortingEnabled(False)
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "1212"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "12123"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "12"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "12"))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "313"))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "131"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.menuIfover.setTitle(_translate("MainWindow", "Ifover"))
