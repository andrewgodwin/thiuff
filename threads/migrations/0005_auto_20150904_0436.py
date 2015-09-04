# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threads', '0004_message_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30, choices=[('spam', 'Spam'), ('abuse', 'Abuse'), ('offensive', 'Offensive'), ('personal', 'Personal Information'), ('hack', 'Malware / Hack'), ('illegal', 'Illegal content'), ('other', 'Other (provide reason)')])),
                ('comment', models.TextField(null=True, blank=True)),
                ('accused', models.ForeignKey(related_name='reports', to=settings.AUTH_USER_MODEL)),
                ('message', models.ForeignKey(related_name='reports', blank=True, to='threads.Message', null=True)),
                ('reporter', models.ForeignKey(related_name='submitted_reports', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(related_name='reports', blank=True, to='threads.Thread', null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='reaction',
            name='message',
        ),
        migrations.RemoveField(
            model_name='reaction',
            name='user',
        ),
        migrations.DeleteModel(
            name='Reaction',
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('message', 'thread', 'reporter')]),
        ),
    ]
