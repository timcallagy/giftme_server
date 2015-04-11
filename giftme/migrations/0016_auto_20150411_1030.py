# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0015_auto_20150406_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebooksession',
            name='email',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 10, 30, 48, 205039)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 10, 30, 48, 208551)),
            preserve_default=True,
        ),
    ]
