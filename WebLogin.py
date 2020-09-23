import sys
import time

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import QCoreApplication


# 先来个窗口
class LoginWeb(QDialog):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.box = QVBoxLayout(self)  # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('点击获取cookies')  # 创建一个按钮涌来了点击获取cookie
        self.btn_get.clicked.connect(QCoreApplication.instance().quit)  # 绑定按钮点击事件

        self.loginWeb = QWebEngineView()
        self.loginWeb.resize(800, 400)  # 设置大小
        self.loginWeb.load(QUrl(
            "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=1600000084&s_url=http://appimg2.qq.com/card/index_v3.html"))  # 设置大小
        self.loginWeb.urlChanged.connect(self.pppp)

        # self.web = MyWebEngineView()  # 创建浏览器组件对象
        # self.web.resize(800, 400)  # 设置大小
        # self.web.load(QUrl(
        #     "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=1600000084&s_url=http://appimg2.qq.com/card/index_v3.html"))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.loginWeb)  # 再放浏览器
        self.loginWeb.show()  # 最后让页面显示出来

        # self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        print(cookie_str)
        # return cookie_str  # 返回拼接好的字符串

    # def get_cookie(self):
    #     cookie = self.loginWeb.get_cookie()
    #     print('获取到cookie: ', cookie)

    def pppp(self, url):
        print(1)

        if url == QUrl('http://appimg2.qq.com/card/index_v3.html'):
            print(2)
            # QCoreApplication.instance().quit
            QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
            self.get_cookie()
            print(3)

            self.close()
            print(4)

        # 创建自己的浏览器控件，继承自QWebEngineView


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # window = QDialog()

    w = LoginWeb()
    # w.setup(window)
    w.show()

    sys.exit(app.exec_())
