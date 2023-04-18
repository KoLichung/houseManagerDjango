from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from bs4 import BeautifulSoup

from modelCore.models import User, HouseCase

# def crawl_managers():
#     driver = webdriver.Chrome()
#     driver.get("https://sale.591.com.tw/saleBroker.html") 

#     # user = User.objects.all().first()
#     # user.name = 'user0Test'
#     # user.save()

#     driver.find_element(By.CSS_SELECTOR, '#regionSh > b').click()
#     # 台北市 新竹市 新竹縣 宜蘭縣 基隆市 桃園市 新北市
#     driver.find_element(By.LINK_TEXT, '新北市').click()
#     # 中正區 大同區 中山區 松山區 大安區 萬華區 信義區 士林區 北投區 內湖區 南港區 文山區 
#     # driver.find_element(By.LINK_TEXT, '文山區').click()
#     driver.find_element(By.LINK_TEXT, '[關閉]').click()
#     time.sleep(random.randint(3,10))

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     lis = soup.find(id='smallList').find_all('li')

#     for li in lis:
#         try:
#             link = li.find('h2').find('a')['href']
#             name = li.find('h2').find('a')['title']
#             print(link)
#             print(name)

#             if User.objects.filter(page_link=link).count()==0:
#                 user = User()
#                 user.name = name
#                 user.page_link = link
#                 user.save()
#         except Exception as e:
#                 print(e)

#     time.sleep(random.randint(3,10))
#     button = driver.find_element(By.CSS_SELECTOR, '.pageNext > span')
#     driver.execute_script("arguments[0].click();", button)
#     time.sleep(random.randint(5,10))

#     i = 0
#     # i 小於頁數
#     while i < 385:
#         print(f'==第 {i+2} 頁==')
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         lis = soup.find(id='smallList').find_all('li')

#         for li in lis:
#             try:
#                 link = li.find('h2').find('a')['href']
#                 name = li.find('h2').find('a')['title']
#                 print(link)
#                 print(name)

#                 if User.objects.filter(page_link=link).count()==0:
#                     user = User()
#                     user.name = name
#                     user.page_link = link
#                     user.save()
#             except Exception as e:
#                 print(e)

#         time.sleep(random.randint(3,10))
#         button = driver.find_element(By.CSS_SELECTOR, '.pageNext > span')
#         driver.execute_script("arguments[0].click();", button)
#         time.sleep(random.randint(5,10))

#         i = i + 1

#     driver.close()

def test_crawl_house_agent_cases(house_agent_url):
    driver = webdriver.Chrome()
    driver.get(house_agent_url) 
    driver.find_element(By.CLASS_NAME, 'house-nav > ul > li').click()
    time.sleep(random.randint(3,10))

    i = 0
    # i 小於頁數
    while i < 4:
        print(f'==第 {i+2} 頁==')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        lis = soup.find(id='photolist').find(id='photolist').find_all('li')

        for li in lis:
            try:
                # from seleniumApp.test import *
                # test_crawl_house_agent_cases("https://www.591.com.tw/broker24177")

                imageLink = li.find("div", {"class": "photo"}).find('a').find('img')['src']
                title = li.find("div", {"class": "details"}).find('h3').find('span').find('a').find('strong').getText()
                county = li.find("div", {"class": "details"}).find('p').find_all('a')[0].getText()
                city = li.find("div", {"class": "details"}).find('p').find_all('a')[1].getText()
                type = li.find("div", {"class": "details"}).find('p',{"class":"l3"}).find('span',{"class":"kind"}).getText().replace('，', '')
                units = li.find("div", {"class": "area"}).getText()
                price = li.find("div", {"class": "prices"}).find("p", {"class": "price"}).getText()

                print(imageLink)
                print(title)
                print(county, city)
                print(type)
                print(units)
                print(price)

                # server 有此筆資料, 則不動
                # server 沒這個資料, 則增加
                # !!! server 有這個資料, 但 list 沒這個資料, 則刪除~ => 還沒做

                if HouseCase.objects.filter(case_link=caseLink).count() == 0:
                    houseCase = HouseCase()
                    houseCase.title = title
                    houseCase.address = county + city
                    houseCase.type = type
                    houseCase.units = units
                    houseCase.price = price
                    houseCase.image = imageLink
                    houseCase.save()

            except Exception as e:
                print(e)

        time.sleep(random.randint(3,10))
        button = driver.find_element(By.CSS_SELECTOR, '.pageNext > span')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(random.randint(5,10))

        i = i + 1

    driver.close()
