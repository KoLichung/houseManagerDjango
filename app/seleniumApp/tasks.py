from celery import shared_task
import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import os
from django.db.models import Q

from modelCore.models import User

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

