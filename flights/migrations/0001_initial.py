# Generated by Django 3.1.3 on 2022-04-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlightRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(max_length=50)),
                ('total_volume', models.IntegerField()),
                ('delivery_date', models.DateTimeField()),
                ('priority_level', models.IntegerField()),
                ('refrigration', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Delayed', 'Delayed')], default='pending', max_length=30)),
            ],
        ),
    ]