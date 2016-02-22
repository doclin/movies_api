#coding=utf8

from bs4 import BeautifulSoup
import requests
import re


class MeituanMovie(object):
    """
    pass
    """
    def __init__(self):
        self.time_out = 2
        self.connection_error_message = 'meituan crash'

    def get_movie_list(self,url,name_list,result):
        try:
            r = requests.get(url)
        except:
            return self.connection_error_message

        soup = BeautifulSoup(r.text)
        meituan_div = soup.find_all('div', class_='movie-cell')
        for i in meituan_div:
            a = i.find_all('a')
            name = a[0]['title']
            meituan_movie_href = a[0]['href']
            meituan_movie_id = re.search(r'\d+', meituan_movie_href).group()

            if name not in name_list:
                name_list.append(name)
                result.append({
                    'movie_name': name,
                    'meituan_movie_id': meituan_movie_id,
                })  
            else:
                index = name_list.index(name)   
                result[index]['meituan_movie_id'] = meituan_movie_id

    def get_district_list(self,url,name_list,result):
        try:
            r = requests.get(url)
        except:
            return self.connection_error_message

        soup = BeautifulSoup(r.text)
        ul = soup.find_all('ul', class_='inline-block-list')
        #ul[2].decompose()
        #ul[0].decompose()
        a = ul[1].find_all('a')
        for i in a:
            distric_name = i.get_text()
            meituan_district_href = i['href']

            if distric_name not in name_list:
                name_list.append(distric_name)
                result.append({
                    'distric_name': distric_name,
                    'meituan_district_href': meituan_district_href,
                })      
            else:
                index = name_list.index(distric_name)
                result[index]['meituan_district_href'] = meituan_district_href

    def get_cinema_list(self,url,name_list,result):
        try:
            r = requests.get(url)
        except:
            return self.connection_error_message
        soup = BeautifulSoup(r.text)
        div = soup.find_all('div', id='J-brand-filter')
        li = div[0].find_all('li')
        for i in li:
            a = i.find_all('a')
            meituan_cinema_href = a[0]['href']
            cinema_name = a[0].get_text()

            if cinema_name not in name_list: 
                name_list.append(cinema_name)
                result.append({
                    'cinema_name':cinema_name,
                    'meituan_cinema_href':meituan_cinema_href,
                })      
            else:
                index = name_list.index(cinema_name)
                result[index]['meituan_cinema_href'] = meituan_cinema_href

    def get_price_list(self,url,name_list,result):
        pass
        
