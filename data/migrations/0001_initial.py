# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-21 12:30
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataRepository',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'data repositories',
            },
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileRecord',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tape_sequential_number', models.IntegerField(blank=True, help_text='sequential ID in tape archive, if applicable. Can contain multiple records.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogicalFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('md5', models.CharField(blank=True, help_text='MD5 hash, if a file', max_length=255, null=True)),
                ('filename', models.CharField(max_length=1000)),
                ('is_folder', models.BooleanField(help_text='True if the LogicalFile is a folder, not a single file.')),
                ('fileset', models.ForeignKey(help_text='The Fileset that this file belongs to.', on_delete=django.db.models.deletion.CASCADE, to='data.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalArchive',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveDataRepository',
            fields=[
                ('datarepository_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.DataRepository')),
                ('identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('tape_contents', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Tape contents, including untracked files.', null=True)),
                ('physical_archive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.PhysicalArchive')),
            ],
            options={
                'verbose_name_plural': 'archive data repositories',
            },
            bases=('data.datarepository',),
        ),
        migrations.CreateModel(
            name='LocalDataRepository',
            fields=[
                ('datarepository_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.DataRepository')),
                ('hostname', models.CharField(blank=True, help_text="Hostname must be unique. e.g. 'NSLaptop'", max_length=1000, null=True)),
                ('path', models.CharField(blank=True, help_text="e.g. 'D:/Data/acquisition/'", max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'local data repositories',
            },
            bases=('data.datarepository',),
        ),
        migrations.CreateModel(
            name='NetworkDataRepository',
            fields=[
                ('datarepository_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.DataRepository')),
                ('fqdn', models.CharField(blank=True, help_text='Fully Qualified Domain Name or IP, e.g. 1.2.3.4 or foxtrot.neuro.ucl.ac.uk', max_length=1000, null=True)),
                ('share', models.CharField(blank=True, help_text="Share name, e.g. 'Data'", max_length=1000, null=True)),
                ('path', models.CharField(blank=True, help_text="Path name after share, e.g. '/subjects/'", max_length=1000, null=True)),
                ('nfs_supported', models.BooleanField(help_text='NFS supported (Linux)')),
                ('smb_supported', models.BooleanField(help_text='SMB supported (Windows)')),
                ('afp_supported', models.BooleanField(help_text='AFP supported (Linux)')),
            ],
            options={
                'verbose_name_plural': 'network data repositories',
            },
            bases=('data.datarepository',),
        ),
        migrations.AddField(
            model_name='filerecord',
            name='data_repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.DataRepository'),
        ),
        migrations.AddField(
            model_name='filerecord',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.LogicalFile'),
        ),
        migrations.AddField(
            model_name='datarepository',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_data.datarepository_set+', to='contenttypes.ContentType'),
        ),
    ]
