# Generated by Django 3.0.7 on 2020-07-20 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0005_auto_20200717_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightpermission',
            name='uav_uid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
