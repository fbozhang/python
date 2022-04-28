# -*- coding:utf-8 -*-
# @Time : 2022/4/25 21:56
# @Author: fbz
# @File : seleniumTest.py
# 下载谷歌浏览器驱动: https://npm.taobao.org/mirrors/chromedriver/
#  把解压后的浏览器驱动 chromedriver 放在python解释器所在的文件夹

import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 创建浏览器对象
web = Chrome()
# 打开一个网址
web.get("http://lagou.com")

# 找到某个元素, 点击他
# el = web.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[1]/a')     # 老方法已经被摒弃, 会报错: DeprecationWarning: find_element_by_xpath is deprecated. Please use find_element(by=By.XPATH, value=xpath) instead
el = web.find_element(by=By.XPATH, value='//*[@id="changeCityBox"]/ul/li[1]/a')
el.click()  # 点击事件

time.sleep(1)   # 让浏览器缓一会

# 找到输入框, 输入python => 输入回车/点击搜索按钮
web.find_element(by=By.XPATH, value='//*[@id="search_input"]').send_keys("python", Keys.ENTER)
time.sleep(1)

web.find_element(by=By.XPATH, value='//*[@id="jobList"]/div[1]/div[1]/div[1]/div[1]/div[1]/a').click()

# 如何进入到新窗口中进行提取
# 注意, 在selenium的眼中, 新窗口默认是不切换过来的
web.switch_to.window(web.window_handles[-1])    # 选择最后一个窗口

# 在新窗口中提取内容
job_detail = web.find_element(by=By.XPATH, value='//*[@id="job_detail"]/dd[2]/div').text
print(job_detail)

# 关掉子窗口
web.close()
# 变更selenium的窗口视角, 回到原来的窗口中
web.switch_to.window(web.window_handles[-1])
print(web.find_element(by=By.XPATH, value='//*[@id="jobList"]/div[1]/div[1]/div[1]/div[1]/div[1]/a').text)

'''
# 如果页面中遇到了 iframe如何处理
web.get("https://app.movie/index.php/vod/play/id/436178/sid/1/nid/1.html")
# 处理iframe的话, 必须先拿到iframe, 然后切换视角到iframe, 再然后才可以拿数据
web.find_element(by=By.XPATH, value='//*[@id="buffer"]')
web.switch_to.frame("buffer")  # 切换到iframe
print(web.find_element(by=By.XPATH, value='/html/body/table/tbody/tr/td/font/strong').text)
web.switch_to.default_content()  # 切换回原页面
'''