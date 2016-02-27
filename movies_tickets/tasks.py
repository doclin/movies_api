#coding=utf8

import sys, os

from bs4 import BeautifulSoup
import requests
import re

from movies_tickets.models import City
from movies_tickets.spiders.meituan import MeituanMovie
from movies_tickets.spiders.nuomi import NuomiMovie
from movies_tickets.spiders.taobao import TaobaoMovie


reload(sys)
sys.setdefaultencoding('utf8')

class MovieList(object):
    """
    上映电影列表
    """
    def __init__(self,city_id):
        self.city = City.objects.get(id=city_id)
        self.meituan_city_id = self.city.meituan_city_id
        self.nuomi_city_id = self.city.nuomi_city_id 
        self.taobao_city_id = self.city.taobao_city_id 
        
        self.meituan_url = ('http://%s.meituan.com/dianying/zuixindianying' % self.meituan_city_id)
        self.nuomi_url = ('http://%s.nuomi.com/pcindex/main/filmlist?type=1' % self.nuomi_city_id)
        self.taobao_url = ('https://dianying.taobao.com/showList.htm?city=%s' % self.taobao_city_id)

        self.result = []
        self.name_list = []

    def get_movie_list(self):
        if self.meituan_city_id:
            meituan_movie = MeituanMovie()
            meituan_result = meituan_movie.get_movie_list(self.meituan_url)
            for meituan_movie in meituan_result:
                if meituan_movie['movie_name'] not in self.name_list:
                    self.name_list.append(meituan_movie['movie_name'])
                    self.result.append(meituan_movie)
                else:
                    index = self.name_list.index(meituan_movie['movie_name'])
                    self.result[index]['meituan_movie_id'] = meituan_movie['meituan_movie_id']


        if self.nuomi_city_id:
            nuomi_movie = NuomiMovie()
            nuomi_error = nuomi_movie.get_movie_list(self.nuomi_url, self.name_list, self.result)
            if nuomi_error:
                self.result[0].append(nuomi_error)

        if self.taobao_city_id:
            taobao_movie = TaobaoMovie()
            taobao_error = taobao_movie.get_movie_list(self.taobao_url, self.name_list, self.result)
            if taobao_error:
                self.result[0].append(taobao_error)

        return self.result


class DistrictList(object):
    """
    行政区列表
    """
    def __init__(self,city_id,**kwargs):
        self.city = City.objects.get(id=city_id)
        self.meituan_city_id = self.city.meituan_city_id
        self.nuomi_city_id = self.city.nuomi_city_id 
        self.taobao_city_id = self.city.taobao_city_id 

        self.meituan_movie_id = kwargs['meituan_movie_id']
        self.nuomi_movie_id = kwargs['nuomi_movie_id']
        self.taobao_movie_id = kwargs['taobao_movie_id']

        self.meituan_url = ('http://%s.meituan.com/dianying/%s?mtt=1.movie'
                            % (self.meituan_city_id, self.meituan_movie_id))
        self.nuomi_url = ('http://%s.nuomi.com/film/%s'%(self.nuomi_city_id, self.nuomi_movie_id))
        self.taobao_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&city=%s'
                           %(self.taobao_movie_id, self.taobao_city_id))

        self.result = [[]]
        self.name_list = ['']

    def get_district_list(self):
        if self.meituan_city_id and self.meituan_movie_id:
            meituan_movie = MeituanMovie()
            meituan_error = meituan_movie.get_district_list(self.meituan_url, self.name_list, self.result)
            if meituan_error:
                self.result[0].append(meituan_error)

        if self.nuomi_city_id and self.nuomi_movie_id:
            nuomi_movie = NuomiMovie()
            nuomi_error = nuomi_movie.get_district_list(self.nuomi_url, self.name_list, self.result)
            if nuomi_error:
                self.result[0].append(nuomi_error)

        if self.taobao_city_id and self.taobao_movie_id:
            taobao_movie = TaobaoMovie()
            taobao_error = taobao_movie.get_district_list(self.taobao_url, self.name_list, self.result)
            if taobao_error:
                self.result[0].append(taobao_error)

        return self.result


class CinemaList(object):
    """
    影院列表
    """
    def __init__(self,city_id,**kwargs):
        self.city = City.objects.get(id=city_id)
        self.meituan_city_id = self.city.meituan_city_id
        self.nuomi_city_id = self.city.nuomi_city_id 
        self.taobao_city_id = self.city.taobao_city_id 
        self.city_byte = self.city.city_name.decode('utf-8')

        self.meituan_movie_id = kwargs['meituan_movie_id']
        self.meituan_district_id = kwargs['meituan_district_id']
        self.nuomi_movie_id = kwargs['nuomi_movie_id']
        self.nuomi_district_id = kwargs['nuomi_district_id']
        self.taobao_movie_id = kwargs['taobao_movie_id']
        self.taobao_district_id = kwargs['taobao_district_id']

        self.meituan_url = ('http://%s.meituan.com/dianying/%s//%s/all?mtt=1.movie'
                            %(self.meituan_city_id, self.meituan_movie_id, self.meituan_district_id))
        self.nuomi_url = ('http://%s.nuomi.com/film/%s/%s/sub0d0/cb0-d10000-s0-o-b1-f0-p1#cinema-nav'
                            %(self.nuomi_city_id, self.nuomi_movie_id, self.nuomi_district_id))
        self.taobao_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&regionName=%s&city=%s'
                            %(self.taobao_movie_id, unicode(self.taobao_district_id), self.taobao_city_id))

        self.result = [[]]
        self.name_list = ['']

    def get_cinema_list(self):
        if self.meituan_district_id:
            meituan_movie = MeituanMovie()
            meituan_error = meituan_movie.get_cinema_list(self.meituan_url, self.name_list, self.result, self.city_byte)
            if meituan_error:
                self.result[0].append(meituan_error)

        if self.nuomi_district_id:
            nuomi_movie = NuomiMovie()
            nuomi_error = nuomi_movie.get_cinema_list(self.nuomi_url, self.name_list, self.result, self.city_byte)
            if nuomi_error:
                self.result[0].append(nuomi_error)

        if self.taobao_district_id:
            taobao_movie = TaobaoMovie()
            taobao_error = taobao_movie.get_cinema_list(self.taobao_url, self.name_list, self.result, self.city_byte)
            if taobao_error:
                self.result[0].append(taobao_error)

        return self.result


class PriceList(object):
    """
    价格列表
    """
    def __init__(self,city_id,**kwargs):
        self.city = City.objects.get(id=city_id)
        self.meituan_city_id = self.city.meituan_city_id
        self.nuomi_city_id = self.city.nuomi_city_id 
        self.taobao_city_id = self.city.taobao_city_id 

        self.meituan_movie_id = kwargs['meituan_movie_id']
        self.meituan_cinema_id = kwargs['meituan_cinema_id']
        self.nuomi_movie_id = kwargs['nuomi_movie_id']
        self.nuomi_cinema_id = kwargs['nuomi_cinema_id']
        self.taobao_movie_id = kwargs['taobao_movie_id']
        self.taobao_cinema_id = kwargs['taobao_cinema_id']

        self.meituan_url = ('http://%s.meituan.com/shop/%s?movieid=%s'
                            %(self.meituan_city_id, self.meituan_cinema_id, self.meituan_movie_id))
        self.nuomi_url = ('http://%s.nuomi.com/pcindex/main/timetable?cinemaid=%s&mid=%s'
                            %(self.nuomi_city_id, self.nuomi_cinema_id, self.nuomi_movie_id))
        self.taobao_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&city=%s&cinemaId=%s'
                            %(self.taobao_movie_id, self.taobao_city_id ,self.taobao_cinema_id))

        self.result = [[]]
        self.start_time_list = ['']

    def get_price_list(self):
        if self.meituan_cinema_id:
            meituan_movie = MeituanMovie()
            meituan_error = meituan_movie.get_price_list(self.meituan_url, self.start_time_list, self.result)
            if meituan_error:
                self.result[0].append(meituan_error)

        if self.nuomi_cinema_id:
            nuomi_movie = NuomiMovie()
            nuomi_error = nuomi_movie.get_price_list(self.nuomi_url, self.start_time_list, self.result)
            if nuomi_error:
                self.result[0].append(nuomi_error)

        if self.taobao_cinema_id:
            taobao_movie = TaobaoMovie()
            taobao_error = taobao_movie.get_price_list(self.taobao_url, self.start_time_list, self.result)
            if taobao_error:
                self.result[0].append(taobao_error)

        return self.result


class CityList(object):
    """
    城市列表
    """
    def __init__(self):
        self.result = []
        self.meituan_url = 'http://www.meituan.com/index/changecity/initiative'
        self.nuomi_url = 'http://www.nuomi.com/pcindex/main/changecity'
        self.taobao_url = 'http://dianying.taobao.com/cityAction.json?activityId&action=cityAction&event_submit_doGetAllRegion=true'

    def update(self):
        meituan_movie = MeituanMovie()
        meituan_error = meituan_movie.get_city_list(self.meituan_url)
        if meituan_error:
            self.result.append(meituan_error)

        nuomi_movie = NuomiMovie()
        nuomi_error = nuomi_movie.get_city_list(self.nuomi_url)
        if nuomi_error:
            self.result.append(nuomi_error)

        taobao_movie = TaobaoMovie()
        taobao_error = taobao_movie.get_city_list(self.taobao_url)
        if taobao_error:
            self.result.append(taobao_error)

        return self.result

































    



        








