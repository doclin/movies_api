#coding=utf8

from bs4 import BeautifulSoup
import requests
import re

from PIL import Image,ImageStat
from StringIO import StringIO

from movies_api.celery import app

MEITUAN_TIME_OUT = 3


#美团电影列表
@app.task(bind=True)
def meituan_get_movie_list(self, url):
    r = requests.get(url, timeout=MEITUAN_TIME_OUT)
    soup = BeautifulSoup(r.text, "html.parser")
    meituan_div = soup.find_all('div', class_='movie-cell')
    result = []
    for i in meituan_div:
        a = i.find_all('a')
        name = a[0]['title']
        junk = u'\uff1a'
        name = name.replace(junk, '')
        name = name.replace(':', '')
        meituan_movie_href = a[0]['href']
        meituan_movie_id = re.search(r'\d+', meituan_movie_href).group()
        result.append({
            'movie_name': name,
            'meituan_movie_id': meituan_movie_id,
            'nuomi_movie_id': '',
            'taobao_movie_id': '',
        })
    return result

#美团行政区列表
@app.task(bind=True)
def meituan_get_district_list(self, url):
    r = requests.get(url, timeout=MEITUAN_TIME_OUT)
    soup = BeautifulSoup(r.text, "html.parser")
    ul = soup.find_all('ul', class_='inline-block-list')
    a = ul[1].find_all('a')
    result = []
    for i in a:
        distric_name = i.get_text()
        meituan_district_href = i['href']
        meituan_district_id = re.search(r'[a-z]+(?=/all)', meituan_district_href).group()
        #去除‘全部’，‘地铁附近’两类
        if meituan_district_id == 'all' or meituan_district_id == 'subway':
            continue
        result.append({
            'district_name': distric_name,
            'meituan_district_id': meituan_district_id,
            'nuomi_district_id': '',
            'taobao_district_id': '',
        })
    return result

#美团电影院列表
@app.task(bind=True)
def meituan_get_cinema_list(self, url, city=u'武汉'):
    r = requests.get(url, timeout=MEITUAN_TIME_OUT)
    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find_all('div', class_='J-cinema-item cinema-item cf')
    junk_left = u'\uff08'
    junk_right = u'\uff09'
    result = []
    for i in div:
        h4 = i.find('h4')
        a = h4.find('a')
        meituan_cinema_href = a['href']
        meituan_cinema_id = re.search(r'(?<=/shop/)\d+', meituan_cinema_href).group()
        #统一各网站电影名称
        cinema_name = a.get_text()
        cinema_name = cinema_name.replace(u'国际', '')
        cinema_name = cinema_name.replace(city, '')
        cinema_name = cinema_name.replace(junk_left, '')
        cinema_name = cinema_name.replace(junk_right, '')
        cinema_name = cinema_name.replace('(', '')
        cinema_name = cinema_name.replace(')', '')
        cinema_name = cinema_name.replace('-', '')
        result.append({
            'cinema_name': cinema_name,
            'meituan_cinema_id': meituan_cinema_id,
            'nuomi_cinema_id': '',
            'taobao_cinema_id': '',
        })
    return result

#美团价格列表
@app.task(bind=True)
def meituan_get_price_list(self, url):
    r = requests.get(url,timeout=MEITUAN_TIME_OUT)
    #不同数字像素和列表
    sum_list = [6647, 3631, 6680, 6137, 5955, 6603, 7381, 4637, 7431, 7304, 575]
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find('table',class_='time-table time-table--current')
    tr = table.find_all('tr')
    result = []
    for i in tr[1:]:
        td = i.find_all('td')
        time = td[0]
        span = time.find_all('span')
        start_time = span[0].get_text()
        end_time = span[1].get_text()
        price_td = td[3]
        div = price_td.find_all('div')
        try:
            i_tag = div[1].find_all('i')
            i_tag = i_tag[:-1]
        except:
            i_tag = div[0].find_all('i')
        meituan_now_price = ''
        #因一次请求中图像可能为同一张，所以以此简化流程
        fixed_add = i_tag[0]['style']
        fixed_add = re.search(r'//s0\.mei.*(?=\);)', fixed_add).group()
        fixed_url = 'http:' + fixed_add
        img_request = requests.get(fixed_url, timeout=MEITUAN_TIME_OUT)
        img = Image.open(StringIO(img_request.content))
        #识别图像
        for j in i_tag:
            style = j['style']
            img_add = re.search(r'//s0\.mei.*(?=\);)', style).group()
            position = re.search(r'(?<=position:).*', style).group()
            position = re.findall(r'\d+', position)
            x_position = int(position[0])
            y_position = int(position[1])
            box = (x_position, y_position, x_position+7, y_position+13)
            if img_add != fixed_add:
                img_url = 'http:' + img_add
                j_request = requests.get(img_url, timeout=MEITUAN_TIME_OUT)
                j_img = Image.open(StringIO(j_request.content))
                img_result = j_img.crop(box)
                result_sta = ImageStat.Stat(img_result)
            else:
                img_result = img.crop(box)
                result_sta = ImageStat.Stat(img_result)
            #与列表比较
            img_sum = int((result_sta.sum)[3])
            try:
                num = sum_list.index(img_sum)
                num_str = str(num)
                meituan_now_price = meituan_now_price + num_str
            except:
                num_str = '.'
                meituan_now_price = meituan_now_price + num_str
        result.append({
            'start_time': start_time,
            'end_time': end_time,
            'meituan_now_price': meituan_now_price,
            'nuomi_now_price': '',
            'taobao_now_price': '',
        })
    return result

#美团城市列表
@app.task(bind=True)
def meituan_get_city_list(self, url):
    from movies_tickets.models import City
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    ol = soup.find_all('ol', class_='hasallcity')
    li = ol[0].find_all('li')
    for i in li:
        a = i.find_all('a')
        for j in a:
            href = j['href']
            meituan_city_id = re.search(r'(?<=://).*(?=\.m)', href).group()
            name = j.get_text()
            first_char = i['id'][-1]
            city = City.objects.filter(city_name=name)
            if city.exists():
                city.update(meituan_city_id=meituan_city_id)
            else:
                City.objects.create(
                    city_name=name,
                    first_char=first_char,
                    meituan_city_id=meituan_city_id,
                )

#美团城市列表-不存入数据库，返回作测试用
@app.task(bind=True)
def meituan_get_city_list_without_saving(self, url):
    result = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    ol = soup.find_all('ol', class_='hasallcity')
    li = ol[0].find_all('li')
    for i in li:
        a = i.find_all('a')
        for j in a:
            href = j['href']
            meituan_city_id = re.search(r'(?<=://).*(?=\.m)', href).group()
            name = j.get_text()
            first_char = i['id'][-1]
            result.append({
                'meituan_city_id': meituan_city_id,
                'city_name': name,
                'first_char': first_char,
            })
    return result
