# Generated by Django 3.0.7 on 2020-07-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0010_auto_20200723_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightpermission',
            name='flight_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flightpermission',
            name='flight_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]