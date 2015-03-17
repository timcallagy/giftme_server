# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0002_auto_20150317_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gift',
            name='owner',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='gift',
            name='owner_id',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
