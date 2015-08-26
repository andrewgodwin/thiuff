# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='threadinteraction',
            name='user',
            field=models.ForeignKey(related_name='interactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='thread',
            name='author',
            field=models.ForeignKey(related_name='threads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='thread',
            name='group',
            field=models.ForeignKey(related_name='threads', to='threads.Group'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='message',
            field=models.ForeignKey(to='threads.Message'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(related_name='reactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='threads.Message', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='thread',
            field=models.ForeignKey(related_name='messages', to='threads.Thread'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='group',
            field=models.ForeignKey(related_name='members', to='threads.Group'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user',
            field=models.ForeignKey(related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together=set([('message', 'user')]),
        ),
    ]
