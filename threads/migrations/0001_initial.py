# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('moderator', models.BooleanField(default=False)),
                ('group', models.ForeignKey(related_name='members', to='threads.Group')),
                ('user', models.ForeignKey(related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('edited', models.DateTimeField(blank=True, null=True)),
                ('score', models.FloatField(db_index=True, default=0)),
                ('author', models.ForeignKey(related_name='messages', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='children', to='threads.Message')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('like', 'Like'), ('informative', 'Informative'), ('surprising', 'Surprising'), ('confusing', 'Confusing'), ('spam', 'Spam'), ('abuse', 'Abuse')], max_length=30)),
                ('message', models.ForeignKey(to='threads.Message')),
                ('user', models.ForeignKey(related_name='reactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], db_index=True, max_length=30)),
                ('score', models.FloatField(db_index=True, default=0)),
                ('title', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(related_name='topics', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(related_name='topics', to='threads.Group')),
            ],
        ),
        migrations.CreateModel(
            name='TopicInteraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_content', models.BooleanField(default=False)),
                ('view_discussion', models.BooleanField(default=False)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('topic', models.ForeignKey(related_name='interactions', to='threads.Topic')),
                ('user', models.ForeignKey(related_name='interactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(related_name='messages', to='threads.Topic'),
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together=set([('message', 'user')]),
        ),
    ]
