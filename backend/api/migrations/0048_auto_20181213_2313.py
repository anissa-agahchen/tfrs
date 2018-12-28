# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-13 23:13
from __future__ import unicode_literals
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

import db_comments.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0047_auto_20181205_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentFileAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('url', models.URLField()),
                ('size', models.BigIntegerField(default=0)),
                ('mime_type', models.CharField(max_length=255)),
                ('security_scan_status', models.CharField(choices=[('NOT RUN', 'Not Run'), ('IN PROGRESS', 'In Progress'), ('PASS', 'Passed'), ('FAIL', 'Failed')], default='NOT RUN', max_length=20)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_documentfileattachment_CREATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'document_file',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.RemoveField(
            model_name='document',
            name='mime_type',
        ),
        migrations.RemoveField(
            model_name='document',
            name='size',
        ),
        migrations.RemoveField(
            model_name='document',
            name='url',
        ),
        migrations.AddField(
            model_name='document',
            name='comment',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='compliance_period',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.CompliancePeriod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documenthistory',
            name='comment',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='documenthistory',
            name='compliance_period',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.CompliancePeriod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentfileattachment',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attachments', to='api.Document'),
        ),
        migrations.AddField(
            model_name='documentfileattachment',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_documentfileattachment_UPDATE_USER', to=settings.AUTH_USER_MODEL),
        ),
    ]
