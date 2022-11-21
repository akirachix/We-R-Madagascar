# Generated by Django 3.1.3 on 2022-11-06 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_auto_20221105_1549'),
        ('shipments', '0002_auto_20221026_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='shipment_id',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='clinic_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.clinic'),
        ),
    ]
