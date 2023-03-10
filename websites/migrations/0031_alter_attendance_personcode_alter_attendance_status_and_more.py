# Generated by Django 4.1.2 on 2022-12-22 09:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0030_alter_attendance_personcode_alter_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='personCode',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('time in', 'Time In'), ('time out', 'Time Out')], max_length=255),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]
