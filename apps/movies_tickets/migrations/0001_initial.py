# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city_name', models.CharField(max_length=20, blank=True)),
                ('meituan_city_id', models.CharField(max_length=20, blank=True)),
                ('taobao_city_id', models.CharField(max_length=20, blank=True)),
                ('nuomi_city_id', models.CharField(max_length=20, blank=True)),
                ('hot_city', models.IntegerField(default=0)),
                ('first_char', models.CharField(max_length=2, blank=True)),
            ],
            options={
                'db_table': 'movies_city',
            },
        ),
    ]
