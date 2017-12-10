# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predictionmodel', '0005_historydatatest_power'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('configname', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RealTime_read',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('value', models.FloatField()),
                ('config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='predictionmodel.Config')),
            ],
        ),
    ]
