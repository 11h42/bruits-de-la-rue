# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_bid_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_public_member',
            field=models.BooleanField(verbose_name='Membre public', default=True),
        ),
    ]
