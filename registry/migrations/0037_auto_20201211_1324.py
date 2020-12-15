# Generated by Django 3.1.3 on 2020-12-11 07:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0036_auto_20201210_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 11, 0, 0, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='operator',
            name='expiration',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 12, 11, 0, 0, tzinfo=utc), null=True),
        ),
    ]