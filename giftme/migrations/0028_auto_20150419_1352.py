# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0027_auto_20150414_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='description',
            field=models.CharField(default=b'', max_length=5000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 13, 51, 59, 240023)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='message',
            field=models.CharField(default=b'', max_length=5000, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 13, 51, 59, 243857)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 13, 51, 59, 244075)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 13, 51, 59, 236287)),
            preserve_default=True,
        ),
    ]
