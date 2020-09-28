from selenium import webdriver
import time

driver = webdriver.Ie()
# driver = webdriver.PhantomJS()
driver.set_window_size(800, 600)
# driver.implicitly_wait(8)

driver.get("https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=1600000084&s_url=http%3A%2F%2Fappimg2.qq.com%2Fcard%2Findex_v3.html")
# driver.quit()
time.sleep(5)
# driver.refresh()
c = driver.get_cookies()
# print(c)
cookies = {}
# 获取cookie中的name和value,转化成requests可以使用的形式
for cookie in c:
    cookies[cookie['name']] = cookie['value']
print(cookies)
# https://zhuanlan.zhihu.com/p/38900589
