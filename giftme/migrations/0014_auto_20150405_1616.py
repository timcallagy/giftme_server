# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0013_auto_20150405_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebooksession',
            name='expiresIn',
        ),
        migrations.AddField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 5, 16, 16, 24, 96024)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 5, 16, 16, 24, 92708)),
            preserve_default=True,
        ),
    ]
