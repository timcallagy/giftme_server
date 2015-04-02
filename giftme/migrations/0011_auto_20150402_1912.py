# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0010_auto_20150329_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 2, 19, 12, 0, 527792)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gift',
            name='url',
            field=models.CharField(default=b'', max_length=1020),
            preserve_default=True,
        ),
    ]
