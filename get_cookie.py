#! /user/bin.python
# -*- coding:UTF-8 -*-


import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


def get_cookies():
    options = webdriver.ChromeOptions()
    location = r"C:\Program Files\chrome-win\chrome.exe"
    options.binary_location = location
    s = Service(r"C:\Program Files\chrome-win\chromedriver.exe")
    chrome = webdriver.Chrome(service=s, options=options)
    driver = chrome
    driver.set_page_load_timeout(5)
    driver.get("https://www.cnki.net/")
    action = ActionChains(driver)

    time.sleep(10)  # 进行登录
    dictCookies = driver.get_cookies()
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    with open('cnki.cookie', 'w') as f:
        f.write(jsonCookies)
    print('cookie saved success')


if __name__ == "__main__":
    get_cookies()
