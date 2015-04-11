# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0016_auto_20150411_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebooksession',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 22, 12, 46, 537215), null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebooksession',
            name='receive_emails',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 22, 12, 46, 533408)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 22, 12, 46, 537078)),
            preserve_default=True,
        ),
    ]
