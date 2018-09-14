# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-24 18:49
from __future__ import unicode_literals

import app.validators.phone
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180123_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallEndRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('call_id', models.IntegerField(unique=True)),
                ('reference_month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('reference_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)])),
            ],
        ),
        migrations.CreateModel(
            name='CallStartRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('call_id', models.IntegerField(unique=True)),
                ('origin_phone', models.IntegerField(validators=[app.validators.phone.validate_size])),
                ('destination_phone', models.IntegerField(validators=[app.validators.phone.validate_size])),
            ],
        ),
    ]