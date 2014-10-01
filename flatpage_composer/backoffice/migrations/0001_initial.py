# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LoginLog'
        db.create_table('LOGIN_LOG', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True, db_column='ID')),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_column='CREATED', blank=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=64, db_column='IP_ADDRESS', blank=True)),
        ))
        db.send_create_signal(u'backoffice', ['LoginLog'])


    def backwards(self, orm):
        # Deleting model 'LoginLog'
        db.delete_table('LOGIN_LOG')


    models = {
        u'backoffice.loginlog': {
            'Meta': {'ordering': "['id']", 'object_name': 'LoginLog', 'db_table': "'LOGIN_LOG'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_column': "'CREATED'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'ID'"}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_column': "'IP_ADDRESS'", 'blank': 'True'})
        }
    }

    complete_apps = ['backoffice']