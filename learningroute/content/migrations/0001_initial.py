# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-17 20:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('states', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('text', models.TextField()),
                ('rate', models.IntegerField()),
                ('time', models.IntegerField()),
                ('tag', models.CharField(blank=True, max_length=15, null=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='states.State')),
            ],
        ),
    ]