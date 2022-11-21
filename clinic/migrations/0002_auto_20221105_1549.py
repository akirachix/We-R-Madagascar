# Generated by Django 3.1.3 on 2022-11-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinic',
            name='address',
        ),
        migrations.RemoveField(
            model_name='clinic',
            name='name',
        ),
        migrations.RemoveField(
            model_name='clinic',
            name='profile',
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='contact',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='district',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
