# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0026_auto_20150414_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 57, 21, 753103)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 57, 21, 757158)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 57, 21, 757423)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 14, 19, 57, 21, 748511)),
            preserve_default=True,
        ),
    ]
