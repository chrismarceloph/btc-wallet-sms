# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'wallets_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'wallets', ['Account'])

        # Adding model 'Wallet'
        db.create_table(u'wallets_wallet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wallets.Account'])),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('main_password', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'wallets', ['Wallet'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'wallets_account')

        # Deleting model 'Wallet'
        db.delete_table(u'wallets_wallet')


    models = {
        u'wallets.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'wallets.wallet': {
            'Meta': {'object_name': 'Wallet'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wallets.Account']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_password': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['wallets']