import sys

# 这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon


class Example(QWidget):

  def __init__(self):
      super().__init__()

      self.initUI()  # 界面绘制交给InitUi方法

      # 控制窗口显示在屏幕中心的方法
  def center(self):

      # 获得窗口
      qr = self.frameGeometry()
      # 获得屏幕中心点
      cp = QDesktopWidget().availableGeometry().center()
      # 显示到屏幕中心
      qr.moveCenter(cp)
      self.move(qr.topLeft())

  def initUI(self):
      # 设置窗口的位置和大小
      self.setGeometry(300, 300, 300, 220)
      # 设置窗口的标题
      self.setWindowTitle('Icon')
      # 设置窗口的图标，引用当前目录下的web.png图片
      self.setWindowIcon(QIcon('wand.ico'))
      self.center()  # 界面绘制交给InitUi方法

      # 显示窗口
      self.show()


if __name__ == '__main__':
    # 创建应用程序和对象
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
