# Generated by Django 3.1.3 on 2021-01-08 05:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0046_auto_20210107_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorization',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 8, 0, 0, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='operator',
            name='expiration',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 8, 0, 0, tzinfo=utc), null=True),
        ),
    ]
