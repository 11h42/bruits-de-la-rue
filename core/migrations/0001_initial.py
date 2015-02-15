# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('recipient_name', models.CharField(max_length=255, blank=True, null=True)),
                ('address1', models.CharField(max_length=255, blank=True, null=True)),
                ('address2', models.CharField(max_length=255, blank=True, null=True)),
                ('zipcode', models.CharField(max_length=10, blank=True, null=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15, blank=True, null=True)),
                ('url_site', models.CharField(max_length=255, blank=True, null=True)),
                ('email', models.CharField(max_length=255, blank=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='core.Address')),
                ('administrator', models.ForeignKey(related_name='associations_administrated', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(null=True, blank=True, related_name='associations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Association',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('begin', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=20, choices=[('SUPPLY', 'Supply'), ('DEMAND', 'Demand')], default='SUPPLY')),
                ('status_bid', models.CharField(max_length=20, choices=[('FERME', 'Closed'), ('ACCEPTE', 'Accepted'), ('EN COURS', 'Running'), ('EN ATTENTE', 'On hold')], default='EN COURS')),
                ('real_author', models.CharField(max_length=255, blank=True, null=True)),
                ('association', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='core.Association')),
            ],
            options={
                'verbose_name': 'Annonce',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BidCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Catégories des annonces',
                'verbose_name': "Catégorie d'une annonce",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='core.BidCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='creator',
            field=models.ForeignKey(related_name='bids_created', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='localization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='core.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='core.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bid',
            name='purchaser',
            field=models.ForeignKey(related_name='bids_accepted', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='addresses',
            field=models.ManyToManyField(null=True, blank=True, to='core.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', verbose_name='groups', blank=True, related_query_name='user', to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', related_name='user_set', verbose_name='user permissions', blank=True, related_query_name='user', to='auth.Permission'),
            preserve_default=True,
        ),
    ]
