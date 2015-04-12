# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0022_auto_20150412_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebooksession',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 14, 49, 37, 174760)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 14, 49, 37, 168809)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 14, 49, 37, 174421)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 14, 49, 37, 163315)),
            preserve_default=True,
        ),
    ]
