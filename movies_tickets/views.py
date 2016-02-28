#coding=utf8

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response

from movies_tickets.models import City
from movies_tickets.tasks import MovieList, DistrictList, CinemaList, PriceList, CityList
from movies_tickets.serializers import CityListSerializer, MovieListSerializer, DistrictListSerializer, CinemaListSerializer, PriceListSerializer
from movies_tickets.response import DoesNotExistResponse, UnKnownResponse


class CityAPI(APIView):
    """
    城市清单API
    """
    serializer_class = CityListSerializer

    def get(self, request):
        """
        获取城市名
        """
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        update = serializer.validated_data.get('update')
        result = []
        #检查是否更新城市数据库
        if update:
            city_list = CityList()
            result = city_list.update()
        cities = City.objects.all()
        for i in cities:
            result.append({
                'city_name': i.city_name,
                'city_id': i.id,
                'hot_city': i.hot_city,
                'first_char': i.first_char,
            })
        return Response(result)


class MovieListAPI(APIView):
    """
    电影列表API
    """
    serializer_class = MovieListSerializer

    def get(self, request):
        """
        获取电影列表
        """
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city_id = serializer.validated_data.get('city_id')
        try:
            movie_list = MovieList(city_id)
        except ObjectDoesNotExist:
            return DoesNotExistResponse()
        except:
            return UnKnownResponse()
        task_result = movie_list.get_movie_list()
        return Response(task_result)


class DistrictListAPI(APIView):
    """
    城市行政区列表API
    """
    serializer_class = DistrictListSerializer

    def get(self, request):
        """
        获取城市行政区列表
        """
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city_id = serializer.validated_data.get('city_id')
        dic = {
            'meituan_movie_id': serializer.validated_data.get('meituan_movie_id'),
            'nuomi_movie_id': serializer.validated_data.get('nuomi_movie_id'),
            'taobao_movie_id': serializer.validated_data.get('taobao_movie_id'),
        }
        try:
            district_list = DistrictList(city_id, **dic)
        except ObjectDoesNotExist:
            return DoesNotExistResponse()
        except:
            return UnKnownResponse()

        task_result = district_list.get_district_list()
        return Response(task_result)


class CinemaListAPI(APIView):
    """
    影院列表API
    """
    serializer_class = CinemaListSerializer

    def get(self, request):
        """
        获取影院列表
        """
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city_id = serializer.validated_data.get('city_id')
        dic = {
            'meituan_district_id': serializer.validated_data.get('meituan_district_id'),
            'meituan_movie_id': serializer.validated_data.get('meituan_movie_id'),
            'nuomi_district_id': serializer.validated_data.get('nuomi_district_id'),
            'nuomi_movie_id': serializer.validated_data.get('nuomi_movie_id'),
            'taobao_district_id': serializer.validated_data.get('taobao_district_id'),
            'taobao_movie_id': serializer.validated_data.get('taobao_movie_id'),
        }
        
        try:
            cinema_list = CinemaList(city_id, **dic)
        except ObjectDoesNotExist:
            return DoesNotExistResponse()
        except:
            return UnKnownResponse()

        task_result = cinema_list.get_cinema_list()
        return Response(task_result)


class PriceListAPI(APIView):
    """
    价格列表API
    """
    serializer_class = PriceListSerializer

    def get(self, request):
        """
        获取价格列表
        """
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city_id = serializer.validated_data.get('city_id')
        dic = {
            'meituan_movie_id': serializer.validated_data.get('meituan_movie_id'),
            'meituan_cinema_id': serializer.validated_data.get('meituan_cinema_id'),
            'nuomi_movie_id': serializer.validated_data.get('nuomi_movie_id'),
            'nuomi_cinema_id': serializer.validated_data.get('nuomi_cinema_id'),
            'taobao_movie_id': serializer.validated_data.get('taobao_movie_id'),
            'taobao_cinema_id': serializer.validated_data.get('taobao_cinema_id'),
        }
        try:
            price_list = PriceList(city_id, **dic)
        except ObjectDoesNotExist:
            return DoesNotExistResponse()
        except:
            return UnKnownResponse()
        task_result = price_list.get_price_list()
        return Response(task_result)
