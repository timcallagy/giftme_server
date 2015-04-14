# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0025_auto_20150413_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebooksession',
            name='gender',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 34, 19, 243156)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 34, 19, 247124)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 34, 19, 247362)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 34, 19, 239449)),
            preserve_default=True,
        ),
    ]
