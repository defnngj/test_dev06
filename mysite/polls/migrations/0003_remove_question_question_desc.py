# Generated by Django 4.0.1 on 2022-01-23 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_question_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_desc',
        ),
    ]
