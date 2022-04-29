# -*- coding:utf-8 -*-
# @Time : 2022/4/30 0:04
# @Author: fbz
# @File : 12306_login.py

import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 如果拿到程序被识别到了怎么办?(window.navigator.webdriver: true)
option = Options()
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('--disable-blink-features=AutomationControlled')

web = Chrome(options=option)

web.get("https://kyfw.12306.cn/otn/resources/login.html")

time.sleep(2)
web.find_element(by=By.XPATH, value='//*[@id="J-userName"]').send_keys("123456")
web.find_element(by=By.XPATH, value='//*[@id="J-password"]').send_keys("123456")
web.find_element(by=By.XPATH, value='//*[@id="J-login"]').click()
time.sleep(1)

# 拖拽
btn = web.find_element(by=By.XPATH, value='//*[@id="nc_1_n1z"]')
ActionChains(web).drag_and_drop_by_offset(btn, 340, 0).perform()