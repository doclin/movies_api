#coding=utf8
from django.test import TestCase
from movies_tickets.spiders import  meituan, nuomi, taobao

class SpiderTestCase(TestCase):
    """
    爬虫测试代码
    """
    def test_meituan_spider(self):
        # 测试获取城市信息
        print "show meituan city list:"
        meituan_city_url = 'http://www.meituan.com/index/changecity/initiative'
        meituan_city_list = meituan.meituan_get_city_list_without_saving(meituan_city_url)
        for i in meituan_city_list:
            print i['city_name']
        meituan_city_id = meituan_city_list[100]['meituan_city_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取电影信息
        print 'show meituan movie list'
        meituan_movie_url = 'http://%s.meituan.com/dianying/zuixindianying' % meituan_city_id
        meituan_movie_list = meituan.meituan_get_movie_list(meituan_movie_url)
        for i in meituan_movie_list:
            print i['movie_name']
        meituan_movie_id = meituan_movie_list[0]['meituan_movie_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取行政区信息
        print 'show meituan district list'
        meituan_district_url = ('http://%s.meituan.com/dianying/%s?mtt=1.movie'
                                % (meituan_city_id, meituan_movie_id))
        meituan_district_list = meituan.meituan_get_district_list(meituan_district_url)
        for i in meituan_district_list:
            print i['district_name']
        meituan_district_id = meituan_district_list[0]['meituan_district_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取影院信息
        print 'show meituan cinema list'
        meituan_cinema_url = ('http://%s.meituan.com/dianying/%s//%s/all?mtt=1.movie'
                              % (meituan_city_id, meituan_movie_id, meituan_district_id))
        meituan_cinema_list = meituan.meituan_get_cinema_list(meituan_cinema_url, )
        for i in meituan_cinema_list:
            print i['cinema_name']
        meituan_cinema_id = meituan_cinema_list[0]['meituan_cinema_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取票价信息
        print 'show meituan price list'
        meituan_price_url = ('http://%s.meituan.com/shop/%s?movieid=%s'
                             % (meituan_city_id, meituan_cinema_id, meituan_movie_id))
        print meituan_price_url
        meituan_price_list = meituan.meituan_get_price_list(meituan_price_url)
        for i in meituan_price_list:
            print i['start_time']

    def test_nuomi_spider(self):
        # 测试获取城市信息
        print "show nuomi city list:"
        nuomi_city_url = 'http://www.nuomi.com/pcindex/main/changecity'
        nuomi_city_list = nuomi.nuomi_get_city_list_without_saving(nuomi_city_url)
        for i in nuomi_city_list:
            print i['city_name']
        nuomi_city_id = nuomi_city_list[15]['nuomi_city_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取电影信息
        print 'show nuomi movie list'
        nuomi_movie_url = 'http://%s.nuomi.com/pcindex/main/filmlist?type=1' % nuomi_city_id
        nuomi_movie_list = nuomi.nuomi_get_movie_list(nuomi_movie_url)
        for i in nuomi_movie_list:
            print i['movie_name']
        nuomi_movie_id = nuomi_movie_list[0]['nuomi_movie_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取行政区信息
        print 'show nuomi district list'
        nuomi_district_url = ('http://%s.nuomi.com/film/%s'
                              % (nuomi_city_id, nuomi_movie_id))
        print nuomi_district_url
        nuomi_district_list = nuomi.nuomi_get_district_list(nuomi_district_url)
        for i in nuomi_district_list:
            print i['district_name']
        nuomi_district_id = nuomi_district_list[0]['nuomi_district_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取影院信息
        print 'show nuomi cinema list'
        nuomi_cinema_url = ('http://%s.nuomi.com/film/%s/%s/sub0d0/cb0-d10000-s0-o-b1-f0-p1#cinema-nav'
                            % (nuomi_city_id, nuomi_movie_id, nuomi_district_id))
        nuomi_cinema_list = nuomi.nuomi_get_cinema_list(nuomi_cinema_url)
        for i in nuomi_cinema_list:
            print i['cinema_name']
        nuomi_cinema_id = nuomi_cinema_list[0]['nuomi_cinema_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取票价信息
        print 'show nuomi price list'
        nuomi_price_url = ('http://%s.nuomi.com/pcindex/main/timetable?cinemaid=%s&mid=%s'
                           % (nuomi_city_id, nuomi_cinema_id, nuomi_movie_id))
        nuomi_price_list = nuomi.nuomi_get_price_list(nuomi_price_url)
        print nuomi_price_url
        for i in nuomi_price_list:
            print i['start_time']

    def test_taobao_spider(self):
        # 测试获取城市信息
        print "show taobao city list:"
        taobao_city_url = 'http://dianying.taobao.com/cityAction.json?activityId&action=cityAction&event_submit_doGetAllRegion=true'
        taobao_city_list = taobao.taobao_get_city_list_without_saving(taobao_city_url)
        for i in taobao_city_list:
            print i['city_name']
        taobao_city_id = taobao_city_list[16]['taobao_city_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取电影信息
        print 'show taobao movie list'
        taobao_movie_url = 'https://dianying.taobao.com/showList.htm?city=%s' % taobao_city_id
        taobao_movie_list = taobao.taobao_get_movie_list(taobao_movie_url)
        for i in taobao_movie_list:
            print i['movie_name']
        taobao_movie_id = taobao_movie_list[0]['taobao_movie_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取行政区信息
        print 'show taobao district list'
        taobao_district_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&city=%s'
                               % (taobao_movie_id, taobao_city_id))
        taobao_district_list = taobao.taobao_get_district_list(taobao_district_url)
        for i in taobao_district_list:
            print i['district_name']
        taobao_district_id = taobao_district_list[0]['taobao_district_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取影院信息
        print 'show taobao cinema list'
        taobao_cinema_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&regionName=%s&city=%s'
                             % (taobao_movie_id, unicode(taobao_district_id), taobao_city_id))
        taobao_cinema_list = taobao.taobao_get_cinema_list(taobao_cinema_url, )
        for i in taobao_cinema_list:
            print i['cinema_name']
        taobao_cinema_id = taobao_cinema_list[0]['taobao_cinema_id']
        print '-----------------------------------------------------------------------------------'
        # 测试获取票价信息
        print 'show taobao price list'
        taobao_price_url = ('https://dianying.taobao.com/showDetailSchedule.htm?showId=%s&city=%s&cinemaId=%s'
                            % (taobao_movie_id, taobao_city_id, taobao_cinema_id))
        print taobao_price_url
        taobao_price_list = taobao.taobao_get_price_list(taobao_price_url)
        for i in taobao_price_list:
            print i['start_time']