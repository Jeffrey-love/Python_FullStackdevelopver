#! /user/bin.python
# -*- coding:UTF-8 -*-


import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def write_by_csv(data):
    """
    写入csv文件操作
    """
    with open('data.csv', 'a', newline='') as csvfile:
        csvfile = csv.writer(csvfile)
        csvfile.writerows(data)


def read_by_csv():
    """
    读取csv文件的数据
    """
    data1 = []
    with open('data.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for line in reader:
            # 转化为元祖，存入列表中
            data2 = (line[0], line[1], line[2], line[3], line[4], line[5], line[6])
            data1.append(data2)
    return data1


def spider(driver, action):
    """
    爬虫主函数，分别爬取此页所有条目的各项信息
    """
    time.sleep(1.5)
    # 设置休眠时间，等待网页完全加载完成，否则缺少必要元素，导致运行出错
    data = read_by_csv()
    data_add = []
    for i in range(1, 11):      # i决定每页爬取多少条 ##############
        # 爬取题目
        title_value = "//tr[{}]/td[2]/a[1]".format(str(i))
        title = driver.find_element(by=By.XPATH, value=title_value)
        title = title.text

        # 爬取作者，因为不止一个作者，所以需要用到循环，并且判断是否取完所有作者
        names = ''
        for j in range(1, 10):
            name_value = "//tr[{}]/td[3]/a[{}]".format(str(i), str(j))
            # 不能用if，因为一旦找不到元素就会终止爬虫程序，所以要用try
            try:
                name = driver.find_element(by=By.XPATH, value=name_value)
            except:
                break
            name = name.text
            if j == 1:
                names += name
            else:
                names += ',' + name

        # 爬取期刊
        periodical_value = "//tr[{}]/td[4]/a[1]".format(str(i))
        periodical = driver.find_element(by=By.XPATH, value=periodical_value)
        periodical = periodical.text

        # 爬取时间
        time_value = "//tbody/tr[{}]/td[5]".format(str(i))
        publish_time = driver.find_element(by=By.XPATH, value=time_value)
        publish_time = publish_time.text

        # 点击每一条论文，进一步爬取信息
        target_value = "//tr[{}]/td[2]/a[1]".format(str(i))
        target = driver.find_element(by=By.XPATH, value=target_value)
        target.click()

        time.sleep(1)
        # 标签页转换
        all_handls = driver.window_handles
        driver.switch_to.window(all_handls[-1])

        # 有的论文点进去不是摘要，而是正文快照，所以分两种情况进行爬取
        try:
            summary_value = "//div/span[@id='ChDivSummary']"
            summary = driver.find_element(by=By.XPATH, value=summary_value)
            summary = summary.text
        except:
            try:
                summary_value = "//div[@class='abstract-text']"
                summary = driver.find_element(by=By.XPATH, value=summary_value)
                summary = summary.text
            except:
                summary = '/'

        # 爬取关键词，同样要多次进行
        keywords = '/'
        for j in range(1, 20):
            try:
                keyword = driver.find_element(by=By.XPATH, value="//p[@class='keywords']/a[{}]".format(j))
            except:
                break
            keyword = keyword.text
            if j == 1:
                keywords = keyword
            else:
                keywords += ',' + keyword

        # 爬取卷号，有些文章没有，所以需要分情况
        try:
            number = driver.find_element(by=By.XPATH, value="//div[@class='top-tip']/span/a[2]")
            number = number.text
        except:
            number = '/'

        # 这里关闭当前标签页
        time.sleep(0.3)
        driver.close()
        time.sleep(0.1)
        driver.switch_to.window(all_handls[0])

        # 去重
        temp = (title, names, keywords, periodical, number, publish_time, summary)
        if temp not in data:
            data_add.append(temp)

    write_by_csv(data_add)


def main():
    """
    主函数，进行浏览器初始化和多页操作
    """
    search = input("输入你要爬取的内容: ")
    options = webdriver.ChromeOptions()
    # 这里调用浏览器驱动，使用的是chrome-win，这样版本固定，便于爬虫
    location = r"C:\Program Files\chrome-win\chrome.exe"
    options.binary_location = location
    s = Service(r"C:\Program Files\chrome-win\chromedriver.exe")
    chrome = webdriver.Chrome(service=s, options=options)
    driver = chrome
    driver.set_page_load_timeout(10)
    driver.get("https://www.cnki.net/")

    # 读取提前保存的cookie
    with open('cnki.cookie', 'r', encoding='utf8') as f:
        list_cookies = json.loads(f.read())
    for cookie in list_cookies:
        cookie_dict = {
            'domain': '.cnki.net',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'path': '/',
            "expires": '',
            'sameSite': 'None',
            'secure': cookie.get('secure')
        }
        driver.add_cookie(cookie_dict)

    driver.get("https://www.cnki.net/")
    action = ActionChains(driver)

    # 这里使用两种方法进行点击，第一种像素定位，第二种xpath元素定位
    action.move_by_offset(350, 220).click().perform()
    action.send_keys(search).perform()
    sousuo = driver.find_element(by=By.XPATH, value="//input[@class='search-btn']")
    action.move_to_element(sousuo).click().perform()

    spider(driver, action)

    # 翻页操作
    while True:
        try:
            # 点击“下一页”
            nextpage = driver.find_element(by=By.XPATH, value="//a[text()='下一页']")
            nextpage.click()
        except Exception as e1:
            # 如果没有下一页，返回报错信息，并退出循环
            print("无法寻找到下一页")
            break
        time.sleep(0.5)
        try:
            # 如果有下一页，再次执行spider
            spider(driver, action)
        except Exception as e2:
            print(e2)
            break
    print("程序运行结束")

    # 退出程序
    driver.quit()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
