# Generated by Django 3.1.3 on 2022-10-26 06:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_auto_20221023_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 26, 0, 0, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='operator',
            name='expiration',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 10, 26, 0, 0, tzinfo=utc), null=True),
        ),
    ]