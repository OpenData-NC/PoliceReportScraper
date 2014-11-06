# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arrest_',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agency', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=250)),
                ('age', models.IntegerField(default=0)),
                ('race', models.CharField(max_length=3)),
                ('sex', models.CharField(default=b'', max_length=2, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'', b'Unspecified')])),
                ('date_occurred', models.DateField()),
                ('time_occurred', models.TimeField()),
                ('address', models.CharField(max_length=250)),
                ('charge', models.CharField(max_length=250)),
                ('offense_code', models.CharField(max_length=3)),
                ('reporting_officer', models.CharField(max_length=250)),
                ('pdf', models.CharField(max_length=250)),
                ('street_address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('county', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=3)),
                ('zip', models.IntegerField(default=0)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Incident_test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agency', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=250)),
                ('age', models.IntegerField(default=0)),
                ('race', models.CharField(max_length=3)),
                ('sex', models.CharField(default=b'', max_length=2, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'', b'Unspecified')])),
                ('on_date', models.DateField()),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('date_reported', models.DateField()),
                ('time_reported', models.TimeField()),
                ('address', models.CharField(max_length=250)),
                ('charge', models.CharField(max_length=250)),
                ('offense_code', models.CharField(max_length=3)),
                ('reporting_officer', models.CharField(max_length=250)),
                ('pdf', models.CharField(max_length=250)),
                ('street_address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=250)),
                ('county', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=3)),
                ('zip', models.IntegerField(default=0)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
