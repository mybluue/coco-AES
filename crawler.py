# coding=gbk

def test():
    import urllib.request

    url = 'http://hsk.blcu.edu.cn/'

    data = urllib.request.urlopen(url).read()

    print(data)


import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import pandas as pd

hsk_url = 'http://hsk.blcu.edu.cn/'

driver = webdriver.Chrome('/home/pyp/D/mywork/group/binshuai/verb-complement/crawler/chromedriver')
driver.get(hsk_url)
driver.implicitly_wait(5)
driver.maximize_window()

print(driver.page_source)

driver.find_element_by_id('input_admin_name').send_keys('mybluue')
driver.find_element_by_id('input_admin_pwd').send_keys('ttt')
verify_num = input('输入验证码：')
driver.find_element_by_id('input_admin_verify').send_keys(verify_num)
driver.find_element_by_id('exec_submit').click()

# 句篇检索
hover_element1 = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/ul[1]/li[4]')
ActionChains(driver).move_to_element(hover_element1).perform()
time.sleep(2)
# 句篇检索 --> 全篇检索
hover_element2 = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/ul[1]/li[4]/dl/dd[3]/a')
ActionChains(driver).move_to_element(hover_element2).click().perform()

# 下拉选择框
s1 = Select(driver.find_element_by_id('zwtm'))
time.sleep(2)
s1.select_by_value('绿色食品与饥饿')

# 点击“检索”
hover_element3 = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[2]/div/div[1]/div[2]/form[3]/div[3]/button')
ActionChains(driver).move_to_element(hover_element3).click().perform()

f = open('绿色食品与饥饿-标注版.txt', 'w')
my_dict = {'id':[], 'essay':[]}

for t in range(103):
    # 获得table的大小
    table1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/table/tbody').text
    header1 = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr').text
    header1 = header1.split(' ')
    all_row = table1.split('\n')

    # 定位并打开表中所有的“标注版”

    for i in range(2,len(all_row)+1):
        try:
            id_locator = '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[%s]/td[%s]'%(i, 1)
            essay_id = driver.find_element_by_xpath(id_locator).text
            biaozhu_locator = '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[%s]/td[%s]/a'%(i, len(header1))
            # biaozhu_locator = '/html/body/div/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr[2]/td[14]/a'
            hover_element4 = driver.find_element_by_xpath(biaozhu_locator)
            ActionChains(driver).move_to_element(hover_element4).click().perform()
            time.sleep(1.5)
            essay_biaozhu = driver.find_element_by_id('text_body').text

            # # /html/body/div[4]/span[1]/a
            # # driver.find_element_by_css_selector('#layui-layer2 > span.layui-layer-setwin > a').click()
            # # # 悬停到关闭按钮
            # hover_element5 = driver.find_element_by_xpath('/html/body/div[4]/span[1]')
            # ActionChains(driver).move_to_element(hover_element5).perform()
            # time.sleep(1.5)
            # # 点击关闭按钮
            # hover_element6 = driver.find_element_by_xpath('/html/body/div[4]/span[1]/a')
            # ActionChains(driver).move_to_element(hover_element6).click().perform()

            # 点击空白处关闭弹窗
            ActionChains(driver).move_by_offset(1,1).click().perform()
            # 存储
            f.writelines(essay_id+'\t'+essay_biaozhu+'\n')
            my_dict['id'].append(essay_id)
            my_dict['essay'].append(essay_biaozhu)
        except:
            queding_element = driver.find_element_by_xpath('/html/body/div[4]/div[3]')
            ActionChains(driver).move_to_element(queding_element).perform()
            time.sleep(1.5)
            queding_element_click = driver.find_element_by_xpath('/html/body/div[4]/div[3]/a')
            ActionChains(driver).move_to_element(queding_element_click).click().perform()

    # 进入下一页
    # NextPage = driver.find_element_by_css_selector("#PageNav > table > tbody > tr > td:nth-child(1) > nav > ul > li:nth-child(13) > a")
    NextPage = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[1]/nav/ul/li[13]/a')
    time.sleep(1.5)
    ActionChains(driver).move_to_element(NextPage).click().perform()
    # driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[2]/div/div/table/tbody/tr/td[1]/nav/ul/li[13]/a').click()

my_df = pd.DataFrame(my_dict)
my_df.to_excel('绿色食品与饥饿-标注版.xlsx', index=False)


