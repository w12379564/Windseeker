# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-14 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictionmodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='resulttest',
            fields=[
                ('time', models.DateTimeField(primary_key=True, serialize=False)),
                ('windspeed', models.FloatField()),
            ],
        ),
    ]
