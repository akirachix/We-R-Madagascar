# Generated by Django 3.0.7 on 2020-06-17 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0004_auto_20200617_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whatsappcomplain',
            name='note',
        ),
        migrations.AlterField(
            model_name='whatsappcomplain',
            name='complainer_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='whatsappcomplain',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='uploads/WhComplains'),
        ),
    ]
