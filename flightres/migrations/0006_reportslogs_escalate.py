# Generated by Django 3.1.3 on 2021-01-08 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightres', '0005_reportslogs'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportslogs',
            name='escalate',
            field=models.CharField(blank=True, choices=[('Escalated', 'Escalated'), ('De-Escalated', 'De-Escalated')], max_length=20, null=True),
        ),
    ]