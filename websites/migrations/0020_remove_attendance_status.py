# Generated by Django 4.1.2 on 2022-11-24 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0019_rename_timeincreated_attendance_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='status',
        ),
    ]