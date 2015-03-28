# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('giftme', '0005_gift_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contributed_by', models.CharField(default=b'', max_length=255)),
                ('amount', models.FloatField(default=b'0', null=True, blank=True)),
                ('contribution_date', models.DateTimeField(default=datetime.datetime(2015, 3, 28, 15, 9, 4, 15385))),
                ('stripe_charge', models.CharField(default=b'', max_length=255, null=True, blank=True)),
                ('gift', models.ForeignKey(to='giftme.Gift')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
