# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admin', models.BooleanField(default=False)),
                ('moderator', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('edited', models.DateTimeField(null=True, blank=True)),
                ('score', models.FloatField(default=0, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30, choices=[('like', 'Like'), ('informative', 'Informative'), ('surprising', 'Surprising'), ('confusing', 'Confusing'), ('spam', 'Spam'), ('abuse', 'Abuse')])),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(db_index=True, max_length=30, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])),
                ('score', models.FloatField(default=0, db_index=True)),
                ('title', models.TextField()),
                ('url', models.URLField(null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadInteraction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('view_content', models.BooleanField(default=False)),
                ('view_discussion', models.BooleanField(default=False)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('thread', models.ForeignKey(related_name='interactions', to='threads.Thread')),
            ],
        ),
    ]
