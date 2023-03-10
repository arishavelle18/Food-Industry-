# Generated by Django 4.1.2 on 2022-12-22 08:14

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0029_alter_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='personCode',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=200)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=django_cryptography.fields.encrypt(models.CharField(choices=[('time in', 'Time In'), ('time out', 'Time Out')], max_length=255)),
        ),
    ]
