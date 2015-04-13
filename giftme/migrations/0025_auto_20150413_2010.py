# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0024_auto_20150413_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 10, 4, 432131)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 10, 4, 436580)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='joined_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 10, 4, 436812)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='added_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 13, 20, 10, 4, 427996)),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contribution',
            unique_together=set([]),
        ),
    ]
