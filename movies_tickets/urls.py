#coding=utf8

from django.conf.urls import url
from movies_tickets.views import CityAPI, MovieListAPI, DistrictListAPI, CinemaListAPI, PriceListAPI

urlpatterns = [
    url(r'^city/$', CityAPI.as_view()),
    url(r'^movie/$', MovieListAPI.as_view()),
    url(r'^district/$', DistrictListAPI.as_view()),
    url(r'^cinema/$', CinemaListAPI.as_view()),
    url(r'^ticket/$', PriceListAPI.as_view()),
]