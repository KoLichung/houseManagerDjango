from celery import shared_task
import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import os
from django.db.models import Q
from modelCore.models import User, HouseCase


import environ

ROOT_DIR = (
    environ.Path(__file__) - 1
)
env = environ.Env()
env.read_env(str(ROOT_DIR.path(".env")))

def crawl_manager_cases_by_requests(user, url):
    # url = 'https://www.591.com.tw/broker24177-sale'
    sale_url = f'{url}-sale'
    print(sale_url)

    # from seleniumApp.tasks import *
    # crawl_manager_cases_by_requests('https://www.591.com.tw/broker37081')

    # payload = {'api_key': env('scraper_key'), 'url': url}
    payload = {'api_key': 'f23a160f9e3ca319f97bd613b2fa047f', 'url': url}
    resp = requests.get('http://api.scraperapi.com', params=payload)

    soup = BeautifulSoup(resp.text, 'html.parser')

    # print(soup)

    nav = soup.find('div',{'id':'head-nav'})
    li = nav.find('li',{'data-stat':'shop-detail-sale'})
    total_case_number= li.find('span',{'class':'ft_13'}).getText().replace('(', '').replace(')', '')
    print('總案件數' + total_case_number)

    integer = int(total_case_number) // 10
    print('總案件數 // 10 = ',integer, '(整數)')
    remainder = int(total_case_number) % 10
    print('總案件數 % 10 = ',remainder, '(餘數)')
    
    # 如果餘數是 0
    # 頁數 = 商數  
    # 如果餘數非 0
    # 頁數 = 商數 + 1
    if remainder == 0:
        total_page_number = integer
    else:
        total_page_number = integer + 1 
    print('總頁數' + str(total_page_number))

    shop_id = url.replace('https://www.591.com.tw/broker','')
    print('shop id: ' + shop_id)

    # cases_url = f'https://www.591.com.tw/index.php?firstRow=10&totalRows=18&shop_id=37081&type=2&m=&o=12&module=shop&action=house'
    # payload = {'api_key': 'f23a160f9e3ca319f97bd613b2fa047f', 'url': cases_url}
    # cases_resp = requests.get('http://api.scraperapi.com', params=payload)
    # cases_soup = BeautifulSoup(cases_resp.text, 'html.parser')
    # print(cases_soup)

    i = 0
    # i 小於頁數
    while i < total_page_number:
        print(f'==第 {i+1} 頁==')
        cases_url = f'https://www.591.com.tw/index.php?firstRow={i}0&totalRows={total_case_number}&shop_id={shop_id}&type=2&m=&o=12&module=shop&action=house'
        payload = {'api_key': 'f23a160f9e3ca319f97bd613b2fa047f', 'url': cases_url}
        cases_resp = requests.get('http://api.scraperapi.com', params=payload)
        cases_soup = BeautifulSoup(cases_resp.text, 'html.parser')
        # print(cases_soup)
        lis = cases_soup.find(id='photolist').find(id='photolist').find_all('li')

        for li in lis:
            try:
                imageLink = li.find("div", {"class": "photo"}).find('a').find('img')['src']
                title = li.find("div", {"class": "details"}).find('h3').find('span').find('a').find('strong').getText()
                county = li.find("div", {"class": "details"}).find('p').find_all('a')[0].getText()
                city = li.find("div", {"class": "details"}).find('p').find_all('a')[1].getText()
                type = li.find("div", {"class": "details"}).find('p',{"class":"l3"}).find('span',{"class":"kind"}).getText().replace('，', '')
                units = li.find("div", {"class": "area"}).getText()
                price = li.find("div", {"class": "prices"}).find("p", {"class": "price"}).getText()
                linkPid = li['id'].replace('zid', '')
                caseLink = f"https://sale.591.com.tw/home/house/detail/2/{linkPid}.html"
                
                print('==========')
                print(imageLink)
                print(title)
                print(county, city)
                print(type)
                print(units)
                print(price)
                print(caseLink)

                # server 有此筆資料, 則不動
                # server 沒這個資料, 則增加
                # !!! server 有這個資料, 但 list 沒這個資料, 則刪除~ => 還沒做

                if HouseCase.objects.filter(case_link=caseLink, user=user).count() == 0:
                    houseCase = HouseCase()
                    houseCase.user = user
                    houseCase.title = title
                    houseCase.address = county + city
                    houseCase.type = type
                    houseCase.units = units
                    houseCase.price = price
                    houseCase.image = imageLink
                    houseCase.case_link = caseLink
                    houseCase.shop_id = shop_id
                    houseCase.save()

            except Exception as e:
                print(e)

        i = i + 1


def assign_crawl_manager_tasks():
    users = User.objects.all()
    for user in users:
        if user.page_link != None and user.company == '':
            crawl_manager_data.delay(user.id)

@shared_task
def crawl_manager_data(user_id):
    user = User.objects.get(id=user_id)
    print(f'{user.id} {user.name} {user.page_link}')

    url = user.page_link
    payload = {'api_key': '7e4c75f026434078700eb374b9456d12', 'url': url}
    resp = requests.get('http://api.scraperapi.com', params=payload)

    # resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    detail = soup.find("span", {"class": "details"})
    lis = detail.find_all('li')

    user.serve_time = lis[0].text.replace('從業年限：','')
    user.company = lis[1].text.replace('就職公司：','')
    user.phone = lis[2].text.replace('行動電話：','').replace('-','')
    user.serve_place = lis[3].text.replace('服務區域：','')
    user.email = lis[4].text.replace('E-mail：','')

    detail_info = soup.find("ul", {"class": "details-info"})
    lis = detail_info.find_all('li')

    user.familiar_complex = lis[0].text.replace('熟悉社區：','')
    user.good_at = lis[1].text.replace('業務特長：','')

    user.save()

def export_managers_to_csv():
    PWD = os.path.dirname(os.path.realpath(__file__ )) 
    path = os.path.join(PWD, "managers.csv")

    f = open(path, 'w')
    writer = csv.writer(f)
    writer.writerow(['name','phone','email','serve_place','company','serve_time','familiar_complex','good_at'])

    users = User.objects.filter(~Q(company='')).order_by('id').values_list('name','phone','email','serve_place','company','serve_time','familiar_complex','good_at')
    for user in users:
        writer.writerow(user)

