# Generated by Django 4.0.2 on 2022-04-17 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='passed',
            field=models.IntegerField(default=0, verbose_name='通过用例'),
        ),
    ]
