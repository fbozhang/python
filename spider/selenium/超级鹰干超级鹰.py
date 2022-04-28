# -*- coding:utf-8 -*-
# @Time : 2022/4/28 20:40
# @Author: fbz
# @File : as.py
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from chaojiying import Chaojiying_Client

web = Chrome()
web.get("http://www.chaojiying.com/user/login/")

# 处理验证码
img = web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[1]/form/div/img').screenshot_as_png
chaojiying = Chaojiying_Client('15217277444', '123456', '932709')
dic = chaojiying.PostPic(img, 1902)
verify_code = dic['pic_str']

# 向页面中填入用户名, 密码, 验证码
web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys("15217277444")
web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys("123456")
web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(verify_code)

time.sleep(5)

# 点击登录
web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()
