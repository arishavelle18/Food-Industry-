# Generated by Django 4.1.2 on 2022-11-24 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0012_historyattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyattendance',
            name='created',
            field=models.DateTimeField(),
        ),
    ]