#coding=utf8

from bs4 import BeautifulSoup
import requests
import re

from movies_tickets.models import City


class TaobaoMovie(object):
    """
    pass
    """
    def __init__(self):
        self.time_out = 2
        self.connection_error_message = 'taobao crash'

    def get_movie_list(self,url,name_list,result):
        try:
            r = requests.get(url, timeout=self.time_out)
        except:
            return self.connection_error_message

        soup = BeautifulSoup(r.text)
        junk = soup.find_all('div', class_='tab-movie-list')
        junk[1].decompose()
        taobao_div = soup.find_all('div', class_='movie-card-wrap')
        for i in taobao_div:
            span = i.find_all('span', class_='bt-l')
            name = span[0].get_text()
            junk = u'\uff1a'
            name = name.replace(junk, '')
            name = name.replace(':', '')
            a = i.find_all('a')
            taobao_movie_href = a[0]['href']
            taobao_movie_id = re.search(r'(?<=showId=)\d+', taobao_movie_href).group()

            if name not in name_list:
                name_list.append(name)
                result.append({
                    'name': name,
                    'taobao_movie_id': taobao_movie_id,
                })
            else:
                index = name_list.index(name)
                result[index]['taobao_movie_id'] = taobao_movie_id

    def get_district_list(self,url,name_list,result):
        try:
            r = requests.get(url, timeout=self.time_out)
        except:
            return self.connection_error_message

        soup = BeautifulSoup(r.text)
        ul = soup.find_all('ul', class_='filter-select')
        li = ul[0].find_all('li')
        #li[2].decompose()
        #li[1].decompose()
        a = li[0].find_all('a')
        for i in a[1:]:
            #taobao_district_href = i['data-param']
            distric_name = i.get_text()
            taobao_district_id = distric_name

            if distric_name not in name_list:
                name_list.append(distric_name)
                result.append({
                    'distric_name': distric_name,
                    'taobao_district_id': taobao_district_id,
                })
            else:
                index = name_list.index(distric_name)
                result[index]['taobao_district_id'] = unicode(taobao_district_id)

    def get_cinema_list(self,url,name_list,result,city):
        try:
            r = requests.get(url, timeout=self.time_out)
        except:
            return self.connection_error_message

        soup = BeautifulSoup(r.text)
        div = soup.find_all('div', class_='select-tags')
        a = div[1].find_all('a')
        junk_left = u'\uff08'
        junk_right = u'\uff09'

        for i in a:
            cinema_name = i.get_text()
            cinema_name = cinema_name.replace('国际', '')
            cinema_name = cinema_name.replace(city, '')
            cinema_name = cinema_name.replace(junk_left, '')
            cinema_name = cinema_name.replace(junk_right, '')
            cinema_name = cinema_name.replace('(', '')
            cinema_name = cinema_name.replace(')', '')
            cinema_name = cinema_name.replace('-', '')
            taobao_cinema_href = i['data-param']
            taobao_cinema_id = re.search(r'(?<=cinemaId=)\d+', taobao_cinema_href).group()

            if cinema_name not in name_list:
                name_list.append(cinema_name)
                result.append({
                    'cinema_name': cinema_name,
                    'taobao_cinema_id': taobao_cinema_id,
                })
            else:
                index = name_list.index(cinema_name)
                result[index]['taobao_cinema_id'] = taobao_cinema_id    

    def get_price_list(self,url,start_time_list,result):
        try:
            r = requests.get(url, timeout=self.time_out)
        except:
            return self.connection_error_message

        soup = BeautifulSoup(r.text)
        thead = soup.find_all('thead')
        thead[0].decompose()
        tr = soup.find_all('tr')
        for i in tr:
            td = i.find_all('td')
            em = td[0].find_all('em')
            start_time = em[0].get_text()
            em[0].decompose()
            end_time_text = td[0].get_text()
            end_time = re.search(r'\d+:\d+', end_time_text).group()
            now_price_text = td[4].em.get_text()
            now_price = re.match(r'^\d+', now_price_text).group()

            if start_time not in start_time_list:
                start_time_list.append(start_time)
                result.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'taobao_now_price': now_price,
                })
            else:
                index = start_time_list.index(start_time)
                result[index]['taobao_now_price'] = now_price

    def get_city_list(self, url):
        try:
            r = requests.get(url)
        except:
            return self.connection_error_message

        info = re.findall(r'"id":.*?pinYin":"\w?', r.text)
        for i in info:
            taobao_city_id = re.search(r'(?<="cityCode":)\d+', i).group()
            name = re.search(r'(?<="regionName":").*?(?=")', i).group()
            first_char = i[-1]

            city = City.objects.filter(city_name=name)
            if city.exists():
                city.update(taobao_city_id=taobao_city_id)
            else:
                City.objects.create(
                    city_name=name,
                    first_char=first_char,
                    taobao_city_id=taobao_city_id
                )



        




