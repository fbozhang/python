# -*- coding:utf-8 -*-
# @Time : 2022/4/28 21:09
# @Author: fbz
# @File : bilibili_login.py


from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from chaojiying import Chaojiying_Client
import time

# 初始化超级鹰
chaojiying = Chaojiying_Client('15217277444', '123456', '932709')

web = Chrome()


def main():
    web.get("https://www.bilibili.com/")
    time.sleep(2)

    # 点击登录
    web.find_element(by=By.XPATH, value='//*[@id="i_cecream"]/div[1]/div[1]/ul[2]/li[1]/li/div[1]/div').click()
    time.sleep(2)
    web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/div[3]/div[2]/div[1]/input').send_keys("123")
    web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/div[3]/div[2]/div[2]/div[1]/input').send_keys("123")
    time.sleep(1)
    web.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/div[3]/div[3]/div[2]').click()
    time.sleep(2)
    # 处理验证码
    img_element = web.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div[6]/div/div/div[2]/div[1]/div/div[2]/img')

    # 用超级鹰去识别验证码
    dic = chaojiying.PostPic(img_element.screenshot_as_png, 9004)
    result = dic['pic_str']
    print(result)


if __name__ == '__main__':
    main()
