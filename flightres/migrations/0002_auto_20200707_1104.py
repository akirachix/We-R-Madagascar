# Generated by Django 3.0.7 on 2020-07-07 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_auto_20200707_1102'),
        ('flightres', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightpermission',
            name='uav_uuid',
            field=models.ForeignKey(blank=True, db_column='uav_uuid', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uav_uuid', to='registry.Aircraft', to_field='unid'),
        ),
    ]
