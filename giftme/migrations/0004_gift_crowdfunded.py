# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0003_auto_20150317_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='crowdfunded',
            field=models.FloatField(default=b'0', null=True, blank=True),
            preserve_default=True,
        ),
    ]
