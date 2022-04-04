# Generated by Django 3.1.3 on 2022-03-14 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delayed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_id', models.CharField(max_length=7)),
                ('clinic_name', models.CharField(max_length=20)),
                ('medication', models.CharField(max_length=20)),
                ('units', models.CharField(max_length=5)),
                ('delivery_date', models.DateField()),
                ('take_of_time', models.DateField()),
                ('delivery_time', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('processed', 'processed'), ('dispatched', 'dispatched')], default='dispatched', max_length=30)),
                ('destination', models.CharField(max_length=20)),
                ('delay_reasons', models.CharField(max_length=50)),
            ],
        ),
    ]
