# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models
import django.db.models.deletion
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', blank=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Utilisateur',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('recipient_name', models.CharField(null=True, blank=True, max_length=255)),
                ('address1', models.CharField(null=True, blank=True, max_length=255)),
                ('address2', models.CharField(null=True, blank=True, max_length=255)),
                ('zipcode', models.CharField(null=True, blank=True, max_length=10)),
                ('town', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Adresse',
            },
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(null=True, blank=True, max_length=15)),
                ('url_site', models.CharField(null=True, blank=True, max_length=255)),
                ('email', models.CharField(null=True, blank=True, max_length=255)),
                ('address', models.ForeignKey(blank=True, to='core.Address', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('administrator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='associations_administrated')),
                ('members', models.ManyToManyField(related_name='associations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Association',
            },
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('begin', models.DateTimeField(null=True, blank=True)),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(default='SUPPLY', choices=[('SUPPLY', 'Supply'), ('DEMAND', 'Demand')], max_length=20)),
                ('status_bid', models.CharField(default='EN COURS', choices=[('FERME', 'Closed'), ('ACCEPTE', 'Accepted'), ('EN COURS', 'Running'), ('EN ATTENTE', 'On hold')], max_length=20)),
                ('real_author', models.CharField(null=True, blank=True, max_length=255)),
                ('association', models.ForeignKey(blank=True, to='core.Association', null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'Annonce',
            },
        ),
        migrations.CreateModel(
            name='BidCategory',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': "Catégorie d'une annonce",
                'verbose_name_plural': 'Catégories des annonces',
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('photo', models.FileField(upload_to='photos/')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='category',
            field=models.ForeignKey(blank=True, to='core.BidCategory', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='bid',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='bids_created'),
        ),
        migrations.AddField(
            model_name='bid',
            name='localization',
            field=models.ForeignKey(blank=True, to='core.Address', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='bid',
            name='photo',
            field=models.ForeignKey(blank=True, to='core.Photo', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='bid',
            name='purchaser',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bids_accepted'),
        ),
        migrations.AddField(
            model_name='user',
            name='addresses',
            field=models.ManyToManyField(to='core.Address'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', to='auth.Group', verbose_name='groups', related_name='user_set'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', blank=True, related_query_name='user', to='auth.Permission', verbose_name='user permissions', related_name='user_set'),
        ),
    ]
