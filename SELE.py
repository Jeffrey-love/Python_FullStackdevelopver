#! /user/bin.python
# -*- coding:UTF-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def click_html(driver):
    htmlicon = driver.find_element(by=By.XPATH,
                                   value="//div[@id='edui4_body']/div[@class='edui-box edui-icon edui-default']")
    htmlicon.click()
    return True


def is_exist(driver, str1):
    # 此函数用于判断页面元素是否存在
    try:
        driver.find_element(by=By.CSS_SELECTOR, value=str1)
    except:
        return False

    return True


def p_exist(driver):
    # 用于判断是否存在<p style……
    driver.switch_to.default_content()
    click_html(driver)
    content = driver.find_element(by=By.XPATH, value="//div[2]/pre[1]/span[@class='cm-tag'][1]")
    print(content.text)
    if content.text == '<p':
        click_html(driver)
        iframe = driver.find_element(by=By.ID, value='ueditor_1')
        driver.switch_to.frame(iframe)
        return True
    else:
        click_html(driver)
        iframe = driver.find_element(by=By.ID, value='ueditor_1')
        driver.switch_to.frame(iframe)
        return False


def editing(driver, action):
    # 此函数用于执行当前页的编辑操作

    # 获取编辑按钮的元素
    bianji = driver.find_elements(by=By.XPATH, value="//a[@class='btn btn-xs btn-info']")
    lent = len(bianji)      # 获取此页上一共有多少条数据（即编辑按钮的个数）
    currenturl = driver.current_url     # 获取当前页的地址
    print("当前页面的url: ", currenturl)
    print('此页一共有: ' + str(lent) + '条数据')
    for i in range(lent):
        print('---开始编辑-----第{}条---->'.format(i + 1))
        bianji[i].click()   # 点击编辑按钮

        # # # # # 执行各种编辑操作
        # 寻找iframe框架，因为'答案解析'的输入框用到了iframe框架，如果不先选择相应的iframe框架，无法锁定到要修改的元素
        iframe = driver.find_element(by=By.ID, value='ueditor_1')
        driver.switch_to.frame(iframe)
        # et2,et3为iframe框架里面可能出现的需要修改的元素
        et0 = "td"
        et2 = "td[class='et2']"
        et3 = "td[class='et3']"
        # 判断是否存在et2,et3这两个元素，经过调试和不完全统计，答案解析中只有这两种元素，元素图片示例见'README'
        # 如果都没有找到
        if is_exist(driver, et3):
            print("收集et3中的内容")
            # 获取et3中元素的内容（全选并复制）
            driver.find_element(by=By.CSS_SELECTOR, value="td[class='et3']").send_keys(Keys.CONTROL, 'a')
            driver.find_element(by=By.CSS_SELECTOR, value="td[class='et3']").send_keys(Keys.CONTROL, 'c')
            print('复制文本')

        elif is_exist(driver, et2):
            print("收集et2中的内容")
            # 获取et2中元素的内容（全选并复制）
            driver.find_element(by=By.CSS_SELECTOR, value="td[class='et2']").send_keys(Keys.CONTROL, 'a')
            driver.find_element(by=By.CSS_SELECTOR, value="td[class='et2']").send_keys(Keys.CONTROL, 'c')
            print('复制文本')

        elif is_exist(driver, et0):
            print("收集et0中的内容")
            # 获取et0中元素的内容（全选并复制）
            driver.find_element(by=By.CSS_SELECTOR, value="td").send_keys(Keys.CONTROL, 'a')
            driver.find_element(by=By.CSS_SELECTOR, value="td").send_keys(Keys.CONTROL, 'c')
            print('复制文本')

        elif p_exist(driver):
            print("收集body中的文本")
            driver.find_element(by=By.CSS_SELECTOR, value="body[class='view']").click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()

        else:
            # 执行回退操作
            print("未找到需要修改的地方，正在回退……")
            driver.back()
            # 回退后要重新获取一次'编辑'元素的位置,否则无法正常运行下一步
            bianji = driver.find_elements(by=By.XPATH, value="//a[@class='btn btn-xs btn-info']")
            continue

        # 从iframe框架移出来
        driver.switch_to.default_content()
        # 获取并点击html小图标
        click_html(driver)
        print('选择html_icom')

        # time.sleep(20)  # 调试用

        # ################
        # 选定输入框
        # 这里用到的原理是，如果包含了et2或et3元素，则可以定位到span元素
        # 将鼠标指针移到span元素的第一个元素，左键点击一次进行选中
        # 再用键盘操作将文本删除并粘贴上剪贴板里的第一条
        # ################
        shurukuang = driver.find_element(by=By.XPATH, value="//div[2]/pre[1]/span[@class='cm-tag'][1]")
        ActionChains(driver).move_to_element(shurukuang).click()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        # 点击提交按钮
        tijiao = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
        tijiao.click()
        # 执行回退操作
        print("修改成功，回退两次")
        driver.back()
        driver.back()
        # 再次获取一次'编辑'元素，否则无法正常执行下一步
        bianji = driver.find_elements(by=By.XPATH, value="//a[@class='btn btn-xs btn-info']")

    return True


def func():
    options = webdriver.ChromeOptions()
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
    # 访问网址:wxform.0527web.com
    driver.get("http://wxform.0527web.com/")
    action = ActionChains(driver)

    # 登录操作,输入账号密码，并且点击登录
    driver.find_element(by=By.NAME, value="username").send_keys('sqhhyy')
    driver.find_element(by=By.NAME, value="password").send_keys('sqhhyy688')
    denglu = driver.find_element(by=By.XPATH, value="//input[@type='submit']")
    denglu.click()
    # 找到'全部应用'的位置，并点击
    yingyong_ul = driver.find_element(by=By.XPATH, value="//div[@class='star-menu']/ul")
    items = yingyong_ul.find_elements(by=By.TAG_NAME, value='li')
    time.sleep(0.5)     # 这里设置0.5s等待时间
    # 因为调试过程中发现如果在页面还没加载出来的时候进行点击操作，会导致右边栏目显示错乱，进而无法进行下一步操作
    # 这里如果还是出错，可以适当延长等待时间
    items[3].click()

    # 点击考试中心
    kaoshi = driver.find_element(by=By.XPATH, value="//div[@class='star-item__name text-over']")
    kaoshi.click()
    # 点击题库管理
    guanli = driver.find_element(by=By.XPATH, value="//span[text()='题库管理']")
    guanli.click()

    time.sleep(10)  # 预留十秒的开始前操作时间进行’筛选操作‘，不需要可以将此行注释掉
    # 执行第一页的编辑操作

    editing(driver, action)

    while True:
        try:
            # 点击“下一页”
            nextpage = driver.find_element(by=By.XPATH, value="//a[text()='下一页»']")
            nextpage.click()
        except Exception as e:
            # 如果没有下一页，返回报错信息，并退出循环
            print("无法寻找到下一页")
            break

        try:
            # 如果有下一页，再次执行“编辑操作”
            editing(driver, action)
        except Exception as e:
            print(e)
            break
    print("程序运行结束")
    time.sleep(10)
    # 程序结束，释放内存
    driver.quit()

    return True


def main():
    try:
        func()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
