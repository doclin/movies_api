#coding=utf8

from django.db import models


class City(models.Model):
    """
    数据库存储各网站城市id
    """
    city_name = models.CharField(max_length=20, blank=True)
    meituan_city_id = models.CharField(max_length=20,blank=True)
    taobao_city_id = models.CharField(max_length=20,blank=True)
    nuomi_city_id = models.CharField(max_length=20,blank=True)
    hot_city = models.IntegerField(default=0) #热门城市
    first_char = models.CharField(max_length=2,blank=True) #首字母
    def __unicode__(self):
        return self.city_name

    class Meta:
        db_table = 'movies_city'



