#coding=utf8

from bs4 import BeautifulSoup
import requests
import re

from movies_api.celery import app

NUOMI_TIME_OUT = 3

#糯米电影列表
@app.task(bind=True)
def nuomi_get_movie_list(self, url):
    r = requests.get(url,timeout=NUOMI_TIME_OUT)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    ul = soup.find('ul', class_='clearfix j-sliders')
    li = ul.find_all('li')
    result = []
    for i in li:
        a = i.find_all('a')
        for j in a:
            name = j['title']
            junk = u'\uff1a'
            name = name.replace(junk, '')
            name = name.replace(':', '')
            href = j['href']
            nuomi_movie_id = re.search(r'\d+', href).group()

            result.append({
                'movie_name': name,
                'meituan_movie_id': '',
                'nuomi_movie_id': nuomi_movie_id,
                'taobao_movie_id': '',
            })
    return result

#糯米行政区列表
@app.task(bind=True)
def nuomi_get_district_list(self, url):
    r = requests.get(url,timeout=NUOMI_TIME_OUT)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', id='j-district-item-wrap')
    span = div.find_all('span')
    result = []
    for i in span:
        a = i.parent
        i.decompose()
        district_name = a.get_text()
        href = a['href']
        nuomi_district_id = re.search(r'(?<=\d/).*(?=/sub)', href).group()
        result.append({
            'district_name': district_name,
            'meituan_district_id': '',
            'nuomi_district_id': nuomi_district_id,
            'taobao_district_id': '',
        })
    return result

#糯米电影院列表
@app.task(bind=True)
def nuomi_get_cinema_list(self, url, city=u'武汉'):
    r = requests.get(url,timeout=NUOMI_TIME_OUT)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find_all('div', class_='cinema-info clearfix')
    junk_left = u'\uff08'
    junk_right = u'\uff09'
    result = []
    for i in div:
        data = i['data-cinema']
        nuomi_cinema_id = re.search(r'(?<=uid":").*(?=","lowe)', data).group()
        h3 = i.find('h3', class_='cib-name')
        text = h3.get_text()
        cinema_name = re.search(r'\S+', text).group()
        cinema_name = cinema_name.replace(u'国际', '')
        cinema_name = cinema_name.replace(city, '')
        cinema_name = cinema_name.replace(junk_left, '')
        cinema_name = cinema_name.replace(junk_right, '')
        cinema_name = cinema_name.replace('(', '')
        cinema_name = cinema_name.replace(')', '')
        cinema_name = cinema_name.replace('-', '')
        result.append({
            'cinema_name': cinema_name,
            'meituan_cinema_id': '',
            'nuomi_cinema_id': nuomi_cinema_id,
            'taobao_cinema_id': '',
        })
    return result

#糯米价格列表
@app.task(bind=True)
def nuomi_get_price_list(self, url):
    r = requests.get(url, timeout=NUOMI_TIME_OUT)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find('div', class_='table')
    tr = div.find_all('tr')
    result = []
    for i in tr:
        td = i.find_all('td')
        end_time_text = td[0].span.get_text()
        end_time = re.search(r'\d+:\d+', end_time_text).group()
        td[0].span.decompose()
        start_time_text = td[0].get_text()
        start_time = re.search(r'\S+', start_time_text).group()
        price_text = td[3].span.get_text()
        nuomi_now_price = re.search(r'\d+', price_text).group()
        result.append({
            'start_time': start_time,
            'end_time': end_time,
            'meituan_now_price': '',
            'nuomi_now_price': nuomi_now_price,
            'taobao_now_price': '',
        })
    return result

#糯米城市列表
@app.task(bind=True)
def nuomi_get_city_list(self, url):
    from movies_tickets.models import City
    r = requests.get(url, timeout=NUOMI_TIME_OUT)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    li = soup.find_all('li', class_='city-list clearfix')
    for i in li:
        a = i.find_all('a')
        for j in a:
            name_text = j.get_text()
            name = re.search(r'\S+', name_text).group()
            href = j['href']
            nuomi_city_id = re.search(r'(?<=//)\w+', href).group()
            first_char = i.find('span', class_='letter fl').get_text()
            city = City.objects.filter(city_name=name)
            if city.exists():
                city.update(nuomi_city_id=nuomi_city_id)
            else:
                City.objects.create(
                    city_name=name,
                    first_char=first_char,
                    nuomi_city_id=nuomi_city_id,
                )

#糯米城市列表-不存入数据库，返回作测试用
@app.task(bind=True)
def nuomi_get_city_list_without_saving(self, url):
    result = []
    r = requests.get(url, timeout=NUOMI_TIME_OUT)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html.parser")
    li = soup.find_all('li', class_='city-list clearfix')
    for i in li:
        a = i.find_all('a')
        for j in a:
            name_text = j.get_text()
            name = re.search(r'\S+', name_text).group()
            href = j['href']
            nuomi_city_id = re.search(r'(?<=//)\w+', href).group()
            first_char = i.find('span', class_='letter fl').get_text()
            result.append({
                'city_name': name,
                'first_char': first_char,
                'nuomi_city_id': nuomi_city_id,
            })
    return result
