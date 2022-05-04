#! /user/bin.python
# -*- coding:UTF-8 -*-
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import configparser
import os
# import sys


def getConfig(section, key):
    config = configparser.ConfigParser()
    a = os.path.split(os.path.realpath(__file__))
    path = 'data.conf'
    config.read(path, encoding="utf-8")
    return config.get(section, key)


def click_html(driver):
    htmlicon = driver.find_element(by=By.XPATH,
                                   value="//div[@id='edui4_body']/div[@class='edui-box edui-icon edui-default']")
    htmlicon.click()
    return True


# def check(url):
#     try:
#         resp = requests.get(url=url, timeout=5)
#         stat = resp.status_code
#         if stat == 404:
#             return stat
#         # elif len(resp.content) == 621:
#             # 域名暂未生效的网页长度为621
#             # return False
#         else:
#             return stat
#     except:
#         return False
def check(url):
    # resp = requests.get(url=url, timeout=5)
    resp = requests.get(url=url, timeout=5)  # 你需要的网址
    time.sleep(0.5)
    stat = resp.status_code
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    return stat


def func(domain_url):
    options = webdriver.ChromeOptions()
    # 这里设置不弹出浏览器
    options.add_argument("headless")
    # 配置chromemium的地址，这里要改成自己电脑中chrome-win下chrome.exe的路径↓↓↓↓↓
    # 这个路径不能太长，否则会报错，建议放在C盘下Program Files目录
    location = r"C:\Program Files\chrome-win\chrome.exe"
    options.binary_location = location
    # 配置chromedriver路径，放在程序同目录下即可
    s = Service(r"F:\study\Programming\Python\PythonCode\CY_Exec\chromedriver.exe")
    # 驱动chrome程序
    chrome = webdriver.Chrome(service=s, options=options)
    driver = chrome
    # 设置隐形等待时间，即接收到完整Response后，所有操作最多等待0.5s（比如找元素的操作）
    driver.implicitly_wait(0.5)
    # 访问网址
    driver.get("https://phpinfo.me/domain")
    # action = ActionChains(driver)

    # ######
    # domain_url = getConfig("data", "url")
    # ######

    driver.find_element(by=By.XPATH, value="//input[@id='domain']").send_keys(domain_url)
    start = driver.find_element(by=By.XPATH, value="//button")
    start.click()
    print("信息搜集中……")
    time.sleep(10)
    ips = driver.find_element(by=By.XPATH, value="//div[@id='info']").text
    elem_list = ips.split('\n')
    i = 0
    for item in elem_list:
        elem_list[i] = item[5:]
        # ip_list[i] = ip_list[i].split('-')
        i += 1
    url_list = list()
    ip_list = list()
    for item in elem_list:
        split = item.find('-')
        url_list.append("http://" + item[:split])
        ip_list.append(item[split + 1:])

    for url, ip in zip(url_list, ip_list):
        resp = check(url)
        if resp == 0:
            continue
        else:
            print(str(resp) + " --- " + url + " -- " + ip)
    print("扫描完毕！")
    # time.sleep(20)
    # 程序结束，释放内存
    driver.quit()

    return True


def main():
    try:
        domain_url = input("输入域名网址:")
        func(domain_url)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
