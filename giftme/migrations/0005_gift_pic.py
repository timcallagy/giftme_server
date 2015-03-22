# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0004_gift_crowdfunded'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='pic',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
