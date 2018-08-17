# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-17 21:03
from __future__ import unicode_literals

import content.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Illustration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('text', models.TextField()),
                ('answer', models.TextField()),
                ('image', models.FileField(blank=True, null=True, upload_to=content.models.upload_image_path_illus)),
                ('image2', models.FileField(blank=True, null=True, upload_to=content.models.upload_image_path_illus)),
                ('credit', models.PositiveSmallIntegerField(default=b'3', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('time', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='content',
            name='rate',
        ),
        migrations.AddField(
            model_name='content',
            name='credit',
            field=models.PositiveSmallIntegerField(default=b'1', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='content',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=content.models.upload_image_path_content),
        ),
        migrations.AddField(
            model_name='content',
            name='image2',
            field=models.FileField(blank=True, null=True, upload_to=content.models.upload_image_path_content),
        ),
        migrations.AddField(
            model_name='illustration',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Content'),
        ),
    ]
