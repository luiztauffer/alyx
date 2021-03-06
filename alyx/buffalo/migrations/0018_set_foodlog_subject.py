# Generated by Django 3.0.5 on 2020-10-29 16:27

from django.db import migrations


def set_foodlog_subject(apps, schema_editor):
    foodlog_model = apps.get_model('buffalo', 'FoodLog')
    subject_model = apps.get_model('buffalo', 'BuffaloSubject')
   
    foodlogs = foodlog_model.objects.all()

    for foodlog in foodlogs:
        if not foodlog.subject and foodlog.session is not None:
            foodlog_subject = subject_model.objects.get(pk=foodlog.session.subject_id)
            foodlog.subject = foodlog_subject
            foodlog.save()


class Migration(migrations.Migration):

    dependencies = [
        ('buffalo', '0017_auto_20210131_0439'),
    ]

    operations = [
        migrations.RunPython(set_foodlog_subject),
    ]
