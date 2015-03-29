# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0009_auto_20150329_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='gift_name',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 14, 42, 58, 70050)),
            preserve_default=True,
        ),
    ]
