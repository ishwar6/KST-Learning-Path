# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-22 08:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userstates', '0005_auto_20180822_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proficiency',
            name='significance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proficiency',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
