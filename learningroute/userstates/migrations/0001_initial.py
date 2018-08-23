# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-21 02:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('states', '0003_auto_20180819_0756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Initialresponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polynomial_proficieny', models.CharField(choices=[('beginer', 'Beginer'), ('intermediate', 'Intermediate'), ('expert', 'Expert')], default='intermediate', max_length=60)),
                ('lineq_two_variable_proficiency_prof', models.CharField(choices=[('beginer', 'Beginer'), ('intermediate', 'Intermediate'), ('expert', 'Expert')], default='intermediate', max_length=60)),
                ('triangels_proficiency', models.CharField(choices=[('beginer', 'Beginer'), ('intermediate', 'Intermediate'), ('expert', 'Expert')], default='intermediate', max_length=60)),
                ('quadrilateral_proficiency', models.CharField(choices=[('beginer', 'Beginer'), ('intermediate', 'Intermediate'), ('expert', 'Expert')], default='intermediate', max_length=60)),
                ('time_willing_to_work', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserCompletedState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.IntegerField(default=0)),
                ('incorrect', models.IntegerField(default=0)),
                ('time_taken', models.IntegerField(blank=True, null=True)),
                ('start_time', models.IntegerField(blank=True, null=True)),
                ('timedate', models.DateTimeField(auto_now_add=True, null=True)),
                ('state', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='states.State')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCurrentState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.IntegerField(default=0)),
                ('total_time', models.IntegerField(blank=True, null=True)),
                ('timedate', models.DateTimeField(auto_now_add=True)),
                ('state', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='states.State')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]