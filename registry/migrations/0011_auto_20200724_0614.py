# Generated by Django 3.0.7 on 2020-07-24 06:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0010_auto_20200723_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 24, 0, 0, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='operator',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 24, 0, 0, tzinfo=utc)),
        ),
    ]