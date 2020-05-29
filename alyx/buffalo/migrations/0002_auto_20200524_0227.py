# Generated by Django 3.0.5 on 2020-05-24 02:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_dataset_hash_version'),
        ('subjects', '0006_auto_20200317_1055'),
        ('buffalo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuffaloSubject',
            fields=[
                ('subject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subjects.Subject')),
                ('unique_id', models.CharField(blank=True, default='', help_text='Monkey Identifier', max_length=255)),
                ('code', models.CharField(blank=True, default='', help_text='Two letter code', max_length=2)),
            ],
            options={
                'abstract': False,
            },
            bases=('subjects.subject',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='Long name', max_length=255)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='Long name', max_length=255)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, help_text='Long name', max_length=255)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='channelrecording',
            name='session_task',
        ),
        migrations.RemoveField(
            model_name='channelrecording',
            name='stl_file',
        ),
        migrations.RemoveField(
            model_name='sessiontask',
            name='dataset_type',
        ),
        migrations.RemoveField(
            model_name='startingpoint',
            name='orientation',
        ),
        migrations.RemoveField(
            model_name='task',
            name='maze_type',
        ),
        migrations.RemoveField(
            model_name='task',
            name='reward_type',
        ),
        migrations.AddField(
            model_name='channelrecording',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='channelrecording',
            name='riples',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')], default='', max_length=180),
        ),
        migrations.AddField(
            model_name='electrode',
            name='channel_number',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='startingpoint',
            name='date_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='startingpoint',
            name='depth',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='dataset_type',
            field=models.ManyToManyField(blank=True, to='data.DatasetType'),
        ),
        migrations.AddField(
            model_name='task',
            name='training',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='channelrecording',
            name='alive',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')], default='', max_length=180),
        ),
        migrations.AlterField(
            model_name='channelrecording',
            name='number_of_cells',
            field=models.CharField(blank=True, choices=[('1', 'nothing'), ('2', 'maybe 1 cell'), ('3', '1 good cell'), ('4', '2+ good cells')], default='', max_length=255),
        ),
        migrations.CreateModel(
            name='ElectrodeTurn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('electrode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buffalo.Electrode')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buffalo.Location'),
        ),
        migrations.AddField(
            model_name='task',
            name='reward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buffalo.Reward'),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='buffalo.Category'),
        ),
    ]
