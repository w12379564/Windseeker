# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-11 18:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictionmodel', '0010_auto_20171209_1957'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RealTime_read',
            new_name='RealTime',
        ),
    ]
