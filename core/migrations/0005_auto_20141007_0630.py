# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141006_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='bids_created'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='purchaser',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='bids_accepted', blank=True, null=True),
        ),
    ]
