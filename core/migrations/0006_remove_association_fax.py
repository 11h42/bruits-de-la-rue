# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141007_0630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='association',
            name='fax',
        ),
    ]
