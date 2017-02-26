# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 17:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tomabi_app', '0003_auto_20170222_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('url', models.URLField()),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tomabi_app.Manga')),
            ],
        ),
    ]
