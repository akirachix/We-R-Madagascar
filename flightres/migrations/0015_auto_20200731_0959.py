# Generated by Django 3.0.7 on 2020-07-31 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0014_localauthorities'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='category',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]