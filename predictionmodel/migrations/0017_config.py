# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 19:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predictionmodel', '0016_auto_20171211_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('RealtimeItem', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='predictionmodel.RealTime')),
                ('configname', models.CharField(max_length=20)),
            ],
        ),
    ]
