# Generated by Django 3.1.3 on 2020-12-11 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0031_auto_20201211_1612'),
    ]

    operations = [
        migrations.RenameField(
            model_name='noflyzone',
            old_name='file_name1',
            new_name='shx_file',
        ),
        migrations.RenameField(
            model_name='noflyzone',
            old_name='file_name2',
            new_name='spatialdata_zip_file',
        ),
        migrations.RemoveField(
            model_name='noflyzone',
            name='file_name3',
        ),
        migrations.RemoveField(
            model_name='noflyzone',
            name='file_name4',
        ),
        migrations.RemoveField(
            model_name='noflyzone',
            name='file_name5',
        ),
    ]
