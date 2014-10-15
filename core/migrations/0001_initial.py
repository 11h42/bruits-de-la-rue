# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(verbose_name='username', max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], unique=True)),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=75, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Utilisateur',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('recipient_name', models.CharField(max_length=255)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255, blank=True, null=True)),
                ('zipcode', models.IntegerField(max_length=10)),
                ('town', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Adresse',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15, blank=True, null=True)),
                ('fax', models.CharField(max_length=15, blank=True, null=True)),
                ('url_site', models.CharField(max_length=255, blank=True, null=True)),
                ('email', models.CharField(max_length=255, blank=True, null=True)),
                ('address', models.ForeignKey(to='core.Address', blank=True, null=True)),
                ('administrator', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='administrator_of')),
                ('members', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True, related_name='members_of')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('begin', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=20, default='SUPPLY', choices=[('SUPPLY', 'Supply'), ('DEMAND', 'Demand')])),
                ('status_bid', models.CharField(max_length=20, default='EN COURS', choices=[('FERME', 'Closed'), ('ACCEPTE', 'Accepted'), ('EN COURS', 'Running'), ('EN ATTENTE', 'On hold')])),
                ('real_author', models.CharField(max_length=255, blank=True, null=True)),
                ('association', models.ForeignKey(to='core.Association', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BidCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': "Catégorie d'une annonce",
                'verbose_name_plural': "Catégorie d'une annonce",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('photo', models.FileField(upload_to='photos/')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bid',
            name='category',
            field=models.ForeignKey(to='core.BidCategory', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='creators'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='localization',
            field=models.ForeignKey(to='core.Address', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='photo',
            field=models.ForeignKey(to='core.Photo', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='purchaser',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='purchasers'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.ManyToManyField(null=True, to='core.Address', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(verbose_name='groups', to='auth.Group', related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_name='user_set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', related_query_name='user', help_text='Specific permissions for this user.', blank=True, related_name='user_set'),
            preserve_default=True,
        ),
    ]
