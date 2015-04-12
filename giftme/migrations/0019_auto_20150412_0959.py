# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0018_auto_20150411_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 9, 59, 11, 190577)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='birthday',
            field=models.DateTimeField(default=datetime.date(1900, 1, 1), null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 9, 59, 11, 194280)),
            preserve_default=True,
        ),
    ]
