#coding=utf8

from bs4 import BeautifulSoup
import requests
import re

class NumomiMovie(object):
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

		soup = BeautifulSoup(r.text)
		ul = soup.find_all('ul', class_='movie-list')
		a = ul[0].find_all('a')
		for i in a:
			data = i['data-log']
			nuomi_movie_id = re.search(r'(?<=movieId":")\d+', data).group()
			name_text = i.find('h4', class_='movie-name-text')
			name = name_text.get_text()

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

		soup = BeautifulSoup(r.text)
		ul = soup.find('ul', class_='widget-filter-list')
		li = ul.find_all('li')
		for i in li:



		

http://m.dianying.baidu.com/api/movie/loadMoreCinema?sfrom=wise_shoubai&sub_channel=&c=218&cc=&lat=0&lng=0&movie_id=9724&from=webapp&day=&wd=2403%2Bnull&metro=&brandId=&pn=0&sell_type=all
http://m.dianying.baidu.com/api/movie/loadMoreCinema?sfrom=wise_shoubai&sub_channel=&c=218&cc=&lat=0&lng=0&movie_id=9724&from=webapp&day=&wd=2788%2Bnull&metro=&brandId=&pn=0&sell_type=all

