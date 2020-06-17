# Generated by Django 3.0.7 on 2020-06-17 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0003_auto_20200617_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsappcomplain',
            name='complainer_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='whatsappcomplain',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='whatsappcomplain',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
