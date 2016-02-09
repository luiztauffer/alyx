# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 10:12
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0017_auto_20160112_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='JSON',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='father',
        ),
        migrations.RemoveField(
            model_name='subject',
            name='mother',
        ),
        migrations.AlterField(
            model_name='action',
            name='start_date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]