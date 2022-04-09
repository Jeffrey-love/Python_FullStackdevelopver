## 项目简介  
  实现某题库后台管理系统的批量化操作，执行条数三万多条，网页自动化操作可以达到一秒一条，并且可多线程操作，效率提高几十倍。  
  主要操作有登录后台，寻找到题库位置，挨个点击每一道题，找到里面的iframe框架，进行内容的修改；修改完后返回刚才的题库页面继续进行下一题的修改。并且支持自动翻页，错误反馈，能够验证此题是否需要修改，避免进行额外的浪费时间的操作。


### 项目小记  
一些selenium语法的笔记  
由于Selenium库的更新，现在只能用语法：`find_element(by=By.XPATH, value="//a[@class='xxxx']")`  
  
隐性等待时间
```python
  # 设置隐性等待时间，即接收到完整Response后，所有操作最多等待0.5s（比如找元素的操作）
  driver.implicitly_wait(0.5)
```
  
涉及到iframe框架，最好用到：  
```python
  iframe = driver.find_element(by=By.ID, value='ueditor_1')
  driver.switch_to.frame(iframe)
```
来切换进iframe框架，否则无法选定其中的标签  
当然操作完iframe内的东西不要忘记切出：  
`driver.switch_to.default_content()`  
  
如果用到了键盘操作，有两种情况：  
1. 第一种，直接对某个标签进行键盘操作
`driver.find_element(by=By.CSS_SELECTOR, value="td").send_keys(Keys.CONTROL, 'a')`  
但是一次只能执行一个键盘操作  
2. 第二种，前面有动作执行，不需要选择标签，直接用键盘操作  
此时语句要有所不同，如果直接send_keys将无法执行“按住ctrl”之类的操作，如下进行全选：  
`ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()`
