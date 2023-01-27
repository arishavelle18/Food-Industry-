# Generated by Django 4.1.2 on 2022-11-24 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0013_alter_historyattendance_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='created',
            new_name='timeInCreated',
        ),
        migrations.AddField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('time in', 'Time In'), ('none', 'None'), ('time out', 'Time out')], default='none', max_length=255),
        ),
        migrations.AddField(
            model_name='attendance',
            name='timeOutCreated',
            field=models.DateTimeField(default=None),
        ),
    ]
