# Generated by Django 3.0.8 on 2020-07-06 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightpermission',
            name='location',
            field=models.URLField(blank=True, null=True),
        ),
    ]
