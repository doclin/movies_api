#coding=utf8

from rest_framework import serializers


class CityListSerializer(serializers.Serializer):
    error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid',
    }
    update = serializers.IntegerField(error_messages=error_messages,default=0)


class MovieListSerializer(serializers.Serializer):
    error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid',
    }
    city_id = serializers.CharField(error_messages=error_messages)


class DistrictListSerializer(serializers.Serializer):
    error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid',
    } 
    city_id = serializers.CharField(error_messages=error_messages)
    taobao_movie_id = serializers.CharField(error_messages=error_messages,allow_blank=True,required=False)
    meituan_movie_id = serializers.CharField(error_messages=error_messages,allow_blank=True,required=False)
    nuomi_movie_id =serializers.CharField(error_messages=error_messages,allow_blank=True,required=False)


class CinemaListSerializer(serializers.Serializer):
    error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid',
    }
    city_id = serializers.CharField(error_messages=error_messages)
    taobao_district_id = serializers.CharField(error_messages=error_messages,allow_blank=True,required=False)
    taobao_movie_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    meituan_movie_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    meituan_district_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    nuomi_movie_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    nuomi_district_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)


class PriceListSerializer(serializers.Serializer):
    error_messages = {
        'required': 'missing_field',
        'invalid': 'invalid',
    }
    city_id = serializers.CharField(error_messages=error_messages)
    taobao_cinema_id = serializers.CharField(error_messages=error_messages,allow_blank=True,required=False)
    taobao_movie_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    meituan_movie_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    meituan_cinema_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    nuomi_movie_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)
    nuomi_cinema_id = serializers.CharField(error_messages=error_messages, allow_blank=True,required=False)