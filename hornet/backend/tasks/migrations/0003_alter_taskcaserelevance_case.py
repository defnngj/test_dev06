# Generated by Django 4.0.2 on 2022-06-19 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_testresult_passed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcaserelevance',
            name='case',
            field=models.TextField(default='', null=True, verbose_name='关联用例'),
        ),
    ]