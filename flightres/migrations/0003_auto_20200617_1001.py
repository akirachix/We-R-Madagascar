# Generated by Django 3.0.7 on 2020-06-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0002_auto_20200605_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsappcomplain',
            name='uav_uid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]