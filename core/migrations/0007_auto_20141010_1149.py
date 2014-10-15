# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_association_fax'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='association',
            options={'verbose_name': 'Association'},
        ),
        migrations.AlterModelOptions(
            name='bid',
            options={'verbose_name': 'Annonce'},
        ),
        migrations.AlterModelOptions(
            name='bidcategory',
            options={'verbose_name': "Catégorie d'une annonce", 'verbose_name_plural': 'Catégories des annonces'},
        ),
        migrations.AlterField(
            model_name='association',
            name='address',
            field=models.ForeignKey(to='core.Address', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='association',
            name='administrator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='associations_administrated', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='association',
            field=models.ForeignKey(to='core.Association', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='category',
            field=models.ForeignKey(to='core.BidCategory', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='localization',
            field=models.ForeignKey(to='core.Address', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='photo',
            field=models.ForeignKey(to='core.Photo', blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='bid',
            name='purchaser',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='bids_accepted', on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
