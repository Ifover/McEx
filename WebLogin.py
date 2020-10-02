from datetime import datetime
import sys
from PyQt5.QtCore import QThread, pyqtSignal

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By


# 先来个窗口
class LoginWeb(QThread):
    my_signal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        # self.cookies = {}
        # self.setup()

    def run(self):
        driver = webdriver.Chrome()
        # driver = webdriver.Ie()
        driver.set_window_size(800, 600)
        driver.get(
            "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=1600000084&s_url=http%3A%2F%2Fappimg2.qq.com%2Fcard%2Findex_v3.html")

        driver.implicitly_wait(10)  # 隐性等待
        # time.sleep(3)

        try:
            wait_process = WebDriverWait(driver, 10, 0.1).until(EC.title_contains(u"魔法卡片"))
            # wait_process = WebDriverWait(driver, 10).until_not(lambda driver: driver.find_element_by_id("login"))

            if wait_process:
                c = driver.get_cookies()
                cookies = {}
                for cookie in c:
                    if cookie['name'] in ['uin', 'skey']:
                        cookies[cookie['name']] = cookie['value']
                # tool.cookies = cookies
                # tool.uin = cookies["uin"][1:]
                # print(tool.uin)

                self.my_signal.emit({
                    "code": 0,
                    "data": {
                        "cookies": cookies,
                        "uin": cookies["uin"][1:]
                    }
                })

                # isLogined = True



        except Exception as e:
            print("error:", e)
            self.my_signal.emit({
                "code": -1,
                "data": {}
            })
            # sys.exit()

        finally:
            driver.quit()

            print(2)
