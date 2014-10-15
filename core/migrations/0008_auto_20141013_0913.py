# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141010_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address1',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='recipient_name',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.CharField(null=True, blank=True, max_length=10),
        ),
    ]
