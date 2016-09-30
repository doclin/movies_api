#coding=utf8

import sys

from requests import RequestException

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
    def __init__(self, city_id):
        self.city = City.objects.get(id=city_id)
        self.meituan_city_id = self.city.meituan_city_id
        self.nuomi_city_id = self.city.nuomi_city_id 
        self.taobao_city_id = self.city.taobao_city_id

        self.meituan_url = ('http://%s.meituan.com/dianying/zuixindianying' % self.meituan_city_id)
        self.nuomi_url = ('http://%s.nuomi.com/pcindex/main/filmlist?type=1' % self.nuomi_city_id)
        self.taobao_url = ('https://dianying.taobao.com/showList.htm?city=%s' % self.taobao_city_id)

        self.result = [[]]
        self.name_list = ['']

    def get_movie_list(self):
        if self.meituan_city_id:
            meituan_movie = MeituanMovie()
            try:
                meituan_result = meituan_movie.get_movie_list(self.meituan_url)
                for meituan_movie in meituan_result: ####
                    if meituan_movie['movie_name'] not in self.name_list:
                        self.name_list.append(meituan_movie['movie_name'])
                        self.result.append(meituan_movie)
                    else:
                        index = self.name_list.index(meituan_movie['movie_name'])
                        self.result[index]['meituan_movie_id'] = meituan_movie['meituan_movie_id']
            except RequestException: 
                self.result[0].append('meituan connection broken')
            except:
                self.result[0].append('meituan unknown error')                   

        if self.nuomi_city_id:
            nuomi_movie = NuomiMovie()
            try:
                nuomi_result = nuomi_movie.get_movie_list(self.nuomi_url)
                for nuomi_movie in nuomi_result:
                    if nuomi_movie['movie_name'] not in self.name_list:
                        self.name_list.append(nuomi_movie['movie_name'])
                        self.result.append(nuomi_movie)
                    else:
                        index = self.name_list.index(nuomi_movie['movie_name'])
                        self.result[index]['nuomi_movie_id'] = nuomi_movie['nuomi_movie_id']
            except RequestException:
                self.result[0].append('nuomi connection broken')
            except:
                self.result[0].append('nuomi unknown error')

        if self.taobao_city_id:
            taobao_movie = TaobaoMovie()
            try:
                taobao_result = taobao_movie.get_movie_list(self.taobao_url)
                for taobao_movie in taobao_result:
                    if taobao_movie['movie_name'] not in self.name_list:
                        self.name_list.append(taobao_movie['movie_name'])
                        self.result.append(taobao_movie)
                    else:
                        index = self.name_list.index(taobao_movie['movie_name'])
                        self.result[index]['taobao_movie_id'] = taobao_movie['taobao_movie_id']
            except RequestException:
                self.result[0].append('taobao connection broken')
            except:
                self.result[0].append('taobao unknown error')

        return self.result


class DistrictList(object):
    """
    行政区列表
    """
    def __init__(self, city_id, **kwargs):
        self.city = City.objects.get(id=city_id)
        self.meituan_city_id = self.city.meituan_city_id
        self.nuomi_city_id = self.city.nuomi_city_id 
        self.taobao_city_id = self.city.taobao_city_id 

        self.meituan_movie_id = kwargs['meituan_movie_id']
        self.nuomi_movie_id = kwargs['nuomi_movie_id']
        self.taobao_movie_id = kwargs['taobao_movie_id']

        self.meituan_url = ('http://%s.meituan.com/dianying/%s?mtt=1.movie'
                            % (self.meituan_city_id, self.meituan_movie_id))
        self.nuomi_url = ('http://%s.nuomi.com/film/%s'
                          % (self.nuomi_city_id, self.nuomi_movie_id))
        self.taobao_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&city=%s'
                           % (self.taobao_movie_id, self.taobao_city_id))

        self.result = [[]]
        self.name_list = ['']

    def get_district_list(self):
        if self.meituan_city_id and self.meituan_movie_id:
            meituan_movie = MeituanMovie()
            try:
                meituan_result = meituan_movie.get_district_list(self.meituan_url)
                for meituan_district in meituan_result:
                    if meituan_district['district_name'] not in self.name_list:
                        self.name_list.append(meituan_district['district_name'])
                        self.result.append(meituan_district)
                    else:
                        index = self.name_list.index(meituan_district['district_name'])
                        self.result[index]['meituan_district_id'] = meituan_district['meituan_district_id']
            except RequestException:
                self.result[0].append('meituan connection broken')
            except:
                self.result[0].append('meituan unknown error')
                    
        if self.nuomi_city_id and self.nuomi_movie_id:
            nuomi_movie = NuomiMovie()
            try:
                nuomi_result = nuomi_movie.get_district_list(self.nuomi_url)
                for nuomi_district in nuomi_result:
                    if nuomi_district['district_name'] not in self.name_list:
                        self.name_list.append(nuomi_district['district_name'])
                        self.result.append(nuomi_district)
                    else:
                        index = self.name_list.index(nuomi_district['district_name'])
                        self.result[index]['nuomi_district_id'] = nuomi_district['nuomi_district_id']
            except RequestException:
                self.result[0].append('nuomi connection broken')
            except:
                self.result[0].append('taobao unknown error')

        if self.taobao_city_id and self.taobao_movie_id:
            taobao_movie = TaobaoMovie()
            try:
                taobao_result = taobao_movie.get_district_list(self.taobao_url)
                for taobao_district in taobao_result:
                    if taobao_district['district_name'] not in self.name_list:
                        self.name_list.append(taobao_district['district_name'])
                        self.result.append(taobao_district)
                    else:
                        index = self.name_list.index(taobao_district['district_name'])
                        self.result[index]['taobao_district_id'] = taobao_district['taobao_district_id']
            except RequestException:
                self.result[0].append('taobao connection broken')
            except:
                self.result[0].append('taobao unknown error')

        return self.result


class CinemaList(object):
    """
    影院列表
    """
    def __init__(self, city_id, **kwargs):
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
                            % (self.meituan_city_id, self.meituan_movie_id, self.meituan_district_id))
        self.nuomi_url = ('http://%s.nuomi.com/film/%s/%s/sub0d0/cb0-d10000-s0-o-b1-f0-p1#cinema-nav'
                          % (self.nuomi_city_id, self.nuomi_movie_id, self.nuomi_district_id))
        self.taobao_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&regionName=%s&city=%s'
                           % (self.taobao_movie_id, unicode(self.taobao_district_id), self.taobao_city_id))

        self.result = [[]]
        self.name_list = ['']

    def get_cinema_list(self):
        if self.meituan_district_id:
            meituan_movie = MeituanMovie()
            try:
                meituan_result = meituan_movie.get_cinema_list(self.meituan_url, self.city_byte)
                for meituan_cinema in meituan_result:
                    if meituan_cinema['cinema_name'] not in self.name_list:
                        self.name_list.append(meituan_cinema['cinema_name'])
                        self.result.append(meituan_cinema)
                    else:
                        index = self.name_list.index(meituan_cinema['cinema_name'])
                        self.result[index]['meituan_cinema_id'] = meituan_cinema['meituan_cinema_id']
            except RequestException:
                self.result[0].append('meituan connection broken')
            except:
                self.result[0].append('meituan unknown error')

        if self.nuomi_district_id:
            nuomi_movie = NuomiMovie()
            try:
                nuomi_result = nuomi_movie.get_cinema_list(self.nuomi_url, self.city_byte)
                for nuomi_cinema in nuomi_result:
                    if nuomi_cinema['cinema_name'] not in self.name_list:
                        self.name_list.append(nuomi_cinema['cinema_name'])
                        self.result.append(nuomi_cinema)
                    else:
                        index = self.name_list.index(nuomi_cinema['cinema_name'])
                        self.result[index]['nuomi_cinema_id'] = nuomi_cinema['nuomi_cinema_id']
            except RequestException:
                self.result[0].append('nuomi connection broken')
            except:
                self.result[0].append('nuomi unknown error')

        if self.taobao_district_id:
            taobao_movie = TaobaoMovie()
            try:
                taobao_result = taobao_movie.get_cinema_list(self.taobao_url, self.city_byte)
                for taobao_cinema in taobao_result:
                    if taobao_cinema['cinema_name'] not in self.name_list:
                        self.name_list.append(taobao_cinema['cinema_name'])
                        self.result.append(taobao_cinema)
                    else:
                        index = self.name_list.index(taobao_cinema['cinema_name'])
                        self.result[index]['taobao_cinema_id'] = taobao_cinema['taobao_cinema_id']
            except RequestException:
                self.result[0].append('taobao connection broken')
            except:
                self.result[0].append('taobao unknown error')

        return self.result


class PriceList(object):
    """
    价格列表
    """
    def __init__(self, city_id, **kwargs):
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
                            % (self.meituan_city_id, self.meituan_cinema_id, self.meituan_movie_id))
        self.nuomi_url = ('http://%s.nuomi.com/pcindex/main/timetable?cinemaid=%s&mid=%s'
                          % (self.nuomi_city_id, self.nuomi_cinema_id, self.nuomi_movie_id))
        self.taobao_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&city=%s&cinemaId=%s'
                           % (self.taobao_movie_id, self.taobao_city_id ,self.taobao_cinema_id))

        self.result = [[]]
        self.start_time_list = ['']

    def get_price_list(self):
        if self.meituan_cinema_id:
            meituan_movie = MeituanMovie()
            try:
                meituan_result = meituan_movie.get_price_list(self.meituan_url)
                for meituan_price in meituan_result:
                    if meituan_price['start_time'] not in self.start_time_list:
                        self.start_time_list.append(meituan_price['start_time'])
                        self.result.append(meituan_price)
                    else:
                        index = self.start_time_list.index(meituan_price['start_time'])
                        self.result[index]['meituan_now_price'] = meituan_price['meituan_now_price']
            except RequestException:
                self.result[0].append('meituan connection broken')
            except:
                self.result[0].append('meituan unknown error')

        if self.nuomi_cinema_id:
            nuomi_movie = NuomiMovie()
            try:
                nuomi_result = nuomi_movie.get_price_list(self.nuomi_url)
                for nuomi_price in nuomi_result:
                    if nuomi_price['start_time'] not in self.start_time_list:
                        self.start_time_list.append(nuomi_price['start_time'])
                        self.result.append(nuomi_price)
                    else:
                        index = self.start_time_list.index(nuomi_price['start_time'])
                        self.result[index]['nuomi_now_price'] = nuomi_price['nuomi_now_price']
            except RequestException:
                self.result[0].append('nuomi connection broken')
            except:
                self.result[0].append('nuomi unknown error')

        if self.taobao_cinema_id:
            taobao_movie = TaobaoMovie()
            try:
                taobao_result = taobao_movie.get_price_list(self.taobao_url)
                for taobao_price in taobao_result:
                    if taobao_price['start_time'] not in self.start_time_list:
                        self.start_time_list.append(taobao_price['start_time'])
                        self.result.append(taobao_price)
                    else:
                        index = self.start_time_list.index(taobao_price['start_time'])
                        self.result[index]['taobao_now_price'] = taobao_price['taobao_now_price']
            except RequestException:
                self.result[0].append('taobao connection broken')
            except:
                self.result[0].append('taobao unknown error')

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
        try:
            meituan_movie.get_city_list(self.meituan_url)
        except RequestException:
            self.result.append('meituan connection broken')
        except:
            self.result.append('meituan unknown error')

        nuomi_movie = NuomiMovie()
        try:
            nuomi_movie.get_city_list(self.nuomi_url)
        except RequestException:
            self.result.append('nuomi connection broken')
        except:
            self.result.append('nuomi unknown error')

        taobao_movie = TaobaoMovie()
        try:
            taobao_movie.get_city_list(self.taobao_url)
        except RequestException:
            self.result.append('taobao connection broken')
        except:
            self.result.append('taobao unknown error')

        return self.result

































    



        








