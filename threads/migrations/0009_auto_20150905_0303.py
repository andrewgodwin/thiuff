# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0008_group_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmember',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='banned',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='moderator',
        ),
        migrations.RemoveField(
            model_name='groupmember',
            name='pending',
        ),
        migrations.AddField(
            model_name='group',
            name='intro',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='num_members',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='group',
            name='num_threads',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='status',
            field=models.CharField(default='member', max_length=30, db_index=True, choices=[('pending', 'Pending'), ('member', 'Member'), ('moderator', 'Moderator'), ('admin', 'Admin'), ('banned', 'Banned')]),
            preserve_default=False,
        ),
    ]
