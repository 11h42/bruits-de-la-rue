# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141006_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='administrator',
            field=models.ForeignKey(related_name='associations_administrated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='association',
            name='members',
            field=models.ManyToManyField(related_name='associations', to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
