# Generated by Django 3.0.7 on 2020-07-07 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aircraft',
            name='unid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
