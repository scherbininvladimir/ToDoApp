# Generated by Django 2.2.6 on 2019-12-17 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20191215_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='todos_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]