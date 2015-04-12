# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0020_auto_20150412_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='owner_name',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 13, 51, 0, 247045)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 13, 51, 0, 250878)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 13, 51, 0, 243451)),
            preserve_default=True,
        ),
    ]
