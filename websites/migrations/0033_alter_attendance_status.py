# Generated by Django 4.1.2 on 2023-01-24 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0032_attendance_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('time in', 'Time In'), ('time out', 'Time Out'), ('breaktime out', 'Breaktime Out'), ('breaktime in', 'Breaktime In')], max_length=255),
        ),
    ]