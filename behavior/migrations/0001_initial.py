# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-21 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSeries',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='misc. narrative e.g. “drifting gratings of different orientations”, “ChoiceWorld behavior events”', null=True)),
                ('generating_software', models.CharField(blank=True, help_text='e.g. “ChoiceWorld 0.8.3”', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeadTracking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='misc. narrative e.g. (“unit: cm” or “unknown scale factor”)', null=True)),
                ('generating_software', models.CharField(blank=True, help_text='e.g. “HeadTracka 0.8.3”', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IntervalSeries',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='misc. narrative e.g. “drifting gratings of different orientations”, “ChoiceWorld behavior intervals”', null=True)),
                ('generating_software', models.CharField(blank=True, help_text='e.g. “ChoiceWorld 0.8.3”', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OptogeneticStimulus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('light_delivery', models.CharField(blank=True, help_text='e.g. “fiber pointed at craniotomy”', max_length=255, null=True)),
                ('description', models.CharField(blank=True, help_text='e.g. “square pulses”, “ramps”', max_length=255, null=True)),
                ('wavelength', models.FloatField(blank=True, help_text='in nm', null=True)),
                ('power_calculation_method', models.CharField(blank=True, help_text='TODO: normalize? measured, nominal', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pharmacology',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('drug', models.CharField(blank=True, help_text='TODO: normalize? Also say what it is dissolved in (DMSO etc)', max_length=255, null=True)),
                ('administration_route', models.CharField(blank=True, help_text='TODO: normalize? IP, IV, IM, surface etc…', max_length=255, null=True)),
                ('start_time', models.FloatField(blank=True, help_text='in seconds relative to experiment start. TODO: not DateTimeField? / TimeDifference', null=True)),
                ('end_time', models.FloatField(blank=True, help_text='equals start time if single application. TODO: should this be an offset? Or DateTimeField? Or TimeDifference?', null=True)),
                ('concentration', models.CharField(blank=True, help_text='TODO: not FloatField? include unit (e.g. g/kg; mM; %)', max_length=255, null=True)),
                ('volume', models.CharField(blank=True, help_text='TODO: not FloatField? include unit (e.g. µL)', max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PupilTracking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('eye', models.CharField(blank=True, choices=[('L', 'Left'), ('R', 'Right')], help_text='Which eye was tracked; left or right', max_length=1, null=True)),
                ('description', models.TextField(blank=True, help_text='misc. narrative e.g. (“unit: mm” or “unknown scale factor”)', null=True)),
                ('generating_software', models.CharField(blank=True, help_text='e.g. “PupilTracka 0.8.3”', max_length=255, null=True)),
                ('experiment', models.ForeignKey(help_text='The Experiment to which this data belongs', on_delete=django.db.models.deletion.CASCADE, related_name='behavior_pupiltracking_related', to='actions.Experiment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
