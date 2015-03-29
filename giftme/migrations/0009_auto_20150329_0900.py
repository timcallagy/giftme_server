# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0008_auto_20150328_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 29, 9, 0, 11, 111849)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='message',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
