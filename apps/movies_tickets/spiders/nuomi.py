#coding=utf8

from bs4 import BeautifulSoup
import requests
import re

class NuomiMovie(object):
    """
    pass
    """
    def __init__(self):
        self.time_out = 2
        self.connection_error_message = 'taobao crash'

    def get_movie_list(self,url,name_list,result):
        try:
            r = requests.get(url,timeout=self.time_out)
        except:
            return self.connection_error_message
        
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        ul = soup.find('ul', class_='clearfix j-sliders')
        li = ul.find_all('li')
        for i in li:
            a = i.find_all('a')
            for j in a:
                name = j['title']
                href = j['href']
                nuomi_movie_id = re.search(r'\d+', href).group()

            if name not in name_list:
                name_list.append(name)
                result.append({
                    'name': name,
                    'nuomi_movie_id': nuomi_movie_id,
                })
            else:
                index = name_list.index(name)
                result[index]['nuomi_movie_id'] = nuomi_movie_id

    def get_district_list(self,url,name_list,result):
        try:
            r = requests.get(url,timeout=self.time_out)
        except:
            return self.connection_error_message

        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        div = soup.find('div', id='j-district-item-wrap')
        span = div.find_all('span')
        for i in span:
            a = i.parent
            i.decompose()
            district_name = a.get_text()
            href = a['href']
            nuomi_district_id = re.search(r'(?<=\d/).*(?=/sub)', href).group()

            if district_name not in name_list:
                name_list.append(district_name)
                result.append({
                    'district_name': district_name,
                    'nuomi_district_id': nuomi_district_id,
                })
            else:
                index = name_list.index(district_name)
                result[index]['nuomi_district_id'] = nuomi_district_id

    def get_cinema_list(self,url,name_list,result):
        try:
            r = requests.get(url,timeout=self.time_out)
        except:
            return self.connection_error_message

        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        div = soup.find_all('div', class_='cinema-info clearfix')
        for i in div:
            data = i['data-cinema']
            nuomi_cinema_id = re.search(r'(?<=uid":").*(?=","lowe)', data).group()
            h3 = i.find('h3', class_='cib-name')
            text = h3.get_text()
            cinema_name = re.search(r'\S+', text).group()

            if cinema_name not in name_list:
                name_list.append(cinema_name)
                result.append({
                    'cinema_name': cinema_name,
                    'nuomi_cinema_id': nuomi_cinema_id,
                })
            else:
                index = name_list.index(cinema_name)
                result[index]['nuomi_cinema_id'] = nuomi_cinema_id



http://hz.nuomi.com/pcindex/main/timetable?cinemaid=37d60a46e6d41f611e1d11c5&mid=9808&needMovieInfo=1&tploption=1&_=1456157781848