# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0017_auto_20150411_2212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facebooksession',
            old_name='receive_emails',
            new_name='receiveEmails',
        ),
        migrations.AlterField(
            model_name='contribution',
            name='contribution_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 22, 56, 30, 962003)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='birthday',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 22, 56, 30, 966726), null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='facebooksession',
            name='expiryTime',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 11, 22, 56, 30, 966596)),
            preserve_default=True,
        ),
    ]
