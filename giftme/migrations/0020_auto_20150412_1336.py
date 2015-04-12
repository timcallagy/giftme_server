# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0019_auto_20150412_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 13, 36, 44, 894020)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 13, 36, 44, 897599)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 12, 13, 36, 44, 901201)),
            preserve_default=True,
        ),
    ]
