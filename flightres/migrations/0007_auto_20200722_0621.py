# Generated by Django 3.0.7 on 2020-07-22 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0009_auto_20200722_0621'),
        ('flightres', '0006_auto_20200720_0431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightpermission',
            name='pilot_cv_url',
        ),
        migrations.RemoveField(
            model_name='flightpermission',
            name='pilot_name',
        ),
        migrations.RemoveField(
            model_name='flightpermission',
            name='pilot_phone_number',
        ),
        migrations.CreateModel(
            name='Pilots',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.CharField(max_length=100)),
                ('cv_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=0)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='registry.Operator')),
            ],
        ),
        migrations.AddField(
            model_name='flightpermission',
            name='pilot_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flightres.Pilots'),
        ),
    ]