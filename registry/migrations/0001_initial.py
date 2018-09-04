# Generated by Django 2.1 on 2018-09-04 11:22

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=140)),
                ('end_date', models.DateTimeField(default=datetime.datetime(2020, 9, 4, 0, 0, tzinfo=utc))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('postcode', models.CharField(default='0', max_length=10, verbose_name='post code')),
                ('city', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=280)),
                ('website', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('operator_type', models.IntegerField(choices=[(0, 'Open')], default=0)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.TextField()),
                ('postcode', models.CharField(default='0', max_length=10, verbose_name='post code')),
                ('city', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('authorized_activities', models.ManyToManyField(related_name='authorized_activities', to='registry.Activity')),
                ('operational_authorizations', models.ManyToManyField(related_name='operational_authorizations', to='registry.Authorization')),
            ],
        ),
        migrations.CreateModel(
            name='Rpas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mass', models.IntegerField()),
                ('manufacturer', models.CharField(max_length=280)),
                ('model', models.CharField(max_length=280)),
                ('serial_number', models.CharField(max_length=280)),
                ('maci_number', models.CharField(max_length=280)),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Operator')),
            ],
        ),
        migrations.AddField(
            model_name='contact',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registry.Operator'),
        ),
    ]
