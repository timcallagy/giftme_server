# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0007_auto_20150328_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contribution',
            old_name='contributed_by',
            new_name='contributor_id',
        ),
        migrations.AddField(
            model_name='contribution',
            name='contributor_name',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 28, 16, 2, 11, 670292)),
            preserve_default=True,
        ),
    ]
