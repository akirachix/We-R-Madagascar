# Generated by Django 3.1.3 on 2022-11-06 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_auto_20221105_1549'),
        ('flights', '0003_auto_20220501_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightrequest',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='flightrequest',
            name='medication',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='flightrequest',
            name='clinic_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.clinic'),
        ),
        migrations.AlterField(
            model_name='flightrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Delayed', 'Delayed'), ('Completed', 'Completed'), ('Processed', 'Processed'), ('Dispatched', 'Dispatched')], default='Pending', max_length=30),
        ),
    ]
