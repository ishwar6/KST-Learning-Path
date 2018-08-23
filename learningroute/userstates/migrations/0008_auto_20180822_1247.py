# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 12:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('states', '0003_auto_20180819_0756'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userstates', '0007_auto_20180822_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCurrentNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incorrect', models.IntegerField(default=0)),
                ('timedate', models.DateTimeField(auto_now_add=True, null=True)),
                ('node', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='states.Node')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='usercompletedstate',
            name='state',
        ),
        migrations.RemoveField(
            model_name='usercompletedstate',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usercurrentstate',
            name='state',
        ),
        migrations.RemoveField(
            model_name='usercurrentstate',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserCompletedState',
        ),
        migrations.DeleteModel(
            name='UserCurrentState',
        ),
    ]
