# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_api.settings')

app = Celery('movies_api')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(('movies_tickets.spiders', ), 'meituan')
app.autodiscover_tasks(('movies_tickets.spiders', ), 'taobao')
app.autodiscover_tasks(('movies_tickets.spiders', ), 'nuomi')

