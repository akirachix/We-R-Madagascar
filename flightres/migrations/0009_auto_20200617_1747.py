# Generated by Django 3.0.7 on 2020-06-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0008_auto_20200617_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='photo',
        ),
        migrations.AddField(
            model_name='report',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]