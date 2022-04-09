### 项目小记  
一些selenium语法的笔记  
由于Selenium库的更新，现在只能用语法：`find_element(by=By.XPATH, value="//a[@class='xxxx']")`  
  
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
