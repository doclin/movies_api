#coding=utf8

from bs4 import BeautifulSoup
import requests
import re

from movies_tickets.models import City


class NuomiMovie(object):
    """
    pass
    """
    def __init__(self):
        self.time_out = 2
        self.connection_error_message = 'nuomi crash'

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
                junk = u'\uff1a'
                name = name.replace(junk, '')
                name = name.replace(':', '')
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

    def get_cinema_list(self,url,name_list,result,city):
        try:
            r = requests.get(url,timeout=self.time_out)
        except:
            return self.connection_error_message

        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        div = soup.find_all('div', class_='cinema-info clearfix')
        junk_left = u'\uff08'
        junk_right = u'\uff09'

        for i in div:
            data = i['data-cinema']
            nuomi_cinema_id = re.search(r'(?<=uid":").*(?=","lowe)', data).group()
            h3 = i.find('h3', class_='cib-name')
            text = h3.get_text()
            
            cinema_name = re.search(r'\S+', text).group()
            cinema_name = cinema_name.replace('国际', '')
            cinema_name = cinema_name.replace(city, '')
            cinema_name = cinema_name.replace(junk_left, '')
            cinema_name = cinema_name.replace(junk_right, '')
            cinema_name = cinema_name.replace('(', '')
            cinema_name = cinema_name.replace(')', '')
            cinema_name = cinema_name.replace('-', '')

            if cinema_name not in name_list:
                name_list.append(cinema_name)
                result.append({
                    'cinema_name': cinema_name,
                    'nuomi_cinema_id': nuomi_cinema_id,
                })
            else:
                index = name_list.index(cinema_name)
                result[index]['nuomi_cinema_id'] = nuomi_cinema_id

    def get_price_list(self,url,start_time_list,result):
        try:
            r = requests.get(url, timeout=self.time_out)
        except:
            return self.connection_error_message

        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        div = soup.find('div', class_='table')
        tr = div.find_all('tr')
        for i in tr:
            td = i.find_all('td')
            end_time_text = td[0].span.get_text()
            end_time = re.search(r'\d+:\d+', end_time_text).group()
            td[0].span.decompose()
            start_time_text = td[0].get_text()
            start_time = re.search(r'\S+', start_time_text).group()
            price_text = td[3].span.get_text()
            nuomi_now_price = re.search(r'\d+', price_text).group()

            if start_time not in start_time_list:
                start_time_list.append(start_time)
                result.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'nuomi_now_price': nuomi_now_price,
                })
            else:
                index = start_time_list.index(start_time)
                result[index]['nuomi_now_price'] = nuomi_now_price

    def get_city_list(self, url):
        try:
            r = requests.get(url, timeout=self.time_out)
        except:
            return self.connection_error_message   
                 
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text)
        li = soup.find_all('li', class_='city-list clearfix')
        for i in li:
            a = i.find_all('a')
            for j in a:
                name_text = j.get_text()
                name = re.search(r'\S+', name_text).group()
                href = j['href']
                nuomi_city_id = re.search(r'(?<=http://)\w+', href).group()
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
            



        



