# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-28 15:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictionmodel', '0021_realtime_generaiondata_realtime_generationstatus_realtime_windtower_realtime_write'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='config',
            name='RealtimeItem',
        ),
        migrations.DeleteModel(
            name='Config',
        ),
        migrations.DeleteModel(
            name='RealTime',
        ),
    ]
