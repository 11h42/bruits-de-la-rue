# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Association'
        db.create_table(u'core_association', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('adress', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('url_site', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact_mail', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('schedule', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Association'])

        # Adding model 'User'
        db.create_table(u'core_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('association_fk_association', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Association'], null=True)),
            ('is_donor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['User'])

        # Adding model 'Message'
        db.create_table(u'core_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_user_fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from_user_fk_user', to=orm['core.User'])),
            ('to_user_fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_user_fk_user', to=orm['core.User'])),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Message'])

        # Adding model 'Bid'
        db.create_table(u'core_bid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caller_fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='caller_fk_user', to=orm['core.User'])),
            ('acceptor_fk_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='acceptor_fk_user', null=True, to=orm['core.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('begin', self.gf('django.db.models.fields.DateField')()),
            ('end', self.gf('django.db.models.fields.DateField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=200, decimal_places=20)),
            ('localization', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('real_author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('emergency_level', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('recurrence', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bidCategory', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Bid'])


    def backwards(self, orm):
        # Deleting model 'Association'
        db.delete_table(u'core_association')

        # Deleting model 'User'
        db.delete_table(u'core_user')

        # Deleting model 'Message'
        db.delete_table(u'core_message')

        # Deleting model 'Bid'
        db.delete_table(u'core_bid')


    models = {
        u'core.association': {
            'Meta': {'object_name': 'Association'},
            'adress': ('django.db.models.fields.TextField', [], {}),
            'contact_mail': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'schedule': ('django.db.models.fields.TextField', [], {}),
            'url_site': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.bid': {
            'Meta': {'object_name': 'Bid'},
            'acceptor_fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'acceptor_fk_user'", 'null': 'True', 'to': u"orm['core.User']"}),
            'begin': ('django.db.models.fields.DateField', [], {}),
            'bidCategory': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'caller_fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'caller_fk_user'", 'to': u"orm['core.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'emergency_level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'end': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'localization': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '200', 'decimal_places': '20'}),
            'real_author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'recurrence': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'core.message': {
            'Meta': {'object_name': 'Message'},
            'from_user_fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_user_fk_user'", 'to': u"orm['core.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_user_fk_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_user_fk_user'", 'to': u"orm['core.User']"})
        },
        u'core.user': {
            'Meta': {'object_name': 'User'},
            'association_fk_association': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Association']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_donor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['core']