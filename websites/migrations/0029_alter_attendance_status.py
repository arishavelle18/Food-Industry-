# Generated by Django 4.1.2 on 2022-12-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0028_alter_attendance_personcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('time in', 'Time In'), ('time out', 'Time Out')], max_length=255),
        ),
    ]
