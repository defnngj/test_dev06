# Generated by Django 4.0.1 on 2022-01-23 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_desc',
            field=models.TextField(default='', null=True),
        ),
    ]